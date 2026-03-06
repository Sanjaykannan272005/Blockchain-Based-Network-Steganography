# -*- coding: utf-8 -*-
"""Test network steganography with blockchain - automated"""

import socket
import json
from web3 import Web3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import hashlib
import sys
import io
import time
import threading

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

w3 = Web3(Web3.HTTPProvider(config['rpc_url']))

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

print("="*60)
print("NETWORK STEGANOGRAPHY + BLOCKCHAIN TEST")
print("="*60)

# Test message
message = "Secret military operation at 0600 hours"
print(f"\nOriginal Message: {message}")

# Generate key
encryption_key = get_random_bytes(32)
print(f"Encryption Key: {encryption_key.hex()[:32]}...")

# Encrypt
encrypted_msg = encrypt_message(message, encryption_key)
print(f"Encrypted: {encrypted_msg[:50]}...")

# Store key on blockchain
msg_hash = hashlib.sha256(message.encode()).hexdigest()
print(f"\nStoring key on blockchain...")

nonce = w3.eth.get_transaction_count(config['wallet_address'])
tx = {
    'nonce': nonce,
    'to': config['wallet_address'],
    'value': 0,
    'gas': 100000,
    'gasPrice': w3.eth.gas_price,
    'data': w3.to_hex(text=f"{msg_hash}:{encryption_key.hex()}"),
    'chainId': config['chain_id']
}

signed_tx = w3.eth.account.sign_transaction(tx, config['private_key'])
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

print(f"TX Hash: {tx_hash.hex()}")
print(f"Waiting for confirmation...")

receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
print(f"Confirmed in block: {receipt['blockNumber']}")

# Retrieve key from blockchain
print(f"\nRetrieving key from blockchain...")
tx_data = w3.eth.get_transaction(tx_hash.hex())
retrieved_data = w3.to_text(tx_data['input'])
retrieved_hash, retrieved_key_hex = retrieved_data.split(':')
retrieved_key = bytes.fromhex(retrieved_key_hex)

print(f"Retrieved Key: {retrieved_key.hex()[:32]}...")

# Decrypt
decrypted_msg = decrypt_message(encrypted_msg, retrieved_key)
print(f"\nDecrypted Message: {decrypted_msg}")

# Verify
if decrypted_msg == message:
    print("\n" + "="*60)
    print("SUCCESS! System working correctly!")
    print("="*60)
    print("\nFlow:")
    print("1. Message encrypted with AES-256")
    print("2. Key stored on Ethereum blockchain")
    print("3. Key retrieved from blockchain")
    print("4. Message decrypted successfully")
    print(f"\nEtherscan: {config['explorer']}/tx/{tx_hash.hex()}")
else:
    print("\nERROR: Decryption failed!")
