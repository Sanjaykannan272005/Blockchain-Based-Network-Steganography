# 🎯 Complete Blockchain Steganography System - User Guide

## ✅ What's Working Now

**ONE PAGE** with everything integrated:
- ✅ **GUI Sender** (left side) - No terminal needed
- ✅ **GUI Receiver** (right side) - No terminal needed  
- ✅ **All 10 Features** - Select any combination
- ✅ **Real-time messaging** - Messages appear instantly
- ✅ **Feature details** - See exactly what each feature does

---

## 🚀 How to Use

### 1. Start the Application

```bash
cd e:\Projects\steganography
python blockchain_web_app.py
```

Visit: **http://localhost:5000/complete-system**

---

### 2. Start the Receiver (Right Side)

1. Click **"Start Listening"** button (top-right corner)
2. Status changes to green "Listening..."
3. Receiver polls for messages every 2 seconds
4. Messages appear automatically when received

---

### 3. Select Features (Left Side)

Check any combination of the 10 features:

- ☑️ **1. Control Rules** - Time-based access control
- ☑️ **2. Trigger Events** - Blockchain event activation
- ☑️ **3. Blockchain Keys** - Auto key derivation (default ON)
- ☑️ **4. Authentication** - Digital signatures
- ☑️ **5. Reputation System** - Trust scoring
- ☑️ **6. Forensic Records** - Tamper-proof records
- ☑️ **7. Multi-Chain Distribution** - Distributed storage
- ☑️ **8. Dead Drop Coordinates** - Timed coordination
- ☑️ **9. Key Rotation** - Auto key changes
- ☑️ **10. Protocol Selection** - Adaptive selection

**You can select ALL 10 features at once!**

---

### 4. Send Message (Left Side)

1. Enter sender address (default provided)
2. Type your secret message
3. Click **"🚀 Encrypt & Send with Selected Features"**
4. See results:
   - ✅ Success confirmation
   - Number of features applied
   - Encrypted message length
   - Details of each feature applied

---

### 5. Receive Message (Right Side)

**Automatic (Recommended):**
- Messages appear automatically in "Received Messages" section
- Shows sender, message, timestamp, and features used

**Manual Decrypt:**
- Paste encrypted message
- Click "Decrypt Message"
- View original message

---

## 🎨 How It Works

### Sender Flow
```
1. User selects features (1-10)
2. User types message
3. Click Send
4. System applies ALL selected features:
   - Feature 1: Checks time window
   - Feature 2: Creates trigger event
   - Feature 3: Derives blockchain key
   - Feature 4: Authenticates sender
   - Feature 5: Updates reputation score
   - Feature 6: Creates forensic record
   - Feature 7: Distributes across chains
   - Feature 8: Creates dead drop
   - Feature 9: Schedules key rotation
   - Feature 10: Selects optimal protocol
5. Message encrypted with AES-256
6. Stored in receiver queue
7. Results displayed
```

### Receiver Flow
```
1. User clicks "Start Listening"
2. Receiver polls every 2 seconds
3. Checks message queue
4. Displays new messages automatically
5. Shows sender, message, features used
```

---

## 💡 Example Usage

### Example 1: Maximum Security (All 10 Features)

1. **Select ALL 10 checkboxes**
2. **Message:** "Attack at dawn"
3. **Click Send**
4. **Result:**
   ```
   ✅ Message Sent Successfully!
   Features Applied: 10 of 10
   
   Feature Details:
   ✓ Control Rules: ✅ Access Allowed
   ✓ Trigger Event Created
   ✓ Blockchain Key: Block #15
   ✓ Authentication: Verified
   ✓ Reputation Score: 105
   ✓ Forensic Record: Block #16
   ✓ Multi-Chain: 3 chains
   ✓ Dead Drop: Created
   ✓ Key Rotation: Scheduled
   ✓ Protocol: TTL
   ```

### Example 2: Basic Encryption (Feature 3 Only)

1. **Select only Feature 3** (Blockchain Keys)
2. **Message:** "Hello World"
3. **Click Send**
4. **Result:**
   ```
   ✅ Message Sent Successfully!
   Features Applied: 1 of 10
   
   Feature Details:
   ✓ Blockchain Key: Block #17
   ```

### Example 3: Authentication + Forensics (Features 4 & 6)

1. **Select Features 4 and 6**
2. **Message:** "Confidential report"
3. **Click Send**
4. **Result:**
   ```
   ✅ Message Sent Successfully!
   Features Applied: 2 of 10
   
   Feature Details:
   ✓ Authentication: Verified
   ✓ Forensic Record: Block #18
   ```

---

## 🔍 What Each Feature Does

### Feature 1: Control Rules
- Checks if current time is within allowed window
- Verifies packet type and encoding method
- Returns: ✅ Access Allowed or ❌ Access Denied

### Feature 2: Trigger Events
- Creates blockchain event with keyword
- Stores trigger in blockchain
- Can activate covert channels

### Feature 3: Blockchain Keys
- Derives encryption key from latest blockchain block
- Uses block hash + index + timestamp
- Key valid for 15 minutes

### Feature 4: Authentication
- Creates digital signature for sender
- Stores authentication record on blockchain
- Provides non-repudiation

### Feature 5: Reputation System
- Tracks sender reputation score (0-100)
- Increases score for clean communications
- Decreases score for detection attempts

### Feature 6: Forensic Records
- Creates SHA-256 hash of message
- Stores commitment on blockchain
- Provides tamper-proof evidence

### Feature 7: Multi-Chain Distribution
- Splits message into parts
- Distributes across multiple blockchains
- Returns transaction hashes

### Feature 8: Dead Drop Coordinates
- Creates time-based coordination point
- Stores protocol and location hint
- Enables asynchronous communication

### Feature 9: Key Rotation
- Schedules automatic key changes
- Sets rotation time and duration
- Enhances forward secrecy

### Feature 10: Protocol Selection
- Analyzes network conditions
- Selects optimal steganography method
- Chooses: timing, size, ttl, or ports

---

## 🎯 Key Benefits

### 1. Everything in ONE Page
- No switching between windows
- No terminal commands needed
- Sender and receiver side-by-side

### 2. All Features Together
- Select any combination of 10 features
- Apply multiple features to single message
- See exactly what each feature does

### 3. Real-time GUI
- Messages appear automatically
- No manual refresh needed
- Visual status indicators

### 4. Complete Visibility
- See all applied features
- View blockchain records
- Track reputation scores

---

## 🔧 Technical Details

### Message Queue
- Messages stored in Python list
- Accessible via `/api/receiver/check`
- Polled every 2 seconds by receiver

### Feature Application
- All selected features applied sequentially
- Each feature creates blockchain record
- Results returned in JSON response

### Encryption
- AES-256-CBC encryption
- Key derived from blockchain
- Base64 encoding for transport

---

## 🚨 Troubleshooting

### Receiver Not Getting Messages
- ✅ Make sure "Start Listening" is clicked
- ✅ Status should show green "Listening..."
- ✅ Wait 2 seconds for polling

### Features Not Applying
- ✅ Check that checkboxes are checked
- ✅ Look for green border around selected features
- ✅ View "Applied Features Details" at bottom

### Decryption Fails
- ✅ Ensure same blockchain key is used
- ✅ Check message wasn't corrupted
- ✅ Verify encryption/decryption timing

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Complete System Page                    │
├──────────────────────────┬──────────────────────────────┤
│     SENDER (Left)        │     RECEIVER (Right)         │
│                          │                              │
│  ☑ Feature 1             │  [Start Listening]           │
│  ☑ Feature 2             │                              │
│  ☑ Feature 3             │  📨 Received Messages:       │
│  ☑ Feature 4             │  ┌────────────────────────┐  │
│  ☑ Feature 5             │  │ Message 1              │  │
│  ☑ Feature 6             │  │ From: 0x627...         │  │
│  ☑ Feature 7             │  │ Message: Hello         │  │
│  ☑ Feature 8             │  │ Features: 10 of 10     │  │
│  ☑ Feature 9             │  └────────────────────────┘  │
│  ☑ Feature 10            │                              │
│                          │  Manual Decrypt:             │
│  [Message Input]         │  [Encrypted Input]           │
│  [🚀 Send]               │  [Decrypt]                   │
│                          │                              │
│  ✅ Results              │                              │
└──────────────────────────┴──────────────────────────────┘
│              Applied Features Details                    │
│  ✓ Control  ✓ Triggers  ✓ Keys  ✓ Auth  ✓ Reputation   │
└─────────────────────────────────────────────────────────┘
```

---

## 🎓 Next Steps

1. **Test with 1 feature** - Start simple
2. **Test with all 10 features** - Maximum security
3. **Try different combinations** - Find optimal setup
4. **View blockchain records** - Check `/api/blockchain/status`
5. **Explore individual features** - Visit feature pages

---

## ✨ Summary

You now have a **complete, unified system** where:
- ✅ Sender and receiver work in GUI (no terminal)
- ✅ All 10 features can be selected together
- ✅ Everything happens on ONE page
- ✅ Messages appear in real-time
- ✅ Full visibility of all features applied

**Just run `python blockchain_web_app.py` and visit `/complete-system`!**
