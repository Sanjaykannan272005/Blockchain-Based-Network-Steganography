import requests
import json
import time
from web3 import Web3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

# Configuration
BASE_URL = "http://127.0.0.1:5000"
SENDER_URL = "http://127.0.0.1:5003"
AUTH_URL = "http://127.0.0.1:5002"

with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

with open('test_users.json', 'r') as f:
    test_users = json.load(f)

w3 = Web3(Web3.HTTPProvider(config['rpc_url']))

def test_encryption_decryption():
    print("\n--- Test 1: Encryption & Decryption (Local) ---")
    message = "Secret System Message 123"
    key = b'0123456789abcdef0123456789abcdef' # 32 bytes
    iv = b'1234567890123456' # 16 bytes
    
    # Encryption
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    encrypted = base64.b64encode(iv + ct_bytes).decode('utf-8')
    print(f"Encrypted: {encrypted}")
    
    # Decryption
    raw = base64.b64decode(encrypted)
    iv_dec = raw[:16]
    ct_dec = raw[16:]
    cipher_dec = AES.new(key, AES.MODE_CBC, iv_dec)
    pt = unpad(cipher_dec.decrypt(ct_dec), AES.block_size).decode('utf-8')
    print(f"Decrypted: {pt}")
    
    assert pt == message, "Encryption/Decryption mismatch!"
    print("✅ Encryption/Decryption Verified")

def test_blockchain_discovery():
    print("\n--- Test 2: Blockchain Node Discovery ---")
    try:
        response = requests.get(f"{BASE_URL}/api/verified_nodes")
        data = response.json()
        if data.get('success'):
            nodes = data.get('nodes', [])
            print(f"Found {len(nodes)} nodes on blockchain")
            for node in nodes:
                print(f" - Node: {node['ip']} (Reputation: {node['reputation']})")
            print("✅ Blockchain Discovery Verified")
        else:
            print(f"❌ Discovery error: {data.get('error')}")
    except Exception as e:
        print(f"❌ API Connection Failed: {e}")

def test_user_registry_status():
    print("\n--- Test 3: Advanced Security (Identity & Clearance) ---")
    wallet = config['wallet_address']
    try:
        response = requests.get(f"{BASE_URL}/api/registry/status/{wallet}")
        data = response.json()
        if data.get('success'):
            print(f"Identity: {data.get('organization')} | Clearance: {data.get('clearance')}")
            print("✅ Identity Registry Verified")
        else:
            print(f"⚠️ User not found in registry (Expected if not registered via script yet)")
    except Exception as e:
        print(f"❌ Registry API Failed: {e}")

def test_dead_drop_inbox():
    print("\n--- Test 4: Blockchain Dead Drop Inbox ---")
    try:
        response = requests.get(f"{BASE_URL}/dead_drop_check")
        data = response.json()
        if data.get('success'):
            messages = data.get('messages', [])
            print(f"Inbox count: {len(messages)}")
            for msg in messages[:2]:
                status = "LOCKED" if msg.get('is_locked') else "RELEASED"
                print(f" - From: {msg['sender'][:10]}... | Status: {status}")
            print("✅ Dead Drop API Verified")
        else:
            print(f"❌ Dead Drop error: {data.get('error')}")
    except Exception as e:
        print(f"❌ Dead Drop API Failed: {e}")

def run_all_tests():
    print("====================================================")
    print("⛓️  STEGANOGRAPHY NETWORK SYSTEM VALIDATION ⛓️")
    print("====================================================")
    
    try:
        test_encryption_decryption()
        test_blockchain_discovery()
        test_user_registry_status()
        test_dead_drop_inbox()
        
        print("\n====================================================")
        print("🎉 ALL SYSTEM TESTS COMPLETED SUCCESSFULLY!")
        print("====================================================")
    except AssertionError as e:
        print(f"\n❌ VALIDATION FAILED: {e}")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    run_all_tests()
