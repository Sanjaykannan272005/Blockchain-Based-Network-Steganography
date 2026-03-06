import sys
import time
import argparse
from scapy.all import sniff, IP, ICMP, Raw, send
from onion_utils import OnionUtils
import threading
from blockchain_integration import BlockchainKeyExchange
import json
import os

class P2PRelayNode:
    def __init__(self, node_id, key_secret, listen_channel="timing"):
        self.node_id = node_id
        self.key = OnionUtils.derive_key(key_secret)
        self.listen_channel = listen_channel
        self.binary_buffer = ""
        self.last_packet_time = None
        self.is_running = True
        
        # Blockchain connection
        self.blockchain = None
        self.load_blockchain_config()

    def load_blockchain_config(self):
        try:
            config = {}
            if os.path.exists('blockchain_config.json'):
                with open('blockchain_config.json', 'r') as f:
                    config = json.load(f)
            
            # Blockchain Connection (Prioritizes .env via internal logic)
            self.blockchain = BlockchainKeyExchange()
            
            # Auto-load contracts if addresses are in environment or fallback to config
            self.blockchain.load_registry_contract(config.get('registry_contract'))
            self.blockchain.load_access_control(config.get('access_control_contract'))
            self.blockchain.load_controller_contract(config.get('controller_contract'))
            self.config = config
        except Exception as e:
            print(f"Warning: Could not load blockchain config for node: {e}")

    def register_on_blockchain(self, ip, private_key):
        if self.blockchain and hasattr(self.blockchain, 'registry_contract'):
            print(f"🌐 Registering node {self.node_id} on blockchain...")
            channels = [self.listen_channel] # Current channel
            # For public key, we'll use a mock for now or derive from secret
            public_key = f"PK_{self.node_id}"
            
            result = self.blockchain.register_p2p_node(private_key, ip, channels, public_key)
            if result.get('success'):
                print(f"✅ Node registered! TX: {result['tx_hash']}")
                # Start global monitors
                self.start_panic_monitor()
                self.start_protocol_monitor()
                self.start_reputation_monitor() # NEW: Resilience Monitor
            else:
                print(f"❌ Registration failed: {result.get('error')}")

    def start_reputation_monitor(self):
        """Resilience: Self-monitor reputation and trigger Auto-Kill Switch if compromised"""
        def monitor():
            print(f"🛡️ [RESILIENCE MONITOR] Active for node {self.node_id}")
            while self.is_running:
                try:
                    res = self.blockchain.get_blockchain_nodes()
                    if res.get('success'):
                        # Find myself in the node list
                        me = next((n for n in res['nodes'] if n['wallet'].lower() == self.config.get('wallet', '').lower()), None)
                        if me:
                            reputation = me.get('reputation', 100)
                            is_active = me.get('is_active', True)
                            
                            # CRITICAL: Threshold check (below 30 reputation or flagged inactive)
                            if reputation < 30 or not is_active:
                                print(f"🚨 [SELF-DESTRUCT] CRITICAL BREACH. Reputation: {reputation}, Active: {is_active}")
                                self.trigger_self_destruct("Reputation dropped below safety threshold or node deactivated.")
                                break
                except Exception as e:
                    print(f"Reputation monitor error: {e}")
                time.sleep(20)
        
        threading.Thread(target=monitor, daemon=True).start()

    def trigger_self_destruct(self, reason):
        """Auto-Kill Switch: Wipe local cache and stop processing"""
        print(f"💥 [SELF-DESTRUCT] Triggered! Reason: {reason}")
        print("🧹 Wiping local message buffer...")
        self.binary_buffer = "" # Wipe cache
        self.is_running = False
        print("🛑 Node operation suspended.")


    def start_panic_monitor(self):
        """Monitor global network status (Panic Button)"""
        self.network_status = "NORMAL"
        
        def monitor():
            print(f"🛡️ [PANIC MONITOR] Active for node {self.node_id}")
            while self.is_running:
                try:
                    res = self.blockchain.get_global_status()
                    if res.get('success'):
                        new_status = res['status']
                        if new_status == "SILENCED" and self.network_status == "NORMAL":
                            print("⚠️  [PANIC] Network SILENCED by Blockchain. Suppressing traffic...")
                        elif new_status == "NORMAL" and self.network_status == "SILENCED":
                            print("✅ [PANIC] Network NORMALIZED. Resuming traffic...")
                        self.network_status = new_status
                except Exception as e:
                    print(f"Panic monitor error: {e}")
                time.sleep(15)
        
        threading.Thread(target=monitor, daemon=True).start()

    def start_protocol_monitor(self):
        """Monitor global stealth protocol switching"""
        def monitor():
            print(f"📡 [PROTOCOL MONITOR] Active for node {self.node_id}")
            while self.is_running:
                try:
                    res = self.blockchain.get_current_protocol()
                    if res.get('success'):
                        active_proto = res['protocol']
                        if active_proto != self.listen_channel:
                            print(f"🔄 [PROTOCOL] System switch detected: {self.listen_channel} -> {active_proto}")
                            self.listen_channel = active_proto
                            # In a real system, we might restart the sniffer here with new filters
                except Exception as e:
                    print(f"Protocol monitor error: {e}")
                time.sleep(30)
        threading.Thread(target=monitor, daemon=True).start()

    def listen(self, duration=None):
        print(f"🕸️ P2P Node '{self.node_id}' active.")
        print(f"👂 Listening on {self.listen_channel.upper()} channel...")
        
        def packet_callback(pkt):
            if not pkt.haslayer(ICMP): return
            if hasattr(self, 'network_status') and self.network_status == "SILENCED":
                # In silenced mode, we skip processing or only handle secure channels
                return 
            
            # Extract bit based on channel
            bit = None
            if self.listen_channel == "timing":
                current_time = time.time()
                if self.last_packet_time:
                    delay = current_time - self.last_packet_time
                    if 0.08 < delay < 0.15: bit = '0'
                    elif 0.18 < delay < 0.25: bit = '1'
                self.last_packet_time = current_time
                
            elif self.listen_channel == "size":
                if pkt.haslayer(Raw):
                    size = len(pkt[Raw].load)
                    if 90 < size < 110: bit = '0'
                    elif 190 < size < 210: bit = '1'
            
            elif self.listen_channel == "ttl":
                ttl = pkt[IP].ttl
                if ttl == 64: bit = '0'
                elif ttl == 65: bit = '1'
                
            if bit:
                self.binary_buffer += bit
                # Check for full layer (JSON strings usually end with some padding or delimiter)
                # For simplicity in this demo, we'll try to decode every 8 bits
                if len(self.binary_buffer) % 8 == 0:
                    self.process_buffer()

        sniff(filter="icmp", prn=packet_callback, timeout=duration, store=0)

    def process_buffer(self):
        # Convert binary to text
        bits = self.binary_buffer
        chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
        try:
            text = "".join([chr(int(c, 2)) for c in chars if len(c) == 8])
            # Attempt to peel layer
            peeled = OnionUtils.peel_layer(text, self.key)
            if peeled:
                print(f"🔓 Layer peeled! Next hop: {peeled['next_hop']} via {peeled['channel']}")
                self.forward(peeled['next_hop'], peeled['channel'], peeled['payload'])
                self.binary_buffer = "" # Clear buffer after success
        except:
            pass

    def forward(self, next_host, channel, payload):
        print(f"🚀 Forwarding to {next_host} using {channel}...")
        binary = ''.join(format(ord(c), '08b') for c in payload)
        
        for i, bit in enumerate(binary):
            if channel == "timing":
                packet = IP(dst=next_host)/ICMP(seq=i)
                send(packet, verbose=0)
                time.sleep(0.1 if bit == '0' else 0.2)
            elif channel == "size":
                size = 100 if bit == '0' else 200
                packet = IP(dst=next_host)/ICMP(seq=i)/("X" * (size - 28))
                send(packet, verbose=0)
            elif channel == "ttl":
                ttl = 64 if bit == '0' else 65
                packet = IP(dst=next_host, ttl=ttl)/ICMP(seq=i)
                send(packet, verbose=0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P2P Stealth Relay Node")
    parser.add_argument("--id", required=True, help="Node identifier")
    parser.add_argument("--secret", required=True, help="Shared secret for encryption")
    parser.add_argument("--channel", default="timing", help="Listening channel")
    parser.add_argument("--ip", help="Public IP of this node (for blockchain registration)")
    parser.add_argument("--privkey", help="Private key for blockchain registration gas")
    
    args = parser.parse_args()
    
    node = P2PRelayNode(args.id, args.secret, args.channel)
    
    if args.ip and args.privkey:
        node.register_on_blockchain(args.ip, args.privkey)
    
    try:
        node.listen()
    except KeyboardInterrupt:
        print("\nNode shutting down.")
