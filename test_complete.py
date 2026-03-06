#!/usr/bin/env python3
"""
Complete Network Steganography Test
Runs both sender and receiver in one script
"""

import subprocess
import time
import sys
import threading

def run_receiver():
    """Run receiver in background"""
    print("🎧 Starting receiver...")
    result = subprocess.run(
        ["python", "network_receiver.py", "timing", "30"],
        capture_output=True,
        text=True
    )
    print("\n" + "="*70)
    print("📥 RECEIVER OUTPUT:")
    print("="*70)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)

def run_sender(message):
    """Run sender after delay"""
    print("⏳ Waiting 3 seconds for receiver to start...")
    time.sleep(3)
    
    print("\n📤 Starting sender...")
    result = subprocess.run(
        ["python", "network_sender.py", "127.0.0.1", message, "timing"],
        capture_output=True,
        text=True
    )
    print("\n" + "="*70)
    print("📤 SENDER OUTPUT:")
    print("="*70)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)

def main():
    print("="*70)
    print("🔐 BLOCKCHAIN NETWORK STEGANOGRAPHY - COMPLETE TEST")
    print("="*70)
    
    if len(sys.argv) < 2:
        message = "Hello World"
        print(f"\nUsing default message: '{message}'")
        print(f"Usage: python test_complete.py \"Your message here\"")
    else:
        message = sys.argv[1]
        print(f"\nMessage: '{message}'")
    
    print("\n🚀 Starting test...")
    print("   This will take about 35 seconds")
    
    # Start receiver in background thread
    receiver_thread = threading.Thread(target=run_receiver)
    receiver_thread.start()
    
    # Run sender
    run_sender(message)
    
    # Wait for receiver to finish
    print("\n⏳ Waiting for receiver to complete...")
    receiver_thread.join()
    
    print("\n" + "="*70)
    print("✅ TEST COMPLETE!")
    print("="*70)
    print("\nIf you see 'MESSAGE RECEIVED' above, it worked!")
    print("If not, make sure you're running as Administrator")

if __name__ == "__main__":
    main()
