#!/usr/bin/env python3
"""
Network Receiver - Run this on the receiving computer
Listens for encrypted messages sent from the web interface
"""

import socket
import json
import hashlib
from Crypto.Cipher import AES
import base64
from datetime import datetime

class NetworkReceiver:
    def __init__(self, port=9999):
        self.port = port
        self.password = "BlockchainStego2024"
        self.key = hashlib.sha256(self.password.encode()).digest()
        
    def decrypt_message(self, encrypted_message):
        """Decrypt AES-256 encrypted message"""
        try:
            encrypted_data = base64.b64decode(encrypted_message)
            iv = encrypted_data[:16]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(encrypted_data[16:])
            pad_length = ord(decrypted[-1:])
            return decrypted[:-pad_length].decode()
        except Exception as e:
            return f"Decryption failed: {e}"
    
    def start_listening(self):
        """Start listening for incoming messages"""
        print("=" * 60)
        print("🔐 BLOCKCHAIN STEGANOGRAPHY - NETWORK RECEIVER")
        print("=" * 60)
        print(f"📡 Listening on port: {self.port}")
        print(f"🔑 Encryption: AES-256-CBC")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print("\n✅ Receiver is ready! Waiting for messages...\n")
        
        # Create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', self.port))
        server_socket.listen(5)
        
        try:
            while True:
                # Accept connection
                client_socket, address = server_socket.accept()
                print(f"\n📨 Incoming connection from: {address[0]}:{address[1]}")
                
                # Receive data
                data = b''
                while True:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                
                client_socket.close()
                
                if data:
                    try:
                        # Parse JSON message
                        message_data = json.loads(data.decode())
                        
                        print("\n" + "=" * 60)
                        print("📬 MESSAGE RECEIVED")
                        print("=" * 60)
                        print(f"From: {message_data.get('sender', 'Unknown')}")
                        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        print(f"Features Used: {len(message_data.get('features', []))} of 10")
                        
                        # Decrypt message
                        encrypted = message_data.get('encrypted_message', '')
                        decrypted = self.decrypt_message(encrypted)
                        
                        print(f"\n🔓 Decrypted Message:")
                        print(f"   {decrypted}")
                        
                        # Show feature details
                        if 'feature_results' in message_data:
                            print(f"\n📋 Feature Details:")
                            fr = message_data['feature_results']
                            if 'control' in fr:
                                print(f"   ✓ Control Rules: {fr['control']['message']}")
                            if 'trigger' in fr:
                                print(f"   ✓ Trigger Event Created")
                            if 'blockchain_key' in fr:
                                print(f"   ✓ Blockchain Key: Block #{fr['blockchain_key']['block_height']}")
                            if 'auth' in fr:
                                print(f"   ✓ Authentication: Verified")
                            if 'reputation' in fr:
                                print(f"   ✓ Reputation Score: {fr['reputation']['score']}")
                            if 'forensic' in fr:
                                print(f"   ✓ Forensic Record: Block #{fr['forensic']['block_number']}")
                            if 'multichain' in fr:
                                print(f"   ✓ Multi-Chain: {len(fr['multichain'])} chains")
                            if 'dead_drop' in fr:
                                print(f"   ✓ Dead Drop: Created")
                            if 'rotation' in fr:
                                print(f"   ✓ Key Rotation: Scheduled")
                            if 'protocol' in fr:
                                print(f"   ✓ Protocol: {fr['protocol'].upper()}")
                        
                        print("=" * 60)
                        print("\n✅ Waiting for next message...\n")
                        
                    except json.JSONDecodeError:
                        print("❌ Error: Invalid message format")
                    except Exception as e:
                        print(f"❌ Error processing message: {e}")
                        
        except KeyboardInterrupt:
            print("\n\n🛑 Receiver stopped by user")
        finally:
            server_socket.close()
            print("👋 Goodbye!")

if __name__ == '__main__':
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     BLOCKCHAIN STEGANOGRAPHY - NETWORK RECEIVER            ║")
    print("║     Run this on the computer that will receive messages    ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\n")
    
    # Get port
    port_input = input("Enter port to listen on (default 9999): ").strip()
    port = int(port_input) if port_input else 9999
    
    # Start receiver
    receiver = NetworkReceiver(port=port)
    receiver.start_listening()
