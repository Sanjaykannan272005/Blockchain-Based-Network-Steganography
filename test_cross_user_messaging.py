import requests
import json
import time

# Configuration
BASE_URL = "http://127.0.0.1:5000"

with open('test_users.json', 'r') as f:
    test_users = json.load(f)

user1 = test_users[0] # Sender
user2 = test_users[1] # Recipient

def test_cross_user():
    print(f"\n🚀 Testing Cross-User Messaging: {user1['name']} -> {user2['name']}")
    
    # 1. Send message from User 1 to User 2
    payload = {
        "recipient": user2['address'],
        "message": f"Hello {user2['name']}, this is a secure drop from {user1['name']}.",
        "release_time": "" # No time-lock for this test
    }
    
    print(f"📤 Sending drop to {user2['address']}...")
    try:
        # Note: In the real app, the server uses its own config wallet to send, 
        # but the dead-drop contract handles recipient indexing.
        response = requests.post(f"{BASE_URL}/dead_drop_send", data=payload)
        if response.status_code == 200:
            print("✅ Message recorded on blockchain!")
        else:
            print(f"❌ Failed to send: {response.text}")
            return
            
        print("⏳ Waiting for transaction to propagate...")
        time.sleep(15) 
        
        # 2. Check User 2's Inbox
        # Note: The current app checks the inbox for the configured 'wallet_address'.
        # For this test, we verify the message is indexable for User 2.
        print(f"📥 Checking inbox for {user2['address']}...")
        # We'll use the API but it might be checking the owner. 
        # Let's check how the inbox API works.
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_cross_user()
