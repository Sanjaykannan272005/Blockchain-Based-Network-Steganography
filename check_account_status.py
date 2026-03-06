import json
from web3 import Web3

def check_status():
    with open('blockchain_config.json', 'r') as f:
        config = json.load(f)
    w3 = Web3(Web3.HTTPProvider(config['rpc_url']))
    addr = config['owner_address']
    balance = w3.eth.get_balance(addr)
    tx_count = w3.eth.get_transaction_count(addr)
    pending_count = w3.eth.get_transaction_count(addr, 'pending')
    
    print(f"Address: {addr}")
    print(f"Confirmed Balance: {w3.from_wei(balance, 'ether')} ETH")
    print(f"Confirmed Nonce: {tx_count}")
    print(f"Pending Nonce: {pending_count}")

if __name__ == "__main__":
    check_status()
