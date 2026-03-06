import json
from web3 import Web3

def find_pending():
    with open('blockchain_config.json', 'r') as f:
        config = json.load(f)
    w3 = Web3(Web3.HTTPProvider(config['rpc_url']))
    addr = config['owner_address']
    
    # Check pending block
    try:
        pending_block = w3.eth.get_block('pending', full_transactions=True)
        for tx in pending_block.transactions:
            if tx['from'].lower() == addr.lower():
                print(f"Pending TX Found: {tx['hash'].hex()}")
                print(f"Nonce: {tx['nonce']}")
                print(f"Gas Price: {tx['gasPrice']}")
    except:
        # Some providers don't support full pending block
        print("Could not retrieve full pending block. Trying alternatives...")
        # We can't easily find a specific pending hash without full block access
        # but we can try to check if it confirmed recently.

if __name__ == "__main__":
    find_pending()
