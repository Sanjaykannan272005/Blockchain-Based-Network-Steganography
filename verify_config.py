import os
import json
import sys
from blockchain_integration import BlockchainKeyExchange

def verify_config():
    print("🔍 Testing Configuration Priority...")
    os.environ['RPC_URL'] = "https://mock-rpc-from-env.io"
    os.environ['REGISTRY_CONTRACT'] = "0x1234567890123456789012345678901234567890"
    blockchain = BlockchainKeyExchange()
    if blockchain.rpc_url == os.environ['RPC_URL']:
        print("✅ SUCCESS: RPC_URL correctly loaded from environment.")
    else:
        print(f"❌ FAILURE: RPC_URL mismatch. Got {blockchain.rpc_url}")
    success = blockchain.load_registry_contract()
    if success:
        print("✅ SUCCESS: Registry contract addr loaded from environment.")
    else:
        print("❌ FAILURE: Registry contract load failed.")

if __name__ == "__main__":
    verify_config()
