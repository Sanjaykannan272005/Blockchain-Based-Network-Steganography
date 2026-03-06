from web3 import Web3
import json
import os

def generate_wallets(count=2):
    w3 = Web3()
    wallets = []
    
    print(f"Generating {count} new test wallets...")
    
    for i in range(count):
        account = w3.eth.account.create()
        wallet = {
            "name": f"Test-User-{i+1}",
            "address": account.address,
            "private_key": account.key.hex()
        }
        wallets.append(wallet)
        print(f"Created: {wallet['name']} ({wallet['address']})")

    # Save to file
    output_file = 'test_users.json'
    with open(output_file, 'w') as f:
        json.dump(wallets, f, indent=4)
    
    print(f"\nSuccessfully saved {count} wallets to {output_file}")
    return wallets

if __name__ == "__main__":
    generate_wallets()
