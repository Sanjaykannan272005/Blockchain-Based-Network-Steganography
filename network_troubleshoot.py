#!/usr/bin/env python3
import os
import sys
import time

try:
    from scapy.all import *
except ImportError:
    print("Error: Scapy not installed. Run: pip install scapy")
    sys.exit(1)

def list_interfaces():
    print("\n--- AVAILABLE NETWORK INTERFACES ---")
    if os.name == 'nt':
        # Windows
        from scapy.arch.windows import get_windows_if_list
        for i in get_windows_if_list():
            print(f"  - Name: {i['name']} (Friendly: {i['description']})")
    else:
        # Linux/macOS
        import socket
        try:
            from scapy.arch import get_if_list
            for iface in get_if_list():
                print(f"  - {iface}")
        except:
            print("  Could not list interfaces using Scapy. Try 'ip addr' or 'ifconfig'.")

def test_icmp_sniff(iface=None):
    print(f"\n--- TESTING ICMP SNIFFING (Interface: {iface if iface else 'Auto'}) ---")
    print("Please send a PING to this machine from the other laptop now...")
    print("Press Ctrl+C to stop.")
    
    def packet_callback(pkt):
        if IP in pkt and ICMP in pkt:
            src = pkt[IP].src
            print(f"  [SUCCESS] Received ICMP (Ping) from {src}")
            return True # Stop after first success

    try:
        if iface:
            sniff(filter="icmp", prn=packet_callback, iface=iface, timeout=30, count=1)
        else:
            sniff(filter="icmp", prn=packet_callback, timeout=30, count=1)
    except PermissionError:
        print("  [ERROR] Permission Denied. Run as sudo/Administrator.")
    except Exception as e:
        print(f"  [ERROR] {e}")

if __name__ == "__main__":
    print("Stealth Network Connectivity Troubleshooting")
    print("============================================")
    
    list_interfaces()
    
    target_iface = input("\nEnter an interface to test (or press Enter for auto): ").strip()
    if not target_iface: target_iface = None
    
    test_icmp_sniff(target_iface)
    
    print("\nTroubleshooting complete.")
    print("If you didn't see [SUCCESS], check your firewall (ufw on Ubuntu, Windows Firewall on Windows).")
