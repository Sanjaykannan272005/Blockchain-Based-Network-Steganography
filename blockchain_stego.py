#!/usr/bin/env python3
"""
Blockchain-Integrated Steganography System
Combines steganography with Ethereum blockchain for key storage
"""

from web3 import Web3
import json
import hashlib
from steganography import hide_data, extract_data

# Load config
with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

w3 = Web3(Web3.HTTPProvider(config['rpc_url']))

def store_key_on_blockchain(message_hash, encryption_key, receiver_address):
    """Store encryption key on Ethereum blockchain"""
    try:
        nonce = w3.eth.get_transaction_count(config['wallet_address'])
        
        tx = {
            'nonce': nonce,
            'to': receiver_address,
            'value': 0,
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
            'data': w3.to_hex(text=f"{message_hash}:{encryption_key}"),
            'chainId': config['chain_id']
        }
        
        signed_tx = w3.eth.account.sign_transaction(tx, config['private_key'])
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        return {
            'success': True,
            'tx_hash': tx_hash.hex(),
            'explorer_url': f"{config['explorer']}/tx/{tx_hash.hex()}"
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_key_from_blockchain(tx_hash):
    """Retrieve encryption key from blockchain"""
    try:
        tx = w3.eth.get_transaction(tx_hash)
        data = w3.to_text(tx['input'])
        message_hash, encryption_key = data.split(':')
        
        return {
            'success': True,
            'encryption_key': encryption_key,
            'message_hash': message_hash,
            'sender': tx['from']
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def hide_with_blockchain(cover_image, output_image, message, password, receiver_address):
    """Hide message in image and store key on blockchain"""
    # Hide message
    result = hide_data(cover_image, output_image, message, password)
    
    if result['success']:
        # Calculate message hash
        msg_hash = hashlib.sha256(message.encode()).hexdigest()
        
        # Store key on blockchain
        blockchain_result = store_key_on_blockchain(msg_hash, password, receiver_address)
        
        return {
            'success': True,
            'stego_image': output_image,
            'tx_hash': blockchain_result.get('tx_hash'),
            'explorer_url': blockchain_result.get('explorer_url')
        }
    
    return result

def extract_with_blockchain(stego_image, tx_hash):
    """Extract message using key from blockchain"""
    # Get key from blockchain
    key_result = get_key_from_blockchain(tx_hash)
    
    if key_result['success']:
        password = key_result['encryption_key']
        
        # Extract message
        result = extract_data(stego_image, password)
        
        return result
    
    return key_result

if __name__ == '__main__':
    print("Blockchain Steganography System")
    print(f"Network: {config['network']}")
    print(f"Wallet: {config['wallet_address']}")
    print(f"Balance: {w3.from_wei(w3.eth.get_balance(config['wallet_address']), 'ether')} ETH")
