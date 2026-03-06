#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test blockchain connection and balance"""

from web3 import Web3
import json
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load config
with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

print("Testing Blockchain Connection...")
print(f"Network: {config['network']}")
print(f"RPC URL: {config['rpc_url']}")

# Connect
w3 = Web3(Web3.HTTPProvider(config['rpc_url']))

# Check connection
if w3.is_connected():
    print("Connected to Ethereum!")
    
    # Check balance
    address = config['wallet_address']
    balance = w3.eth.get_balance(address)
    eth_balance = w3.from_wei(balance, 'ether')
    
    print(f"\nWallet Info:")
    print(f"Address: {address}")
    print(f"Balance: {eth_balance} ETH")
    print(f"Block Number: {w3.eth.block_number}")
    print(f"\nView on Etherscan:")
    print(f"{config['explorer']}/address/{address}")
    
    if eth_balance > 0:
        print("\nYou have test ETH! Ready to use blockchain features.")
    else:
        print("\nNo ETH balance. Get test ETH from faucet.")
else:
    print("Failed to connect to Ethereum")
