import threading
import time
import requests
import json
import subprocess
import sys

# Windows local physical IP and Interface (discovered)
LOCAL_IP = "10.210.59.20"
INTERFACE = "Wi-Fi"

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def run_test():
    # 1. Clear receiver logs
    try:
        requests.post('http://localhost:5001/api/receiver/clear_logs', timeout=5)
        log("Cleared receiver logs.")
    except Exception as e:
        log(f"Warning: Could not clear logs: {e}")

    # 2. Start receiver extraction (TIMING channel, 25s)
    def start_extract():
        log(f"Triggering receiver extraction (Timing, 25s) on {INTERFACE}...")
        try:
            r = requests.post('http://localhost:5001/api/receiver/extract', 
                             json={'channel':'timing','duration':25,'stealth':False, 'iface': INTERFACE},
                             timeout=5)
            log(f"Extract response: {r.text}")
        except Exception as e:
            log(f"Error starting extraction: {e}")

    t = threading.Thread(target=start_extract)
    t.start()
    
    log("Waiting for sniff to initialize...")
    time.sleep(5) 

    # 3. Send message via sender to PHYSICAL IP
    log(f"Sending message 'VERIFIED' via timing channel to {LOCAL_IP}...")
    send_cmd = [sys.executable, 'network_sender.py', LOCAL_IP, 'VERIFIED', 'timing']
    try:
        # We increase timeout because sending bits via timing takes time
        subprocess.run(send_cmd, check=True, timeout=120)
        log("Sender finished.")
    except Exception as e:
        log(f"Sender failed or timed out: {e}")

    # 4. Wait for extraction to complete + buffer
    log("Waiting for extraction results (35s)...")
    time.sleep(35)

    # 5. Fetch logs and verify
    try:
        logs_res = requests.get('http://localhost:5001/api/receiver/logs', timeout=5).json()
        log("Receiver Logs:")
        print(json.dumps(logs_res, indent=2))

        # Look for the specific success indicator in the logs
        found = any('[SUCCESS] Message extracted: VERIFIED' in entry for entry in logs_res.get('logs', []))
        if found:
            log("SUCCESS: Message 'VERIFIED' detected and decoded!")
            return True
        else:
            log("FAILURE: Message not found in logs.")
            return False
    except Exception as e:
        log(f"Error fetching logs: {e}")
        return False

if __name__ == "__main__":
    success = run_test()
    if not success:
        sys.exit(1)
