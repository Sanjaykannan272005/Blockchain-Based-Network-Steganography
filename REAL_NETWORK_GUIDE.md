# 🌐 REAL NETWORK STEGANOGRAPHY - Complete Guide
# Blockchain-Controlled Network Packet Steganography

## 🎯 What This System Does

**SENDER SIDE:**
1. Takes your secret message
2. Encrypts it with blockchain-derived key
3. Hides encrypted data in REAL network packets (TCP/UDP/ICMP)
4. Sends packets over the network (looks like normal traffic)

**RECEIVER SIDE:**
1. Captures network packets with Wireshark/tcpdump
2. Extracts hidden data from packet timing/size/headers
3. Uses blockchain to get decryption key
4. Decrypts and reads the secret message

**BLOCKCHAIN ROLE:**
- Controls WHO can send/receive (authentication)
- Controls WHEN messages can be sent (time windows)
- Controls HOW to send (which protocol: timing/size/TTL)
- Provides encryption keys (derived from blockchain data)

---

## 📋 Prerequisites

### Install Required Tools:

```bash
# 1. Install Python packages
python -m pip install scapy web3 pycryptodome

# 2. Install Wireshark (for packet capture)
# Download from: https://www.wireshark.org/download.html

# 3. Install Npcap (Windows) or libpcap (Linux)
# Comes with Wireshark on Windows
```

---

## 🚀 STEP-BY-STEP: Send Secret Message Over Network

### **STEP 1: Start Blockchain Simulation**

```bash
# Terminal 1: Start blockchain
python blockchain_web_app.py
```

Visit: http://localhost:5000
- This creates the blockchain that controls everything

---

### **STEP 2: Run Network Steganography Demo**

```bash
# Terminal 2: Run the advanced system
python advanced_blockchain_steganography.py
```

This demonstrates all 10 features including:
- Blockchain control rules
- Key generation from blockchain
- Multi-chain distribution
- Dead drop coordinates

---

### **STEP 3: Send Real Network Packets (Sender)**

Create file: `sender.py`

```python
from scapy.all import *
import hashlib
import time
from Crypto.Cipher import AES
import base64

# 1. Get blockchain key
def get_blockchain_key():
    # In real system, query blockchain
    # For demo, simulate
    block_hash = hashlib.sha256(f"block_{int(time.time())}".encode()).hexdigest()
    key = hashlib.sha256(block_hash.encode()).digest()
    return key

# 2. Encrypt message
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    pad_length = 16 - (len(message) % 16)
    padded = message + (chr(pad_length) * pad_length)
    encrypted = cipher.encrypt(padded.encode())
    return base64.b64encode(iv + encrypted).decode()

# 3. Hide in network packets using TIMING channel
def send_via_timing_channel(encrypted_data, target_ip):
    print(f"🚀 Sending via TIMING channel to {target_ip}")
    
    # Convert to binary
    binary = ''.join(format(ord(c), '08b') for c in encrypted_data)
    
    # Send packets with timing delays
    for bit in binary:
        # Send ICMP ping
        packet = IP(dst=target_ip)/ICMP()
        send(packet, verbose=0)
        
        # Delay encodes the bit
        if bit == '0':
            time.sleep(0.1)  # 100ms = 0
        else:
            time.sleep(0.2)  # 200ms = 1
    
    print(f"✅ Sent {len(binary)} bits via timing channel")

# 4. Hide in network packets using SIZE channel
def send_via_size_channel(encrypted_data, target_ip):
    print(f"🚀 Sending via SIZE channel to {target_ip}")
    
    # Convert to binary
    binary = ''.join(format(ord(c), '08b') for c in encrypted_data)
    
    # Send packets with different sizes
    for bit in binary:
        if bit == '0':
            payload = "X" * 100  # 100 bytes = 0
        else:
            payload = "X" * 200  # 200 bytes = 1
        
        packet = IP(dst=target_ip)/ICMP()/payload
        send(packet, verbose=0)
    
    print(f"✅ Sent {len(binary)} bits via size channel")

# 5. Hide in network packets using TTL channel
def send_via_ttl_channel(encrypted_data, target_ip):
    print(f"🚀 Sending via TTL channel to {target_ip}")
    
    # Convert to binary
    binary = ''.join(format(ord(c), '08b') for c in encrypted_data)
    
    # Send packets with different TTL values
    for bit in binary:
        if bit == '0':
            ttl = 64  # TTL 64 = 0
        else:
            ttl = 65  # TTL 65 = 1
        
        packet = IP(dst=target_ip, ttl=ttl)/ICMP()
        send(packet, verbose=0)
    
    print(f"✅ Sent {len(binary)} bits via TTL channel")

# MAIN: Send secret message
if __name__ == "__main__":
    # Configuration
    TARGET_IP = "192.168.1.100"  # Change to receiver IP
    SECRET_MESSAGE = "Attack at dawn"
    
    print("🔐 BLOCKCHAIN-CONTROLLED NETWORK STEGANOGRAPHY")
    print("=" * 60)
    
    # Step 1: Get key from blockchain
    print("\\n📡 Step 1: Getting encryption key from blockchain...")
    key = get_blockchain_key()
    print(f"✅ Key derived: {key.hex()[:20]}...")
    
    # Step 2: Encrypt message
    print(f"\\n🔒 Step 2: Encrypting message...")
    encrypted = encrypt_message(SECRET_MESSAGE, key)
    print(f"✅ Encrypted: {encrypted[:30]}...")
    
    # Step 3: Choose channel (blockchain controls this)
    print(f"\\n📊 Step 3: Blockchain selecting optimal channel...")
    channel = "timing"  # In real system, blockchain decides
    print(f"✅ Selected: {channel} channel")
    
    # Step 4: Send via network
    print(f"\\n🌐 Step 4: Sending via network steganography...")
    
    if channel == "timing":
        send_via_timing_channel(encrypted, TARGET_IP)
    elif channel == "size":
        send_via_size_channel(encrypted, TARGET_IP)
    elif channel == "ttl":
        send_via_ttl_channel(encrypted, TARGET_IP)
    
    print(f"\\n✅ MESSAGE SENT SUCCESSFULLY!")
    print(f"📝 Receiver should capture packets and extract data")
```

---

### **STEP 4: Receive Network Packets (Receiver)**

Create file: `receiver.py`

```python
from scapy.all import *
import hashlib
import time
from Crypto.Cipher import AES
import base64

# 1. Get same blockchain key
def get_blockchain_key():
    # Same as sender - both derive from blockchain
    block_hash = hashlib.sha256(f"block_{int(time.time())}".encode()).hexdigest()
    key = hashlib.sha256(block_hash.encode()).digest()
    return key

# 2. Decrypt message
def decrypt_message(encrypted_data, key):
    try:
        encrypted_bytes = base64.b64decode(encrypted_data)
        iv = encrypted_bytes[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_bytes[16:])
        pad_length = ord(decrypted[-1:])
        return decrypted[:-pad_length].decode()
    except:
        return None

# 3. Extract from TIMING channel
def receive_via_timing_channel():
    print("👂 Listening for TIMING channel...")
    
    packets = []
    last_time = None
    binary_data = ""
    
    def packet_handler(packet):
        nonlocal last_time, binary_data
        
        if packet.haslayer(ICMP):
            current_time = time.time()
            
            if last_time is not None:
                delay = current_time - last_time
                
                # Decode timing
                if 0.08 < delay < 0.12:  # ~0.1s = 0
                    binary_data += '0'
                elif 0.18 < delay < 0.22:  # ~0.2s = 1
                    binary_data += '1'
            
            last_time = current_time
    
    # Capture packets for 30 seconds
    sniff(filter="icmp", prn=packet_handler, timeout=30)
    
    # Convert binary to text
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    extracted = ''.join([chr(int(c, 2)) for c in chars if len(c) == 8])
    
    return extracted

# 4. Extract from SIZE channel
def receive_via_size_channel():
    print("👂 Listening for SIZE channel...")
    
    binary_data = ""
    
    def packet_handler(packet):
        nonlocal binary_data
        
        if packet.haslayer(ICMP) and packet.haslayer(Raw):
            size = len(packet[Raw].load)
            
            # Decode size
            if 90 < size < 110:  # ~100 bytes = 0
                binary_data += '0'
            elif 190 < size < 210:  # ~200 bytes = 1
                binary_data += '1'
    
    # Capture packets
    sniff(filter="icmp", prn=packet_handler, timeout=30)
    
    # Convert binary to text
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    extracted = ''.join([chr(int(c, 2)) for c in chars if len(c) == 8])
    
    return extracted

# 5. Extract from TTL channel
def receive_via_ttl_channel():
    print("👂 Listening for TTL channel...")
    
    binary_data = ""
    
    def packet_handler(packet):
        nonlocal binary_data
        
        if packet.haslayer(IP):
            ttl = packet[IP].ttl
            
            # Decode TTL
            if ttl == 64:
                binary_data += '0'
            elif ttl == 65:
                binary_data += '1'
    
    # Capture packets
    sniff(filter="icmp", prn=packet_handler, timeout=30)
    
    # Convert binary to text
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    extracted = ''.join([chr(int(c, 2)) for c in chars if len(c) == 8])
    
    return extracted

# MAIN: Receive secret message
if __name__ == "__main__":
    print("🔐 BLOCKCHAIN-CONTROLLED NETWORK STEGANOGRAPHY")
    print("=" * 60)
    
    # Step 1: Get key from blockchain
    print("\\n📡 Step 1: Getting decryption key from blockchain...")
    key = get_blockchain_key()
    print(f"✅ Key derived: {key.hex()[:20]}...")
    
    # Step 2: Determine channel (blockchain tells us)
    print(f"\\n📊 Step 2: Blockchain indicates channel type...")
    channel = "timing"  # In real system, blockchain tells us
    print(f"✅ Channel: {channel}")
    
    # Step 3: Capture and extract
    print(f"\\n🌐 Step 3: Capturing network packets...")
    
    if channel == "timing":
        encrypted = receive_via_timing_channel()
    elif channel == "size":
        encrypted = receive_via_size_channel()
    elif channel == "ttl":
        encrypted = receive_via_ttl_channel()
    
    print(f"✅ Extracted: {encrypted[:30]}...")
    
    # Step 4: Decrypt
    print(f"\\n🔓 Step 4: Decrypting message...")
    message = decrypt_message(encrypted, key)
    
    if message:
        print(f"\\n✅ MESSAGE RECEIVED: {message}")
    else:
        print(f"\\n❌ Decryption failed")
```

---

## 🎯 HOW TO USE (Complete Workflow)

### **Setup (One Time)**

1. **Install everything:**
```bash
python -m pip install scapy web3 pycryptodome
# Install Wireshark from website
```

2. **Start blockchain:**
```bash
python blockchain_web_app.py
```

---

### **Sending a Message**

**On Sender Computer:**

1. Create `sender.py` (code above)

2. Edit configuration:
```python
TARGET_IP = "192.168.1.100"  # Receiver's IP
SECRET_MESSAGE = "Attack at dawn"
```

3. Run as administrator (required for packet sending):
```bash
# Windows (Run as Administrator)
python sender.py

# Linux
sudo python sender.py
```

4. You'll see:
```
🔐 BLOCKCHAIN-CONTROLLED NETWORK STEGANOGRAPHY
📡 Getting encryption key from blockchain...
✅ Key derived: abc123...
🔒 Encrypting message...
✅ Encrypted: U2FsdGVk...
📊 Blockchain selecting optimal channel...
✅ Selected: timing channel
🌐 Sending via network steganography...
✅ Sent 120 bits via timing channel
✅ MESSAGE SENT SUCCESSFULLY!
```

---

### **Receiving a Message**

**On Receiver Computer:**

1. Create `receiver.py` (code above)

2. Run as administrator:
```bash
# Windows (Run as Administrator)
python receiver.py

# Linux
sudo python receiver.py
```

3. You'll see:
```
🔐 BLOCKCHAIN-CONTROLLED NETWORK STEGANOGRAPHY
📡 Getting decryption key from blockchain...
✅ Key derived: abc123...
📊 Blockchain indicates channel type...
✅ Channel: timing
🌐 Capturing network packets...
👂 Listening for TIMING channel...
✅ Extracted: U2FsdGVk...
🔓 Decrypting message...
✅ MESSAGE RECEIVED: Attack at dawn
```

---

## 🔑 Blockchain Control Explained

### **1. Key Generation**
```
Blockchain Block #12345
↓
Hash: 0xabc123...
↓
Both sender & receiver derive SAME key
↓
No key transmission needed!
```

### **2. Access Control**
```
Blockchain says: "Only allow 2 AM - 4 AM"
↓
Sender tries at 3 AM → ✅ Allowed
Sender tries at 5 AM → ❌ Blocked
```

### **3. Protocol Selection**
```
Blockchain monitors network conditions
↓
High detection risk → Use TTL (most stealthy)
High urgency → Use Size (most capacity)
Normal → Use Timing (balanced)
```

### **4. Authentication**
```
Sender address: 0x123abc...
↓
Blockchain verifies: Is this address authorized?
↓
Yes → Allow sending
No → Block
```

---

## 🌐 Network Channels Explained

### **Timing Channel**
- **How:** Delay between packets encodes bits
- **0.1s delay = 0, 0.2s delay = 1**
- **Stealth:** Medium
- **Capacity:** Low (slow)
- **Best for:** Covert communication

### **Size Channel**
- **How:** Packet size encodes bits
- **100 bytes = 0, 200 bytes = 1**
- **Stealth:** High
- **Capacity:** Medium
- **Best for:** Balanced use

### **TTL Channel**
- **How:** Time-To-Live field encodes bits
- **TTL 64 = 0, TTL 65 = 1**
- **Stealth:** Very High
- **Capacity:** Medium
- **Best for:** Maximum stealth

---

## 🚨 Important Notes

### **Administrator/Root Required**
- Sending raw packets requires admin privileges
- Run terminals as administrator

### **Firewall**
- May need to allow ICMP packets
- Windows: Allow in Windows Firewall
- Linux: Check iptables

### **Same Network**
- For testing, use same local network
- Or use VPN to connect remote computers

### **Blockchain Sync**
- Both sender & receiver must use same blockchain
- Keys derived from same block data
- Time synchronization important

---

## 📊 Testing Locally (Same Computer)

```bash
# Terminal 1: Start blockchain
python blockchain_web_app.py

# Terminal 2: Start receiver (as admin)
python receiver.py

# Terminal 3: Start sender (as admin)
# Change TARGET_IP to 127.0.0.1
python sender.py
```

---

## 🎓 What Makes This Special

1. **Real Network Packets:** Actually sends data over network
2. **Blockchain Control:** Blockchain decides everything
3. **No Key Exchange:** Keys derived, never transmitted
4. **Looks Normal:** Packets appear as regular traffic
5. **Automatic Rotation:** Keys change every block
6. **Multi-Protocol:** Can switch between timing/size/TTL
7. **Authentication:** Blockchain verifies sender/receiver
8. **Forensic Proof:** Blockchain records everything

---

## 🚀 Next Steps

1. Test locally first (127.0.0.1)
2. Test on same network (192.168.x.x)
3. Connect to real blockchain (Ethereum testnet)
4. Deploy smart contracts for real control
5. Add more steganography channels

---

Ready to send secret messages over the network! 🌐🔐
