import json
import time
from blockchain_integration import BlockchainKeyExchange

def onboard():
    # Load config
    with open('blockchain_config.json', 'r') as f:
        config = json.load(f)
    
    # Load test users
    with open('test_users.json', 'r') as f:
        test_users = json.load(f)
        
    blockchain = BlockchainKeyExchange(rpc_url=config['rpc_url'])
    blockchain.load_user_registry(config['user_registry_contract'] if 'user_registry_contract' in config else config['registry_contract'])
    blockchain.load_access_control(config['access_control_contract'])
    
    admin_private_key = config['private_key']
    
    for user in test_users:
        print(f"\n--- Onboarding {user['name']} ({user['address']}) ---")
        
        # 1. User registers themselves
        print(f"1. Self-registering {user['name']}...")
        reg_res = blockchain.register_user(
            user['private_key'], 
            user['name'], 
            "Shadow-Unit", 
            "TOP_SECRET"
        )
        if reg_res.get('success'):
            print(f"   ✅ Registration TX: {reg_res['tx_hash']}")
        else:
            print(f"   ❌ Registration failed: {reg_res.get('error')}")
            continue # Skip if registration fails
            
        time.sleep(2) # Brief pause for chain processing
        
        # 2. Admin verifies user (Level: ENCRYPTED_SENDER = 3)
        print(f"2. Admin verifying {user['name']} (Level 3)...")
        verify_res = blockchain.verify_user(admin_private_key, user['address'], 3)
        if verify_res.get('success'):
            print(f"   ✅ Verification TX: {verify_res['tx_hash']}")
        else:
            print(f"   ❌ Verification failed: {verify_res.get('error')}")
            
        time.sleep(2)
        
        # 3. Admin grants Access Control whitelist
        print(f"3. Granting Whitelist access to {user['name']}...")
        grant_res = blockchain.grant_access(admin_private_key, user['address'], 0, f"Authorized for {user['name']}")
        if grant_res.get('success'):
            print(f"   ✅ Access Control TX: {grant_res['tx_hash']}")
        else:
            print(f"   ❌ Access Control failed: {grant_res.get('error')}")

    print("\n🚀 Onboarding complete for all test users!")

if __name__ == "__main__":
    onboard()
