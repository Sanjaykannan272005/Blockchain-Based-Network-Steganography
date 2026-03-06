# -*- coding: utf-8 -*-
"""
Network Steganography with Blockchain Key Exchange
Sender: Encrypts message, sends over network, stores key on blockchain
"""

import socket
import json
from web3 import Web3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import base64
import hashlib
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load blockchain config
with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

w3 = Web3(Web3.HTTPProvider(config['rpc_url']))

def encrypt_message(message, key):
    """Encrypt message with AES"""
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted = cipher.encrypt(pad(message.encode(), AES.block_size))
    return base64.b64encode(cipher.iv + encrypted).decode()

def store_key_on_blockchain(message_hash, encryption_key, receiver_address):
    """Store encryption key on blockchain"""
    try:
        nonce = w3.eth.get_transaction_count(config['wallet_address'])
        
        # Store key as hex string
        key_hex = encryption_key.hex()
        
        tx = {
            'nonce': nonce,
            'to': receiver_address,
            'value': 0,
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
            'data': w3.to_hex(text=f"{message_hash}:{key_hex}"),
            'chainId': config['chain_id']
        }
        
        signed_tx = w3.eth.account.sign_transaction(tx, config['private_key'])
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"Key stored on blockchain!")
        print(f"TX Hash: {tx_hash.hex()}")
        print(f"Etherscan: {config['explorer']}/tx/{tx_hash.hex()}")
        
        return tx_hash.hex()
    except Exception as e:
        print(f"Blockchain error: {e}")
        return None

def send_encrypted_message(host, port, message, receiver_address):
    """Send encrypted message over network, store key on blockchain"""
    
    print("\n" + "="*60)
    print("NETWORK STEGANOGRAPHY - SENDER")
    print("="*60)
    
    # Generate encryption key
    encryption_key = get_random_bytes(32)  # AES-256
    print(f"\nOriginal Message: {message}")
    print(f"Encryption Key: {encryption_key.hex()[:32]}...")
    
    # Encrypt message
    encrypted_msg = encrypt_message(message, encryption_key)
    print(f"Encrypted Message: {encrypted_msg[:50]}...")
    
    # Calculate message hash
    msg_hash = hashlib.sha256(message.encode()).hexdigest()
    print(f"Message Hash: {msg_hash[:32]}...")
    
    # Store key on blockchain
    print("\nStoring key on blockchain...")
    tx_hash = store_key_on_blockchain(msg_hash, encryption_key, receiver_address)
    
    if not tx_hash:
        print("Failed to store key on blockchain!")
        return
    
    # Wait for confirmation
    print("Waiting for blockchain confirmation...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    
    if receipt['status'] != 1:
        print("Blockchain transaction failed!")
        return
    
    print(f"Confirmed in block: {receipt['blockNumber']}")
    
    # Send encrypted message over network
    print(f"\nSending encrypted message to {host}:{port}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        
        # Send data
        data = {
            'encrypted_message': encrypted_msg,
            'tx_hash': tx_hash,
            'message_hash': msg_hash
        }
        
        sock.send(json.dumps(data).encode())
        sock.close()
        
        print("Message sent successfully!")
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Encrypted message: Sent over network")
        print(f"Encryption key: Stored on blockchain")
        print(f"TX Hash: {tx_hash}")
        print(f"Receiver needs TX hash to decrypt!")
        
    except ConnectionRefusedError:
        print(f"\nERROR: Cannot connect to receiver at {host}:{port}")
        print("Make sure receiver is running first!")
        print("\nRun in another terminal: python network_receiver_blockchain.py")
        print(f"\nYour message is encrypted and key is on blockchain.")
        print(f"TX Hash: {tx_hash}")
    except Exception as e:
        print(f"Network error: {e}")
        print(f"\nKey stored on blockchain: {tx_hash}")

if __name__ == '__main__':
    # Configuration
    RECEIVER_HOST = 'localhost'
    RECEIVER_PORT = 9999
    RECEIVER_ADDRESS = config['wallet_address']
    
    print("\n" + "="*60)
    print("NETWORK STEGANOGRAPHY - SENDER")
    print("="*60)
    print(f"\nReceiver: {RECEIVER_HOST}:{RECEIVER_PORT}")
    print("Make sure receiver is running!\n")
    
    # Message to send
    message = input("Enter secret message: ")
    
    # Send
    send_encrypted_message(RECEIVER_HOST, RECEIVER_PORT, message, RECEIVER_ADDRESS)
