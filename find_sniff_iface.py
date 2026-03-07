from scapy.all import sniff, get_working_ifaces
import threading
import time
import os
import subprocess

def p(pkt):
    print(f"Captured on {pkt.sniffed_on}")

def start_sniff():
    print("Sniffing on ALL interfaces for 10 seconds...")
    try:
        # Sniff on all interfaces by not specifying iface (Scapy default behavior)
        # or specifically try known loopback names
        sniff(filter="icmp", timeout=10, prn=p)
    except Exception as e:
        print(f"Sniff error: {e}")

t = threading.Thread(target=start_sniff)
t.start()

time.sleep(2)
print("Pinging 127.0.0.1 and physical IP...")
subprocess.run(["ping", "-n", "3", "127.0.0.1"])
subprocess.run(["ping", "-n", "3", "10.210.59.20"])

t.join()
print("Done.")
