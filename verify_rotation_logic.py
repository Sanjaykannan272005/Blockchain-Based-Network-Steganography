import hashlib
import json
import time
from Crypto.Cipher import AES
import base64
from blockchain_integration import BlockchainKeyExchange
from network_sender import get_blockchain_key as sender_get_key, encrypt_message
from network_receiver import get_blockchain_key as receiver_get_key, decrypt_message

def test_rotation():
    print("=== Testing Block-Hash Key Rotation ===")
    
    # 1. Sender Side
    print("\n[SENDER] Deriving key for latest block...")
    key, key_hash, block_num = sender_get_key()
    if block_num == 0:
        print("❌ Block-Hash Key Rotation failed (Simulation fallback used)")
        return
    
    print(f"✅ Key derived from Block #{block_num}")
    print(f"   Key hash: {key_hash}")
    
    secret = "Top secret block-hash message"
    encrypted = encrypt_message(secret, key)
    # Add header
    transmission = f"BK:{block_num}:{encrypted}"
    print(f"📡 Transmission payload: {transmission[:50]}...")
    
    # 2. Receiver Side
    print("\n[RECEIVER] Detecting transmission...")
    if transmission.startswith("BK:"):
        parts = transmission.split(":", 2)
        target_block = int(parts[1])
        captured_payload = parts[2]
        print(f"🔗 Header detected: Block #{target_block}")
        
        # Recover key
        rec_key, rec_hash, _ = receiver_get_key(target_block)
        print(f"✅ Key recovered from Blockchain")
        print(f"   Recovered key hash: {rec_hash}")
        
        if rec_hash == key_hash:
            print("💎 KEY MATCH CONFIRMED!")
        else:
            print("❌ KEY MISMATCH!")
            return
            
        # Decrypt
        decrypted = decrypt_message(captured_payload, rec_key)
        print(f"🔓 Decrypted: {decrypted}")
        
        if decrypted == secret:
            print("\n🌟 SUCCESS: Block-Hash Key Rotation verified end-to-end!")
        else:
            print("\n❌ FAILURE: Decryption mismatch")

if __name__ == "__main__":
    test_rotation()
