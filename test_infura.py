#!/usr/bin/env python3
"""
Test Infura Connection
Verify your API key works
"""

import json
import requests

# Load config
with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

print("=" * 60)
print("TESTING INFURA CONNECTION")
print("=" * 60)
print(f"\nAPI Key: {config['infura_api_key'][:10]}...")
print(f"Network: {config['network']}")
print(f"RPC URL: {config['rpc_url']}")
print("\nTesting connection...\n")

# Test connection
try:
    response = requests.post(
        config['rpc_url'],
        json={
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": [],
            "id": 1
        },
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        
        if 'result' in data:
            block_number = int(data['result'], 16)
            
            print("CONNECTION SUCCESSFUL!")
            print(f"\nCurrent Block Number: {block_number}")
            print(f"Network: Sepolia Testnet")
            print(f"Status: CONNECTED")
            print("\n" + "=" * 60)
            print("Your Infura API key is working!")
            print("=" * 60)
            print("\nNext steps:")
            print("1. Get test ETH from faucet")
            print("2. Create Ethereum wallet")
            print("3. Deploy smart contract")
            print("4. Start using real blockchain!")
            
        else:
            print("❌ ERROR:", data.get('error', 'Unknown error'))
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ CONNECTION FAILED: {e}")
    print("\nTroubleshooting:")
    print("- Check your internet connection")
    print("- Verify API key is correct")
    print("- Try again in a few minutes")
