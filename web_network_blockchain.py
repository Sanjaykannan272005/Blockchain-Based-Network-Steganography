# -*- coding: utf-8 -*-
"""Web Interface for Network Steganography + Blockchain"""

from flask import Flask, render_template, request, jsonify
from web3 import Web3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import hashlib
import json
import socket
import threading

app = Flask(__name__)

# Load config
with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

w3 = Web3(Web3.HTTPProvider(config['rpc_url']))

# Store received messages
received_messages = []

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted = cipher.encrypt(pad(message.encode(), AES.block_size))
    return base64.b64encode(cipher.iv + encrypted).decode()

def decrypt_message(encrypted_msg, key):
    encrypted_data = base64.b64decode(encrypted_msg)
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

def store_key_on_blockchain(message_hash, encryption_key, receiver_address):
    nonce = w3.eth.get_transaction_count(config['wallet_address'])
    tx = {
        'nonce': nonce,
        'to': receiver_address,
        'value': 0,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
        'data': w3.to_hex(text=f"{message_hash}:{encryption_key.hex()}"),
        'chainId': config['chain_id']
    }
    signed_tx = w3.eth.account.sign_transaction(tx, config['private_key'])
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return tx_hash.hex()

def get_key_from_blockchain(tx_hash):
    tx = w3.eth.get_transaction(tx_hash)
    data = w3.to_text(tx['input'])
    msg_hash, key_hex = data.split(':')
    return bytes.fromhex(key_hex), msg_hash

def network_receiver():
    """Background thread to receive messages"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 9999))
    sock.listen(1)
    
    while True:
        try:
            conn, addr = sock.accept()
            data = conn.recv(4096).decode()
            conn.close()
            
            if data:
                msg_data = json.loads(data)
                encryption_key, _ = get_key_from_blockchain(msg_data['tx_hash'])
                decrypted = decrypt_message(msg_data['encrypted_message'], encryption_key)
                
                received_messages.append({
                    'message': decrypted,
                    'tx_hash': msg_data['tx_hash'],
                    'encrypted': msg_data['encrypted_message'][:50] + '...'
                })
        except:
            pass

# Start receiver in background
receiver_thread = threading.Thread(target=network_receiver, daemon=True)
receiver_thread.start()

@app.route('/')
def index():
    balance = w3.from_wei(w3.eth.get_balance(config['wallet_address']), 'ether')
    return render_template('network_blockchain_web.html', 
                         wallet=config['wallet_address'],
                         balance=balance)

@app.route('/send', methods=['POST'])
def send_message():
    try:
        message = request.json['message']
        receiver_host = request.json.get('host', 'localhost')
        receiver_port = int(request.json.get('port', 9999))
        
        # Encrypt
        encryption_key = get_random_bytes(32)
        encrypted_msg = encrypt_message(message, encryption_key)
        msg_hash = hashlib.sha256(message.encode()).hexdigest()
        
        # Store key on blockchain
        tx_hash = store_key_on_blockchain(msg_hash, encryption_key, config['wallet_address'])
        w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        # Send over network
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((receiver_host, receiver_port))
        sock.send(json.dumps({
            'encrypted_message': encrypted_msg,
            'tx_hash': tx_hash,
            'message_hash': msg_hash
        }).encode())
        sock.close()
        
        return jsonify({
            'success': True,
            'tx_hash': tx_hash,
            'explorer_url': f"{config['explorer']}/tx/{tx_hash}"
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/received')
def get_received():
    return jsonify({'messages': received_messages})

@app.route('/balance')
def get_balance():
    balance = w3.eth.get_balance(config['wallet_address'])
    return jsonify({
        'balance': w3.from_wei(balance, 'ether'),
        'address': config['wallet_address']
    })

if __name__ == '__main__':
    print(f"Wallet: {config['wallet_address']}")
    print(f"Balance: {w3.from_wei(w3.eth.get_balance(config['wallet_address']), 'ether')} ETH")
    print("Web interface: http://localhost:5000")
    app.run(debug=True, port=5000)
