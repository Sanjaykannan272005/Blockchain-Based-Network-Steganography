#!/usr/bin/env python3
"""
Test network connectivity between sender and receiver
"""

import socket
import sys

def test_connection(target_ip, port=9999):
    """Test if we can connect to target IP and port"""
    print(f"\n{'='*60}")
    print(f"Testing connection to {target_ip}:{port}")
    print(f"{'='*60}\n")
    
    try:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        print(f"Attempting to connect...")
        sock.connect((target_ip, port))
        
        print(f"✅ SUCCESS! Connected to {target_ip}:{port}")
        print(f"\nThis means:")
        print(f"  • The receiver is running on {target_ip}")
        print(f"  • Port {port} is open")
        print(f"  • Network path is clear")
        print(f"\nYou can now send messages to this IP!")
        
        sock.close()
        return True
        
    except socket.timeout:
        print(f"❌ TIMEOUT - Cannot reach {target_ip}:{port}")
        print(f"\nPossible issues:")
        print(f"  • Receiver is not running on {target_ip}")
        print(f"  • Firewall is blocking port {port}")
        print(f"  • Wrong IP address")
        return False
        
    except ConnectionRefusedError:
        print(f"❌ CONNECTION REFUSED - {target_ip}:{port}")
        print(f"\nPossible issues:")
        print(f"  • Receiver is NOT running on {target_ip}")
        print(f"  • Port {port} is not listening")
        print(f"\nSolution:")
        print(f"  Run this on {target_ip}:")
        print(f"  python network_receiver_standalone.py")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        target_ip = sys.argv[1]
    else:
        target_ip = input("Enter receiver IP address: ").strip()
    
    test_connection(target_ip)
    
    print(f"\n{'='*60}")
    print(f"Next steps:")
    print(f"{'='*60}")
    print(f"\n1. On receiver computer ({target_ip}):")
    print(f"   python network_receiver_standalone.py")
    print(f"\n2. On sender computer (this computer):")
    print(f"   python blockchain_web_app.py")
    print(f"   Open: http://localhost:5000")
    print(f"   Select 'Network' and enter: {target_ip}")
    print(f"\n3. Send a message!")
    print()
