import json
from web3 import Web3
from datetime import datetime

def check_inbox():
    with open('blockchain_config.json', 'r') as f:
        config = json.load(f)
    w3 = Web3(Web3.HTTPProvider(config['rpc_url']))
    with open('DeadDrop_ABI.json', 'r') as f:
        abi = json.load(f)
    contract = w3.eth.contract(address=config['dead_drop_contract'], abi=abi)
    my_address = config['wallet_address']
    
    print(f"Checking Inbox for: {my_address}")
    data = contract.functions.getMyMessages().call({'from': my_address})
    
    contents, senders, timestamps, releaseTimes = data
    print(f"Total messages: {len(contents)}")
    
    for i in range(len(contents)):
        is_locked = contents[i] == "[LOCKED]"
        print(f"Message {i}:")
        print(f"  Sender: {senders[i]}")
        print(f"  Content: {contents[i]}")
        print(f"  Locked: {'YES' if is_locked else 'NO'}")
        print(f"  Release Time: {datetime.fromtimestamp(releaseTimes[i])}")

if __name__ == "__main__":
    check_inbox()
