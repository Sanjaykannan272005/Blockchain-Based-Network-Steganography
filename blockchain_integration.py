#!/usr/bin/env python3
"""
Blockchain Integration for Steganography
- Store message hash on Ethereum
- Store encryption key on blockchain
- Retrieve key from blockchain for decryption
- Network Registry and Access Control
"""

from web3 import Web3
import hashlib
import json
import os
import sys
import time
import subprocess
from datetime import datetime

class BlockchainKeyExchange:
    """Handle encryption key exchange and network management via blockchain"""
    
    def __init__(self, rpc_url=None):
        """Initialize Web3 connection with environment variable support"""
        # Load from .env or fallback to provided rpc_url or default
        env_rpc = os.getenv('RPC_URL')
        self.rpc_url = env_rpc if env_rpc else (rpc_url if rpc_url else "https://sepolia.infura.io/v3/b9fc4ab7927e41fdb20bf3f50dd6afad")
        
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.contract_address = os.getenv('REGISTRY_CONTRACT')
        
    # ==========================
    # ABI Definitions
    # ==========================

    def get_contract_abi(self):
        """Standard DeadDrop contract ABI (Minimal)"""
        return [
            {"inputs":[{"name":"recipient","type":"address"},{"name":"content","type":"string"},{"name":"releaseTime","type":"uint256"}],"name":"sendMessage","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[],"name":"getMyMessages","outputs":[{"name":"","type":"string[]"},{"name":"","type":"address[]"},{"name":"","type":"uint256[]"},{"name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},
            {"anonymous":False,"inputs":[{"indexed":True,"name":"sender","type":"address"},{"indexed":True,"name":"recipient","type":"address"},{"indexed":False,"name":"timestamp","type":"uint256"}],"name":"MessageSent","type":"event"}
        ]

    def get_access_control_abi(self):
        """ABI for SenderAccessControl contract"""
        return [
            {"inputs":[{"name":"_sender","type":"address"}],"name":"isSenderAllowed","outputs":[{"name":"isAllowed","type":"bool"},{"name":"reason","type":"string"}],"stateMutability":"view","type":"function"},
            {"inputs":[{"name":"_sender","type":"address"},{"name":"_duration","type":"uint256"},{"name":"_reason","type":"string"}],"name":"grantAccess","outputs":[],"stateMutability":"nonpayable","type":"function"}
        ]

    def get_user_registry_abi(self):
        """ABI for SecureUserRegistry contract"""
        return [
            {"inputs":[{"name":"","type":"address"}],"name":"verifiedUsers","outputs":[{"name":"userAddress","type":"address"},{"name":"name","type":"string"},{"name":"organization","type":"string"},{"name":"securityClearance","type":"string"},{"name":"publicKeyHash","type":"bytes32"},{"name":"level","type":"uint8"},{"name":"registrationTime","type":"uint256"},{"name":"verificationTime","type":"uint256"},{"name":"verifiedBy","type":"address"},{"name":"isActive","type":"bool"},{"name":"reputationScore","type":"uint256"},{"name":"biometricHash","type":"bytes32"}],"stateMutability":"view","type":"function"},
            {"inputs":[{"name":"_user","type":"address"},{"name":"_permission","type":"string"}],"name":"hasPermission","outputs":[{"name":"","type":"bool"}],"stateMutability":"view","type":"function"},
            {"inputs":[{"name":"_name","type":"string"},{"name":"_organization","type":"string"},{"name":"_securityClearance","type":"string"},{"name":"_publicKeyHash","type":"bytes32"},{"name":"_biometricHash","type":"bytes32"}],"name":"registerUser","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[{"name":"_userAddress","type":"address"},{"name":"_level","type":"uint8"}],"name":"verifyUser","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[{"name":"","type":"uint256"}],"name":"pendingUsersList","outputs":[{"name":"","type":"address"}],"stateMutability":"view","type":"function"},
            {"inputs":[{"name":"","type":"uint256"}],"name":"verifiedUsersList","outputs":[{"name":"","type":"address"}],"stateMutability":"view","type":"function"},
            {"inputs":[{"name":"","type":"address"}],"name":"pendingUsers","outputs":[{"name":"userAddress","type":"address"},{"name":"name","type":"string"},{"name":"organization","type":"string"},{"name":"securityClearance","type":"string"},{"name":"publicKeyHash","type":"bytes32"},{"name":"level","type":"uint8"},{"name":"registrationTime","type":"uint256"},{"name":"verificationTime","type":"uint256"},{"name":"verifiedBy","type":"address"},{"name":"isActive","type":"bool"},{"name":"reputationScore","type":"uint256"},{"name":"biometricHash","type":"bytes32"}],"stateMutability":"view","type":"function"},
            {"inputs":[],"name":"getPendingUsersCount","outputs":[{"name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
            {"inputs":[],"name":"getVerifiedUsersCount","outputs":[{"name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
            {"inputs":[{"name":"_user","type":"address"},{"name":"_reason","type":"string"}],"name":"blockUser","outputs":[],"stateMutability":"nonpayable","type":"function"}
        ]

    def get_controller_abi(self):
        """ABI for AdvancedSteganographyController contract"""
        return [
            {"inputs":[],"name":"currentProtocol","outputs":[{"name":"","type":"string"}],"stateMutability":"view","type":"function"},
            {"inputs":[{"name":"_newProtocol","type":"string"}],"name":"switchProtocol","outputs":[],"stateMutability":"nonpayable","type":"function"}
        ]

    def get_registry_abi(self):
        """ABI for StealthRegistry contract"""
        return [
            {"inputs":[],"name":"currentStatus","outputs":[{"name":"","type":"uint8"}],"stateMutability":"view","type":"function"},
            {"inputs":[],"name":"toggleEmergencyStatus","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[{"name":"_node","type":"address"}],"name":"reportNodeFailure","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[{"name":"_ip","type":"string"},{"name":"_channels","type":"string[]"},{"name":"_publicKey","type":"string"}],"name":"registerNode","outputs":[],"stateMutability":"nonpayable","type":"function"},
            {"inputs":[],"name":"getAllNodes","outputs":[{"components":[{"name":"wallet","type":"address"},{"name":"ip","type":"string"},{"name":"channels","type":"string[]"},{"name":"publicKey","type":"string"},{"name":"lastSeen","type":"uint256"},{"name":"isActive","type":"bool"},{"name":"reputation","type":"uint256"}],"name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"}
        ]

    # ==========================
    # Contract Loaders
    # ==========================

    def load_registry_contract(self, address=None):
        if not address: address = os.getenv('REGISTRY_CONTRACT')
        if not address: return False
        self.registry_contract = self.w3.eth.contract(address=Web3.to_checksum_address(address), abi=self.get_registry_abi())
        return True

    def load_access_control(self, address=None):
        if not address: address = os.getenv('ACCESS_CONTROL_CONTRACT')
        if not address: return False
        self.access_control = self.w3.eth.contract(address=Web3.to_checksum_address(address), abi=self.get_access_control_abi())
        return True

    def load_user_registry(self, address=None):
        if not address: address = os.getenv('USER_REGISTRY_CONTRACT')
        if not address: return False
        self.user_registry = self.w3.eth.contract(address=Web3.to_checksum_address(address), abi=self.get_user_registry_abi())
        return True

    def load_controller_contract(self, address=None):
        if not address: address = os.getenv('CONTROLLER_CONTRACT')
        if not address: return False
        self.controller = self.w3.eth.contract(address=Web3.to_checksum_address(address), abi=self.get_controller_abi())
        return True

    def load_dead_drop_contract(self, address=None):
        if not address: address = os.getenv('DEAD_DROP_CONTRACT')
        if not address: return False
        self.dead_drop_contract = self.w3.eth.contract(address=Web3.to_checksum_address(address), abi=self.get_contract_abi())
        return True

    # ==========================
    # Utility Methods
    # ==========================

    def _send_tx(self, func, private_key):
        """Helper to build, sign and broadcast transactions"""
        try:
            account = self.w3.eth.account.from_key(private_key)
            # Use 'pending' to get the latest nonce including unconfirmed txs
            nonce = self.w3.eth.get_transaction_count(account.address, 'pending')
            
            # Fetch base fee and add 20% multiplier for reliability
            gas_price = int(self.w3.eth.gas_price * 1.2)
            
            tx = func.build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': gas_price
            })
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
            
            # Robust extraction of raw transaction data
            raw_tx = getattr(signed_tx, 'rawTransaction', None)
            if raw_tx is None:
                raw_tx = getattr(signed_tx, 'raw_transaction', None)
            if raw_tx is None:
                try:
                    raw_tx = signed_tx['rawTransaction']
                except:
                    raw_tx = signed_tx.get('rawTransaction') or signed_tx.get('raw_transaction')
            
            if raw_tx is None:
                raise ValueError("Could not extract rawTransaction from signed_tx")
                
            tx_hash = self.w3.eth.send_raw_transaction(raw_tx)
            return {'success': True, 'tx_hash': self.w3.to_hex(tx_hash)}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_latest_block_data(self):
        try:
            block = self.w3.eth.get_block('latest')
            return {'success': True, 'number': block['number'], 'hash': self.w3.to_hex(block['hash'])}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    # ==========================
    # Feature Methods: Registry
    # ==========================

    def get_global_status(self):
        if not hasattr(self, 'registry_contract'): return {'success': False, 'error': 'Registry not loaded'}
        try:
            status = self.registry_contract.functions.currentStatus().call()
            return {'success': True, 'status': 'SILENCED' if status == 1 else 'NORMAL'}
        except Exception as e: return {'success': False, 'error': str(e)}

    def toggle_emergency_status(self, private_key):
        if not hasattr(self, 'registry_contract'): return {'success': False, 'error': 'Registry not loaded'}
        return self._send_tx(self.registry_contract.functions.toggleEmergencyStatus(), private_key)

    def report_node_failure(self, private_key, node_wallet):
        if not hasattr(self, 'registry_contract'): return {'success': False, 'error': 'Registry not loaded'}
        return self._send_tx(self.registry_contract.functions.reportNodeFailure(node_wallet), private_key)

    def register_p2p_node(self, private_key, ip, channels, public_key):
        if not hasattr(self, 'registry_contract'): return {'success': False, 'error': 'Registry not loaded'}
        return self._send_tx(self.registry_contract.functions.registerNode(ip, channels, public_key), private_key)

    def get_blockchain_nodes(self):
        if not hasattr(self, 'registry_contract'): return {'success': False, 'error': 'Registry not loaded'}
        try:
            nodes_data = self.registry_contract.functions.getAllNodes().call()
            active_nodes = []
            for node in nodes_data:
                active_nodes.append({
                    'wallet': node[0], 'ip': node[1], 'channels': node[2],
                    'public_key': node[3], 'last_seen': node[4], 'is_active': node[5], 'reputation': node[6]
                })
            return {'success': True, 'nodes': active_nodes}
        except Exception as e: return {'success': False, 'error': str(e)}

    def get_node_pqa_public_key(self, wallet_address):
        """Retrieve the PQA public key for a specific node wallet"""
        if not hasattr(self, 'registry_contract'): return None
        try:
            node = self.registry_contract.functions.nodes(wallet_address).call()
            if node[5]: # isActive
                return node[3] # publicKey field
            return None
        except:
            return None

    # ==========================
    # Feature Methods: Access Control
    # ==========================

    def check_access(self, sender_address):
        """Check if sender is whitelisted (Internal helper for UI)"""
        if not hasattr(self, 'access_control'): return {'success': True, 'allowed': True}
        try:
            res = self.access_control.functions.isSenderAllowed(sender_address).call()
            return {'success': True, 'allowed': res[0], 'reason': res[1]}
        except Exception as e: return {'success': False, 'error': str(e)}

    def grant_access(self, private_key, sender_address, duration=0, reason="Authorized via logic"):
        if not hasattr(self, 'access_control'): return {'success': False, 'error': 'Access Control not loaded'}
        return self._send_tx(self.access_control.functions.grantAccess(sender_address, duration, reason), private_key)

    # ==========================
    # Feature Methods: User Registry
    # ==========================

    def register_user(self, private_key, name, organization, clearance):
        if not hasattr(self, 'user_registry'): return {'success': False, 'error': 'User Registry not loaded'}
        pub_key_hash = self.w3.solidity_keccak(['string'], [f"PUB_{name}"]) 
        bio_hash = self.w3.solidity_keccak(['string'], [f"BIO_{name}"])
        return self._send_tx(self.user_registry.functions.registerUser(name, organization, clearance, pub_key_hash, bio_hash), private_key)

    def verify_user(self, private_key, user_address, level):
        if not hasattr(self, 'user_registry'): return {'success': False, 'error': 'User Registry not loaded'}
        return self._send_tx(self.user_registry.functions.verifyUser(user_address, level), private_key)

    def block_user(self, private_key, user_address, reason="Administrative Action"):
        if not hasattr(self, 'user_registry'): return {'success': False, 'error': 'User Registry not loaded'}
        return self._send_tx(self.user_registry.functions.blockUser(user_address, reason), private_key)

    def get_pending_users(self):
        if not hasattr(self, 'user_registry'): return {'success': False, 'error': 'User Registry not loaded'}
        try:
            count = self.user_registry.functions.getPendingUsersCount().call()
            users = []
            for i in range(count):
                addr = self.user_registry.functions.pendingUsersList(i).call()
                data = self.user_registry.functions.pendingUsers(addr).call()
                users.append({
                    'address': addr, 'name': data[1], 'organization': data[2],
                    'clearance': data[3], 'level': data[5], 'registrationTime': data[6]
                })
            return {'success': True, 'users': users}
        except Exception as e: return {'success': False, 'error': str(e)}

    def get_verified_users(self):
        if not hasattr(self, 'user_registry'): return {'success': False, 'error': 'User Registry not loaded'}
        try:
            count = self.user_registry.functions.getVerifiedUsersCount().call()
            users = []
            for i in range(count):
                addr = self.user_registry.functions.verifiedUsersList(i).call()
                data = self.user_registry.functions.verifiedUsers(addr).call()
                users.append({
                    'address': addr, 'name': data[1], 'organization': data[2],
                    'clearance': data[3], 'level': data[5], 'isActive': data[9], 'reputation': data[10]
                })
            return {'success': True, 'users': users}
        except Exception as e: return {'success': False, 'error': str(e)}

    def get_user_clearance(self, address):
        if not hasattr(self, 'user_registry'): return {'success': False, 'error': 'User Registry not loaded'}
        try:
            user_data = self.user_registry.functions.verifiedUsers(address).call()
            levels = ["NONE", "READ_ONLY", "BASIC_SENDER", "ENCRYPTED_SENDER", "TRIGGER_CREATOR", "FULL_ACCESS"]
            return {
                'success': True, 'name': user_data[1], 'organization': user_data[2],
                'clearance': user_data[3], 'level': levels[user_data[5]] if user_data[5] < len(levels) else "UNKNOWN",
                'isActive': user_data[9], 'reputation': user_data[10]
            }
        except Exception as e: return {'success': False, 'error': str(e)}

    # ==========================
    # Feature Methods: Controller
    # ==========================

    def get_current_protocol(self):
        if not hasattr(self, 'controller'): return {'success': True, 'protocol': 'timing'} # Default
        try:
            proto = self.controller.functions.currentProtocol().call()
            return {'success': True, 'protocol': proto}
        except Exception as e: return {'success': False, 'error': str(e)}

    def switch_protocol(self, private_key, new_protocol):
        if not hasattr(self, 'controller'): return {'success': False, 'error': 'Controller not loaded'}
        return self._send_tx(self.controller.functions.switchProtocol(new_protocol), private_key)

    # ==========================
    # Feature Methods: Dead Drop
    # ==========================

    def send_to_deaddrop(self, private_key, recipient, encrypted_content, release_time=0):
        if not hasattr(self, 'dead_drop_contract'): return {'success': False, 'error': 'Dead Drop not loaded'}
        return self._send_tx(self.dead_drop_contract.functions.sendMessage(recipient, encrypted_content, int(release_time)), private_key)

    def get_from_deaddrop(self, address):
        if not hasattr(self, 'dead_drop_contract'): return {'success': False, 'error': 'Dead Drop not loaded'}
        try:
            data = self.dead_drop_contract.functions.getMyMessages().call({'from': address})
            messages = []
            for i in range(len(data[0])):
                messages.append({
                    'content': data[0][i], 'sender': data[1][i], 'timestamp': data[2][i], 'release_time': data[3][i],
                    'is_locked': data[0][i] == "[LOCKED]",
                    'formatted_time': datetime.fromtimestamp(data[2][i]).strftime('%Y-%m-%d %H:%M:%S')
                })
            return {'success': True, 'messages': messages}
        except Exception as e: return {'success': False, 'error': str(e)}

    def get_all_deaddrop_events(self, limit=50):
        if not hasattr(self, 'dead_drop_contract'): return {'success': False, 'error': 'Dead Drop not loaded'}
        try:
            events = self.dead_drop_contract.events.MessageSent.get_logs(fromBlock=max(0, self.w3.eth.block_number - 5000), toBlock='latest')
            history = []
            for event in reversed(events[-limit:]):
                args = event['args']
                history.append({
                    'sender': args['sender'], 'recipient': args['recipient'], 'timestamp': args['timestamp'],
                    'tx_hash': event['transactionHash'].hex(), 'formatted_time': datetime.fromtimestamp(args['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                })
            return {'success': True, 'history': history}
        except Exception as e: return {'success': False, 'error': str(e)}

# ==========================
# Legacy / Compatibility Functions
# ==========================

class SimulatedBlockchain:
    def __init__(self):
        self.transactions = {}
        self.block_number = 1000000
    def store_message(self, sender, message_hash, encryption_key, receiver):
        tx_hash = hashlib.sha256(f"{sender}{message_hash}{encryption_key}{time.time()}".encode()).hexdigest()
        self.transactions[tx_hash] = {'sender': sender, 'receiver': receiver, 'message_hash': message_hash, 'encryption_key': encryption_key, 'timestamp': int(time.time()), 'confirmed': True}
        return {'tx_hash': tx_hash, 'status': 'confirmed'}
    def get_key(self, tx_hash):
        return self.transactions.get(tx_hash, {'error': 'Not found'})

simulated_blockchain = SimulatedBlockchain()

def store_on_blockchain(sender, message, encryption_key, receiver):
    return simulated_blockchain.store_message(sender, hashlib.sha256(message.encode()).hexdigest(), encryption_key, receiver)

def retrieve_from_blockchain(tx_hash):
    return simulated_blockchain.get_key(tx_hash)

def verify_message_integrity(message, tx_hash):
    data = retrieve_from_blockchain(tx_hash)
    return hashlib.sha256(message.encode()).hexdigest() == data.get('message_hash')

if __name__ == '__main__':
    print("Blockchain Integration Loaded.")
