# -*- coding: utf-8 -*-
"""Enhanced Hybrid Receiver - Network Stego + Blockchain Dead Drop"""

from flask import Flask, render_template, jsonify, request, Response
import json
import subprocess
import os
import sys
import threading
import time
from datetime import datetime
from blockchain_integration import BlockchainKeyExchange
from log_streamer import streamer

app = Flask(__name__)

# Security & Config
config = {}
try:
    if os.path.exists('blockchain_config.json'):
        with open('blockchain_config.json', 'r') as f:
            config = json.load(f)
except Exception as e:
    print(f"Warning: Could not load blockchain_config.json: {e}")

blockchain = BlockchainKeyExchange()
# Auto-load contracts if addresses are in environment or fallback to config
blockchain.load_registry_contract(config.get('registry_contract'))
blockchain.load_access_control(config.get('access_control_contract'))
blockchain.load_user_registry(config.get('user_registry_contract'))
blockchain.load_controller_contract(config.get('controller_contract'))
blockchain.load_dead_drop_contract(config.get('dead_drop_contract'))
start_time = time.time()
capture_logs = []

def add_log(msg, category="INFO"):
    log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    capture_logs.append(log_entry)
    if len(capture_logs) > 50: capture_logs.pop(0)
    streamer.emit(msg, category)

@app.route('/api/logs/stream')
def stream_logs():
    return Response(streamer.generate(), mimetype='text/event-stream')

# ==========================
# API Endpoints
# ==========================

@app.route('/')
def index():
    admin_addr = config.get('owner_address', config.get('wallet_address', '')).lower()
    return render_template('receiver_web.html', wallet=config.get('wallet_address'), admin_address=admin_addr)

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/api/receiver/status')
def get_status():
    """Get status of the local node and network"""
    net_status = "NORMAL"
    reputation = 100
    node_info = {}
    
    if config.get('registry_contract'):
        try:
            blockchain.load_registry_contract(config['registry_contract'])
            res = blockchain.get_global_status()
            if res.get('success'): net_status = res['status']
            
            # Get my reputation
            if config.get('wallet_address'):
                nodes_res = blockchain.get_blockchain_nodes()
                if nodes_res.get('success'):
                    for n in nodes_res['nodes']:
                        if n['wallet'].lower() == config['wallet_address'].lower():
                            reputation = n['reputation']
                            node_info = n
                            break
        except: pass

    return jsonify({
        'uptime': int(time.time() - start_time),
        'net_status': net_status,
        'reputation': reputation,
        'wallet': config.get('wallet_address'),
        'node_info': node_info,
        'logs': capture_logs[-5:]
    })

@app.route('/api/receiver/extract', methods=['POST'])
def extract_stego():
    """Trigger network_receiver.py to capture and extract messages"""
    data = request.get_json()
    channel = data.get('channel', 'timing')
    duration = int(data.get('duration', 30))
    use_stealth = data.get('stealth', False)
    selected_iface = data.get('iface')
    
    def run_extraction():
        add_log(f"Starting {channel.upper()} extraction (Duration: {duration}s) on {selected_iface or 'Auto-detected'} interface...")
        cmd = [sys.executable, '-u', 'network_receiver.py']
        cmd.append(channel if channel and channel != 'auto' else 'timing')
        cmd.append(str(duration))
        if use_stealth: cmd.append("--stealth")
        if selected_iface:
            cmd.extend(["--iface", selected_iface])
        
        # Stealth mode needs extra time for Scapy cleanup on Windows
        proc_timeout = duration + 60 if use_stealth else duration + 20
        
        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                encoding='utf-8', errors='replace',
                timeout=proc_timeout, env=env
            )
            combined = result.stdout + result.stderr
            add_log(f"Extraction complete.")
            if "MESSAGE RECEIVED:" in combined:
                msg = combined.split("MESSAGE RECEIVED:")[1].strip().split('\n')[0].strip()
                add_log(f"[SUCCESS] Message extracted: {msg}")
            elif result.returncode != 0:
                err = (result.stderr or '').strip().splitlines()
                # Show last meaningful error line
                last_err = next((l for l in reversed(err) if l.strip()), 'Unknown error')
                add_log(f"Extraction failed: {last_err}")
            else:
                add_log("No message found in traffic.")
        except subprocess.TimeoutExpired:
            add_log(f"Extraction timed out after {proc_timeout}s -- no covert traffic detected.")
        except Exception as e:
            add_log(f"Error: {str(e)}")

    thread = threading.Thread(target=run_extraction)
    thread.start()
    return jsonify({'success': True, 'message': f'Extraction started for {duration} seconds'})

@app.route('/api/receiver/inbox')
def get_blockchain_inbox():
    """Fetch messages for this wallet from DeadDrop.sol"""
    if not config.get('dead_drop_contract') or not config.get('wallet_address'):
        return jsonify({'success': False, 'error': 'Contract or wallet not configured'})
        
    try:
        blockchain.load_dead_drop_contract(config['dead_drop_contract'])
        res = blockchain.get_from_deaddrop(config['wallet_address'])
        if res.get('success'):
            return jsonify({'success': True, 'messages': res['messages']})
        else:
            return jsonify({'success': False, 'error': res.get('error')})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/receiver/decrypt', methods=['POST'])
def decrypt_drop():
    """Decrypt a blockchain dead drop message"""
    data = request.get_json()
    encrypted_msg = data.get('encrypted_msg')
    
    # Simple time-bucketed decryption (matches sender/receiver logic)
    import hashlib, base64
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    
    try:
        # Check if hybrid tag exists
        clean_msg = encrypted_msg
        if "[hybrid" in encrypted_msg:
            # Format: [hybrid|key:TIME|hash:HASH] CIPHERTEXT
            parts = encrypted_msg.split("] ", 1)
            clean_msg = parts[1]
            
        # Try current and last minute buckets
        now = int(time.time() / 60) * 60
        for t in [now, now - 60]:
            key = hashlib.sha256(f"block_{t}".encode()).digest()
            try:
                raw_data = base64.b64decode(clean_msg)
                iv = raw_data[:16]
                ciphertext = raw_data[16:]
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
                return jsonify({'success': True, 'decrypted': decrypted})
            except: continue
            
        return jsonify({'success': False, 'error': 'Decryption failed. Wrong key or corrupted data.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/receiver/logs')
def get_logs():
    return jsonify({'logs': capture_logs})

if __name__ == '__main__':
    print(f"Enhanced Receiver API active on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)
