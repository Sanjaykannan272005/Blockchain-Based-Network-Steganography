import json
from web3 import Web3

with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

w3 = Web3(Web3.HTTPProvider(config['rpc_url']))
address = config['wallet_address']

balance = w3.eth.get_balance(address)
eth_balance = w3.from_wei(balance, 'ether')

nonce_latest = w3.eth.get_transaction_count(address, 'latest')
nonce_pending = w3.eth.get_transaction_count(address, 'pending')

print(f"Address: {address}")
print(f"Balance: {eth_balance} ETH")
print(f"Latest Nonce: {nonce_latest}")
print(f"Pending Nonce: {nonce_pending}")
