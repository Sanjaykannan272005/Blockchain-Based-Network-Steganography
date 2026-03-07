# -*- coding: utf-8 -*-
"""Sender Web Interface - Separate Page"""

from flask import Flask, render_template, request, jsonify, Response
from web3 import Web3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import base64
import hashlib
import json
import socket
import os
from blockchain_integration import BlockchainKeyExchange
import requests
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
# Auto-load contracts
blockchain.load_registry_contract(config.get('registry_contract'))
blockchain.load_access_control(config.get('access_control_contract'))

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(blockchain.rpc_url))

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted = cipher.encrypt(pad(message.encode(), AES.block_size))
    return base64.b64encode(cipher.iv + encrypted).decode()

def store_key_on_blockchain(message_hash, encryption_key, receiver_address, password):
    # Encrypt the key with password before storing
    from Crypto.Protocol.KDF import PBKDF2
    password_key = PBKDF2(password.encode(), b'salt', dkLen=32)
    cipher = AES.new(password_key, AES.MODE_CBC)
    encrypted_key = cipher.encrypt(pad(encryption_key, AES.block_size))
    encrypted_key_b64 = base64.b64encode(cipher.iv + encrypted_key).decode()
    
    wallet_address = os.getenv('OPERATOR_ADDRESS', config.get('wallet_address'))
    private_key = os.getenv('OPERATOR_PRIVATE_KEY', config.get('private_key'))
    chain_id = int(os.getenv('CHAIN_ID', config.get('chain_id', 11155111)))

    nonce = w3.eth.get_transaction_count(wallet_address)
    tx = {
        'nonce': nonce,
        'to': receiver_address,
        'value': 0,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
        'data': w3.to_hex(text=f"{message_hash}:{encrypted_key_b64}"),
        'chainId': chain_id
    }
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return tx_hash.hex()

@app.route('/')
def index():
    balance = w3.from_wei(w3.eth.get_balance(config['wallet_address']), 'ether')
    admin_addr = config.get('owner_address', config.get('wallet_address', '')).lower()
    return render_template('sender_web.html', wallet=config['wallet_address'], balance=balance, admin_address=admin_addr)

@app.route('/api/logs/stream')
def stream_logs():
    return Response(streamer.generate(), mimetype='text/event-stream')

@app.route('/send', methods=['POST'])
def send_message():
    try:
        message = request.json['message']
        receiver_host = request.json['host']
        receiver_port = int(request.json['port'])
        password = request.json['password']
        
        encryption_key = get_random_bytes(32)
        encrypted_msg = encrypt_message(message, encryption_key)
        msg_hash = hashlib.sha256(message.encode()).hexdigest()
        
        tx_hash = store_key_on_blockchain(msg_hash, encryption_key, config['wallet_address'], password)
        streamer.emit(f"Key stored on blockchain. TX: {tx_hash}", "BLOCKCHAIN")
        
        # Don't wait for confirmation - send immediately
        streamer.emit(f"Connecting to receiver {receiver_host}:{receiver_port}...", "NETWORK")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((receiver_host, receiver_port))
        sock.send(json.dumps({
            'encrypted_message': encrypted_msg,
            'tx_hash': tx_hash,
            'message_hash': msg_hash
        }).encode())
        sock.close()
        streamer.emit(f"Message payload delivered successfully.", "SUCCESS")
        
        return jsonify({
            'success': True,
            'tx_hash': tx_hash,
            'explorer_url': f"{config['explorer']}/tx/{tx_hash}"
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/balance')
def get_balance():
    target_wallet = request.args.get('wallet', config['wallet_address'])
    try:
        balance = w3.eth.get_balance(w3.to_checksum_address(target_wallet))
        return jsonify({'balance': w3.from_wei(balance, 'ether')})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/verified_nodes')
def proxy_nodes():
    try:
        res = requests.get('http://localhost:5000/api/verified_nodes', timeout=5)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({'success': False, 'error': 'Dashboard offline', 'nodes': []})

@app.route('/api/protocol/analytics')
def proxy_analytics():
    try:
        live = request.args.get('live', 'false')
        res = requests.get(f'http://localhost:5000/api/protocol/analytics?live={live}', timeout=5)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({'success': False, 'error': 'Dashboard offline'})

@app.route('/network_hide', methods=['POST'])
def network_hide_proxy():
    # Allow local templates to call /network_hide which is actually in app.py
    try:
        # Forward form data
        res = requests.post('http://localhost:5000/network_hide', data=request.form, timeout=10)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/dead_drop_check')
def proxy_dead_drop_check():
    try:
        res = requests.get('http://localhost:5000/dead_drop_check', timeout=5)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({'success': False, 'error': 'Dashboard offline'})

@app.route('/dead_drop_send_hybrid', methods=['POST'])
def proxy_dead_drop_send_hybrid():
    try:
        res = requests.post('http://localhost:5000/dead_drop_send_hybrid', json=request.json, timeout=10)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("Sender Web Interface")
    print("Open: http://localhost:5003")
    app.run(debug=True, host='0.0.0.0', port=5003)
