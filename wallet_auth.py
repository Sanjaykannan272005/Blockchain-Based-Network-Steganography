"""
Wallet Authentication Module for Steganography
Integrates MetaMask wallet authentication with smart contract access control
"""

from web3 import Web3
from eth_account.messages import encode_defunct
import json
from datetime import datetime, timedelta

class WalletAuthenticator:
    """Handles wallet authentication and message verification"""
    
    def __init__(self, w3, contract_address, contract_abi):
        """
        Initialize wallet authenticator
        
        Args:
            w3: Web3 instance
            contract_address: Address of SenderAccessControl contract
            contract_abi: Contract ABI
        """
        self.w3 = w3
        self.contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        
    def verify_wallet_signature(self, message, signature, signer_address):
        """
        Verify a message was signed by the claimed signer
        
        Args:
            message: Original message string
            signature: Signature hex string
            signer_address: Expected signer address
            
        Returns:
            dict with success status and details
        """
        try:
            # Create message hash as MetaMask would
            message_hash = encode_defunct(text=message)
            
            # Recover signer from signature
            recovered_address = self.w3.eth.account.recover_message(
                message_hash,
                signature=signature
            )
            
            # Check if recovered address matches
            if recovered_address.lower() == signer_address.lower():
                return {
                    'valid': True,
                    'signer': recovered_address,
                    'message': 'Signature valid'
                }
            else:
                return {
                    'valid': False,
                    'expected': signer_address,
                    'recovered': recovered_address,
                    'message': 'Signature does not match signer'
                }
        except Exception as e:
            return {
                'valid': False,
                'message': f'Signature verification failed: {str(e)}'
            }
    
    def is_sender_allowed(self, sender_address):
        """
        Check if sender is allowed via smart contract
        
        Args:
            sender_address: Wallet address to check
            
        Returns:
            dict with permission status and details
        """
        try:
            # Call smart contract
            is_allowed, reason = self.contract.functions.isSenderAllowed(
                sender_address
            ).call()
            
            return {
                'allowed': is_allowed,
                'reason': reason
            }
        except Exception as e:
            return {
                'allowed': False,
                'reason': f'Contract check failed: {str(e)}'
            }
    
    def get_access_details(self, sender_address):
        """
        Get detailed access information for a sender
        
        Args:
            sender_address: Wallet address to check
            
        Returns:
            dict with access details
        """
        try:
            allowed, granted_at, expires_at, reason = self.contract.functions.getAccessDetails(
                sender_address
            ).call()
            
            # Format timestamps
            granted_at_str = datetime.fromtimestamp(granted_at).isoformat() if granted_at else None
            expires_at_str = None
            time_remaining = None
            
            if expires_at > 0:
                expires_at_datetime = datetime.fromtimestamp(expires_at)
                expires_at_str = expires_at_datetime.isoformat()
                
                # Check how much time remaining
                now = datetime.now()
                if now < expires_at_datetime:
                    time_remaining = int((expires_at_datetime - now).total_seconds())
            
            return {
                'allowed': allowed,
                'granted_at': granted_at_str,
                'expires_at': expires_at_str,
                'time_remaining_seconds': time_remaining,
                'reason': reason,
                'is_permanent': expires_at == 0
            }
        except Exception as e:
            return {
                'error': str(e)
            }
    
    def authenticate_message(self, message, signature, sender_address):
        """
        Complete authentication: verify signature AND check access
        
        Args:
            message: Message content
            signature: Wallet signature
            sender_address: Claimed sender address
            
        Returns:
            dict with complete authentication result
        """
        # Step 1: Verify signature
        sig_result = self.verify_wallet_signature(message, signature, sender_address)
        
        if not sig_result['valid']:
            return {
                'authenticated': False,
                'reason': 'Invalid signature',
                'details': sig_result
            }
        
        # Step 2: Check whitelist
        access_result = self.is_sender_allowed(sender_address)
        
        if not access_result['allowed']:
            return {
                'authenticated': False,
                'reason': access_result['reason'],
                'signer_valid': True
            }
        
        # Step 3: Get full details
        details = self.get_access_details(sender_address)
        
        return {
            'authenticated': True,
            'sender': sender_address,
            'access_details': details
        }
    
    def create_signing_message(self, message_hash, recipient=None):
        """
        Create a standardized message for signing
        
        Args:
            message_hash: Hash of the steganographic message
            recipient: Optional recipient address
            
        Returns:
            Standard message for user to sign
        """
        timestamp = datetime.now().isoformat()
        
        signing_message = f"""Steganography Message Authentication

Message Hash: {message_hash}
Timestamp: {timestamp}"""
        
        if recipient:
            signing_message += f"\nRecipient: {recipient}"
        
        signing_message += "\n\nSign this message to authenticate your identity."
        
        return signing_message


def load_access_control_contract(w3, contract_address_str):
    """
    Load the SenderAccessControl contract
    
    Args:
        w3: Web3 instance
        contract_address_str: Contract address string
        
    Returns:
        Tuple of (contract, contract_address)
    """
    # Standard contract ABI for SenderAccessControl
    contract_abi = [
        {
            "inputs": [{"internalType": "address", "name": "_sender", "type": "address"}],
            "name": "isSenderAllowed",
            "outputs": [
                {"internalType": "bool", "name": "isAllowed", "type": "bool"},
                {"internalType": "string", "name": "reason", "type": "string"}
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [{"internalType": "address", "name": "_sender", "type": "address"}],
            "name": "getAccessDetails",
            "outputs": [
                {"internalType": "bool", "name": "allowed", "type": "bool"},
                {"internalType": "uint256", "name": "grantedAt", "type": "uint256"},
                {"internalType": "uint256", "name": "expiresAt", "type": "uint256"},
                {"internalType": "string", "name": "reason", "type": "string"}
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]
    
    contract_address = Web3.to_checksum_address(contract_address_str)
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    
    return contract, contract_address
