import json
import time
from web3 import Web3
from blockchain_integration import BlockchainKeyExchange

def test_timelock_enforcement():
    print("[TEST] Verifying Time-Lock Enforcement...")
    
    # Load config
    try:
        with open('blockchain_config.json', 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"ERROR: Could not load config: {e}")
        return False

    try:
        blockchain = BlockchainKeyExchange(rpc_url=config['rpc_url'])
        blockchain.load_dead_drop_contract(config['dead_drop_contract'])
        
        my_address = config['wallet_address']
        private_key = config['private_key']
        
        # 1. Send a message with a 5-minute time-lock
        release_time = int(time.time()) + 300 # 5 minutes from now
        print(f"STATUS: Sending message with release time: {release_time}")
        
        result = blockchain.send_to_deaddrop(private_key, my_address, "SECRET_DATA_LOCKED", release_time=release_time)
        
        if not result['success']:
            print(f"FAILURE: Failed to send message to blockchain. Error details: {result.get('error')}")
            # If the error is 'gas' related, it might be due to low balance
            return False
            
        print(f"SUCCESS: Message sent! TX Hash: {result['tx_hash']}")
        
        # 2. Immediately try to retrieve and verify it is [LOCKED]
        print("STATUS: Attempting immediate retrieval (should be [LOCKED])...")
        messages = blockchain.get_from_deaddrop(my_address)
        
        if messages['success']:
            found = False
            for msg in messages['messages']:
                # Find the message we just sent (approximate check by release_time)
                if abs(msg['release_time'] - release_time) < 10:
                    found = True
                    print(f"STATUS: Found message in inbox. Content: '{msg['content']}'")
                    if msg['content'] == "[LOCKED]":
                        print("SUCCESS: [VERIFIED] Smart contract correctly masked the content!")
                        return True
                    else:
                        print("FAILURE: [BUG] Content was retrieved before release time!")
                        return False
            if not found:
                print("FAILURE: Could not find the test message in the inbox. Blockchain sync delay?")
                return False
        else:
            print(f"FAILURE: Error retrieving messages: {messages.get('error')}")
            return False
    except Exception as e:
        print(f"FAILURE: Unexpected error during test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    # Force UTF-8 for Windows output if possible, but emojis are already removed
    success = test_timelock_enforcement()
    if success:
        print("\nTIME-LOCK VERIFICATION COMPLETE: ALL TESTS PASSED")
    else:
        print("\nTIME-LOCK VERIFICATION FAILED: TEST ERRORS DETECTED")
        sys.exit(1)
