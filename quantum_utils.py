import base64
import os
import json
import hashlib

# Note: The 'kyber-py' package translates to the 'kyber' module
try:
    from kyber.kyber import Kyber768
except ImportError:
    # Handle different package versions if necessary
    try:
        from kyber import Kyber768
    except ImportError:
        print("❌ kyber-py library not found. System will fallback to classical security.")
        Kyber768 = None

class QuantumUtils:
    """Wrapper for Crystals-Kyber (Kyber-768) Implementation"""
    
    @staticmethod
    def generate_keypair():
        """Generate a new Kyber-768 KeyPair"""
        if not Kyber768:
            return None, None
        pk, sk = Kyber768.keygen()
        return pk, sk

    @staticmethod
    def encapsulate(public_key):
        """Generate a shared secret and ciphertext for a given public key"""
        if not Kyber768:
            return None, None
        c, ss = Kyber768.enc(public_key)
        return c, ss

    @staticmethod
    def decapsulate(ciphertext, secret_key):
        """Extract shared secret from ciphertext using secret key"""
        if not Kyber768:
            return None
        ss = Kyber768.dec(ciphertext, secret_key)
        return ss

    @staticmethod
    def bytes_to_base64(data):
        return base64.b64encode(data).decode('utf-8')

    @staticmethod
    def base64_to_bytes(data_b64):
        return base64.b64decode(data_b64)

    @staticmethod
    def get_hybrid_key(quantum_secret, classical_secret):
        """Derive a final key from PQA secret and Blockchain secret"""
        combined = quantum_secret + classical_secret
        return hashlib.sha256(combined).digest()

    @staticmethod
    def save_local_keys(pk, sk, filename="quantum_keys.json"):
        """Save keys locally for node identity"""
        data = {
            "public_key": QuantumUtils.bytes_to_base64(pk),
            "secret_key": QuantumUtils.bytes_to_base64(sk)
        }
        with open(filename, "w") as f:
            json.dump(data, f)
        print(f"🔒 Quantum keys saved to {filename}")

    @staticmethod
    def load_local_keys(filename="quantum_keys.json"):
        """Load keys if they exist"""
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
                return (
                    QuantumUtils.base64_to_bytes(data["public_key"]),
                    QuantumUtils.base64_to_bytes(data["secret_key"])
                )
        return None, None
