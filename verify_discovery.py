import json
from web3 import Web3

def verify_discovery():
    print("🔍 Fetching Verified Nodes from Blockchain...")
    with open('blockchain_config.json', 'r') as f:
        config = json.load(f)
    
    w3 = Web3(Web3.HTTPProvider(config['rpc_url']))
    with open('Registry_ABI.json', 'r') as f:
        abi = json.load(f)
        
    contract = w3.eth.contract(address=config['registry_contract'], abi=abi)
    nodes = contract.functions.getAllNodes().call()
    
    if not nodes:
        print("❌ No nodes found in registry.")
        return

    print(f"✅ Found {len(nodes)} verified nodes:")
    for i, node in enumerate(nodes):
        print(f"--- Node {i+1} ---")
        print(f"  Wallet:   {node[0]}")
        print(f"  IP:       {node[1]}")
        print(f"  Channels: {node[2]}")
        print(f"  Pub Key:  {node[3]}")
        print(f"  Active:   {node[5]}")

if __name__ == "__main__":
    verify_discovery()
