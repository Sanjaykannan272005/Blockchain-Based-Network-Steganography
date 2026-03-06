import json
from web3 import Web3

def verify_contracts():
    print("=== Verification of New Contracts ===")
    
    with open('blockchain_config.json', 'r') as f:
        config = json.load(f)
    
    w3 = Web3(Web3.HTTPProvider(config['rpc_url']))
    
    # Check Dead Drop
    print(f"Checking DeadDrop at: {config['dead_drop_contract']}")
    with open('DeadDrop_ABI.json', 'r') as f:
        dead_drop_abi = json.load(f)
    
    dead_drop = w3.eth.contract(address=config['dead_drop_contract'], abi=dead_drop_abi)
    try:
        count = dead_drop.functions.getMessageCount().call({'from': config['wallet_address']})
        print(f"✅ DeadDrop reachable. Initial messages: {count}")
    except Exception as e:
        print(f"❌ DeadDrop error: {e}")
        
    # Check Registry
    print(f"Checking StealthRegistry at: {config['registry_contract']}")
    # Assuming standard ABI for registry exists or using part of it
    registry_abi = [
        {
            "inputs": [],
            "name": "getAllNodes",
            "outputs": [
                {
                    "components": [
                        {"internalType": "address", "name": "wallet", "type": "address"},
                        {"internalType": "string", "name": "ip", "type": "string"},
                        {"internalType": "string[]", "name": "channels", "type": "string[]"},
                        {"internalType": "string", "name": "publicKey", "type": "string"},
                        {"internalType": "uint256", "name": "lastSeen", "type": "uint256"},
                        {"internalType": "bool", "name": "isActive", "type": "bool"}
                    ],
                    "internalType": "struct StealthRegistry.Node[]",
                    "name": "",
                    "type": "tuple[]"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]
    
    registry = w3.eth.contract(address=config['registry_contract'], abi=registry_abi)
    try:
        nodes = registry.functions.getAllNodes().call()
        print(f"✅ StealthRegistry reachable. Active nodes: {len(nodes)}")
    except Exception as e:
        print(f"❌ StealthRegistry error: {e}")

if __name__ == "__main__":
    verify_contracts()
