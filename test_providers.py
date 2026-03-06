# -*- coding: utf-8 -*-
"""Test blockchain connection with multiple providers"""

from web3 import Web3
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

providers = [
    ("Alchemy", f"https://eth-sepolia.g.alchemy.com/v2/{config['alchemy_api_key']}"),
    ("Infura", f"https://sepolia.infura.io/v3/{config['infura_api_key']}")
]

print("Testing Blockchain Providers...\n")

for name, url in providers:
    print(f"Testing {name}...")
    try:
        w3 = Web3(Web3.HTTPProvider(url))
        if w3.is_connected():
            balance = w3.eth.get_balance(config['wallet_address'])
            eth_balance = w3.from_wei(balance, 'ether')
            print(f"  SUCCESS! Balance: {eth_balance} ETH")
            print(f"  Block: {w3.eth.block_number}")
            
            # Update config with working provider
            config['rpc_url'] = url
            with open('blockchain_config.json', 'w') as f:
                json.dump(config, f, indent=2)
            print(f"  Updated config to use {name}\n")
            break
        else:
            print(f"  Failed to connect\n")
    except Exception as e:
        print(f"  Error: {e}\n")

print(f"\nWallet: {config['wallet_address']}")
print(f"Etherscan: {config['explorer']}/address/{config['wallet_address']}")
