# 🚀 Quick Start & Reference Guide

---

## ⚡ 60-Second Overview

**What is this?**
A military-grade secure communication system that:
1. **Encrypts** messages using AES-256 
2. **Hides** them in images using LSB steganography (invisible)
3. **Controls** access via blockchain smart contracts
4. **Transmits** over network securely
5. **Verifies** sender/receiver authenticity

**Key Innovation**: Uses blockchain for access control, not for storing messages. This means:
- ✅ Messages are private (not on public blockchain)
- ✅ Blockchain proves who sent/received
- ✅ Tamper-proof audit trail
- ✅ Decentralized key management

---

## 🛠️ Installation (5 Minutes)

### **Step 1: Clone/Download**
```bash
cd e:\Projects\steganography
```

### **Step 2: Install Python Dependencies**
```bash
pip install -r requirements.txt
```

This installs:
- `Flask` - Web server
- `Pillow` - Image processing
- `pycryptodome` - Encryption
- `web3.py` - Blockchain interaction
- `numpy` - Data processing

### **Step 3: Verify Blockchain Config**
```bash
cat blockchain_config.json
```

Should show:
```json
{
  "network": "sepolia",
  "rpc_url": "https://sepolia.infura.io/...",
  "chain_id": 11155111
}
```

---

## 📱 Three Ways to Use

### **Option 1: Web Interface (Easiest)**

```bash
python app.py
# Open: http://localhost:5000
```

**What you can do:**
- Upload image
- Enter message & password
- Click "Hide Data"
- Download stego image
- Extract messages
- Analyze capacity

**Best for**: First-time users, GUI lovers

---

### **Option 2: Blockchain Web App**

```bash
python blockchain_web_app.py
# Open: http://localhost:5000/dashboard
```

**What you can do:**
- Send messages with blockchain features
- Verify transactions on Etherscan
- Check reputation scores
- Setup smart contracts
- View forensic records

**Best for**: Advanced users, full features

---

### **Option 3: Command Line (CLI)**

```bash
# Hide message
python cli.py hide cover.png output.png \
  -d "Secret message" \
  -p "MyPassword123"

# Extract message
python cli.py extract output.png \
  -p "MyPassword123"

# Check capacity
python cli.py capacity cover.png
```

**Best for**: Scripting, automation, headless servers

---

## 🎯 Common Tasks

### **Task 1: Share Secret Message with Colleague**

```
Step 1: Find a nice image (landscape.jpg)
Step 2: Start Flask app: python app.py
Step 3: Go to http://localhost:5000
Step 4: Click "Hide Data" tab
Step 5: Upload landscape.jpg
Step 6: Enter message: "Project delayed 2 weeks"
Step 7: Set password: "CompanySecret2024"
Step 8: Click "Hide Data"
Step 9: Download stego_image.png
Step 10: Send stego_image.png via email
Step 11: Colleague opens in browser
Step 12: Click "Extract Data"
Step 13: Upload stego_image.png
Step 14: Enter password: "CompanySecret2024"
Step 15: See message: "Project delayed 2 weeks"
```

### **Task 2: Send Message Over Network (Live)**

```bash
# Terminal 1 - Receiver
python network_receiver_blockchain.py

# Terminal 2 - Sender
python network_sender_blockchain.py \
  --host 127.0.0.1 \
  --port 9999 \
  --message "Secret Intel: Attack at Dawn" \
  --receiver 0x7A2C2AF27b1E4afBBaBfcfc6e30Dd411D432AcA4

# Results:
# Receiver terminal: "NEW MESSAGE: Secret Intel: Attack at Dawn"
# TX hash on Ethereum Sepolia: 0xabc123def456...
# Etherscan: https://sepolia.etherscan.io/tx/0xabc123def456...
```

### **Task 3: Use All 10 Blockchain Features**

```bash
python blockchain_web_app.py
# Visit: http://localhost:5000/complete-system

Sender side (Left):
1. ☑ Select Feature 1: Control Rules
2. ☑ Select Feature 2: Trigger Events
3. ☑ Select Feature 3: Blockchain Keys
4. ☑ Select Feature 4: Authentication
5. ☑ Select Feature 5: Reputation System
6. ☑ Select Feature 6: Forensic Records
7. ☑ Select Feature 7: Multi-Chain
8. ☑ Select Feature 8: Dead Drop
9. ☑ Select Feature 9: Key Rotation
10. ☑ Select Feature 10: Protocol Adapt
11. Type message: "TOP SECRET"
12. Click "Encrypt & Send with All Features"

Receiver side (Right):
1. Click "Start Listening"
2. Message appears automatically
3. Shows which features were used
4. Displays blockchain verification
5. View on Etherscan: https://sepolia.etherscan.io/...
```

---

## 🔐 Security Checklist

- [ ] Use strong passwords (12+ chars, numbers, symbols)
- [ ] Use lossless formats (PNG best, avoid JPEG)
- [ ] Test extraction before sending
- [ ] Verify blockchain transactions (check Etherscan)
- [ ] Use different passwords per message
- [ ] Don't store private keys in files (use hardware wallet)
- [ ] Verify receiver address before sending
- [ ] Keep blockchain_config.json secure

---

## 📊 Size Recommendations

| Image | Max Message | Best For |
|-------|-------------|----------|
| 500×500 | ~70 KB | Short messages |
| 1000×1000 | ~280 KB | Documents |
| 2000×2000 | ~1.1 MB | Large files |
| 4000×4000 | ~4.4 MB | Archives |

**Tip**: If message is too big:
```bash
python cli.py capacity image.png
# Shows exact capacity in bytes
```

---

## 🐛 Troubleshooting

### **Problem: "Image too small"**
```
Solution: Use larger image
- 100x100 = 3.7 KB (too small)
- 500x500 = 93 KB (good)
- Add black border to image to increase size
```

### **Problem: "Wrong password"**
```
Solution:
- Password is case-sensitive
- Check for spaces before/after
- Exact password must match
- Passwords don't match? Start over
```

### **Problem: "Blockchain connection failed"**
```
Solution:
- Check internet connection
- Verify API key in blockchain_config.json
- Try test: python test_providers.py
- Use TestNet (free testnet available)
```

### **Problem: "Cannot extract message"**
```
Solution:
1. Delete from outputs/ folder
2. Re-extract from original stego image
3. Verify password is correct
4. Check image wasn't corrupted
5. Try: python test_complete.py
```

### **Problem: "Flask won't start"**
```
Solution:
# Check port 5000 is free
netstat -ano | findstr :5000

# If occupied, kill process or use different port
python app.py --port 5001
# Then visit: http://localhost:5001
```

---

## 🔗 Blockchain Explorer

**View Transactions Live**:
- Network: Sepolia Testnet
- Explorer: https://sepolia.etherscan.io
- Your address: 0x7A2C2AF27b1E4afBBaBfcfc6e30Dd411D432AcA4

**To see your transactions:**
1. Get TX hash from app output
2. Go to: https://sepolia.etherscan.io/tx/{TX_HASH}
3. See: Block, timestamp, gas used, function called
4. Verify: Message was sent at this exact time

---

## 💰 Get Test ETH (Free)

Since Sepolia is testnet, you need free test ETH:

```bash
# Sepolia Faucet (Free ETH)
https://sepoliafaucet.com

# Steps:
1. Go to website
2. Paste address: 0x7A2C2AF27b1E4afBBaBfcfc6e30Dd411D432AcA4
3. Click "Send Test ETH"
4. Wait 30 seconds
5. Check balance: python check_balance.py
```

---

## 📁 File Organization

```
YOUR PROJECT
├── app.py                        ← Start here (web UI)
├── blockchain_web_app.py         ← Advanced features
├── network_receiver.py           ← Network listening
├── network_sender.py             ← Network sending
├── cli.py                        ← Command line tool
├── steganography.py              ← Core LSB engine
├── advanced_blockchain_stego.py  ← 10 features
├── blockchain_config.json        ← Settings
├── requirements.txt              ← Dependencies
├── templates/                    ← HTML UI files
├── uploads/                      ← User uploads
├── outputs/                      ← Generated stego images
└── __pycache__/                  ← Python cache (ignore)
```

---

## 🎓 Learning Path

### **Beginner (30 mins)**
```
1. Read: README.md
2. Run: python app.py
3. Upload image, hide message
4. Extract and verify
5. Check capacity
```

### **Intermediate (1 hour)**
```
1. Read: COMPLETE_SYSTEM_GUIDE.md
2. Run: python blockchain_web_app.py
3. Try sending a message
4. Check blockchain transaction
5. View on Etherscan
```

### **Advanced (2+ hours)**
```
1. Read: PROJECT_ANALYSIS_DETAILED.md
2. Read: BLOCKCHAIN_EXPLANATION.md
3. Try all 10 features
4. Study: AdvancedSteganographyController.sol
5. Run: test_complete.py
```

### **Expert (Full day)**
```
1. Deploy smart contracts locally
2. Run: network_receiver_blockchain.py
3. Send messages live
4. Test multi-chain distribution
5. Modify features in code
6. Create custom applications
```

---

## 🎬 Demo Mode

```bash
# Run simple demo
python simple_demo.py

# What it does:
1. Creates test image
2. Hides message: "Hello World"
3. Password: "demo123"
4. Shows capacity analysis
5. Extracts and verifies
6. Takes 30 seconds
```

---

## 📞 Quick Commands Reference

```bash
# Start web interface
python app.py

# Start blockchain app
python blockchain_web_app.py

# Start network receiver
python network_receiver_blockchain.py

# Test blockchain connection
python test_providers.py

# Check wallet balance
python check_balance.py

# Clean up files
python clean.py

# Run all tests
python test_complete.py

# Extract from any image
python cli.py extract image.png -p "password"

# Hide in any image
python cli.py hide cover.png output.png -d "message" -p "pass"

# Check capacity
python cli.py capacity image.png
```

---

## 🌟 Pro Tips

1. **Largest capacity**: Use 4000×4000 PNG (6 MB capacity)
2. **Fastest extraction**: Use CLI instead of web UI
3. **Most secure**: Enable all 10 blockchain features
4. **Verify messages**: Always check blockchain TX
5. **Different passwords**: Use unique password per message
6. **Backup images**: Keep originals, encrypted versions
7. **Share safely**: Email stego images (looks normal)
8. **Auto-cleanup**: Run `python clean.py` after testing

---

## 📚 Documentation Files

| File | Purpose | Read Time |
|------|---------|-----------|
| README.md | Overview & setup | 10 min |
| COMPLETE_SYSTEM_GUIDE.md | User guide | 15 min |
| PROJECT_ANALYSIS_DETAILED.md | Technical deep dive | 30 min |
| BLOCKCHAIN_EXPLANATION.md | How blockchain works | 20 min |
| DATAFLOW_AND_FEATURES.md | Data flow + features | 25 min |
| SECURITY_ANALYSIS.md | Security details | 15 min |

---

## ✅ Success Criteria

You've successfully set up when:
- [ ] `python app.py` runs without errors
- [ ] Web interface opens in browser
- [ ] Can hide message in image
- [ ] Can extract message from stego image
- [ ] Extracted message matches original
- [ ] `python test_complete.py` passes
- [ ] Blockchain transactions appear on Etherscan
- [ ] CLI commands work correctly

---

## 🚀 Next Steps

1. **Play around**: Try different image sizes & messages
2. **Test blockchain**: Send real messages end-to-end
3. **Study code**: Understand LSB algorithm
4. **Modify**: Add your own features
5. **Deploy**: Use in real scenarios

---

## 📖 Example Walkthrough

### **Send a Classified Document Covertly**

```bash
# Step 1: Create presentation
# Save as: presentation.pdf (5 MB)

# Step 2: Compress to fit
# 4000x4000 PNG has ~4.4 MB capacity
# PDF is small enough

# Step 3: Create cover image
# Download: high-quality 4000x4000 landscape photo

# Step 4: Hide document
python cli.py hide landscape.png stego.png \
  -d "$(cat presentation.pdf)" \
  -p "ClassifiedAces2024Secret!"

# Step 5: Send image
# Email stego.png to recipient
# Looks like normal landscape photo
# No one suspects anything

# Step 6: Recipient extracts
python cli.py extract stego.png \
  -p "ClassifiedAces2024Secret!" \
  > received_presentation.pdf

# Step 7: View document
# open received_presentation.pdf

# Result: Classified doc successfully transmitted
# - Invisible to mail systems
# - Undetectable without password
# - Military-grade encryption
# - Timestamped on blockchain
```

---

## 💡 Key Concepts

**Steganography**: Art of hiding data in plain sight
- **LSB**: Modify Least Significant Bits of pixels
- **Imperceptible**: Changes invisible to human eye
- **Deniable**: Looks like normal image

**Encryption**: Make data unreadable without key
- **AES-256**: Military-grade encryption
- **256-bit key**: ~2^256 combinations (unbreakable)
- **CBC mode**: Each block depends on previous

**Blockchain**: Decentralized ledger
- **Smart Contracts**: Code that enforces rules
- **Transactions**: Immutable record of events
- **Verification**: Network consensus confirms validity

---

## 🎯 Final Checklist

Before using in production:
- [ ] Test everything locally first
- [ ] Use hardware wallet (not file storage)
- [ ] Enable all 10 features
- [ ] Verify blockchain transactions
- [ ] Use strong passwords (16+ chars)
- [ ] Keep backups of original images
- [ ] Document all procedures
- [ ] Train users properly
- [ ] Regular security audits
- [ ] Monitor blockchain activity

---

**You're now ready to use the Blockchain Network Steganography System! 🎉**

*Happy and secure communicating!*

---

*Quick Start Guide - February 12, 2026*
