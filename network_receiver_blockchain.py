# -*- coding: utf-8 -*-
"""
Network Steganography with Blockchain Key Exchange
Receiver: Receives encrypted message, retrieves key from blockchain, decrypts
"""

import socket
import json
from web3 import Web3
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import hashlib
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load blockchain config
with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

w3 = Web3(Web3.HTTPProvider(config['rpc_url']))

def get_key_from_blockchain(tx_hash):
    """Retrieve encryption key from blockchain"""
    try:
        tx = w3.eth.get_transaction(tx_hash)
        data = w3.to_text(tx['input'])
        msg_hash, key_hex = data.split(':')
        encryption_key = bytes.fromhex(key_hex)
        
        return encryption_key, msg_hash
    except Exception as e:
        print(f"Blockchain error: {e}")
        return None, None

def decrypt_message(encrypted_msg, key):
    """Decrypt message with AES"""
    try:
        encrypted_data = base64.b64decode(encrypted_msg)
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        
        return decrypted.decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        return None

def start_receiver(host, port):
    """Start receiver to listen for encrypted messages"""
    
    print("\n" + "="*60)
    print("NETWORK STEGANOGRAPHY - RECEIVER")
    print("="*60)
    print(f"\nListening on {host}:{port}...")
    print("Waiting for encrypted messages...\n")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    
    while True:
        try:
            conn, addr = sock.accept()
            print(f"\nConnection from {addr}")
            
            # Receive data
            data = conn.recv(4096).decode()
            conn.close()
            
            if not data:
                continue
            
            # Parse data
            msg_data = json.loads(data)
            encrypted_msg = msg_data['encrypted_message']
            tx_hash = msg_data['tx_hash']
            msg_hash = msg_data['message_hash']
            
            print(f"Received encrypted message: {encrypted_msg[:50]}...")
            print(f"TX Hash: {tx_hash}")
            
            # Get key from blockchain
            print("\nRetrieving key from blockchain...")
            encryption_key, stored_hash = get_key_from_blockchain(tx_hash)
            
            if not encryption_key:
                print("Failed to retrieve key!")
                continue
            
            print(f"Key retrieved: {encryption_key.hex()[:32]}...")
            
            # Verify hash
            if stored_hash != msg_hash:
                print("WARNING: Message hash mismatch!")
                continue
            
            # Decrypt message
            print("\nDecrypting message...")
            decrypted_msg = decrypt_message(encrypted_msg, encryption_key)
            
            if decrypted_msg:
                print("\n" + "="*60)
                print("DECRYPTED MESSAGE")
                print("="*60)
                print(f"\n{decrypted_msg}\n")
                print("="*60)
            else:
                print("Decryption failed!")
            
        except KeyboardInterrupt:
            print("\nShutting down...")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    sock.close()

if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 9999
    
    start_receiver(HOST, PORT)
