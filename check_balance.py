#!/usr/bin/env python3
"""
Check Ethereum Wallet Balance
"""

from web3 import Web3
import json

# Load config
with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

# Your wallet address
wallet_address = '0x7A2C2AF27b1E4afBBaBfcfc6e30Dd411D432AcA4'

# Connect to Ethereum
w3 = Web3(Web3.HTTPProvider(config['rpc_url']))

print("=" * 60)
print("CHECKING WALLET BALANCE")
print("=" * 60)
print(f"\nWallet: {wallet_address}")
print(f"Network: Sepolia Testnet")
print("\nChecking balance...\n")

try:
    # Get balance
    balance_wei = w3.eth.get_balance(wallet_address)
    balance_eth = w3.from_wei(balance_wei, 'ether')
    
    # Get transaction count
    tx_count = w3.eth.get_transaction_count(wallet_address)
    
    print("=" * 60)
    print("WALLET STATUS")
    print("=" * 60)
    print(f"\nBalance: {balance_eth} ETH")
    print(f"Transactions: {tx_count}")
    
    if balance_eth > 0:
        print(f"\nStatus: FUNDED")
        print("\nYou have test ETH! Ready to use blockchain!")
        print("\nNext steps:")
        print("1. Deploy smart contract on Remix")
        print("2. Update blockchain_integration.py")
        print("3. Start sending messages on real blockchain!")
    else:
        print(f"\nStatus: NO FUNDS")
        print("\nYou need test ETH!")
        print("\nGet free test ETH:")
        print("1. Visit: https://sepoliafaucet.com")
        print(f"2. Paste address: {wallet_address}")
        print("3. Click 'Send Me ETH'")
        print("4. Wait 30 seconds")
        print("5. Run this script again")
    
    print("\n" + "=" * 60)
    print(f"Etherscan: https://sepolia.etherscan.io/address/{wallet_address}")
    print("=" * 60)
    
except Exception as e:
    print(f"Error: {e}")
