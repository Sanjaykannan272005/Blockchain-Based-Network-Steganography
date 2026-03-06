import threading
import time
import json
import subprocess
import sys
from onion_utils import OnionUtils

def run_relay(node_id, secret, channel):
    print(f"Starting Relay {node_id}...")
    subprocess.run([sys.executable, "p2p_node.py", "--id", node_id, "--secret", secret, "--channel", channel])

def test_p2p_flow():
    # Setup Hops
    # Circuit: Sender -> Relay1 (Timing) -> Relay2 (Size) -> Recipient (Direct/TTL)
    hops = [
        {"ip": "127.0.0.1", "channel": "timing", "secret": "s1"},
        {"ip": "127.0.0.1", "channel": "size", "secret": "s2"}
    ]
    
    msg = "P2P Onion Route Verified"
    
    print("=" * 70)
    print("🕸️ P2P MULTI-HOP STEGANOGRAPHY SIMULATION")
    print("=" * 70)
    
    # Normally we'd start relay nodes as separate processes
    # For this simulation, we'll just demonstrate the onion creation and peeling 
    # to avoid complex multi-sniffing conflicts on one interface in one go.
    
    print("\n1. Building Onion...")
    key1 = OnionUtils.derive_key("s1")
    key2 = OnionUtils.derive_key("s2")
    
    # Wrappping
    inner_msg = f"{{'msg': '{msg}', 'final': 'target'}}"
    layer2_data = json.dumps({"next_hop": "127.0.0.1", "channel": "ttl", "payload": inner_msg})
    layer2_enc = OnionUtils.encrypt_layer(layer2_data, key2)
    
    layer1_data = json.dumps({"next_hop": "127.0.0.1", "channel": "size", "payload": layer2_enc})
    onion = OnionUtils.encrypt_layer(layer1_data, key1)
    
    print(f"✅ Created 2-layer onion: {len(onion)} chars")
    
    print("\n2. Simulating Hop 1 (Relay 1 peeling)...")
    peeled1 = OnionUtils.peel_layer(onion, key1)
    print(f"🔓 Relay 1 peeled layer! Next: {peeled1['next_hop']} via {peeled1['channel']}")
    
    print("\n3. Simulating Hop 2 (Relay 2 peeling)...")
    peeled2 = OnionUtils.peel_layer(peeled1['payload'], key2)
    print(f"🔓 Relay 2 peeled layer! Next: {peeled2['next_hop']} via {peeled2['channel']}")
    print(f"🏁 Final Destination Payload: {peeled2['payload']}")
    
    if "P2P Onion Route Verified" in peeled2['payload']:
        print("\n✅ SIMULATION SUCCESS: Multi-hop onion encoding/decoding verified!")

if __name__ == "__main__":
    test_p2p_flow()
