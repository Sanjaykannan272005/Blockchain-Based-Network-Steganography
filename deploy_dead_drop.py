import json
import time
from web3 import Web3
from solcx import compile_standard, install_solc

# Install specific Solidity compiler version
print("1. Installing Solidity Compiler...")
install_solc('0.8.0')

# Load Configuration
print("2. Loading Configuration...")
with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

RPC_URL = config['rpc_url']
PRIVATE_KEY = config['private_key']
MY_ADDRESS = config['owner_address']

# Connect to Blockchain
w3 = Web3(Web3.HTTPProvider(RPC_URL))
chain_id = config['chain_id']

if not w3.is_connected():
    print("❌ Failed to connect to Blockchain. Check RPC URL.")
    exit(1)
print(f"✅ Connected to Blockchain (Chain ID: {chain_id})")

# Read Solidity File
with open('DeadDrop.sol', 'r') as file:
    dead_drop_file = file.read()

# Compile Solidity
print("3. Compiling Smart Contract...")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"DeadDrop.sol": {"content": dead_drop_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

bytecode = compiled_sol["contracts"]["DeadDrop.sol"]["DeadDrop"]["evm"]["bytecode"]["object"]
abi = json.loads(compiled_sol["contracts"]["DeadDrop.sol"]["DeadDrop"]["metadata"])["output"]["abi"]

# Deploy Contract
print("4. Deploying Contract...")
DeadDrop = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.get_transaction_count(MY_ADDRESS)

transaction = DeadDrop.constructor().build_transaction({
    "chainId": chain_id,
    "from": MY_ADDRESS,
    "nonce": nonce,
    "gasPrice": w3.eth.gas_price
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
# Debug print
print(f"DEBUG DIR: {dir(signed_txn)}")

try:
    if hasattr(signed_txn, 'rawTransaction'):
        raw_tx = signed_txn.rawTransaction
    elif hasattr(signed_txn, 'rawTransaction'): # checking dict access handled below
         raw_tx = signed_txn['rawTransaction']
    else:
        # Try snake case
        raw_tx = getattr(signed_txn, 'raw_transaction', None)
        if not raw_tx:
             # Try dict
             raw_tx = signed_txn.get('rawTransaction') or signed_txn.get('raw_transaction')

    if not raw_tx:
        raise ValueError(f"Could not find rawTransaction in {signed_txn}")

except Exception as e:
    print(f"Error handling signed_txn: {e}")
    raw_tx = None # will fail below but printed logic above

print("   Sending transaction...")
try:
    tx_hash = w3.eth.send_raw_transaction(raw_tx)
    print(f"   Transaction Sent! Hash: {tx_hash.hex()}")
    
    print("   Waiting for confirmation...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    contract_address = tx_receipt.contractAddress
    print(f"✅ Contract Deployed Successfully!")
    print(f"📍 Contract Address: {contract_address}")
    
    # Update Config
    config['dead_drop_contract'] = contract_address
    with open('blockchain_config.json', 'w') as f:
        json.dump(config, f, indent=4)
    print("✅ Updated blockchain_config.json")
    
    # Save ABI
    with open('DeadDrop_ABI.json', 'w') as f:
        json.dump(abi, f, indent=4)
    print("✅ Saved DeadDrop_ABI.json")
    
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"❌ Deployment Failed: {e}")
