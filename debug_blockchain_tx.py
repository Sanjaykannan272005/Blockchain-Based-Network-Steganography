
import json
import os
import sys
from web3 import Web3
from blockchain_integration import BlockchainKeyExchange

def test_transactions():
    try:
        if not os.path.exists('blockchain_config.json'):
            print("Error: blockchain_config.json not found")
            return

        with open('blockchain_config.json', 'r') as f:
            config = json.load(f)

        rpc_url = config.get('rpc_url')
        if not rpc_url:
            print("Error: rpc_url not found in config")
            return

        print(f"Connecting to RPC: {rpc_url}")
        blockchain = BlockchainKeyExchange(rpc_url=rpc_url)
        
        addr = config.get('wallet_address')
        pk = config.get('private_key')
        
        if not addr or not pk:
            print("Error: wallet_address or private_key not found in config")
            return

        print(f"Testing with address: {addr}")
        balance_wei = blockchain.w3.eth.get_balance(addr)
        balance_eth = blockchain.w3.from_wei(balance_wei, 'ether')
        print(f"Balance: {balance_eth} ETH")

        # 1. Test Protocol Switch
        print("\n[1/2] Testing Switch Protocol...")
        controller_addr = config.get('controller_contract')
        if controller_addr:
            blockchain.load_controller_contract(controller_addr)
            # Try switching to current protocol to avoid state change if possible, or just 'timing'
            res = blockchain.switch_protocol(pk, 'timing')
            print(f"Switch Result: {res}")
        else:
            print("Controller contract not configured")

        # 2. Test Panic Trigger
        print("\n[2/2] Testing Panic Trigger...")
        registry_addr = config.get('registry_contract')
        if registry_addr:
            blockchain.load_registry_contract(registry_addr)
            res = blockchain.toggle_emergency_status(pk)
            print(f"Panic Result: {res}")
        else:
            print("Registry contract not configured")

    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_transactions()
