# 🚀 SEPARATE SENDER & RECEIVER - QUICK START

## ✅ Now you have TWO separate web interfaces!

### 📥 RECEIVER (Port 5001)
- Receives messages
- Click "Start Listening" button
- Shows decrypted messages

### 📤 SENDER (Port 5000)
- Sends messages
- Enter receiver IP address
- Sends encrypted message over network

---

## 🎯 How to Use:

### Step 1: Start RECEIVER
```bash
python receiver_web.py
```
Open: **http://localhost:5001**

Click: **"Start Listening"** button

### Step 2: Start SENDER
```bash
python sender_web.py
```
Open: **http://localhost:5000**

Enter:
- Message: `Hello World`
- Receiver IP: `localhost` (or receiver's IP)
- Port: `9999`

Click: **"Send Encrypted Message"**

### Step 3: Check RECEIVER
Go back to receiver page (http://localhost:5001)
- Message appears automatically!
- Shows decrypted message

---

## 💡 Same Machine (Testing):

**Terminal 1:**
```bash
python receiver_web.py
```
Browser 1: http://localhost:5001 → Click "Start Listening"

**Terminal 2:**
```bash
python sender_web.py
```
Browser 2: http://localhost:5000 → Send message to `localhost`

---

## 🌐 Different Machines (Real Usage):

### Machine A (Receiver):
```bash
python receiver_web.py
```
1. Open: http://localhost:5001
2. Click "Start Listening"
3. Note your IP address (e.g., 192.168.1.100)

### Machine B (Sender):
```bash
python sender_web.py
```
1. Open: http://localhost:5000
2. Message: "Secret message"
3. Receiver IP: `192.168.1.100` (Machine A's IP)
4. Port: `9999`
5. Click "Send"

Machine A will receive and decrypt automatically!

---

## 📊 What Happens:

```
SENDER (Port 5000)
  ↓
1. Encrypt message with AES-256
  ↓
2. Store key on blockchain → Ethereum
  ↓
3. Send encrypted message → Network → RECEIVER (Port 9999)
  ↓
RECEIVER (Port 5001)
  ↓
4. Receive encrypted message
  ↓
5. Get key from blockchain
  ↓
6. Decrypt and display message
```

---

## ⚡ Key Features:

### Receiver:
✅ **Start/Stop button** - Control when to listen
✅ **Real-time updates** - Auto-refresh every 2 seconds
✅ **Shows sender IP** - Know who sent the message
✅ **Clear messages** - Clean up received messages

### Sender:
✅ **Enter receiver IP** - Send to any machine
✅ **Blockchain integration** - Key stored automatically
✅ **Balance display** - See remaining ETH
✅ **Transaction link** - View on Etherscan

---

## 🔧 Ports:

- **Sender Web:** Port 5000
- **Receiver Web:** Port 5001
- **Network Listener:** Port 9999

---

## 🚨 Important:

1. **Start receiver FIRST** - Click "Start Listening"
2. **Then send message** - From sender page
3. **Wait ~20 seconds** - Blockchain confirmation time
4. **Message appears** - On receiver page automatically

---

## ✅ Quick Test:

**Terminal 1:**
```bash
python receiver_web.py
```
Open http://localhost:5001 → Click "Start Listening"

**Terminal 2:**
```bash
python sender_web.py
```
Open http://localhost:5000 → Send to `localhost`

**Result:** Message appears on receiver page! 🎉

---

**Two separate interfaces = Better control!** 🚀
