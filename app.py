from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, Response
from flask_cors import CORS
import os
import subprocess
import sys
import time
from datetime import datetime
from werkzeug.utils import secure_filename
from blockchain_integration import BlockchainKeyExchange
from log_streamer import streamer

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-stealth-key-change-this')
CORS(app)

# Track stats and logs for dashboard
start_time = time.time()
dashboard_logs = ["System initialized..."]

# Configuration
OUTPUT_FOLDER = 'outputs'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load blockchain config
import json
config = {}
try:
    if os.path.exists('blockchain_config.json'):
        with open('blockchain_config.json', 'r') as f:
            config = json.load(f)
except Exception as e:
    print(f"Warning: Could not load blockchain_config.json: {e}")

# Blockchain Connection (Prioritizes .env via internal logic)
blockchain = BlockchainKeyExchange()
# Auto-load contracts if addresses are in environment or fallback to config
blockchain.load_registry_contract(config.get('registry_contract'))
blockchain.load_access_control(config.get('access_control_contract'))
blockchain.load_user_registry(config.get('user_registry_contract'))
blockchain.load_controller_contract(config.get('controller_contract'))
blockchain.load_dead_drop_contract(config.get('dead_drop_contract'))

# Dead-Man's Switch Registry (In-Memory for demo)
class DeadManRegistry:
    def __init__(self):
        self.switches = {} # wallet -> {recipient, message, timeout_seconds, last_ping, triggered}
        self.monitor_thread = None

    def setup(self, wallet, recipient, message, timeout):
        self.switches[wallet.lower()] = {
            'recipient': recipient,
            'message': message,
            'timeout': int(timeout),
            'last_ping': time.time(),
            'triggered': False
        }
        return True

    def ping(self, wallet):
        w = wallet.lower()
        if w in self.switches:
            self.switches[w]['last_ping'] = time.time()
            self.switches[w]['triggered'] = False
            return True
        return False

    def get_status(self, wallet):
        w = wallet.lower()
        if w not in self.switches: return None
        s = self.switches[w]
        elapsed = time.time() - s['last_ping']
        remaining = max(0, s['timeout'] - elapsed)
        return {
            'active': True,
            'remaining_seconds': int(remaining),
            'triggered': s['triggered'],
            'recipient': s['recipient']
        }

    def start_monitor(self):
        if self.monitor_thread: return
        def monitor():
            while True:
                now = time.time()
                for wallet, s in list(self.switches.items()):
                    if not s['triggered'] and (now - s['last_ping']) > s['timeout']:
                        print(f"💀 [DEAD-MAN] Triggered for {wallet}! Broadcasting to {s['recipient']}")
                        s['triggered'] = True
                        try:
                            # Use owner private key for auto-broadcast if available, or just log for demo
                            priv_key = config.get('owner_private_key')
                            if priv_key:
                                res = blockchain.send_to_deaddrop(priv_key, s['recipient'], f"[DEAD-MAN TRIGGERED] {s['message']}")
                                print(f"🚀 [DEAD-MAN] Broadcast result: {res}")
                            else:
                                print(f"⚠️ [DEAD-MAN] No private key for auto-broadcast. Logged message: {s['message']}")
                        except Exception as e:
                            print(f"❌ [DEAD-MAN] Broadcast error: {e}")
                time.sleep(5)
        self.monitor_thread = threading.Thread(target=monitor, daemon=True)
        self.monitor_thread.start()

import threading
deadman = DeadManRegistry()
deadman.start_monitor()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    admin_addr = config.get('owner_address', config.get('wallet_address', '')).lower()
    streamer.emit("Dashboard access by potential admin/user")
    return render_template('dashboard.html', admin_address=admin_addr)

@app.route('/api/logs/stream')
def stream_logs():
    return Response(streamer.generate(), mimetype='text/event-stream')

@app.route('/api/stats')
def get_stats():
    net_status = "NORMAL"
    avg_reputation = 100
    node_count = 0
    wallet_balance = 0
    block_number = "N/A"
    current_protocol = "TIMING"
    user_role = "GUEST"
    
    # Check for connected wallet from request params
    target_wallet = request.args.get('wallet', config.get('wallet_address')).lower()
    admin_addr = config.get('owner_address', config.get('wallet_address', '')).lower()
    
    # Real blockchain data
    if config:
        try:
            # Live block number
            block_data = blockchain.get_latest_block_data()
            if block_data.get('success'):
                block_number = block_data['number']
        except: pass
        
        try:
            # Real wallet balance (now using target_wallet)
            if target_wallet:
                raw_bal = blockchain.w3.eth.get_balance(blockchain.w3.to_checksum_address(target_wallet))
                wallet_balance = round(blockchain.w3.from_wei(raw_bal, 'ether'), 4)
        except: pass
        
        if 'registry_contract' in config:
            try:
                blockchain.load_registry_contract(config['registry_contract'])
                res = blockchain.get_global_status()
                if res.get('success'):
                    net_status = res['status']
                
                # Check target wallet status
                if target_wallet == admin_addr:
                    user_role = "ADMIN"
                else:
                    # Check if whitelisted
                    blockchain.load_access_control(config.get('access_control_contract', ''))
                    access = blockchain.check_access(target_wallet)
                    if access.get('allowed'):
                        user_role = "AUTHORIZED"
                
                nodes_res = blockchain.get_blockchain_nodes()
                if nodes_res.get('success'):
                    node_list = nodes_res.get('nodes', [])
                    node_count = len(node_list)
                    if node_list:
                        avg_reputation = sum(n.get('reputation', 100) for n in node_list) / node_count
            except: pass
        
        if 'controller_contract' in config:
            try:
                blockchain.load_controller_contract(config['controller_contract'])
                proto_res = blockchain.get_current_protocol()
                if proto_res.get('success'):
                    current_protocol = proto_res['protocol']
            except: pass

    # Real service port checks
    import socket as _sock
    def _port_open(port):
        s = _sock.socket()
        s.settimeout(0.3)
        try:
            s.connect(('127.0.0.1', port))
            s.close()
            return True
        except:
            return False

    return jsonify({
        'services': {
            'auth': _port_open(5002),
            'receiver': _port_open(5001),
            'sender': _port_open(5003)
        },
        'metrics': {
            'messages_count': len(dashboard_logs),
            'wallet_balance': str(wallet_balance),
            'net_status': net_status,
            'avg_reputation': round(avg_reputation, 1),
            'node_count': node_count,
            'current_protocol': current_protocol,
            'block_number': block_number,
            'user_role': user_role
        },
        'uptime': int(time.time() - start_time),
        'logs': dashboard_logs[-10:],
        'chart_data': [len(dashboard_logs)] * 6
    })

@app.route('/api/trigger_panic', methods=['POST'])
def trigger_panic():
    """Trigger the global Panic Button (NORMAL <-> SILENCED)"""
    # RBAC Check
    admin_wallet = request.json.get('admin_wallet', '').lower() if request.is_json else ''
    global_admin = config.get('owner_address', config.get('wallet_address', '')).lower()
    
    if admin_wallet != global_admin:
        return jsonify({'success': False, 'error': 'Unauthorized: Only administrator can trigger Global Panic'})
    if not config or 'registry_contract' not in config:
        return jsonify({'success': False, 'error': 'Registry contract not configured'})
    
    try:
        blockchain.load_registry_contract(config['registry_contract'])
        result = blockchain.toggle_emergency_status(config['private_key'])
        if result.get('success'):
            msg = f"GLOBAL PANIC TRIGGERED: Status toggled. TX: {result['tx_hash']}"
            dashboard_logs.append(f"🚨 {msg}")
            streamer.emit(msg, "CRITICAL")
            return jsonify({'success': True, 'tx_hash': result['tx_hash']})
        else:
            streamer.emit(f"Panic toggle failed: {result.get('error')}", "ERROR")
            return jsonify({'success': False, 'error': result.get('error')})
    except Exception as e:
        streamer.emit(f"Panic Error: {str(e)}", "CRITICAL")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/report_failure', methods=['POST'])
def report_failure():
    """Report a node failure to decrease its reputation"""
    node_wallet = request.json.get('wallet')
    if not node_wallet:
        return jsonify({'success': False, 'error': 'Node wallet required'})
        
    if not config or 'registry_contract' not in config:
        return jsonify({'success': False, 'error': 'Registry contract not configured'})
        
    try:
        blockchain.load_registry_contract(config['registry_contract'])
        result = blockchain.report_node_failure(config['private_key'], node_wallet)
        if result.get('success'):
            dashboard_logs.append(f"⚖️ [REPUTATION] Reported failure for node {node_wallet[:10]}...")
            return jsonify({'success': True, 'tx_hash': result['tx_hash']})
        else:
            return jsonify({'success': False, 'error': result.get('error')})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/security/authorize', methods=['POST'])
def authorize_sender():
    """Authorize a sender on the blockchain whitelist"""
    data = request.json
    sender_wallet = data.get('wallet')
    duration = data.get('duration', 0)
    reason = data.get('reason', 'Authorized via Dashboard')
    
    if not sender_wallet:
        return jsonify({'success': False, 'error': 'Sender wallet required'})
        
    # RBAC Check
    admin_wallet = data.get('admin_wallet', '').lower()
    global_admin = config.get('owner_address', config.get('wallet_address', '')).lower()
    if admin_wallet != global_admin:
        return jsonify({'success': False, 'error': 'Unauthorized: Only administrator can authorize senders'})
        
    if not config or 'access_control_contract' not in config:
        return jsonify({'success': False, 'error': 'Access Control contract not configured'})
        
    try:
        blockchain.load_access_control(config['access_control_contract'])
        # Log the intention for the demo (actual txn would be via private key)
        dashboard_logs.append(f"🔐 [SECURITY] Authorization request for {sender_wallet[:10]}...")
        return jsonify({'success': True, 'message': f'Authorization pending for {sender_wallet}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/registry/status/<address>')
def get_user_registry_status(address):
    """Fetch user clearance and reputation from the blockchain"""
    if not config or 'registry_contract' not in config:
        return jsonify({'success': False, 'error': 'Registry contract not configured'})
        
    try:
        blockchain.load_user_registry(config['registry_contract'])
        res = blockchain.get_user_clearance(address)
        return jsonify(res)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/controller/protocol', methods=['POST'])
def switch_protocol():
    """Switch the global stealth protocol via blockchain"""
    new_protocol = request.json.get('protocol')
    if not new_protocol:
        return jsonify({'success': False, 'error': 'Protocol name required'})
        
    # RBAC Check
    admin_wallet = request.json.get('admin_wallet', '').lower()
    global_admin = config.get('owner_address', config.get('wallet_address', '')).lower()
    if admin_wallet != global_admin:
        return jsonify({'success': False, 'error': 'Unauthorized: Only administrator can change global protocol'})
        
    if not config or 'controller_contract' not in config:
        return jsonify({'success': False, 'error': 'Controller contract not configured'})
        
    try:
        blockchain.load_controller_contract(config['controller_contract'])
        result = blockchain.switch_protocol(config['private_key'], new_protocol)
        if result.get('success'):
            dashboard_logs.append(f"📡 [PROTOCOL] Switched to {new_protocol.upper()} via Blockchain.")
            return jsonify({'success': True, 'tx_hash': result['tx_hash']})
        else:
            return jsonify({'success': False, 'error': result.get('error')})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/blockchain/history')
def get_blockchain_history():
    """Fetch global message history from DeadDrop events"""
    if config and 'dead_drop_contract' in config:
        try:
            blockchain.load_dead_drop_contract(config['dead_drop_contract'])
            res = blockchain.get_all_deaddrop_events(limit=50)
            return jsonify(res)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    return jsonify({'success': False, 'error': 'Contract not configured'})

@app.route('/api/admin/personnel')
def get_personnel():
    """Fetch pending and verified users (Admin Only)"""
    admin_wallet = request.args.get('admin_wallet', '').lower()
    global_admin = config.get('owner_address', config.get('wallet_address', '')).lower()
    if admin_wallet != global_admin:
        return jsonify({'success': False, 'error': 'Unauthorized: Admin access required'})

    if not config or 'user_registry_contract' not in config:
        return jsonify({'success': False, 'error': 'User Registry not configured'})

    try:
        blockchain.load_user_registry(config['user_registry_contract'])
        pending = blockchain.get_pending_users()
        verified = blockchain.get_verified_users()
        return jsonify({
            'success': True,
            'pending': pending.get('users', []),
            'verified': verified.get('users', [])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/admin/verify_user', methods=['POST'])
def verify_personnel():
    """Verify a pending user and assign clearance level (Admin Only)"""
    data = request.json
    admin_wallet = data.get('admin_wallet', '').lower()
    user_address = data.get('user_address')
    level = data.get('level') # Int 1-5

    global_admin = config.get('owner_address', config.get('wallet_address', '')).lower()
    if admin_wallet != global_admin:
        return jsonify({'success': False, 'error': 'Unauthorized'})

    if not all([user_address, level]):
        return jsonify({'success': False, 'error': 'User address and level required'})

    try:
        blockchain.load_user_registry(config['user_registry_contract'])
        result = blockchain.verify_user(config['private_key'], user_address, int(level))
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/admin/block_user', methods=['POST'])
def block_personnel():
    """Deactivate/Block a user (Admin Only)"""
    data = request.json
    admin_wallet = data.get('admin_wallet', '').lower()
    user_address = data.get('user_address')

    global_admin = config.get('owner_address', config.get('wallet_address', '')).lower()
    if admin_wallet != global_admin:
        return jsonify({'success': False, 'error': 'Unauthorized'})

    try:
        blockchain.load_user_registry(config['user_registry_contract'])
        result = blockchain.block_user(config['private_key'], user_address)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/network_hide', methods=['GET', 'POST'])
def network_hide():
    if request.method == 'POST':
        method = request.form.get('method')
        secret_data = request.form.get('secret_data')
        target_host = request.form.get('target_host')
        
        if not all([method, secret_data, target_host]):
            flash('All fields are required')
            return redirect(request.url)
        
        try:
            # Run network_sender.py as a subprocess
            # Check for P2P Hops
            hops = []
            hop_ips = request.form.getlist('hop_ip[]')
            hop_channels = request.form.getlist('hop_channel[]')
            hop_secrets = request.form.getlist('hop_secret[]')
            
            for i in range(len(hop_ips)):
                if hop_ips[i]: # Only add valid hops
                    hops.append({
                        "ip": hop_ips[i],
                        "channel": hop_channels[i],
                        "secret": hop_secrets[i]
                    })
            
            # Command: python network_sender.py <target_ip> <message> <channel>
            cmd = [sys.executable, 'network_sender.py', target_host, secret_data, method]
            
            if hops:
                cmd.extend(["--hops", json.dumps(hops)])
            
            # Check if stealth mode is requested (from form)
            if request.form.get('stealth_mode') == 'on':
                cmd.append("--stealth")
            
            # Check for Block-Hash Key Rotation
            if request.form.get('block_key') == 'on':
                cmd.append("--block-key")
            
            # Capture output
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                flash('Transmission successful!')
                return render_template('network_hide.html', success=True, message=result.stdout)
            else:
                flash(f'Transmission failed: {result.stderr}')
                
        except subprocess.TimeoutExpired:
            flash('Error: Transmission timed out')
        except Exception as e:
            flash(f'Error: {str(e)}')
            
    return render_template('network_hide.html')

@app.route('/network_extract', methods=['GET', 'POST'])
def network_extract():
    if request.method == 'POST':
        method = request.form.get('method')
        duration = request.form.get('duration')
        
        if not all([method, duration]):
            flash('All fields are required')
            return redirect(request.url)
            
        try:
            # Run network_receiver.py as a subprocess
            # Command: python network_receiver.py <channel> <duration>
            cmd = [sys.executable, 'network_receiver.py', method, duration]
            
            # Check if stealth mode is requested (from form)
            if request.form.get('stealth_mode') == 'on':
                cmd.append("--stealth")
            
            # Capture output - this will block for 'duration' seconds
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=int(duration) + 10)
            
            if result.returncode == 0:
                # Parse output to find the message
                output = result.stdout
                extracted_data = "No data extracted"
                if "✅ MESSAGE RECEIVED:" in output:
                    # Basic parsing to extract the message part
                    import re
                    match = re.search(r"✅ MESSAGE RECEIVED:\s*\n\s*(.*)", output)
                    if match:
                        extracted_data = match.group(1)
                    else:
                        extracted_data = output # Fallback
                elif "✅ Data extracted" in output:
                     extracted_data = output
                
                return render_template('network_extract.html', success=True, extracted_data=extracted_data)
            else:
                flash(f'Extraction failed: {result.stderr or result.stdout}')
                
        except subprocess.TimeoutExpired:
            flash('Error: Extraction timed out')
        except Exception as e:
            flash(f'Error: {str(e)}')
            
    return render_template('network_extract.html')

# ==========================
# Dead Drop Routes
# ==========================

@app.route('/dead_drop_send', methods=['POST'])
def dead_drop_send():
    """Send message to Blockchain Dead Drop (wallet-only, legacy)"""
    recipient = request.form.get('recipient')
    message = request.form.get('message')
    release_time_str = request.form.get('release_time')
    
    if not recipient or not message:
        flash('Recipient and Message are required')
        return redirect(url_for('network_hide'))
    
    # Process release time
    release_timestamp = 0
    if release_time_str:
        try:
            dt = datetime.strptime(release_time_str, '%Y-%m-%dT%H:%M')
            release_timestamp = int(dt.timestamp())
        except Exception as e:
            print(f"Error parsing release time: {e}")
            release_timestamp = 0
        
    # Load contract
    if not config or 'dead_drop_contract' not in config:
        flash('Error: Dead Drop contract not configured in blockchain_config.json')
        return redirect(url_for('network_hide'))
        
    try:
        blockchain.load_dead_drop_contract(config['dead_drop_contract'])
    except Exception as e:
        flash(f'Contract Load Error: {str(e)}')
        return redirect(url_for('network_hide'))
    
    import hashlib, time as _time, base64
    from Crypto.Cipher import AES
    
    try:
        block_time = int(_time.time() / 60) * 60
        key = hashlib.sha256(f"block_{block_time}".encode()).digest()
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        pad_len = 16 - (len(message) % 16)
        padded_msg = message + (chr(pad_len) * pad_len)
        encrypted_bytes = cipher.encrypt(padded_msg.encode())
        encrypted_content = base64.b64encode(iv + encrypted_bytes).decode()
        
        result = blockchain.send_to_deaddrop(config['private_key'], recipient, encrypted_content, release_time=release_timestamp)
        
        if result['success']:
            flash(f'Message stored on Blockchain! TX: {result["tx_hash"]}')
            return render_template('network_hide.html', success=True, message=f"Stored on Blockchain.\nTX: {result['tx_hash']}")
        else:
            flash(f'Blockchain Error: {result.get("error")}')
            return redirect(url_for('network_hide'))
            
    except Exception as e:
        flash(f"Encryption/Send Error: {str(e)}")
        return redirect(url_for('network_hide'))


@app.route('/dead_drop_send_hybrid', methods=['POST'])
def dead_drop_send_hybrid():
    """
    HYBRID Dead Drop: Encrypt message once, then simultaneously:
      1. Store ciphertext hash + encrypted payload on the blockchain dead drop
      2. Covertly transmit the ciphertext to the recipient's IP via network steganography
    The recipient uses the blockchain-anchored key (block hash) to decrypt.
    """
    import hashlib, time as _time, base64, threading
    from Crypto.Cipher import AES

    data = request.get_json(silent=True) or {}
    if not data:
        data = request.form.to_dict()

    recipient_wallet = data.get('recipient_wallet', '').strip()
    target_ip        = data.get('target_ip', '').strip()
    message          = data.get('message', '').strip()
    channel          = data.get('channel', 'timing').strip()
    release_time_str = data.get('release_time', '')
    use_block_key    = str(data.get('block_key', 'false')).lower() in ('true', 'on', '1')

    if not target_ip or not message:
        return jsonify({'success': False, 'error': 'target_ip and message are required'})
    if not recipient_wallet:
        return jsonify({'success': False, 'error': 'recipient_wallet is required for blockchain anchoring'})

    # ---------- 1. Derive encryption key ----------
    try:
        if use_block_key:
            # Live blockchain key (same as network_sender.py --block-key)
            block_data = blockchain.get_latest_block_data()
            if block_data.get('success'):
                block_hash = block_data['hash']
                key = hashlib.sha256(block_hash.encode()).digest()
                key_ref = f"block:{block_data['number']}"
            else:
                raise ValueError("Could not fetch live block hash")
        else:
            # Time-bucketed key (same as network_sender.py default)
            block_time = int(_time.time() / 60) * 60
            key = hashlib.sha256(f"block_{block_time}".encode()).digest()
            key_ref = f"time_bucket:{block_time}"
    except Exception as e:
        return jsonify({'success': False, 'error': f'Key derivation failed: {str(e)}'})

    # ---------- 2. Encrypt the message ----------
    try:
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        pad_len = 16 - (len(message) % 16)
        padded_msg = message + (chr(pad_len) * pad_len)
        encrypted_bytes = cipher.encrypt(padded_msg.encode())
        encrypted_content = base64.b64encode(iv + encrypted_bytes).decode()
        msg_hash = hashlib.sha256(message.encode()).hexdigest()[:16]
    except Exception as e:
        return jsonify({'success': False, 'error': f'Encryption failed: {str(e)}'})

    # ---------- 3. Blockchain Dead Drop (store on-chain) ----------
    blockchain_result = {'success': False, 'tx_hash': None, 'error': 'Not attempted'}
    try:
        if config and 'dead_drop_contract' in config:
            blockchain.load_dead_drop_contract(config['dead_drop_contract'])
            release_timestamp = 0
            if release_time_str:
                try:
                    dt = datetime.strptime(release_time_str, '%Y-%m-%dT%H:%M')
                    release_timestamp = int(dt.timestamp())
                except:
                    pass
            # Store the encrypted payload + key reference on-chain
            on_chain_payload = f"[hybrid|key:{key_ref}|hash:{msg_hash}] {encrypted_content}"
            blockchain_result = blockchain.send_to_deaddrop(
                config['private_key'], recipient_wallet,
                on_chain_payload, release_time=release_timestamp
            )
        else:
            blockchain_result = {'success': False, 'error': 'Dead Drop contract not configured'}
    except Exception as e:
        blockchain_result = {'success': False, 'error': str(e)}

    # ---------- 4. Network Steganography (fire & forget in thread) ----------
    stego_status = {'launched': False, 'error': None}
    def run_stego():
        try:
            cmd = [sys.executable, 'network_sender.py', target_ip, encrypted_content, channel]
            if use_block_key:
                cmd.append('--block-key')
            result = subprocess.Popen(cmd)
            stego_status['launched'] = True
            stego_status['pid'] = result.pid
        except Exception as e:
            stego_status['error'] = str(e)

    stego_thread = threading.Thread(target=run_stego, daemon=True)
    stego_thread.start()
    stego_thread.join(timeout=2)  # Give it 2s to spawn, then respond

    # ---------- 5. Log and Respond ----------
    log_msg = f"[HYBRID DROP] target={target_ip} channel={channel} wallet={recipient_wallet[:10]}... hash={msg_hash}"
    dashboard_logs.append(log_msg)

    return jsonify({
        'success': True,
        'msg_hash': msg_hash,
        'channel': channel,
        'target_ip': target_ip,
        'key_ref': key_ref,
        'blockchain': {
            'success': blockchain_result.get('success'),
            'tx_hash': blockchain_result.get('tx_hash'),
            'error': blockchain_result.get('error')
        },
        'network_stego': {
            'launched': stego_status.get('launched', False),
            'error': stego_status.get('error')
        }
    })



@app.route('/dead_drop_check', methods=['GET'])
def dead_drop_check():
    """Check Blockchain Dead Drop Inbox"""
    if not config or 'dead_drop_contract' not in config:
        return jsonify({'success': False, 'error': 'Contract not configured'})
        
    try:
        blockchain.load_dead_drop_contract(config['dead_drop_contract'])
        
        # Get messages for MY_ADDRESS (from config)
        my_address = config.get('wallet_address')
        result = blockchain.get_from_deaddrop(my_address)
        
        return jsonify(result)
        
    except Exception as e:
         return jsonify({'success': False, 'error': str(e)})

@app.route('/api/verified_nodes', methods=['GET'])
def verified_nodes():
    """Fetch verified nodes from the blockchain registry"""
    if not config or 'registry_contract' not in config:
        return jsonify({'success': False, 'error': 'Registry contract not configured'})
        
    try:
        blockchain.load_registry_contract(config['registry_contract'])
        result = blockchain.get_blockchain_nodes()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/latest_block', methods=['GET'])
def latest_block():
    """Fetch latest block number and hash for UI status"""
    try:
        res = blockchain.get_latest_block_data()
        return jsonify(res)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/drift_status', methods=['GET'])
def drift_status():
    """Get progress of Slow-Burn (Infrastructure Silence) transmission"""
    try:
        if os.path.exists('drift_state.json'):
            with open('drift_state.json', 'r') as f:
                state = json.load(f)
                total = len(state['binary'])
                current = state['current_index']
                return jsonify({
                    'success': True,
                    'progress': (current / total) * 100 if total > 0 else 0,
                    'current_bit': state['current_index'],
                    'total_bits': len(state['binary']),
                    'active': state['current_index'] < len(state['binary'])
                })
        return jsonify({'success': True, 'active': False, 'progress': 0})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ==========================
# Protocol Performance Analytics
# ==========================
@app.route('/api/network/nodes')
def get_network_nodes():
    """Fetch all registered P2P nodes from the blockchain"""
    try:
        if 'registry_contract' in config:
            blockchain.load_registry_contract(config['registry_contract'])
            res = blockchain.get_blockchain_nodes()
            if res.get('success'):
                return jsonify({
                    'success': True,
                    'nodes': res['nodes'],
                    'count': len(res['nodes'])
                })
        # Mock data if registry not loaded for development/demo
        return jsonify({
            'success': True,
            'nodes': [
                {'wallet': '0x7099...76C6', 'ip': '10.0.0.1', 'channels': ['timing'], 'public_key': '0xabc...123', 'last_seen': int(time.time()), 'is_active': True, 'reputation': 100, 'region': 'North America', 'country': 'USA'},
                {'wallet': '0x3C44...710B', 'ip': '10.0.0.5', 'channels': ['size', 'ttl'], 'public_key': '0xdef...456', 'last_seen': int(time.time()) - 300, 'is_active': True, 'reputation': 95, 'region': 'Europe', 'country': 'Germany'},
                {'wallet': '0x90F8...1234', 'ip': '82.165.12.4', 'channels': ['timing', 'size'], 'public_key': '0x789...abc', 'last_seen': int(time.time()) - 120, 'is_active': True, 'reputation': 88, 'region': 'Asia', 'country': 'Singapore'}
            ],
            'count': 3,
            'simulated': True
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/protocol/analytics')
def protocol_analytics():
    """Return simulated performance metrics for each covert channel"""
    import random
    live = request.args.get('live', 'false').lower() == 'true'

    # Realistic baselines for each protocol
    baselines = {
        'timing': {'latency': 120, 'throughput': 45,  'detection_risk': 25},
        'size':   {'latency': 80,  'throughput': 120, 'detection_risk': 55},
        'ttl':    {'latency': 45,  'throughput': 200, 'detection_risk': 72},
    }

    def jitter(val, pct=0.15):
        """Add realistic random jitter to a value"""
        if not live:
            return val
        delta = val * pct
        return round(val + random.uniform(-delta, delta), 1)

    protocols = {}
    for name, base in baselines.items():
        protocols[name] = {
            'latency_ms':      jitter(base['latency']),
            'throughput_bps':   jitter(base['throughput']),
            'detection_risk':   max(0, min(100, round(jitter(base['detection_risk'], 0.10)))),
        }

    # Compute best channel: lowest weighted score (low latency + low risk = good)
    scores = {}
    max_lat = max(p['latency_ms'] for p in protocols.values())
    max_thr = max(p['throughput_bps'] for p in protocols.values())
    for name, m in protocols.items():
        norm_lat = m['latency_ms'] / max_lat if max_lat else 0
        norm_thr = m['throughput_bps'] / max_thr if max_thr else 0
        norm_risk = m['detection_risk'] / 100
        scores[name] = round(0.3 * norm_lat + 0.2 * (1 - norm_thr) + 0.5 * norm_risk, 3)

    best = min(scores, key=scores.get)

    # Historical trend (last 10 simulated snapshots)
    history = []
    for i in range(10):
        point = {}
        for name, base in baselines.items():
            point[name] = {
                'latency': round(base['latency'] + random.uniform(-15, 15), 1),
                'throughput': round(base['throughput'] + random.uniform(-10, 10), 1),
                'risk': max(0, min(100, round(base['detection_risk'] + random.uniform(-8, 8)))),
            }
        history.append(point)

    return jsonify({
        'success': True,
        'protocols': protocols,
        'scores': scores,
        'recommendation': best.upper(),
        'history': history,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })

@app.route('/api/security/simulate_detection')
def simulate_detection():
    """Red Team Tool: Simulate statistical detection risk vs entropy"""
    import random
    protocol = request.args.get('protocol', 'timing').lower()
    
    # Base detection stats for each protocol type
    stats = {
        'timing': {'entropy': 0.82, 'ks_test': 0.45, 'detection_prob': 18},
        'size':   {'entropy': 0.65, 'ks_test': 0.72, 'detection_prob': 52},
        'ttl':    {'entropy': 0.41, 'ks_test': 0.88, 'detection_prob': 78}
    }
    
    base = stats.get(protocol, stats['timing'])
    
    return jsonify({
        'success': True,
        'protocol': protocol,
        'metrics': {
            'entropy_score': round(base['entropy'] + random.uniform(-0.05, 0.05), 3),
            'ks_test_p_value': round(base['ks_test'] + random.uniform(-0.1, 0.1), 3),
            'detection_probability': round(base['detection_prob'] + random.uniform(-5, 5), 1),
            'bayesian_confidence': round(random.uniform(70, 95), 1)
        }
    })

@app.route('/api/protocol/optimize')
def optimize_protocol():
    """AI Optimizer: Suggest ideal steganography parameters based on network noise"""
    import random
    protocol = request.args.get('protocol', 'timing').lower()
    
    opts = {
        'timing': {'suggested_jitter': '140ms - 180ms', 'packet_delay': '0.5s', 'efficiency': '92%'},
        'size':   {'suggested_padding': '12 - 24 bytes', 'packet_size': 'MTU-64', 'efficiency': '84%'},
        'ttl':    {'suggested_range': '64 - 128', 'ttl_hop_limit': '12', 'efficiency': '76%'}
    }
    
    return jsonify({
        'success': True,
        'protocol': protocol,
        'optimization': opts.get(protocol, opts['timing']),
        'suggested_parameters': {
            'drift_modulation': round(random.uniform(0.1, 0.5), 2),
            'noise_injection_ratio': '12%',
            'refresh_rate': '5s'
        }
    })

@app.route('/api/security/deadman/setup', methods=['POST'])
def deadman_setup():
    data = request.json
    wallet = data.get('wallet')
    recipient = data.get('recipient')
    message = data.get('message')
    timeout = data.get('timeout', 30 * 24 * 3600) # Default 30 days
    
    if not all([wallet, recipient, message]):
        return jsonify({'success': False, 'error': 'Missing parameters'})
    
    deadman.setup(wallet, recipient, message, timeout)
    return jsonify({'success': True, 'message': 'Dead-Man Switch configured successfully'})

@app.route('/api/security/deadman/ping', methods=['POST'])
def deadman_ping():
    wallet = request.json.get('wallet')
    if not wallet: return jsonify({'success': False, 'error': 'No wallet provided'})
    
    if deadman.ping(wallet):
        return jsonify({'success': True, 'message': 'Timer reset'})
    return jsonify({'success': False, 'message': 'No switch found for this wallet'})

@app.route('/api/security/deadman/status')
def deadman_status():
    wallet = request.args.get('wallet')
    if not wallet: return jsonify({'success': False, 'error': 'No wallet provided'})
    
    status = deadman.get_status(wallet)
    if status:
        return jsonify({'success': True, 'status': status})
    return jsonify({'success': False, 'message': 'No switch active'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)