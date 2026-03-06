# 🚀 NETWORK STEGANOGRAPHY + BLOCKCHAIN

## 🎯 Correct Architecture

### How It Works:

```
SENDER                    NETWORK                    RECEIVER
------                    -------                    --------
1. Encrypt message   →    2. Send encrypted     →   4. Receive encrypted
   with AES key              message over TCP          message

3. Store AES key     →    BLOCKCHAIN            →   5. Get AES key from
   on Ethereum                                        blockchain

                                                  6. Decrypt message
```

---

## 📊 Data Flow:

### Step 1: Sender Side
```
Message: "Secret military operation"
    ↓
Generate AES-256 key
    ↓
Encrypt message with key
    ↓
├─→ Encrypted message → Network (TCP)
└─→ AES key → Blockchain (Ethereum)
```

### Step 2: Receiver Side
```
Receive encrypted message from network
    ↓
Get TX hash
    ↓
Retrieve AES key from blockchain
    ↓
Decrypt message
    ↓
Original message: "Secret military operation"
```

---

## 🚀 Quick Start:

### Terminal 1 - Start Receiver:
```bash
python network_receiver_blockchain.py
```
Or double-click: `start_blockchain_receiver.bat`

### Terminal 2 - Send Message:
```bash
python network_sender_blockchain.py
```
Or double-click: `start_blockchain_sender.bat`

---

## 💡 Example Session:

### Sender:
```
Enter secret message: Attack at dawn

Encryption Key: a1b2c3d4e5f6...
Encrypted Message: U2FsdGVkX1...
Message Hash: bb3fa736...

Storing key on blockchain...
TX Hash: 0x7c61ef3da821a897...
Confirmed in block: 10237568

Sending encrypted message to localhost:9999...
Message sent successfully!

SUMMARY:
- Encrypted message: Sent over network
- Encryption key: Stored on blockchain
- TX Hash: 0x7c61ef3da821a897...
```

### Receiver:
```
Listening on localhost:9999...

Connection from ('127.0.0.1', 54321)
Received encrypted message: U2FsdGVkX1...
TX Hash: 0x7c61ef3da821a897...

Retrieving key from blockchain...
Key retrieved: a1b2c3d4e5f6...

Decrypting message...

============================================================
DECRYPTED MESSAGE
============================================================

Attack at dawn

============================================================
```

---

## 🔐 Security Features:

✅ **Encrypted Network Traffic**
   - Message encrypted with AES-256
   - Only ciphertext travels over network
   - No plaintext exposure

✅ **Blockchain Key Storage**
   - Encryption key stored on Ethereum
   - Immutable and transparent
   - Decentralized key exchange

✅ **Message Integrity**
   - SHA-256 hash verification
   - Detects tampering
   - Ensures authenticity

---

## 🎯 Why This Architecture?

### Traditional Problems:
❌ Sending key with message = insecure  
❌ Pre-shared keys = key distribution problem  
❌ Central key server = single point of failure  

### Blockchain Solution:
✅ Decentralized key storage  
✅ Transparent and verifiable  
✅ Immutable transaction history  
✅ No central authority needed  

---

## 📁 Files:

- `network_sender_blockchain.py` - Sends encrypted message + stores key
- `network_receiver_blockchain.py` - Receives message + retrieves key
- `start_blockchain_sender.bat` - Quick start sender
- `start_blockchain_receiver.bat` - Quick start receiver
- `blockchain_config.json` - Blockchain configuration

---

## 🔧 Configuration:

Edit `network_sender_blockchain.py`:
```python
RECEIVER_HOST = 'localhost'  # Change for remote
RECEIVER_PORT = 9999
RECEIVER_ADDRESS = '0x...'   # Receiver's wallet
```

Edit `network_receiver_blockchain.py`:
```python
HOST = 'localhost'  # 0.0.0.0 for all interfaces
PORT = 9999
```

---

## 🌐 Remote Usage:

### For Internet Communication:

**Receiver (Server):**
```python
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 9999
```

**Sender (Client):**
```python
RECEIVER_HOST = '203.0.113.5'  # Public IP
RECEIVER_PORT = 9999
```

**Firewall:**
- Open port 9999 (or your chosen port)
- Forward port on router if behind NAT

---

## 💰 Blockchain Costs:

- **Per Message:** ~0.001 ETH (~$0.002 on testnet)
- **Your Balance:** 0.05 ETH = ~50 messages
- **Gas Used:** ~24,000 gas per transaction

---

## 🔍 Verify on Etherscan:

Every key storage is visible:
```
https://sepolia.etherscan.io/address/0x7A2C2AF27b1E4afBBaBfcfc6e30Dd411D432AcA4
```

Click any transaction to see:
- Sender/Receiver addresses
- Timestamp
- Gas used
- Input data (contains encrypted key)

---

## 🎯 Advantages:

1. **Network Steganography:**
   - Encrypted message travels over normal network
   - Looks like regular encrypted traffic
   - No image files needed

2. **Blockchain Key Exchange:**
   - Decentralized key distribution
   - No pre-shared secrets needed
   - Transparent and auditable

3. **Security:**
   - AES-256 encryption
   - Blockchain immutability
   - Message integrity verification

---

## 🚨 Important Notes:

⚠️ **Network Traffic:**
- Encrypted message sent over TCP
- Anyone can intercept (but can't decrypt without key)
- Use VPN for additional privacy

⚠️ **Blockchain Visibility:**
- Encryption key stored on public blockchain
- Anyone with TX hash can retrieve key
- Share TX hash securely with receiver only

⚠️ **Test Network:**
- Currently using Sepolia testnet
- Free test ETH
- For production, use mainnet

---

## 📊 Comparison:

| Method | Message | Key | Security |
|--------|---------|-----|----------|
| **Traditional** | Network | Network | ❌ Both exposed |
| **Pre-shared** | Network | Pre-shared | ⚠️ Key distribution problem |
| **This System** | Network | Blockchain | ✅ Decentralized & secure |

---

## 🎉 Ready to Use!

### Step 1: Start receiver
```bash
python network_receiver_blockchain.py
```

### Step 2: Send message
```bash
python network_sender_blockchain.py
```

### Step 3: Watch the magic!
- Message encrypted and sent over network
- Key stored on blockchain
- Receiver decrypts automatically

---

**Network Steganography + Blockchain = Secure Communication!** 🚀🔐
