import json
from web3 import Web3

with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

w3 = Web3(Web3.HTTPProvider(config['rpc_url']))
tx_hash = '0xa0d11f4629f341a09109b380eaaaf54463373d83922e38c8b213cacd3fe5c96f'

try:
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    if receipt is None:
        print("Transaction is still pending or was dropped.")
    else:
        status = "SUCCESS" if receipt['status'] == 1 else "REVERTED"
        print(f"Transaction mined in block: {receipt['blockNumber']}")
        print(f"Status: {status}")
        print(f"Gas Used: {receipt['gasUsed']}")
except Exception as e:
    print(f"Error fetching receipt: {e}")
