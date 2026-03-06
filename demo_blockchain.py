# -*- coding: utf-8 -*-
"""Simple Blockchain Steganography Demo"""

from web3 import Web3
import json
import hashlib
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load config
with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

w3 = Web3(Web3.HTTPProvider(config['rpc_url']))

print("=" * 60)
print("BLOCKCHAIN STEGANOGRAPHY DEMO")
print("=" * 60)

# Check connection
if not w3.is_connected():
    print("ERROR: Cannot connect to Ethereum")
    sys.exit(1)

balance = w3.from_wei(w3.eth.get_balance(config['wallet_address']), 'ether')
print(f"\nWallet: {config['wallet_address']}")
print(f"Balance: {balance} ETH")
print(f"Network: {config['network']}")

# Demo: Store encryption key on blockchain
print("\n" + "=" * 60)
print("DEMO: Storing Encryption Key on Blockchain")
print("=" * 60)

message = "Secret military operation at 0600 hours"
password = "supersecret123"
receiver = config['wallet_address']

print(f"\nMessage: {message}")
print(f"Password: {password}")

# Calculate message hash
msg_hash = hashlib.sha256(message.encode()).hexdigest()
print(f"Message Hash: {msg_hash[:16]}...")

# Create transaction
print("\nCreating blockchain transaction...")
try:
    nonce = w3.eth.get_transaction_count(config['wallet_address'])
    
    tx = {
        'nonce': nonce,
        'to': receiver,
        'value': 0,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
        'data': w3.to_hex(text=f"{msg_hash}:{password}"),
        'chainId': config['chain_id']
    }
    
    print(f"Gas Price: {w3.from_wei(tx['gasPrice'], 'gwei')} Gwei")
    print(f"Estimated Cost: {w3.from_wei(tx['gas'] * tx['gasPrice'], 'ether')} ETH")
    
    # Sign and send
    signed_tx = w3.eth.account.sign_transaction(tx, config['private_key'])
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"\nTransaction sent!")
    print(f"TX Hash: {tx_hash.hex()}")
    print(f"Etherscan: {config['explorer']}/tx/{tx_hash.hex()}")
    
    # Wait for confirmation
    print("\nWaiting for confirmation...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    
    if receipt['status'] == 1:
        print("SUCCESS! Transaction confirmed")
        print(f"Block: {receipt['blockNumber']}")
        print(f"Gas Used: {receipt['gasUsed']}")
        
        # Retrieve data
        print("\n" + "=" * 60)
        print("DEMO: Retrieving Key from Blockchain")
        print("=" * 60)
        
        tx_data = w3.eth.get_transaction(tx_hash.hex())
        retrieved_data = w3.to_text(tx_data['input'])
        retrieved_hash, retrieved_password = retrieved_data.split(':')
        
        print(f"\nRetrieved Password: {retrieved_password}")
        print(f"Retrieved Hash: {retrieved_hash[:16]}...")
        print(f"Sender: {tx_data['from']}")
        
        if retrieved_password == password:
            print("\nVERIFIED! Password matches")
        
    else:
        print("FAILED! Transaction reverted")
        
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "=" * 60)
print("Demo complete! Check Etherscan for details.")
print("=" * 60)
