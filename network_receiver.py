#!/usr/bin/env python3
"""
Network Steganography Receiver
Captures network packets and extracts hidden messages
Controlled by blockchain
"""

try:
    from scapy.all import *
except ImportError:
    print("ERROR: Scapy not installed")
    print("Install: python -m pip install scapy")
    exit(1)

import hashlib
import time
from Crypto.Cipher import AES
import base64
import sys
import os
import socket
from quantum_utils import QuantumUtils

# Blockchain key derivation (same as sender)
def get_blockchain_key(block_number=None):
    """Derive decryption key from blockchain data (Real or Simulated)"""
    try:
        from blockchain_integration import BlockchainKeyExchange
        import json
        import os
        
        # Load config to get RPC URL
        rpc_url = "https://sepolia.infura.io/v3/b9fc4ab7927e41fdb20bf3f50dd6afad"
        if os.path.exists('blockchain_config.json'):
            with open('blockchain_config.json', 'r') as f:
                config = json.load(f)
                rpc_url = config.get('rpc_url', rpc_url)
        
        blockchain = BlockchainKeyExchange(rpc_url=rpc_url)
        
        if block_number:
            print(f" Retrieving Hash for Block #{block_number}...")
            res = blockchain.get_block_hash(block_number)
        else:
            print(f" Retrieving Latest Block Hash...")
            res = blockchain.get_latest_block_data()
            block_number = res.get('number')
            
        if res.get('success'):
            block_hash = res['hash']
            key = hashlib.sha256(block_hash.encode()).digest()
            return key, block_hash[:20], block_number
    except Exception as e:
        print(f"️ Blockchain Error: {e}. Falling back to simulation.")

    # Fallback to simulation (same as before)
    block_time = int(time.time() / 60) * 60  # Round to minute
    sim_hash = hashlib.sha256(f"block_{block_time}".encode()).hexdigest()
    key = hashlib.sha256(sim_hash.encode()).digest()
    return key, sim_hash[:20], 0

# Decrypt message
def decrypt_message(encrypted_data, key):
    """Decrypt message with AES-256"""
    try:
        encrypted_bytes = base64.b64decode(encrypted_data)
        iv = encrypted_bytes[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_bytes[16:])
        pad_length = ord(decrypted[-1:])
        return decrypted[:-pad_length].decode()
    except Exception as e:
        print(f"   Decryption error: {e}")
        return None

# Receive via TIMING channel
def receive_via_timing(duration=60):
    """Extract data from packet timing delays"""
    print(f" Listening for TIMING channel (duration: {duration}s)...")
    print(f"   Waiting for packets...")
    
    last_time = None
    binary_data = ""
    packet_count = 0
    
    def packet_handler(packet):
        nonlocal last_time, binary_data, packet_count
        
        if packet.haslayer(ICMP):
            current_time = time.time()
            packet_count += 1
            
            if last_time is not None:
                delay = current_time - last_time
                
                # Widened windows to handle Windows scheduler jitter
                # Bit 0: ~0.1s delay  (sender sleeps 0.1s)
                # Bit 1: ~0.2s delay  (sender sleeps 0.2s)
                if 0.04 < delay < 0.15:   # 40ms - 150ms = bit 0
                    binary_data += '0'
                elif 0.15 < delay < 0.35: # 150ms - 350ms = bit 1
                    binary_data += '1'
                # else: ignore noise packets
                
                if len(binary_data) % 80 == 0 and len(binary_data) > 0:
                    print(f"   Received: {len(binary_data)} bits")
            
            last_time = current_time
    
    # Capture packets
    sniff(filter="icmp", prn=packet_handler, timeout=duration, store=0, iface=IFACE)
    
    print(f" Captured {packet_count} packets, extracted {len(binary_data)} bits")
    
    # Convert binary to text
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    extracted = ''.join([chr(int(c, 2)) for c in chars if len(c) == 8])
    
    return extracted

# Receive via SIZE channel
def receive_via_size(duration=60):
    """Extract data from packet sizes"""
    print(f" Listening for SIZE channel (duration: {duration}s)...")
    print(f"   Waiting for packets...")
    
    binary_data = ""
    packet_count = 0
    
    def packet_handler(packet):
        nonlocal binary_data, packet_count
        
        if packet.haslayer(ICMP) and packet.haslayer(Raw):
            size = len(packet[Raw].load)
            packet_count += 1
            
            # Widened SIZE decode windows (stealth uses Gaussian around 400/600 bytes)
            # Bit 0: 64-450 bytes
            # Bit 1: 450-1500 bytes
            if 64 <= size < 450:
                binary_data += '0'
            elif 450 <= size <= 1500:
                binary_data += '1'
            
            if len(binary_data) % 80 == 0 and len(binary_data) > 0:
                print(f"   Received: {len(binary_data)} bits")
    
    # Capture packets
    sniff(filter="icmp", prn=packet_handler, timeout=duration, store=0, iface=IFACE)
    
    print(f" Captured {packet_count} packets, extracted {len(binary_data)} bits")
    
    # Convert binary to text
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    extracted = ''.join([chr(int(c, 2)) for c in chars if len(c) == 8])
    
    return extracted

# Receive via TTL channel
def receive_via_ttl(duration=60):
    """Extract data from TTL field"""
    print(f" Listening for TTL channel (duration: {duration}s)...")
    print(f"   Waiting for packets...")
    
    binary_data = ""
    packet_count = 0
    
    def packet_handler(packet):
        nonlocal binary_data, packet_count
        
        if packet.haslayer(IP) and packet.haslayer(ICMP):
            ttl = packet[IP].ttl
            packet_count += 1
            
            # Decode TTL
            if ttl == 64:
                binary_data += '0'
            elif ttl == 65:
                binary_data += '1'
            
            if len(binary_data) % 80 == 0 and len(binary_data) > 0:
                print(f"   Received: {len(binary_data)} bits")
    
    # Capture packets
    sniff(filter="icmp", prn=packet_handler, timeout=duration, store=0, iface=IFACE)
    
    print(f" Captured {packet_count} packets, extracted {len(binary_data)} bits")
    
    # Convert binary to text
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    extracted = ''.join([chr(int(c, 2)) for c in chars if len(c) == 8])
    
    return extracted

# Main
def main():
    print("=" * 70)
    print("BLOCKCHAIN-CONTROLLED NETWORK STEGANOGRAPHY - RECEIVER")
    print("=" * 70)
    
    # Configuration
    if len(sys.argv) < 2:
        print("\nUsage: python network_receiver.py <channel> [duration]")
        print("\nExamples:")
        print("  python network_receiver.py timing")
        print("  python network_receiver.py size 120")
        print("\nChannels: timing, size, ttl")
        print("Duration: seconds to listen (default: 60)")
        return
    
    CHANNEL = sys.argv[1]
    DURATION = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    
    # Handle optional interface
    IFACE = None
    if "--iface" in sys.argv:
        try:
            idx = sys.argv.index("--iface")
            IFACE = sys.argv[idx + 1]
        except:
            pass
            
    # Auto-detect on Windows if not provided
    if not IFACE and os.name == 'nt':
        try:
            from scapy.all import get_working_ifaces
            # Match 10.210.59.20 specifically or any non-loopback
            ifaces = get_working_ifaces()
            for i in ifaces:
                if i.ip == '10.210.59.20' or (not i.ip.startswith('127.') and not i.ip.startswith('169.254')):
                    IFACE = i.name
                    break
        except:
            pass

    print(f"\n[CONFIG] Configuration:")
    print(f"   Channel: {CHANNEL}")
    print(f"   Duration: {DURATION} seconds")
    if IFACE:
        print(f"   Interface: {IFACE}")
    
    # Step 1: Get key from blockchain
    print(f"\n[STEP 1] Getting decryption key from blockchain...")
    key, key_hash, block_num = get_blockchain_key()
    print(f"[SUCCESS] Default key derived from blockchain")
    
    # Step 2: Capture and extract
    print(f"\n[STEP 2] Capturing network packets...")
    
    # Check if Stealth 2.0 is requested
    USE_STEALTH_2_0 = "--stealth" in sys.argv
    if USE_STEALTH_2_0:
        from stealth_engine import StealthEngine
        stealth = StealthEngine()
        print("[STEALTH 2.0 ACTIVE] Using Adaptive Bayesian Decoding...")

    try:
        if CHANNEL == "timing":
            if USE_STEALTH_2_0:
                print(f"Listening for STEALTH TIMING channel (duration: {DURATION}s)...")
                last_time = [None]
                binary_list = []
                def stealth_handler(packet):
                    current_time = time.time()
                    if last_time[0] is not None:
                        delay = current_time - last_time[0]
                        bit = stealth.decode_bit(delay, 'timing')
                        binary_list.append(bit)
                        if len(binary_list) % 20 == 0:
                            print(f"   Received: {len(binary_list)} stealth bits")
                    last_time[0] = current_time
                sniff(filter="icmp", prn=stealth_handler, timeout=DURATION, store=0, iface=IFACE)
                binary_data = "".join(binary_list)
                encrypted = "".join([chr(int(binary_data[i:i+8], 2)) for i in range(0, (len(binary_data)//8)*8, 8)])
            else:
                encrypted = receive_via_timing(DURATION)
                
        elif CHANNEL == "size":
            if USE_STEALTH_2_0:
                print(f"Listening for STEALTH SIZE channel (duration: {DURATION}s)...")
                binary_list = []
                def stealth_handler(packet):
                    if packet.haslayer(Raw):
                        size = len(packet[Raw].load) + 28
                        bit = stealth.decode_bit(size, 'size')
                        binary_list.append(bit)
                        if len(binary_list) % 20 == 0:
                            print(f"   Received: {len(binary_list)} stealth bits")
                sniff(filter="icmp", prn=stealth_handler, timeout=DURATION, store=0, iface=IFACE)
                binary_data = "".join(binary_list)
                encrypted = "".join([chr(int(binary_data[i:i+8], 2)) for i in range(0, (len(binary_data)//8)*8, 8)])
            else:
                encrypted = receive_via_size(DURATION)
                
        elif CHANNEL == "ttl":
            encrypted = receive_via_ttl(DURATION)
        elif CHANNEL == "drift":
            print(f"[INFRASTRUCTURE SILENCE] Listening for Slow-Burn channel...")
            print(f"Duration: {DURATION}s (statistical accumulation active)")
            
            last_time = [None]
            binary_list = []
            BASE_INTERVAL = 10 # Matches the sender's demo interval
            
            def drift_handler(packet):
                current_time = time.time()
                if last_time[0] is not None:
                    delay = current_time - last_time[0]
                    # Statistical decoding based on BASE_INTERVAL
                    # 9.95s = 0, 10.05s = 1
                    diff = delay - BASE_INTERVAL
                    if -0.1 < diff < -0.01: # 0
                        binary_list.append('0')
                        print(f"   [- Drift] Bit 0 detected (delay: {delay:.2f}s)")
                    elif 0.01 < diff < 0.1: # 1
                        binary_list.append('1')
                        print(f"   [+ Drift] Bit 1 detected (delay: {delay:.2f}s)")
                    
                    if len(binary_list) % 5 == 0 and len(binary_list) > 0:
                        print(f"   Accumulated: {len(binary_list)} drift bits")
                last_time[0] = current_time
            
            sniff(filter="icmp", prn=drift_handler, timeout=DURATION, store=0, iface=IFACE)
            binary_data = "".join(binary_list)
            encrypted = "".join([chr(int(binary_data[i:i+8], 2)) for i in range(0, (len(binary_data)//8)*8, 8)])
        else:
            print(f"Error: Unknown channel: {CHANNEL}")
            return
            
        if not encrypted or len(encrypted) < 5:
            print(f"\n[ERROR] No valid data extracted (extracted {len(encrypted) if encrypted else 0} chars)")
            return
        
        print(f"[SUCCESS] Data extracted")
        print(f"   Encrypted: {encrypted[:40]}...")
        
        # Step 3: Decrypt
        print(f"\n[STEP 3] Decrypting message...")
        
        # detect PQA Mode
        if encrypted.startswith("PQA:"):
            try:
                parts = encrypted.split(":", 2)
                pqa_c_b64 = parts[1]
                encrypted = parts[2]
                print(f"[PQA MODE DETECTED] Extracting quantum ciphertext...")
                
                # Load local PQA keys
                pk, sk = QuantumUtils.load_local_keys()
                if sk:
                    pqa_c = QuantumUtils.base64_to_bytes(pqa_c_b64)
                    ss = QuantumUtils.decapsulate(pqa_c, sk)
                    if ss:
                        # Derive Hybrid Key
                        key = QuantumUtils.get_hybrid_key(ss, key)
                        print(f"Hybrid Key derived from Kyber shared secret")
                    else:
                        print(f"PQA Decapsulation failed (Key Mismatch?)")
                else:
                    print(f"Local PQA Secret Key not found (quantum_keys.json)")
            except Exception as e:
                print(f"PQA Error: {e}")

        message = decrypt_message(encrypted, key)
        
        if message:
            print(f"\n" + "-" * 70)
            print(f"MESSAGE RECEIVED:")
            print(f"   {message}")
            print(f"-" * 70)
        else:
            print(f"\n[ERROR] Decryption failed")
            print(f"   Possible reasons:")
            print(f"   - Wrong channel selected")
            print(f"   - Key mismatch (time sync issue)")
            print(f"   - Incomplete data received")
        
    except PermissionError:
        print(f"\n ERROR: Permission denied")
        print(f"   Run as administrator/root:")
        print(f"   Windows: Run terminal as Administrator")
        print(f"   Linux: sudo python network_receiver.py ...")
    except Exception as e:
        print(f"\n ERROR: {e}")

if __name__ == "__main__":
    main()
