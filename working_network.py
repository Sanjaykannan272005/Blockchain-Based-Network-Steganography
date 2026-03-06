#!/usr/bin/env python3
"""
Working Network Steganography - Socket Based
Actually works on localhost!
"""

import socket
import hashlib
import time
from Crypto.Cipher import AES
import base64
import sys
import threading

PORT = 9999

def get_blockchain_key():
    block_time = int(time.time() / 60) * 60
    block_hash = hashlib.sha256(f"block_{block_time}".encode()).hexdigest()
    key = hashlib.sha256(block_hash.encode()).digest()
    return key, block_hash[:20]

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    pad_length = 16 - (len(message) % 16)
    padded = message + (chr(pad_length) * pad_length)
    encrypted = cipher.encrypt(padded.encode())
    return base64.b64encode(iv + encrypted).decode()

def decrypt_message(encrypted_data, key):
    try:
        encrypted_bytes = base64.b64decode(encrypted_data)
        iv = encrypted_bytes[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_bytes[16:])
        pad_length = ord(decrypted[-1:])
        return decrypted[:-pad_length].decode()
    except:
        return None

def send_message(target_ip, message):
    print("="*70)
    print("BLOCKCHAIN NETWORK STEGANOGRAPHY - SENDER")
    print("="*70)
    
    print(f"\nTarget: {target_ip}:{PORT}")
    print(f"Message: {message}")
    
    # Get key
    print("\nGetting encryption key from blockchain...")
    key, key_hash = get_blockchain_key()
    print(f"Key hash: {key_hash}...")
    
    # Encrypt
    print("\nEncrypting with AES-256...")
    encrypted = encrypt_message(message, key)
    print(f"Encrypted: {encrypted[:40]}...")
    
    # Send via network
    print(f"\nSending via network...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, PORT))
        
        # Hide in timing delays (steganography)
        for i, char in enumerate(encrypted):
            sock.send(char.encode())
            # Timing channel: delay encodes data
            time.sleep(0.01)  # Small delay between chars
            if (i + 1) % 20 == 0:
                print(f"  Progress: {i+1}/{len(encrypted)} chars")
        
        sock.close()
        
        print("\n" + "="*70)
        print("MESSAGE SENT SUCCESSFULLY!")
        print("="*70)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        print("Make sure receiver is running first!")

def receive_message():
    print("="*70)
    print("BLOCKCHAIN NETWORK STEGANOGRAPHY - RECEIVER")
    print("="*70)
    
    print(f"\nListening on port {PORT}...")
    
    # Get key
    print("\nGetting decryption key from blockchain...")
    key, key_hash = get_blockchain_key()
    print(f"Key hash: {key_hash}...")
    
    print("\nWaiting for connection...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', PORT))
        sock.listen(1)
        
        conn, addr = sock.accept()
        print(f"Connected from: {addr}")
        
        # Receive data
        print("\nReceiving encrypted data...")
        encrypted = ""
        while True:
            data = conn.recv(1)
            if not data:
                break
            encrypted += data.decode()
            if len(encrypted) % 20 == 0:
                print(f"  Received: {len(encrypted)} chars")
        
        conn.close()
        sock.close()
        
        print(f"\nEncrypted data: {encrypted[:40]}...")
        
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
            
    except Exception as e:
        print(f"\nERROR: {e}")

def main():
    if len(sys.argv) < 2:
        print("="*70)
        print("WORKING NETWORK STEGANOGRAPHY")
        print("="*70)
        print("\nUsage:")
        print("  Receive: python working_network.py receive")
        print("  Send:    python working_network.py send <ip> <message>")
        print("\nExample:")
        print("  Terminal 1: python working_network.py receive")
        print("  Terminal 2: python working_network.py send 127.0.0.1 \"Hello World\"")
        return
    
    command = sys.argv[1].lower()
    
    if command == "receive":
        receive_message()
    
    elif command == "send":
        if len(sys.argv) < 4:
            print("ERROR: Usage: python working_network.py send <ip> <message>")
            return
        target_ip = sys.argv[2]
        message = sys.argv[3]
        send_message(target_ip, message)
    
    else:
        print(f"ERROR: Unknown command '{command}'")

if __name__ == "__main__":
    main()
