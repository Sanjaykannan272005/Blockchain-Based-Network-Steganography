import json
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time

class OnionUtils:
    """Utilities for building and peeling onion-layered steganographic packets"""
    
    @staticmethod
    def derive_key(shared_secret):
        """Derive a 32-byte AES key from a shared secret"""
        return hashlib.sha256(str(shared_secret).encode()).digest()

    @staticmethod
    def encrypt_layer(data, key):
        """Encrypt a layer of the onion"""
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        encrypted = cipher.encrypt(pad(data.encode(), 16))
        return base64.b64encode(iv + encrypted).decode()

    @staticmethod
    def decrypt_layer(encrypted_data, key):
        """Decrypt a layer of the onion"""
        try:
            raw = base64.b64decode(encrypted_data)
            iv = raw[:16]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(raw[16:]), 16)
            return decrypted.decode()
        except Exception as e:
            return None

    @classmethod
    def create_onion(cls, message, hops, keys):
        """
        Create a multi-layered onion.
        hops: list of (ip, channel) pairs
        keys: list of keys for each hop
        """
        # Outer layer is the final recipient
        # Structure: {"next_hop": "IP", "channel": "timing", "payload": "..."}
        
        current_payload = message
        
        # Iterate backwards through hops to build layers
        for i in range(len(hops)-1, -1, -1):
            hop_ip, hop_channel = hops[i]
            layer_data = json.dumps({
                "next_hop": hop_ip,
                "channel": hop_channel,
                "payload": current_payload
            })
            current_payload = cls.encrypt_layer(layer_data, keys[i])
            
        return current_payload

    @classmethod
    def peel_layer(cls, encrypted_onion, key):
        """Peel one layer of the onion"""
        peeled = cls.decrypt_layer(encrypted_onion, key)
        if peeled:
            try:
                return json.loads(peeled)
            except:
                return None
        return None

if __name__ == "__main__":
    # Test onion creation and peeling
    key1 = OnionUtils.derive_key("hop1_pass")
    key2 = OnionUtils.derive_key("hop2_pass")
    
    msg = "Secret Intel"
    hops = [("192.168.1.5", "size"), ("10.0.0.5", "timing")]
    keys = [key1, key2]
    
    onion = OnionUtils.create_onion(msg, hops, keys)
    print(f"Onion created: {onion[:50]}...")
    
    # Peel Hop 1
    layer1 = OnionUtils.peel_layer(onion, key1)
    print(f"Hop 1 peeled: {layer1['next_hop']} via {layer1['channel']}")
    
    # Peel Hop 2
    layer2 = OnionUtils.peel_layer(layer1['payload'], key2)
    print(f"Hop 2 peeled: {layer2['next_hop']} via {layer2['channel']}")
    print(f"Final Message: {layer2['payload']}")
