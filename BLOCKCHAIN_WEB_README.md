# 🔗 Blockchain Steganography Web Interface

Complete, interactive web application for blockchain-assisted network steganography with all 10 features and step-by-step blockchain setup.

---

## 🚀 Quick Start

### Installation

```bash
# Clone or navigate to project directory
cd e:\Projects\steganography

# Install dependencies
pip install -r requirements_web.txt

# Run the application
python blockchain_web_app.py
```

**Visit:** http://localhost:5000

---

## 📦 What's Included

### ✅ Complete Web Application
- **Flask-based** web server
- **Responsive Bootstrap UI** with dark theme
- **Real-time blockchain** simulation
- **10 interactive features**
- **Secure encryption** (AES-256-CBC)
- **REST API** endpoints

### ✅ Setup Wizard
4-step blockchain configuration:
1. Network Setup (Ethereum, Polygon, Arbitrum, etc.)
2. Account Setup (Wallet configuration)
3. Steganography Configuration
4. Verification & Testing

### ✅ 10 Features Dashboard
All features accessible from main dashboard:
1. 📋 Smart Contract Control
2. 🕳️ Trigger Events
3. 🔑 Blockchain-Derived Keys
4. 🔐 Digital Authentication
5. 📊 Reputation System
6. 🕵️ Forensic Records
7. ⛓️ Multi-Chain Distribution
8. 📍 Dead Drop Coordinates
9. 🔄 Key Rotation
10. 🎭 Protocol Selection

### ✅ Messaging System
- Encrypt messages with blockchain-derived keys
- Decrypt received messages
- View forensic hashes
- Track reputation scores

### ✅ API Endpoints
- Configuration APIs
- Feature-specific APIs
- Messaging APIs
- Blockchain status API

---

## 📂 File Structure

```
blockchain_web_app.py              # Main Flask application
requirements_web.txt               # Python dependencies
WEB_INTERFACE_GUIDE.md            # Detailed guide

templates/
├── dashboard.html                 # Main dashboard (all features)
├── setup.html                     # 4-step setup wizard
├── messaging.html                 # Send/receive messages
└── features/
    ├── feature_1_control.html     # Smart Contract Control
    ├── feature_2_triggers.html    # Trigger Events
    ├── feature_3_keys.html        # Blockchain Keys
    ├── feature_4_auth.html        # Authentication
    └── feature_5_10_preview.html  # Other features (backend ready)
```

---

## 🎯 Feature Pages

### Feature 1: Smart Contract Control
**URL:** `/feature/1-control`
- Set access control rules
- Define time windows
- Choose packet types
- Specify encoding methods
- Real-time access verification

### Feature 2: Trigger Events
**URL:** `/feature/2-triggers`
- Publish trigger keywords to blockchain
- Monitor active triggers
- Common examples (ALGORITHM_V2, EMERGENCY_STOP)
- Automatic agent activation

### Feature 3: Blockchain-Derived Keys
**URL:** `/feature/3-keys`
- Derive encryption keys from blockchain blocks
- Understand key derivation process
- View current encryption key
- Derive keys from specific blocks
- See automatic key rotation

### Feature 4: Digital Authentication
**URL:** `/feature/4-auth`
- Authenticate users via blockchain
- Create digital signatures
- Verify message authenticity
- Non-repudiation (can't deny sending)
- Court-admissible proof

### Features 5-10: Backend Ready
**URL:** `/feature/5-10-preview`
- All features are functional in backend
- Frontend UI coming soon
- Can use via REST API endpoints
- Use from Python code directly

---

## ⚙️ Setup Wizard Walkthrough

### Step 1: Network Configuration

**For Local Testing (Ganache):**
```
Network Name: ethereum
RPC URL: http://127.0.0.1:7545
Chain ID: 5777
Gas Limit: 6721975
Gas Price: 20000000000
```

**For Polygon Mumbai Testnet:**
```
Network Name: polygon
RPC URL: https://rpc-mumbai.maticvigil.com
Chain ID: 80001
Gas Limit: 6721975
Gas Price: 100000000000
```

**For Arbitrum Goerli:**
```
Network Name: arbitrum
RPC URL: https://goerli-rollup.arbitrum.io/rpc
Chain ID: 421613
Gas Limit: 6721975
Gas Price: 100000000000
```

### Step 2: Account Configuration

**Test Account (DO NOT USE WITH REAL FUNDS):**
```
Account Name: default
Address: 0x627306090abaB3A6e1400e9345bC60c78a8BEf57
Private Key: 0xc87509a1c067bbde78beb793e6fa76530b6382a4c3a632f29a9f6d1c0e92235ee
```

### Step 3: Steganography Configuration

```
Password: YourStrongPassword123!
Key Rotation Interval: 600 seconds (10 minutes)
Reputation Threshold: 50 (out of 100)
Max Message Size: 1000 bytes
Default Method: ttl (TTL Channel)
```

### Step 4: Verification

System will test:
- ✓ Blockchain connection
- ✓ Account accessibility
- ✓ Encryption functionality

---

## 💬 Messaging Interface

### Send Message
1. Enter your wallet address: `0x627306090abaB3A6e1400e9345bC60c78a8BEf57`
2. Type message: `"Secret message"`
3. Click **Encrypt & Send**
4. Receive:
   - Encrypted message (base64)
   - Forensic hash (SHA-256)
   - Updated reputation score

### Receive Message
1. Go to "Receive Message" tab
2. Paste encrypted message
3. Click **Decrypt**
4. View original message
5. Copy to clipboard

---

## 🔐 Security Features

### Encryption
- **Algorithm:** AES-256-CBC (military-grade)
- **Key Derivation:** SHA-256
- **Mode:** Cipher Block Chaining
- **Padding:** PKCS7

### Blockchain Integration
- **Immutable Records:** Once on blockchain, can't be changed
- **Distributed Consensus:** Multiple nodes verify transactions
- **Timestamping:** Proof of when something happened
- **Non-Repudiation:** Can't deny sending (digital signatures)

### Key Management
- **Automatic Rotation:** Keys change every 15 seconds
- **Blockchain-Derived:** Both parties independently compute identical keys
- **No Transmission:** Keys never sent over network (no interception risk)
- **Temporary Validity:** Each key only valid for 15 minutes

---

## 🌐 API Endpoints

### Status
```
GET /api/blockchain/status
Returns: {
  total_blocks, 
  chain_valid, 
  latest_block,
  networks,
  accounts
}
```

### Setup
```
POST /api/setup/network
POST /api/setup/account
```

### Features
```
POST /api/feature/1/update           # Update control rules
POST /api/feature/2/create           # Create trigger
POST /api/feature/3/derive           # Derive key
POST /api/feature/4/authenticate     # Authenticate user
POST /api/feature/5/update           # Update reputation
POST /api/feature/6/create           # Create forensic record
POST /api/feature/7/distribute       # Distribute across chains
POST /api/feature/8/create           # Create dead drop
POST /api/feature/9/schedule         # Schedule rotation
POST /api/feature/10/select          # Select protocol
```

### Messaging
```
POST /api/message/send
Request: {sender_address, message}
Response: {encrypted_message, forensic_hash, reputation}

POST /api/message/receive
Request: {encrypted_message}
Response: {message}
```

---

## 🎓 Learning Path

### Beginner
1. **Visit Dashboard:** Understand all 10 features
2. **Run Setup:** Configure a test network
3. **Send Message:** Try encryption/decryption
4. **Read Guide:** Study WEB_INTERFACE_GUIDE.md

### Intermediate
1. **Explore Features 1-4:** Interactive pages
2. **Study API:** Review REST endpoint structure
3. **Understand Blockchain:** How blocks are created
4. **Try Configurations:** Different networks/accounts

### Advanced
1. **Review Source Code:** Study Flask implementation
2. **Extend Features:** Add new functionality
3. **Integrate Code:** Use in own projects
4. **Deploy Network:** Connect to real testnet
5. **Write Smart Contracts:** Deploy real blockchain contracts

---

## 🔧 Troubleshooting

### Port 5000 Already in Use
```bash
python blockchain_web_app.py
# Change in browser to: http://localhost:5001
```

Or edit `blockchain_web_app.py` last line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module Not Found Errors
```bash
pip install -r requirements_web.txt
# Or individual packages:
pip install flask==2.3.0
pip install pycryptodomex==4.16.0
```

### Blockchain Connection Failed
- ✓ Check RPC URL is correct
- ✓ For Ganache: ensure it's running on port 7545
- ✓ For testnet: check network is live
- ✓ Verify network connectivity

### Encryption Fails
- ✓ Ensure same password for encrypt/decrypt
- ✓ Check message isn't corrupted
- ✓ Verify message format (base64)

### Cannot Add Network
- ✓ Verify all fields are filled
- ✓ Check Chain ID is numeric
- ✓ Ensure RPC URL is valid

---

## 📊 Example Workflows

### Workflow 1: Military Operation Authorization

```
1. Setup Blockchain
   - Configure Ethereum network
   - Add general account
   
2. Set Control Rules (Feature 1)
   - Time window: 2:00 AM - 4:00 AM
   - Packet type: TCP
   - Method: TTL channel
   
3. Send Encrypted Order (Messaging)
   - General encrypts: "Attack at 0600 hours"
   - System derives key from blockchain
   - Hides in network traffic
   
4. Verify Authenticity (Feature 4)
   - General's signature proves authorization
   - Blockchain timestamp: 2:37 AM
   - Court-admissible evidence
```

### Workflow 2: Intelligence Agent Communication

```
1. Pre-Deploy Agent (Setup)
   - Configure light client (Ethereum network)
   - Add agent account
   - Pre-load 5 algorithms
   
2. Deploy Agent
   - Agent goes to field (enemy territory)
   - Has agent software + blockchain client
   
3. HQ Sends Intelligence (Feature 3)
   - HQ publishes data
   - Key derived from block #12345
   - Both HQ & agent compute same key
   
4. Algorithm Compromise (Feature 2)
   - Enemy breaks algorithm
   - HQ publishes: "ALGORITHM_V2"
   - Agent detects trigger on blockchain
   - Both switch to V2 within 15 seconds
   - Enemy loses capability
```

### Workflow 3: Whistleblower Protection

```
1. Setup Anonymous (No Setup)
   - Use public API (Infura, Alchemy)
   - No need for full node
   
2. Send Evidence (Messaging)
   - Whistleblower encrypts: "Company illegally dumped waste"
   - Message hidden in normal web traffic
   
3. Prove Authenticity (Feature 6)
   - Journalist verifies with forensic hash
   - Blockchain proves: time, sender, authenticity
   - Whistleblower identity protected
```

---

## 🌟 Key Concepts

### Blockchain as Control Layer (Not Data Storage)
- Don't store secrets ON blockchain (it's public!)
- Use blockchain to CONTROL when to use secrets
- Algorithm + blockchain = unbreakable encryption

### Automatic Key Rotation
- New key every 15 seconds (new blockchain block)
- If 1 key compromised: only 15 seconds exposed
- Sender & receiver automatically synchronized

### Algorithm Flexibility
- Pre-load multiple algorithms (V1-V5)
- Change via blockchain trigger (ALGORITHM_V2)
- No risky communication needed
- Agents automatically switch

### Public + Secret = Security
- **Public:** Blockchain data (everyone sees)
- **Secret:** Derivation algorithm (only authorized parties)
- **Result:** Unbreakable encryption (product of both)

---

## 📝 Configuration File

The system saves configuration to `blockchain_config.json`:

```json
{
  "networks": {
    "ethereum": {
      "url": "http://127.0.0.1:7545",
      "chain_id": 5777,
      "gas_limit": 6721975,
      "gas_price": 20000000000
    }
  },
  "accounts": {
    "default": {
      "address": "0x627306090abaB3A6e1400e9345bC60c78a8BEf57",
      "private_key": "0xc87509a1c067bbde78beb793e6fa76530b6382a4c3a632f29a9f6d1c0e92235ee"
    }
  },
  "steganography": {}
}
```

---

## 🚀 Next Steps

1. **Get Started:** Run the app and visit http://localhost:5000
2. **Complete Setup:** Use the wizard to configure blockchain
3. **Explore Features:** Click each feature to learn how it works
4. **Send Messages:** Test encryption/decryption
5. **Study Code:** Review blockchain_web_app.py
6. **Extend:** Add more features or integrate with your project

---

## 📚 Documentation

- **Web Guide:** See WEB_INTERFACE_GUIDE.md
- **Project Overview:** See COMPLETE_PROJECT_README.md
- **Feature Details:** See GUIDE_EXPLANATION.md
- **Source Code:** See blockchain_steganography.py

---

## 🔒 Security Notice

**This is an educational system for learning blockchain steganography.**

- ⚠️ Do not use with real money
- ⚠️ Do not use with real private keys
- ⚠️ Use testnet only
- ✓ For production, implement proper security
- ✓ For real use, deploy real smart contracts
- ✓ For deployment, use professional audit

---

## 🎯 Features Status

| Feature | Frontend | Backend | API | Status |
|---------|----------|---------|-----|--------|
| 1. Control Rules | ✅ | ✅ | ✅ | Complete |
| 2. Trigger Events | ✅ | ✅ | ✅ | Complete |
| 3. Blockchain Keys | ✅ | ✅ | ✅ | Complete |
| 4. Authentication | ✅ | ✅ | ✅ | Complete |
| 5. Reputation | ⚙️ | ✅ | ✅ | Backend Ready |
| 6. Forensics | ⚙️ | ✅ | ✅ | Backend Ready |
| 7. Multi-Chain | ⚙️ | ✅ | ✅ | Backend Ready |
| 8. Dead Drops | ⚙️ | ✅ | ✅ | Backend Ready |
| 9. Key Rotation | ⚙️ | ✅ | ✅ | Backend Ready |
| 10. Protocols | ⚙️ | ✅ | ✅ | Backend Ready |

---

## 💡 Tips & Tricks

### Using Test Accounts
```bash
# Create new Ganache test account
# Copy address and private key
# Add to setup
```

### Monitoring Blockchain
```bash
# Open Dashboard
# Refresh every 5 seconds
# Watch blocks increment
```

### Testing Messaging
```bash
# Open messaging.html
# Send test message
# Copy encrypted output
# Paste in receive tab
# Decrypt successfully
```

### Debugging
```bash
# Check browser console (F12)
# Check Flask server output
# Verify blockchain_config.json
```

---

## 📞 Support

For issues or questions:
1. Check WEB_INTERFACE_GUIDE.md
2. Review error messages
3. Check browser console (F12)
4. Review Flask output
5. Study source code

---

**Ready to start?** Run `python blockchain_web_app.py` and visit http://localhost:5000! 🚀

