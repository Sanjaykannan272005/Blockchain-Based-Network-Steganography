import json
import time
from web3 import Web3
from solcx import compile_standard, install_solc

def deploy_advanced_contracts():
    print("1. Installing Solidity Compiler...")
    install_solc('0.8.0')

    print("2. Loading Configuration...")
    with open('blockchain_config.json', 'r') as f:
        config = json.load(f)

    RPC_URL = config['rpc_url']
    PRIVATE_KEY = config['private_key']
    MY_ADDRESS = config['owner_address']
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    chain_id = config['chain_id']

    if not w3.is_connected():
        print("❌ Failed to connect to Blockchain.")
        return

    contracts_to_deploy = ["SecureUserRegistry", "AdvancedSteganographyController"]
    new_addresses = {}

    for contract_name in contracts_to_deploy:
        print(f"\n--- Deploying {contract_name} ---")
        with open(f'{contract_name}.sol', 'r') as file:
            source = file.read()

        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {f"{contract_name}.sol": {"content": source}},
                "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode.object"]}}},
            },
            solc_version="0.8.0",
        )

        bytecode = compiled_sol["contracts"][f"{contract_name}.sol"][contract_name]["evm"]["bytecode"]["object"]
        abi = compiled_sol["contracts"][f"{contract_name}.sol"][contract_name]["abi"]

        Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        nonce = w3.eth.get_transaction_count(MY_ADDRESS)

        transaction = Contract.constructor().build_transaction({
            "chainId": chain_id,
            "from": MY_ADDRESS,
            "nonce": nonce,
            "gas": 4000000,
            "gasPrice": int(w3.eth.gas_price * 1.5)
        })

        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
        
        # Handle different signed_txn object structures
        if hasattr(signed_txn, 'rawTransaction'):
            raw_tx = signed_txn.rawTransaction
        elif hasattr(signed_txn, 'raw_transaction'):
            raw_tx = signed_txn.raw_transaction
        else:
            raw_tx = signed_txn.get('rawTransaction') or signed_txn.get('raw_transaction')

        tx_hash = w3.eth.send_raw_transaction(raw_tx)
        print(f"   Sent! Hash: {tx_hash.hex()}")
        
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        addr = tx_receipt.contractAddress
        print(f"✅ {contract_name} Deployed at {addr}")
        new_addresses[contract_name] = addr

    # Update Config
    config['user_registry_contract'] = new_addresses["SecureUserRegistry"]
    config['controller_contract'] = new_addresses["AdvancedSteganographyController"]
    
    with open('blockchain_config.json', 'w') as f:
        json.dump(config, f, indent=4)
    print("\n✅ Updated blockchain_config.json with all contract addresses.")

if __name__ == "__main__":
    deploy_advanced_contracts()
