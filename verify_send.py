import requests
import json

url = "http://localhost:5000/dead_drop_send_hybrid"
payload = {
    "target_ip": "127.0.0.1",
    "recipient_wallet": "0x7A2C2AF27b1E4afBBaBfcfc6e30Dd411D432AcA4",
    "message": "FINAL_CERTIFICATION_TEST_001",
    "channel": "timing",
    "block_key": True
}

try:
    response = requests.post(url, json=payload, timeout=60)
    print(f"Status: {response.status_code}")
    tx_hash = response.json().get('blockchain', {}).get('tx_hash')
    with open('tx_hash.txt', 'w') as f:
        f.write(str(tx_hash))
    print("Saved hash to tx_hash.txt")
except Exception as e:
    print(f"Error: {str(e)}")
