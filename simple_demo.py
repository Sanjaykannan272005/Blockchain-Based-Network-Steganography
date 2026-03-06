#!/usr/bin/env python3
"""
Simple File-Based Blockchain Steganography Demo
No timing issues - works with files
"""

import hashlib
import time
from Crypto.Cipher import AES
import base64
import sys

def get_blockchain_key():
    """Get blockchain key - fixed for demo"""
    # Use fixed time so both sender/receiver get same key
    block_hash = hashlib.sha256(b"demo_block_12345").hexdigest()
    key = hashlib.sha256(block_hash.encode()).digest()
    return key, block_hash[:20]

def encrypt_message(message, key):
    """Encrypt with AES-256"""
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    pad_length = 16 - (len(message) % 16)
    padded = message + (chr(pad_length) * pad_length)
    encrypted = cipher.encrypt(padded.encode())
    return base64.b64encode(iv + encrypted).decode()

def decrypt_message(encrypted_data, key):
    """Decrypt with AES-256"""
    try:
        encrypted_bytes = base64.b64decode(encrypted_data)
        iv = encrypted_bytes[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_bytes[16:])
        pad_length = ord(decrypted[-1:])
        return decrypted[:-pad_length].decode()
    except Exception as e:
        return None

def send_message(message):
    """Send encrypted message"""
    print("="*70)
    print("BLOCKCHAIN STEGANOGRAPHY - SENDER")
    print("="*70)
    
    print(f"\nMessage: {message}")
    
    # Get blockchain key
    print("\nGetting encryption key from blockchain...")
    key, key_hash = get_blockchain_key()
    print(f"Key hash: {key_hash}...")
    
    # Encrypt
    print("\nEncrypting with AES-256...")
    encrypted = encrypt_message(message, key)
    print(f"Encrypted: {encrypted[:40]}...")
    
    # Save to file (simulates network transmission)
    with open("encrypted_message.txt", "w") as f:
        f.write(encrypted)
    
    print("\n" + "="*70)
    print("MESSAGE SENT!")
    print("="*70)
    print(f"\nEncrypted message saved to: encrypted_message.txt")
    print(f"Receiver can now decrypt it with: python simple_demo.py receive")

def receive_message():
    """Receive and decrypt message"""
    print("="*70)
    print("BLOCKCHAIN STEGANOGRAPHY - RECEIVER")
    print("="*70)
    
    # Check file exists
    try:
        with open("encrypted_message.txt", "r") as f:
            encrypted = f.read()
    except FileNotFoundError:
        print("\nERROR: No encrypted message found!")
        print("Run sender first: python simple_demo.py send \"Your message\"")
        return
    
    print(f"\nEncrypted message: {encrypted[:40]}...")
    
    # Get blockchain key
    print("\nGetting decryption key from blockchain...")
    key, key_hash = get_blockchain_key()
    print(f"Key hash: {key_hash}...")
    
    # Decrypt
    print("\nDecrypting with AES-256...")
    message = decrypt_message(encrypted, key)
    
    if message:
        print("\n" + "="*70)
        print("MESSAGE RECEIVED:")
        print("="*70)
        print(f"\n{message}\n")
        print("="*70)
    else:
        print("\nERROR: Decryption failed!")

def main():
    if len(sys.argv) < 2:
        print("="*70)
        print("BLOCKCHAIN STEGANOGRAPHY - SIMPLE DEMO")
        print("="*70)
        print("\nUsage:")
        print("  Send:    python simple_demo.py send \"Your message\"")
        print("  Receive: python simple_demo.py receive")
        print("\nExample:")
        print("  python simple_demo.py send \"Hello World\"")
        print("  python simple_demo.py receive")
        return
    
    command = sys.argv[1].lower()
    
    if command == "send":
        if len(sys.argv) < 3:
            print("ERROR: Please provide a message")
            print("Usage: python simple_demo.py send \"Your message\"")
            return
        message = sys.argv[2]
        send_message(message)
    
    elif command == "receive":
        receive_message()
    
    else:
        print(f"ERROR: Unknown command '{command}'")
        print("Use 'send' or 'receive'")

if __name__ == "__main__":
    main()
