#!/usr/bin/env python3
"""
Network Steganography Sender
Sends secret messages hidden in network packets
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
from quantum_utils import QuantumUtils

# Blockchain key derivation
def get_blockchain_key(block_number=None):
    """Derive encryption key from blockchain data (Real or Simulated)"""
    try:
        from blockchain_integration import BlockchainKeyExchange
        import json
        
        # Load config to get RPC URL
        rpc_url = "https://sepolia.infura.io/v3/b9fc4ab7927e41fdb20bf3f50dd6afad"
        if os.path.exists('blockchain_config.json'):
            with open('blockchain_config.json', 'r') as f:
                config = json.load(f)
                rpc_url = config.get('rpc_url', rpc_url)
        
        blockchain = BlockchainKeyExchange(rpc_url=rpc_url)
        
        if block_number:
            print(f"🔗 Fetching Hash for Block #{block_number}...")
            res = blockchain.get_block_hash(block_number)
        else:
            print(f"🔗 Fetching Latest Block Hash...")
            res = blockchain.get_latest_block_data()
            block_number = res.get('number')
            
        if res.get('success'):
            block_hash = res['hash']
            key = hashlib.sha256(block_hash.encode()).digest()
            return key, block_hash[:20], block_number
    except Exception as e:
        print(f"⚠️ Blockchain Error: {e}. Falling back to simulation.")

    # Fallback to simulation (same as before)
    block_time = int(time.time() / 60) * 60  # Round to minute
    sim_hash = hashlib.sha256(f"block_{block_time}".encode()).hexdigest()
    key = hashlib.sha256(sim_hash.encode()).digest()
    return key, sim_hash[:20], 0

# Encrypt message
def encrypt_message(message, key):
    """Encrypt message with AES-256"""
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    pad_length = 16 - (len(message) % 16)
    padded = message + (chr(pad_length) * pad_length)
    encrypted = cipher.encrypt(padded.encode())
    return base64.b64encode(iv + encrypted).decode()

# Send via TIMING channel
def send_via_timing(encrypted_data, target_ip):
    """Hide data in packet timing delays"""
    print(f"🚀 Sending via TIMING channel to {target_ip}")
    
    # Convert to binary
    binary = ''.join(format(ord(c), '08b') for c in encrypted_data)
    
    print(f"📊 Sending {len(binary)} bits ({len(encrypted_data)} chars)")
    
    # Send packets with timing delays
    for i, bit in enumerate(binary):
        # Send ICMP ping
        packet = IP(dst=target_ip)/ICMP(seq=i)
        send(packet, verbose=0)
        
        # Delay encodes the bit
        if bit == '0':
            time.sleep(0.1)  # 100ms = 0
        else:
            time.sleep(0.2)  # 200ms = 1
        
        if (i + 1) % 80 == 0:
            print(f"  Progress: {i+1}/{len(binary)} bits")
    
    print(f"✅ Sent {len(binary)} bits via timing channel")

# Send via SIZE channel
def send_via_size(encrypted_data, target_ip):
    """Hide data in packet sizes"""
    print(f"🚀 Sending via SIZE channel to {target_ip}")
    
    # Convert to binary
    binary = ''.join(format(ord(c), '08b') for c in encrypted_data)
    
    print(f"📊 Sending {len(binary)} bits ({len(encrypted_data)} chars)")
    
    # Send packets with different sizes
    for i, bit in enumerate(binary):
        if bit == '0':
            payload = "X" * 100  # 100 bytes = 0
        else:
            payload = "X" * 200  # 200 bytes = 1
        
        packet = IP(dst=target_ip)/ICMP(seq=i)/payload
        send(packet, verbose=0)
        
        if (i + 1) % 80 == 0:
            print(f"  Progress: {i+1}/{len(binary)} bits")
    
    print(f"✅ Sent {len(binary)} bits via size channel")

# Send via TTL channel
def send_via_ttl(encrypted_data, target_ip):
    """Hide data in TTL field"""
    print(f"🚀 Sending via TTL channel to {target_ip}")
    
    # Convert to binary
    binary = ''.join(format(ord(c), '08b') for c in encrypted_data)
    
    print(f"📊 Sending {len(binary)} bits ({len(encrypted_data)} chars)")
    
    # Send packets with different TTL values
    for i, bit in enumerate(binary):
        if bit == '0':
            ttl = 64  # TTL 64 = 0
        else:
            ttl = 65  # TTL 65 = 1
        
        packet = IP(dst=target_ip, ttl=ttl)/ICMP(seq=i)
        send(packet, verbose=0)
        
        if (i + 1) % 80 == 0:
            print(f"  Progress: {i+1}/{len(binary)} bits")
    
    print(f"✅ Sent {len(binary)} bits via TTL channel")

# Main
def main():
    print("=" * 70)
    print("BLOCKCHAIN-CONTROLLED NETWORK STEGANOGRAPHY - SENDER")
    print("=" * 70)
    
    # Configuration
    if len(sys.argv) < 3:
        print("\nUsage: python network_sender.py <target_ip> <message> [channel]")
        print("\nExamples:")
        print("  python network_sender.py 192.168.1.100 \"Attack at dawn\"")
        print("  python network_sender.py 127.0.0.1 \"Secret message\" timing")
        print("\nChannels: timing (default), size, ttl")
        return
    
    TARGET_IP = sys.argv[1]
    SECRET_MESSAGE = sys.argv[2]
    CHANNEL = sys.argv[3] if len(sys.argv) > 3 else "timing"
    
    print(f"\n📝 Configuration:")
    print(f"   Target IP: {TARGET_IP}")
    print(f"   Message: {SECRET_MESSAGE}")
    print(f"   Channel: {CHANNEL}")
    
    # Step 1: Get key from blockchain
    print(f"\n📡 Step 1: Getting encryption key from blockchain...")
    
    BLOCK_KEY_MODE = "--block-key" in sys.argv
    key, key_hash, block_num = get_blockchain_key()
    print(f"✅ Key derived from blockchain")
    print(f"   Key hash: {key_hash}...")
    if block_num > 0:
        print(f"   Using Block: #{block_num}")
    
    # Step 2: Encrypt message
    print(f"\n🔒 Step 2: Encrypting message...")
    
    # Check for Quantum-Safe Target
    USE_QUANTUM = "--quantum" in sys.argv
    pqa_ciphertext = None
    
    if USE_QUANTUM:
        from blockchain_integration import BlockchainKeyExchange
        import json
        
        # Try to find receiver's PQA public key
        rpc_url = "https://sepolia.infura.io/v3/b9fc4ab7927e41fdb20bf3f50dd6afad"
        if os.path.exists('blockchain_config.json'):
            with open('blockchain_config.json', 'r') as f:
                config = json.load(f)
                rpc_url = config.get('rpc_url', rpc_url)
        
        blockchain = BlockchainKeyExchange(rpc_url=rpc_url)
        # For simplicity in the CLI, we might need a --receiver-wallet arg if TARGET_IP is just an IP
        # But we can try to find a node in the registry that matches the TARGET_IP
        nodes_res = blockchain.get_blockchain_nodes()
        target_pk_b64 = None
        
        if nodes_res.get('success'):
            for node in nodes_res['nodes']:
                if node['ip'] == TARGET_IP:
                    target_pk_b64 = node['public_key']
                    print(f"🕵️ Target PQA Public Key found in Registry: {target_pk_b64[:20]}...")
                    break
        
        if target_pk_b64:
            try:
                target_pk = QuantumUtils.base64_to_bytes(target_pk_b64)
                c, ss = QuantumUtils.encapsulate(target_pk)
                pqa_ciphertext = c
                # Derive Hybrid Key
                key = QuantumUtils.get_hybrid_key(ss, key)
                print(f"🛡️ [HYBRID PQA ACTIVE] Key hardened with Kyber-768")
            except Exception as e:
                print(f"⚠️ PQA Error: {e}. Defaulting to Classical.")
        else:
            print(f"⚠️ No PQA Public Key found for {TARGET_IP}. Defaulting to Classical.")

    encrypted_payload = encrypt_message(SECRET_MESSAGE, key)
    
    # Prepend PQA Ciphertext if used
    if pqa_ciphertext:
        # Prepend PQA: followed by length-prefixed ciphertext
        # But since Kyber-768 'c' is fixed length (1088), we can just prepend a tag
        c_b64 = QuantumUtils.bytes_to_base64(pqa_ciphertext)
        encrypted_payload = f"PQA:{c_b64}:{encrypted_payload}"
        print(f"   PQA Header Added (Size: {len(c_b64)} chars)")

    # If using Block Key, prepend the block number so the receiver can recover it
    if BLOCK_KEY_MODE and block_num > 0:
        encrypted_payload = f"BK:{block_num}:{encrypted_payload}"
        print(f"   Block-Key Header Added: BK:{block_num}")
    
    # Check if P2P (Onion Routing) is requested
    HOPS_ARG = None
    for i, arg in enumerate(sys.argv):
        if arg == "--hops" and i + 1 < len(sys.argv):
            HOPS_ARG = sys.argv[i+1]
            break
            
    if HOPS_ARG:
        from onion_utils import OnionUtils
        import json
        try:
            hops_data = json.loads(HOPS_ARG)
            # hops_data: [{"ip": "...", "channel": "...", "secret": "..."}, ...]
            print(f"🕸️ [P2P MODE] Building {len(hops_data)} onion layers...")
            
            hops = [(h['ip'], h['channel']) for h in hops_data]
            keys = [OnionUtils.derive_key(h['secret']) for h in hops_data]
            
            # Use the already encrypted payload (which may have BK: header) as the core
            inner_payload = encrypted_payload
            
            # Wrap in onion layers
            encrypted = OnionUtils.create_onion(inner_payload, hops, keys)
            print(f"✅ Onion built: {len(encrypted)} characters")
            
            # The FIRST hop protocol is what we use initially
            TARGET_IP = hops[0][0]
            CHANNEL = hops[0][1]
            print(f"📍 Entry Node: {TARGET_IP} using {CHANNEL}")
            
        except Exception as e:
            print(f"❌ P2P Error: {e}")
            return
    else:
        print(f"🔒 Finalizing Payload...")
        encrypted = encrypted_payload
        print(f"✅ Payload ready")
        print(f"   Content: {encrypted[:40]}...")
        print(f"   Length: {len(encrypted)} characters")
    
    # Step 3: Send via network
    print(f"\n🌐 Step 3: Sending via network steganography...")
    print(f"   Channel: {CHANNEL}")
    
    # Check if Stealth 2.0 is requested
    USE_STEALTH_2_0 = "--stealth" in sys.argv
    if USE_STEALTH_2_0:
        from stealth_engine import StealthEngine
        stealth = StealthEngine()
        print("🚀 [STEALTH 2.0 ACTIVE] Mimicking traffic DNA patterns...")
    
    try:
        # Get bits for stealth modulation
        binary = ''.join(format(ord(c), '08b') for c in encrypted)
        
        if CHANNEL == "timing":
            if USE_STEALTH_2_0:
                print(f"🚀 Sending via STEALTH TIMING channel to {TARGET_IP}")
                for i, bit in enumerate(binary):
                    packet = IP(dst=TARGET_IP)/ICMP(seq=i)
                    send(packet, verbose=0)
                    delay = stealth.get_stealth_delay(bit)
                    time.sleep(delay)
                    if (i + 1) % 20 == 0:
                        print(f"  Stealth Progress: {i+1}/{len(binary)} bits")
            else:
                send_via_timing(encrypted, TARGET_IP)
                
        elif CHANNEL == "size":
            if USE_STEALTH_2_0:
                print(f"🚀 Sending via STEALTH SIZE channel to {TARGET_IP}")
                for i, bit in enumerate(binary):
                    size = stealth.get_stealth_size(bit)
                    payload = "X" * (size - 28) # Adjust for IP/ICMP headers
                    packet = IP(dst=TARGET_IP)/ICMP(seq=i)/payload
                    send(packet, verbose=0)
                    if (i + 1) % 20 == 0:
                        print(f"  Stealth Progress: {i+1}/{len(binary)} bits")
            else:
                send_via_size(encrypted, TARGET_IP)
                
        elif CHANNEL == "ttl":
            send_via_ttl(encrypted, TARGET_IP)
        elif CHANNEL == "drift":
            from infrastructure_drift import InfrastructureDrift
            # In drift mode, we use the InfrastructureDrift engine to manage intervals
            drift_engine = InfrastructureDrift(encrypted, base_interval=10) # 10s for demo
            print(f"🚀 [INFRASTRUCTURE SILENCE] Starting slow-burn transmission...")
            
            while True:
                delay = drift_engine.get_next_delay()
                if delay is None: break
                
                packet = IP(dst=TARGET_IP)/ICMP(type=8, code=0, seq=drift_engine.state['current_index'])
                send(packet, verbose=0)
                
                print(f"📡 Bit {drift_engine.state['current_index']} modulated. Next in {delay:.2f}s")
                print(f"📊 Progress: {drift_engine.get_progress():.2f}%")
                time.sleep(delay)
        else:
            print(f"❌ Unknown channel: {CHANNEL}")
            return
        
        print(f"\n✅ MESSAGE SENT SUCCESSFULLY!")
        print(f"📝 Receiver should run: python network_receiver.py {CHANNEL}")
        
    except PermissionError:
        print(f"\n❌ ERROR: Permission denied")
        print(f"   Run as administrator/root:")
        print(f"   Windows: Run terminal as Administrator")
        print(f"   Linux: sudo python network_sender.py ...")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()
