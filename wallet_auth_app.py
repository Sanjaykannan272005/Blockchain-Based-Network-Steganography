"""
Wallet Authentication Web App - Flask Backend
Handles MetaMask verification, smart contract integration, and access control
"""

from flask import Flask, render_template, jsonify, request
from web3 import Web3
from eth_account.messages import encode_defunct
import json
from wallet_auth import WalletAuthenticator, load_access_control_contract
from blockchain_integration import BlockchainKeyExchange
import sys
import time
import os

from flask_cors import CORS
import sys

# Configure UTF-8 for Windows terminals to avoid UnicodeEncodeError
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.errorhandler(Exception)
def handle_exception(e):
    """Ensure ALL errors return JSON instead of HTML"""
    print(f"[CRASH] Unhandled Exception: {str(e)}")
    import traceback
    traceback.print_exc()
    return jsonify({
        'success': False, 
        'error': f"Internal Server Error: {str(e)}",
        'traceback': traceback.format_exc() if app.debug else None
    }), 500

@app.before_request
def log_request_info():
    if request.path != '/api/status':
        print(f"[REQUEST] {request.method} {request.path}")

@app.errorhandler(400)
def bad_request(e):
    return jsonify({'success': False, 'error': 'Bad Request: ' + str(e)}), 400

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'success': False, 'error': 'Not Found: ' + str(e)}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'success': False, 'error': 'Internal Server Error: ' + str(e)}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"[CRASH] Unhandled Exception: {str(e)}")
    return jsonify({'success': False, 'error': str(e)}), 500

# Load blockchain config
config = {}
try:
    if os.path.exists('blockchain_config.json'):
        with open('blockchain_config.json', 'r') as f:
            config = json.load(f)
except Exception as e:
    print(f"Warning: Could not load blockchain_config.json: {e}")

# Blockchain Integration (Prioritizes .env)
blockchain = BlockchainKeyExchange()
blockchain.load_user_registry(config.get('user_registry_contract'))
blockchain.load_access_control(config.get('access_control_contract'))

# Initialize Web3 (using the URL from the integration layer)
w3 = Web3(Web3.HTTPProvider(blockchain.rpc_url, request_kwargs={'timeout': 10}))
try:
    if w3.is_connected():
        print(f"[INIT] Connected to blockchain: True")
    else:
        print(f"[INIT] Connected to blockchain: False (Check RPC URL)")
except Exception as e:
    print(f"[INIT] Blockchain connection check failed: {e}")

# Admin / Owner address
ADMIN_ADDRESS = os.getenv('OPERATOR_ADDRESS', config.get('owner_address', config.get('wallet_address', ''))).lower()
print(f"[INIT] Admin address configured: {ADMIN_ADDRESS}")

@app.route('/')
def index():
    """Main wallet authentication page"""
    return render_template('wallet_auth.html')

@app.route('/verify_signature', methods=['POST'])
def verify_signature():
    """
    Verify a message signature and check access
    
    Request JSON:
    {
        "message": "message text",
        "signature": "0x...",
        "signer": "0x..."
    }
    """
    try:
        data = request.json
        message = data.get('message')
        signature = data.get('signature')
        signer = data.get('signer')
        
        print(f"\n[VERIFY] Verifying signature for {signer[:20]}...")
        print(f"[VERIFY] Message length: {len(message)}")
        
        if not all([message, signature, signer]):
            return jsonify({
                'authenticated': False,
                'reason': 'Missing required fields'
            }), 400
        
        # Verify signature
        try:
            message_hash = encode_defunct(text=message)
            recovered = w3.eth.account.recover_message(message_hash, signature=signature)
            
            print(f"[VERIFY] Expected: {signer}")
            print(f"[VERIFY] Recovered: {recovered}")
            
            if recovered.lower() != signer.lower():
                return jsonify({
                    'authenticated': False,
                    'reason': 'Signature does not match signer'
                })
            
            print(f"[VERIFY] Signature valid")
            
        except Exception as e:
            print(f"[VERIFY] Signature verification failed: {str(e)}")
            return jsonify({
                'authenticated': False,
                'reason': f'Signature invalid: {str(e)}'
            }), 400
        
        # Check whitelist / Registry
        access_status = check_whitelist(signer)
        
        # Also check User Registry for on-chain status
        on_chain_status = blockchain.get_user_clearance(signer)
        if on_chain_status.get('success') and on_chain_status.get('isActive'):
            # Override or merge with whitelist
            access_status['allowed'] = True
            access_status['reason'] = f"On-Chain Cleared: {on_chain_status['level']}"
            access_status['on_chain'] = True
            access_status['details'] = on_chain_status

        print(f"[VERIFY] Final Access status: {access_status}")
        
        if access_status['allowed']:
            print(f"[VERIFY] Authentication successful")
            return jsonify({
                'authenticated': True,
                'sender': signer,
                'is_admin': signer.lower() == ADMIN_ADDRESS,
                'access_details': access_status
            })
        else:
            # Still return is_admin even if not "allowed" in whitelist
            is_admin = signer.lower() == ADMIN_ADDRESS
            if is_admin:
                 return jsonify({
                    'authenticated': True,
                    'sender': signer,
                    'is_admin': True,
                    'access_details': {'allowed': True, 'reason': 'System Administrator', 'is_permanent': True}
                })
            
            print(f"[VERIFY] Authentication failed: {access_status['reason']}")
            return jsonify({
                'authenticated': False,
                'reason': access_status['reason'],
                'is_admin': False
            })
        
    except Exception as e:
        print(f"[ERROR] Verification failed: {str(e)}")
        return jsonify({
            'authenticated': False,
            'reason': f'Verification error: {str(e)}'
        }), 500

@app.route('/api/register_personnel', methods=['POST'])
def register_personnel_api():
    """Submit registration request to the smart contract (Requires Private Key in demo)"""
    try:
        data = request.json
        private_key = data.get('private_key')
        name = data.get('name')
        org = data.get('organization')
        clearance = data.get('clearance', 'BASIC')

        if not all([private_key, name, org]):
            return jsonify({'success': False, 'error': 'Private Key, Name, and Organization are required'})

        print(f"[REGISTER] Registering {name} on-chain...")
        result = blockchain.register_user(private_key, name, org, clearance)
        return jsonify(result)
    except Exception as e:
        print(f"[REGISTER] CRITICAL EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f"Backend Error: {str(e)}"})

@app.route('/api/debug_check', methods=['GET'])
def debug_check():
    """Diagnostic endpoint to verify backend state"""
    is_connected = False
    try:
        is_connected = w3.is_connected()
    except: pass
    
    return jsonify({
        'config_loaded': 'user_registry_contract' in config,
        'registry_address': config.get('user_registry_contract'),
        'blockchain_connected': is_connected,
        'registry_loaded': hasattr(blockchain, 'user_registry'),
        'admin_address': ADMIN_ADDRESS
    })

@app.route('/api/status', methods=['GET'])
def get_service_status():
    """Basic health check"""
    is_connected = False
    try:
        is_connected = w3.is_connected()
    except: pass
    
    return jsonify({
        'status': 'online',
        'blockchain': is_connected,
        'registry_loaded': hasattr(blockchain, 'user_registry')
    })

@app.route('/check_access', methods=['GET'])
def check_access():
    """Check if a sender has access"""
    try:
        sender = request.args.get('sender')
        
        if not sender:
            return jsonify({'error': 'Missing sender parameter'}), 400
        
        print(f"[CHECK] Checking access for {sender[:20]}...")
        
        status = check_whitelist(sender)
        return jsonify(status)
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/grant_access', methods=['POST'])
def grant_access():
    """Grant access to a sender (owner only)"""
    try:
        data = request.json
        sender = data.get('sender')
        duration = data.get('duration', 0)
        reason = data.get('reason', '')
        owner = data.get('owner')
        
        print(f"\n[GRANT] Granting access to {sender[:20]}...")
        print(f"[GRANT] Duration: {duration}s, Reason: {reason}")
        
        if not sender or not owner:
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
            
        # RBAC Check: Only Admin can grant access
        if owner.lower() != ADMIN_ADDRESS:
            print(f"[GRANT] ✗ Unauthorized attempt by {owner[:20]}")
            return jsonify({
                'success': False,
                'error': 'Unauthorized: Only administrator can manage access'
            }), 403
        
        # In production, this would call the smart contract
        # For now, store in simulated whitelist
        sender_whitelist[sender.lower()] = {
            'allowed': True,
            'granted_at': __import__('datetime').datetime.now().isoformat(),
            'expires_at': None if duration == 0 else (__import__('datetime').datetime.now() + __import__('datetime').timedelta(seconds=duration)).isoformat(),
            'reason': reason,
            'duration': duration
        }
        
        print(f"[GRANT] ✓ Access granted")
        return jsonify({'success': True, 'message': 'Access granted'})
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/revoke_access', methods=['POST'])
def revoke_access():
    """Revoke access from a sender (owner only)"""
    try:
        data = request.json
        sender = data.get('sender')
        owner = data.get('owner')
        
        print(f"\n[REVOKE] Revoking access from {sender[:20]}...")
        
        if not sender or not owner:
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
            
        # RBAC Check: Only Admin can revoke access
        if owner.lower() != ADMIN_ADDRESS:
            print(f"[REVOKE] ✗ Unauthorized attempt by {owner[:20]}")
            return jsonify({
                'success': False,
                'error': 'Unauthorized: Only administrator can manage access'
            }), 403
        
        # Remove from whitelist
        if sender.lower() in sender_whitelist:
            del sender_whitelist[sender.lower()]
            print(f"[REVOKE] ✓ Access revoked")
        else:
            print(f"[REVOKE] Sender not in whitelist")
        
        return jsonify({'success': True, 'message': 'Access revoked'})
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/get_permissions', methods=['GET'])
def get_permissions():
    """Get all active permissions"""
    try:
        print(f"\n[PERMISSIONS] Fetching {len(sender_whitelist)} permissions...")
        
        permissions = []
        now = __import__('datetime').datetime.now()
        
        for sender, perm in sender_whitelist.items():
            if not perm['allowed']:
                continue
            
            time_remaining = None
            if perm['expires_at']:
                expires_dt = __import__('datetime').datetime.fromisoformat(perm['expires_at'])
                if expires_dt > now:
                    time_remaining = int((expires_dt - now).total_seconds())
                    is_permanent = False
                else:
                    continue  # Skip expired
            else:
                is_permanent = True
            
            permissions.append({
                'address': sender,
                'granted_at': perm['granted_at'],
                'expires_at': perm['expires_at'],
                'time_remaining_seconds': time_remaining,
                'is_permanent': is_permanent,
                'reason': perm['reason']
            })
        
        return jsonify({'permissions': permissions})
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({'permissions': [], 'error': str(e)})

def check_whitelist(sender_address):
    """Check if sender is in whitelist and access is valid"""
    sender_lower = sender_address.lower()
    
    if sender_lower not in sender_whitelist:
        return {
            'allowed': False,
            'reason': 'Sender not in whitelist'
        }
    
    perm = sender_whitelist[sender_lower]
    
    if not perm['allowed']:
        return {
            'allowed': False,
            'reason': 'Access revoked'
        }
    
    # Check expiration
    if perm['expires_at']:
        expires_dt = __import__('datetime').datetime.fromisoformat(perm['expires_at'])
        if __import__('datetime').datetime.now() > expires_dt:
            return {
                'allowed': False,
                'reason': 'Access expired'
            }
        
        time_remaining = int((__import__('datetime').datetime.fromisoformat(perm['expires_at']) - __import__('datetime').datetime.now()).total_seconds())
    else:
        time_remaining = None
    
    return {
        'allowed': True,
        'granted_at': perm['granted_at'],
        'expires_at': perm['expires_at'],
        'time_remaining_seconds': time_remaining,
        'is_permanent': perm['expires_at'] is None,
        'reason': perm['reason']
    }

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Wallet Authentication Service")
    print("="*60)
    print("Open: http://localhost:5002")
    print("Blockchain:", "Connected" if w3.is_connected() else "Disconnected")
    print("="*60 + "\n")
    sys.stdout.flush()
    
    app.run(host='0.0.0.0', port=5002, debug=True, use_reloader=False, threaded=True)
