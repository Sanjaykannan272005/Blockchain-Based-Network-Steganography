import json
from web3 import Web3

def check_balance():
    with open('blockchain_config.json', 'r') as f:
        config = json.load(f)
    w3 = Web3(Web3.HTTPProvider(config['rpc_url']))
    balance = w3.eth.get_balance(config['owner_address'])
    print(f"Address: {config['owner_address']}")
    print(f"Balance: {w3.from_hex(hex(balance)) if isinstance(balance, str) else w3.from_wei(balance, 'ether')} ETH")

if __name__ == "__main__":
    check_balance()
