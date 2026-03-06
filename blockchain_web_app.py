#!/usr/bin/env python3
"""
🔗 Blockchain Steganography Web Interface
Complete web application with all 10 features
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import hashlib
import time
from datetime import datetime, timedelta
from functools import wraps
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from blockchain_integration import store_on_blockchain, retrieve_from_blockchain, verify_message_integrity

app = Flask(__name__)
app.secret_key = os.urandom(32)

# ============================================================================
# BLOCKCHAIN CONFIGURATION
# ============================================================================

class BlockchainConfig:
    """Manage blockchain configuration"""
    
    def __init__(self, config_file="blockchain_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Load blockchain configuration"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "networks": {},
                "contracts": {},
                "accounts": {},
                "steganography": {}
            }
    
    def save_config(self):
        """Save blockchain configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def update_network(self, name, url, chain_id, gas_limit, gas_price):
        """Add or update blockchain network"""
        self.config["networks"][name] = {
            "url": url,
            "chain_id": chain_id,
            "gas_limit": gas_limit,
            "gas_price": gas_price
        }
        self.save_config()
        return True
    
    def update_account(self, name, address, private_key):
        """Add or update account"""
        self.config["accounts"][name] = {
            "address": address,
            "private_key": private_key
        }
        self.save_config()
        return True

# Initialize config
blockchain_config = BlockchainConfig()

# ============================================================================
# SIMPLE BLOCKCHAIN SIMULATION
# ============================================================================

class SimpleBlockchain:
    """Simplified blockchain for demonstration"""
    
    def __init__(self):
        self.chain = []
        self.blocks = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create genesis block"""
        genesis = {
            'index': 0,
            'timestamp': time.time(),
            'data': 'Genesis Block',
            'previous_hash': '0',
            'hash': hashlib.sha256(b'Genesis Block').hexdigest()
        }
        self.chain.append(genesis)
        return genesis
    
    def add_block(self, data):
        """Add new block"""
        previous_block = self.chain[-1]
        new_block = {
            'index': len(self.chain),
            'timestamp': time.time(),
            'data': data,
            'previous_hash': previous_block['hash'],
            'hash': hashlib.sha256(
                f"{len(self.chain)}{time.time()}{data}{previous_block['hash']}".encode()
            ).hexdigest()
        }
        self.chain.append(new_block)
        return new_block
    
    def get_latest_block(self):
        """Get latest block"""
        return self.chain[-1]
    
    def verify_chain(self):
        """Verify blockchain integrity"""
        for i in range(1, len(self.chain)):
            if self.chain[i]['previous_hash'] != self.chain[i-1]['hash']:
                return False
        return True

# Global blockchain instance
blockchain = SimpleBlockchain()

# ============================================================================
# 10 BLOCKCHAIN STEGANOGRAPHY FEATURES
# ============================================================================

class BlockchainSteganographyEngine:
    """Core engine with all 10 features"""
    
    def __init__(self):
        self.password = "BlockchainStego2024"
        self.key = hashlib.sha256(self.password.encode()).digest()
        
        # Feature 1: Control Rules
        self.control_rules = {
            'start_time': int(time.time()),
            'end_time': int(time.time()) + 86400,  # 24 hours
            'packet_type': 'tcp',
            'encoding_method': 'ttl',
            'max_payload': 1000,
            'active': True
        }
        
        # Feature 2: Trigger Events
        self.trigger_events = []
        
        # Feature 3: Blockchain Keys (derived from blocks)
        self.blockchain_keys = {}
        
        # Feature 4: Authentication Records
        self.auth_records = {}
        
        # Feature 5: Reputation System
        self.reputation_scores = {}
        
        # Feature 6: Forensic Records
        self.forensic_records = []
        
        # Feature 7: Multi-Chain Distribution
        self.chain_records = []
        
        # Feature 8: Dead Drops
        self.dead_drops = []
        
        # Feature 9: Key Rotation Schedule
        self.key_rotations = []
        
        # Feature 10: Protocol Configuration
        self.protocol_configs = {
            'timing': {'stealth': 90, 'capacity': 20, 'robustness': 30},
            'size': {'stealth': 60, 'capacity': 60, 'robustness': 50},
            'ttl': {'stealth': 75, 'capacity': 50, 'robustness': 80},
            'ports': {'stealth': 40, 'capacity': 90, 'robustness': 40}
        }
    
    # FEATURE 1: Blockchain-Controlled Steganography
    def set_control_rules(self, start_time, end_time, packet_type, encoding_method, max_payload):
        """Set steganography control rules"""
        self.control_rules = {
            'start_time': start_time,
            'end_time': end_time,
            'packet_type': packet_type,
            'encoding_method': encoding_method,
            'max_payload': max_payload,
            'active': True
        }
        
        # Store in blockchain
        block = blockchain.add_block({
            'type': 'control_rules',
            'rules': self.control_rules
        })
        return block
    
    def check_access_allowed(self):
        """Check if steganography is allowed"""
        current_time = int(time.time())
        if self.control_rules['active']:
            if self.control_rules['start_time'] <= current_time <= self.control_rules['end_time']:
                return True, "✅ Access Allowed"
        return False, "❌ Access Denied - Outside allowed window"
    
    # FEATURE 2: Blockchain-Triggered Covert Channel
    def create_trigger_event(self, keyword):
        """Create trigger event on blockchain"""
        trigger = {
            'keyword': keyword,
            'timestamp': int(time.time()),
            'block_number': len(blockchain.chain),
            'activated': True
        }
        self.trigger_events.append(trigger)
        
        block = blockchain.add_block({
            'type': 'trigger_event',
            'trigger': trigger
        })
        return trigger, block
    
    def monitor_triggers(self):
        """Monitor for trigger events"""
        return self.trigger_events
    
    # FEATURE 3: Blockchain Key Generation
    def derive_key_from_blockchain(self, block_index=None):
        """Derive encryption key from blockchain"""
        if block_index is None:
            block_index = len(blockchain.chain) - 1
        
        if block_index >= len(blockchain.chain):
            return None
        
        block = blockchain.chain[block_index]
        key_material = f"{block['hash']}{block['index']}{int(block['timestamp'])}"
        derived_key = hashlib.sha256(key_material.encode()).digest()
        
        return {
            'key': derived_key.hex()[:32],
            'block_hash': block['hash'],
            'block_height': block['index'],
            'timestamp': block['timestamp'],
            'valid_until': int(block['timestamp']) + 900  # 15 min
        }
    
    # FEATURE 4: Decentralized Authentication
    def authenticate_user(self, user_address):
        """Authenticate user on blockchain"""
        signature = hashlib.sha256(
            f"{user_address}{time.time()}".encode()
        ).hexdigest()
        
        auth_record = {
            'user': user_address,
            'signature': signature,
            'timestamp': int(time.time()),
            'expires': int(time.time()) + 1800,  # 30 min
            'verified': True
        }
        self.auth_records[user_address] = auth_record
        
        block = blockchain.add_block({
            'type': 'authentication',
            'record': auth_record
        })
        return auth_record
    
    # FEATURE 5: Reputation System
    def update_reputation(self, user_address, action):
        """Update user reputation score"""
        if user_address not in self.reputation_scores:
            self.reputation_scores[user_address] = {
                'score': 100,
                'clean_communications': 0,
                'detection_attempts': 0,
                'last_updated': int(time.time())
            }
        
        rep = self.reputation_scores[user_address]
        
        if action == 'clean_communication':
            rep['score'] += 5
            rep['clean_communications'] += 1
        elif action == 'detection_attempt':
            rep['score'] -= 20
            rep['detection_attempts'] += 1
        
        rep['score'] = max(0, min(100, rep['score']))
        rep['last_updated'] = int(time.time())
        
        block = blockchain.add_block({
            'type': 'reputation',
            'user': user_address,
            'reputation': rep
        })
        return rep
    
    # FEATURE 6: Forensic Verification
    def create_forensic_record(self, message, sender_address):
        """Create forensic verification record"""
        message_hash = hashlib.sha256(message.encode()).hexdigest()
        
        forensic = {
            'commitment_hash': message_hash,
            'timestamp': int(time.time()),
            'block_number': len(blockchain.chain),
            'creator': sender_address,
            'verified': True
        }
        self.forensic_records.append(forensic)
        
        block = blockchain.add_block({
            'type': 'forensic_record',
            'record': forensic
        })
        return forensic, message_hash
    
    # FEATURE 7: Multi-Chain Distribution
    def distribute_across_chains(self, message, chains=['ethereum', 'polygon', 'arbitrum']):
        """Distribute message across multiple blockchains"""
        # Split message into parts
        part_size = len(message) // len(chains)
        parts = [
            message[i*part_size:(i+1)*part_size]
            for i in range(len(chains))
        ]
        
        chain_records = []
        for i, (chain_name, part) in enumerate(zip(chains, parts)):
            part_hash = hashlib.sha256(part.encode()).hexdigest()
            record = {
                'chain_name': chain_name,
                'part_hash': part_hash,
                'block_number': len(blockchain.chain),
                'transaction_hash': f"0x{hashlib.sha256(f'{chain_name}{part}'.encode()).hexdigest()}"
            }
            chain_records.append(record)
        
        block = blockchain.add_block({
            'type': 'multi_chain_distribution',
            'records': chain_records
        })
        return chain_records
    
    # FEATURE 8: Dead Drop Coordinates
    def create_dead_drop(self, start_time, end_time, protocol, location_hint):
        """Create dead drop for message coordination"""
        dead_drop = {
            'start_time': start_time,
            'end_time': end_time,
            'protocol': protocol,
            'pattern_hash': hashlib.sha256(
                f"{start_time}{end_time}{protocol}".encode()
            ).hexdigest(),
            'location_hint': location_hint,
            'active': True
        }
        self.dead_drops.append(dead_drop)
        
        block = blockchain.add_block({
            'type': 'dead_drop',
            'drop': dead_drop
        })
        return dead_drop
    
    # FEATURE 9: Key Rotation Schedule
    def schedule_key_rotation(self, rotation_time, new_key_hash, valid_duration):
        """Schedule automatic key rotation"""
        rotation = {
            'rotation_time': rotation_time,
            'key_hash': new_key_hash,
            'valid_duration': valid_duration,
            'active': True
        }
        self.key_rotations.append(rotation)
        
        block = blockchain.add_block({
            'type': 'key_rotation',
            'rotation': rotation
        })
        return rotation
    
    # FEATURE 10: Protocol Configuration
    def get_optimal_protocol(self, network_conditions, threat_level, message_size):
        """Dynamically select optimal steganography protocol"""
        # Simple heuristic for protocol selection
        if threat_level == 'high':
            return 'ttl'
        elif message_size > 500:
            return 'size'
        elif network_conditions == 'quiet':
            return 'timing'
        else:
            return 'ttl'
    
    def encrypt_message(self, message):
        """Encrypt message with AES-256"""
        cipher = AES.new(self.key, AES.MODE_CBC)
        iv = cipher.iv
        pad_length = 16 - (len(message) % 16)
        padded = message + (chr(pad_length) * pad_length)
        encrypted = cipher.encrypt(padded.encode())
        return base64.b64encode(iv + encrypted).decode()
    
    def decrypt_message(self, encrypted_message):
        """Decrypt message with AES-256"""
        try:
            encrypted_data = base64.b64decode(encrypted_message)
            iv = encrypted_data[:16]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(encrypted_data[16:])
            pad_length = ord(decrypted[-1:])
            return decrypted[:-pad_length].decode()
        except:
            return None

# Global engine instance
stego_engine = BlockchainSteganographyEngine()

# ============================================================================
# ROUTES - SETUP & CONFIGURATION
# ============================================================================

@app.route('/')
def index():
    """Main page - new frontend"""
    return render_template('new_frontend.html')

@app.route('/dashboard')
def dashboard():
    """Old dashboard"""
    latest_block = blockchain.get_latest_block()
    is_configured = len(blockchain_config.config.get('networks', {})) > 0
    
    return render_template('dashboard.html',
                          total_blocks=len(blockchain.chain),
                          latest_block=latest_block,
                          is_configured=is_configured)

@app.route('/setup')
def setup():
    """Blockchain setup wizard"""
    current_config = blockchain_config.config
    return render_template('setup.html', config=current_config)

@app.route('/api/setup/network', methods=['POST'])
def api_setup_network():
    """Configure blockchain network"""
    data = request.json
    try:
        blockchain_config.update_network(
            data['name'],
            data['url'],
            int(data['chain_id']),
            int(data['gas_limit']),
            int(data['gas_price'])
        )
        return jsonify({'status': 'success', 'message': 'Network configured'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/setup/account', methods=['POST'])
def api_setup_account():
    """Configure blockchain account"""
    data = request.json
    try:
        blockchain_config.update_account(
            data['name'],
            data['address'],
            data['private_key']
        )
        return jsonify({'status': 'success', 'message': 'Account configured'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/blockchain/status')
def api_blockchain_status():
    """Get blockchain status"""
    latest_block = blockchain.get_latest_block()
    return jsonify({
        'total_blocks': len(blockchain.chain),
        'chain_valid': blockchain.verify_chain(),
        'latest_block': {
            'index': latest_block['index'],
            'hash': latest_block['hash'],
            'timestamp': latest_block['timestamp']
        },
        'networks': list(blockchain_config.config.get('networks', {}).keys()),
        'accounts': list(blockchain_config.config.get('accounts', {}).keys())
    })

# ============================================================================
# ROUTES - 10 FEATURES
# ============================================================================

# FEATURE 1: Control Rules
@app.route('/feature/1-control')
def feature_control():
    """Feature 1: Blockchain-Controlled Steganography"""
    allowed, message = stego_engine.check_access_allowed()
    return render_template('features/feature_1_control.html',
                          rules=stego_engine.control_rules,
                          allowed=allowed,
                          message=message)

@app.route('/api/feature/1/update', methods=['POST'])
def api_feature_1_update():
    """Update control rules"""
    data = request.json
    try:
        block = stego_engine.set_control_rules(
            int(data['start_time']),
            int(data['end_time']),
            data['packet_type'],
            data['encoding_method'],
            int(data['max_payload'])
        )
        return jsonify({'status': 'success', 'block': block})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# FEATURE 2: Trigger Events
@app.route('/feature/2-triggers')
def feature_triggers():
    """Feature 2: Blockchain-Triggered Covert Channel"""
    triggers = stego_engine.monitor_triggers()
    return render_template('features/feature_2_triggers.html', triggers=triggers)

@app.route('/api/feature/2/create', methods=['POST'])
def api_feature_2_create():
    """Create trigger event"""
    data = request.json
    try:
        trigger, block = stego_engine.create_trigger_event(data['keyword'])
        return jsonify({'status': 'success', 'trigger': trigger, 'block': block})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# FEATURE 3: Key Generation
@app.route('/feature/3-keys')
def feature_keys():
    """Feature 3: Blockchain-Derived Keys"""
    key_data = stego_engine.derive_key_from_blockchain()
    return render_template('features/feature_3_keys.html', key_data=key_data)

@app.route('/api/feature/3/derive', methods=['POST'])
def api_feature_3_derive():
    """Derive key from blockchain"""
    data = request.json
    try:
        block_index = int(data.get('block_index', len(blockchain.chain) - 1))
        key_data = stego_engine.derive_key_from_blockchain(block_index)
        return jsonify({'status': 'success', 'key_data': key_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# FEATURE 4: Authentication
@app.route('/feature/4-auth')
def feature_auth():
    """Feature 4: Decentralized Authentication"""
    return render_template('features/feature_4_auth.html')

@app.route('/api/feature/4/authenticate', methods=['POST'])
def api_feature_4_auth():
    """Authenticate user"""
    data = request.json
    try:
        auth_record = stego_engine.authenticate_user(data['user_address'])
        return jsonify({'status': 'success', 'auth_record': auth_record})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# FEATURE 5: Reputation
@app.route('/feature/5-reputation')
def feature_reputation():
    """Feature 5: Reputation System"""
    reps = stego_engine.reputation_scores
    return render_template('features/feature_5_reputation.html', reputations=reps)

@app.route('/api/feature/5/update', methods=['POST'])
def api_feature_5_update():
    """Update reputation"""
    data = request.json
    try:
        rep = stego_engine.update_reputation(data['user_address'], data['action'])
        return jsonify({'status': 'success', 'reputation': rep})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# FEATURE 6: Forensic Records
@app.route('/feature/6-forensics')
def feature_forensics():
    """Feature 6: Forensic Verification"""
    records = stego_engine.forensic_records
    return render_template('features/feature_6_forensics.html', records=records)

@app.route('/api/feature/6/create', methods=['POST'])
def api_feature_6_create():
    """Create forensic record"""
    data = request.json
    try:
        forensic, msg_hash = stego_engine.create_forensic_record(
            data['message'],
            data['sender_address']
        )
        return jsonify({'status': 'success', 'forensic': forensic, 'hash': msg_hash})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# FEATURE 7: Multi-Chain Distribution
@app.route('/feature/7-multichain')
def feature_multichain():
    """Feature 7: Multi-Chain Distribution"""
    records = stego_engine.chain_records
    return render_template('features/feature_7_multichain.html', records=records)

@app.route('/api/feature/7/distribute', methods=['POST'])
def api_feature_7_distribute():
    """Distribute across chains"""
    data = request.json
    try:
        chains = data.get('chains', ['ethereum', 'polygon', 'arbitrum'])
        records = stego_engine.distribute_across_chains(data['message'], chains)
        return jsonify({'status': 'success', 'records': records})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# FEATURE 8: Dead Drops
@app.route('/feature/8-deaddrops')
def feature_deaddrops():
    """Feature 8: Dead Drop Coordinates"""
    drops = stego_engine.dead_drops
    return render_template('features/feature_8_deaddrops.html', drops=drops)

@app.route('/api/feature/8/create', methods=['POST'])
def api_feature_8_create():
    """Create dead drop"""
    data = request.json
    try:
        drop = stego_engine.create_dead_drop(
            int(data['start_time']),
            int(data['end_time']),
            data['protocol'],
            data['location_hint']
        )
        return jsonify({'status': 'success', 'drop': drop})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# FEATURE 9: Key Rotation
@app.route('/feature/9-rotation')
def feature_rotation():
    """Feature 9: Key Rotation Schedule"""
    rotations = stego_engine.key_rotations
    return render_template('features/feature_9_rotation.html', rotations=rotations)

@app.route('/api/feature/9/schedule', methods=['POST'])
def api_feature_9_schedule():
    """Schedule key rotation"""
    data = request.json
    try:
        rotation = stego_engine.schedule_key_rotation(
            int(data['rotation_time']),
            data['key_hash'],
            int(data['valid_duration'])
        )
        return jsonify({'status': 'success', 'rotation': rotation})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# FEATURE 10: Protocol Selection
@app.route('/feature/10-protocols')
def feature_protocols():
    """Feature 10: Protocol Configuration"""
    configs = stego_engine.protocol_configs
    return render_template('features/feature_10_protocols.html', configs=configs)

@app.route('/api/feature/10/select', methods=['POST'])
def api_feature_10_select():
    """Select optimal protocol"""
    data = request.json
    try:
        protocol = stego_engine.get_optimal_protocol(
            data['network_conditions'],
            data['threat_level'],
            int(data['message_size'])
        )
        return jsonify({'status': 'success', 'protocol': protocol})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# ============================================================================
# ROUTES - MESSAGING
# ============================================================================

@app.route('/messaging')
def messaging():
    """Send and receive messages"""
    return render_template('messaging.html')

@app.route('/network-messaging')
def network_messaging():
    """Network messaging with real packet transmission"""
    return render_template('network_messaging.html')

@app.route('/complete-system')
def complete_system():
    """Complete unified system with all features"""
    return render_template('complete_system.html')

@app.route('/simple-wizard')
def simple_wizard():
    """Simple step-by-step wizard for sending messages"""
    return render_template('simple_wizard.html')

@app.route('/modern')
def modern_ui():
    """Modern clean user interface"""
    return render_template('modern_ui.html')

@app.route('/receiver')
def web_receiver():
    """Web-based network receiver"""
    return render_template('web_receiver.html')

# Global message queue for receiver
received_messages = []

# Network receiver thread
import threading
import socket

def start_network_listener():
    """Start network listener in background thread"""
    def listen():
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('0.0.0.0', 9999))
            server_socket.listen(5)
            print("\n" + "="*60)
            print("📡 NETWORK RECEIVER ACTIVE")
            print("Port: 9999")
            print("Status: Listening for incoming messages")
            print("="*60 + "\n")
            
            while True:
                try:
                    client_socket, address = server_socket.accept()
                    print(f"\n📨 Incoming connection from {address[0]}:{address[1]}")
                    
                    data = b''
                    while True:
                        chunk = client_socket.recv(4096)
                        if not chunk:
                            break
                        data += chunk
                    client_socket.close()
                    
                    if data:
                        message_data = json.loads(data.decode())
                        received_messages.append(message_data)
                        print(f"✅ Message received and stored!")
                        print(f"   From: {message_data.get('sender', 'Unknown')[:30]}...")
                        print(f"   Message: {message_data.get('message', '')[:50]}...")
                        print(f"   Total messages: {len(received_messages)}\n")
                except Exception as e:
                    print(f"❌ Receiver error: {e}")
        except Exception as e:
            print(f"❌ Network listener failed to start: {e}")
            print("   Port 9999 may already be in use")
            print("   Close any other receiver and restart Flask app\n")
    
    thread = threading.Thread(target=listen, daemon=True)
    thread.start()

@app.route('/api/receiver/check')
def api_receiver_check():
    """Check for received messages"""
    global received_messages
    print(f"API check: {len(received_messages)} messages in queue")
    return jsonify({'messages': received_messages, 'count': len(received_messages)})


@app.route('/all-features')
def all_features():
    """Single-page UI that combines all features for sending messages"""
    return render_template('all_features.html')

@app.route('/api/message/send', methods=['POST'])
def api_message_send():
    """Send encrypted message with blockchain key storage"""
    global received_messages
    data = request.json
    try:
        features = data.get('features', [])
        message = data['message']
        sender = data['sender_address']
        target_ip = data.get('target_ip')
        password = data.get('password', 'BlockchainStego2024')
        receiver = data.get('receiver_address', '0xReceiver')
        
        # Create custom encryption key from password
        custom_key = hashlib.sha256(password.encode()).digest()
        encryption_key_hex = custom_key.hex()
        
        # Store key on blockchain
        blockchain_result = store_on_blockchain(
            sender=sender,
            message=message,
            encryption_key=encryption_key_hex,
            receiver=receiver
        )
        
        # Encrypt with custom password
        cipher = AES.new(custom_key, AES.MODE_CBC)
        iv = cipher.iv
        pad_length = 16 - (len(message) % 16)
        padded = message + (chr(pad_length) * pad_length)
        encrypted = cipher.encrypt(padded.encode())
        encrypted_message = base64.b64encode(iv + encrypted).decode()
        
        # Apply features (shortened)
        feature_results = {}
        if 3 in features:
            key_data = stego_engine.derive_key_from_blockchain()
            feature_results['blockchain_key'] = key_data
        
        # Send over network
        network_status = 'local'
        if target_ip and target_ip != '127.0.0.1':
            try:
                import socket
                import threading
                def send_network():
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(5)
                        sock.connect((target_ip, 9999))
                        message_data = {
                            'sender': sender,
                            'encrypted_message': encrypted_message,
                            'blockchain_tx': blockchain_result['tx_hash'],
                            'timestamp': int(time.time()),
                            'features': features
                        }
                        sock.send(json.dumps(message_data).encode())
                        sock.close()
                    except Exception as e:
                        print(f"Network send error: {e}")
                thread = threading.Thread(target=send_network)
                thread.start()
                network_status = 'sent_to_network'
            except Exception as e:
                network_status = f'failed: {str(e)}'
        
        # Store in local queue
        received_messages.append({
            'sender': sender,
            'encrypted_message': encrypted_message,
            'blockchain_tx': blockchain_result['tx_hash'],
            'timestamp': int(time.time()),
            'features': features
        })
        
        return jsonify({
            'status': 'success',
            'encrypted_message': encrypted_message,
            'blockchain_tx': blockchain_result['tx_hash'],
            'block_number': blockchain_result.get('block_number'),
            'block_explorer': blockchain_result.get('block_explorer'),
            'features_applied': len(features),
            'network_status': network_status
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/message/decrypt', methods=['POST'])
def api_message_decrypt():
    """Decrypt message using key from blockchain"""
    data = request.json
    try:
        encrypted_message = data['encrypted_message']
        blockchain_tx = data.get('blockchain_tx')
        password = data.get('password')
        
        # Get key from blockchain if tx provided
        if blockchain_tx:
            blockchain_data = retrieve_from_blockchain(blockchain_tx)
            if 'error' not in blockchain_data:
                encryption_key_hex = blockchain_data['encryption_key']
                custom_key = bytes.fromhex(encryption_key_hex)
            else:
                return jsonify({'status': 'error', 'message': 'Blockchain transaction not found'}), 400
        elif password:
            custom_key = hashlib.sha256(password.encode()).digest()
        else:
            return jsonify({'status': 'error', 'message': 'Need blockchain_tx or password'}), 400
        
        # Decrypt
        encrypted_data = base64.b64decode(encrypted_message)
        iv = encrypted_data[:16]
        cipher = AES.new(custom_key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_data[16:])
        pad_length = ord(decrypted[-1:])
        message = decrypted[:-pad_length].decode()
        
        return jsonify({
            'status': 'success',
            'message': message,
            'key_source': 'blockchain' if blockchain_tx else 'password'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Decryption failed'}), 400

@app.route('/api/message/receive', methods=['POST'])
def api_message_receive():
    """Receive and decrypt message"""
    data = request.json
    try:
        # Decrypt message
        decrypted = stego_engine.decrypt_message(data['encrypted_message'])
        
        if decrypted:
            return jsonify({
                'status': 'success',
                'message': decrypted
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Decryption failed'
            }), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("Blockchain Steganography Web Interface")
    print("=" * 60)
    print("Starting Flask application...")
    print("Visit: http://localhost:5000")
    print("Setup: http://localhost:5000/setup")
    print("=" * 60)
    
    # Start network listener
    start_network_listener()
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
