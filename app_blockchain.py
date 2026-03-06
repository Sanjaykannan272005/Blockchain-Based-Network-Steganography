#!/usr/bin/env python3
"""
Blockchain-Integrated Steganography Web App
"""

from flask import Flask, render_template, request, jsonify, send_file
from web3 import Web3
import json
import os
import hashlib
from steganography import hide_data, extract_data

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Load blockchain config
with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

w3 = Web3(Web3.HTTPProvider(config['rpc_url']))

@app.route('/')
def index():
    balance = w3.from_wei(w3.eth.get_balance(config['wallet_address']), 'ether')
    return render_template('blockchain_app.html', 
                         wallet=config['wallet_address'],
                         balance=balance,
                         network=config['network'])

@app.route('/hide_blockchain', methods=['POST'])
def hide_blockchain():
    """Hide message and store key on blockchain"""
    try:
        file = request.files['image']
        message = request.form['message']
        password = request.form['password']
        receiver = request.form.get('receiver', config['wallet_address'])
        
        cover_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], f'stego_{file.filename}')
        
        file.save(cover_path)
        
        # Hide message
        result = hide_data(cover_path, output_path, message, password)
        
        if result['success']:
            # Store key on blockchain
            msg_hash = hashlib.sha256(message.encode()).hexdigest()
            
            nonce = w3.eth.get_transaction_count(config['wallet_address'])
            tx = {
                'nonce': nonce,
                'to': receiver,
                'value': 0,
                'gas': 100000,
                'gasPrice': w3.eth.gas_price,
                'data': w3.to_hex(text=f"{msg_hash}:{password}"),
                'chainId': config['chain_id']
            }
            
            signed_tx = w3.eth.account.sign_transaction(tx, config['private_key'])
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            return jsonify({
                'success': True,
                'stego_image': f'stego_{file.filename}',
                'tx_hash': tx_hash.hex(),
                'explorer_url': f"{config['explorer']}/tx/{tx_hash.hex()}"
            })
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/extract_blockchain', methods=['POST'])
def extract_blockchain():
    """Extract message using key from blockchain"""
    try:
        file = request.files['image']
        tx_hash = request.form['tx_hash']
        
        stego_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(stego_path)
        
        # Get key from blockchain
        tx = w3.eth.get_transaction(tx_hash)
        data = w3.to_text(tx['input'])
        msg_hash, password = data.split(':')
        
        # Extract message
        result = extract_data(stego_path, password)
        
        if result['success']:
            result['sender'] = tx['from']
            result['message_hash'] = msg_hash
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/check_balance')
def check_balance():
    """Check wallet balance"""
    balance = w3.eth.get_balance(config['wallet_address'])
    return jsonify({
        'address': config['wallet_address'],
        'balance': w3.from_wei(balance, 'ether'),
        'network': config['network']
    })

@app.route('/download/<filename>')
def download(filename):
    """Download stego image"""
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    print(f"🔗 Blockchain: {config['network']}")
    print(f"💰 Wallet: {config['wallet_address']}")
    print(f"💵 Balance: {w3.from_wei(w3.eth.get_balance(config['wallet_address']), 'ether')} ETH")
    app.run(debug=True, port=5000)
