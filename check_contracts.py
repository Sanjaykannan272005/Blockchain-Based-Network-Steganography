import json
from web3 import Web3

def check_contracts():
    with open('blockchain_config.json', 'r') as f:
        config = json.load(f)
    
    w3 = Web3(Web3.HTTPProvider(config['rpc_url']))
    if not w3.is_connected():
        print("Failed to connect to Sepolia RPC")
        return

    print(f"Connected to Sepolia. Block height: {w3.eth.block_number}")
    
    contracts = {
        "StealthRegistry": config['registry_contract'],
        "DeadDrop": config['dead_drop_contract'],
        "SenderAccessControl": config['access_control_contract']
    }

    for name, addr in contracts.items():
        code = w3.eth.get_code(addr)
        if len(code) > 2:
            print(f"✅ {name} verified at {addr}")
        else:
            print(f"❌ {name} NOT FOUND at {addr}")

if __name__ == "__main__":
    check_contracts()
