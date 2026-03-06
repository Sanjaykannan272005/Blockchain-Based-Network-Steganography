import json
import time
from web3 import Web3
from datetime import datetime, timedelta

def verify_timelock():
    print("=== Blockchain Time-Lock Verification ===")
    
    # Load config
    with open('blockchain_config.json', 'r') as f:
        config = json.load(f)
    
    w3 = Web3(Web3.HTTPProvider(config['rpc_url']))
    with open('DeadDrop_ABI.json', 'r') as f:
        abi = json.load(f)
    
    contract = w3.eth.contract(address=config['dead_drop_contract'], abi=abi)
    
    # 1. Schedule a message 2 minutes in the future
    release_time = int(time.time()) + 120 # 2 minutes
    print(f"1. Scheduling message for release at: {datetime.fromtimestamp(release_time)}")
    
    private_key = config['private_key']
    my_address = config['wallet_address']
    
    tx = contract.functions.sendMessage(
        my_address,
        "SECRET_TIME_LOCKED_DATA",
        release_time
    ).build_transaction({
        'from': my_address,
        'nonce': w3.eth.get_transaction_count(my_address),
        'gas': 300000,
        'gasPrice': w3.eth.gas_price
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    
    # Robust raw tx handling
    raw_tx = getattr(signed_tx, 'rawTransaction', None) or getattr(signed_tx, 'raw_transaction', None)
    if not raw_tx:
        raw_tx = signed_tx[0] if isinstance(signed_tx, tuple) else signed_tx.get('rawTransaction')
        
    tx_hash = w3.eth.send_raw_transaction(raw_tx)
    print(f"   Transaction sent: {tx_hash.hex()}")
    print("   Waiting for confirmation...")
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("✅ Message stored.")
    
    # 2. Check status immediately
    print("2. Checking status immediately (should be [LOCKED])...")
    data = contract.functions.getMyMessages().call({'from': my_address})
    latest_content = data[0][-1]
    print(f"   Content retrieved: {latest_content}")
    
    if latest_content == "[LOCKED]":
        print("✅ Correct: Message is locked.")
    else:
        print("❌ Error: Message is NOT locked!")

if __name__ == "__main__":
    verify_timelock()
