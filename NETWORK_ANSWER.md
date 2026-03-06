# ✅ ANSWER: How to Receive Messages on Another Computer

## Your Question:
**"In simple wizard, network receiver - if I put the IP of the computer and send a message, how to receive it in another computer?"**

---

## 🎯 THE ANSWER

### On the Receiving Computer (Computer B):

**Run this command:**
```bash
cd e:\Projects\steganography
python network_receiver_standalone.py
```

**Or use the quick start:**
```bash
start_receiver.bat
```

**That's it!** The receiver will:
1. Show its IP address
2. Start listening on port 9999
3. Display messages as they arrive
4. Decrypt and show the content

---

## 📋 Complete Step-by-Step

### COMPUTER B (Receiver) - Do This First

**Step 1:** Install dependency
```bash
pip install pycryptodomex
```

**Step 2:** Find your IP address
```bash
ipconfig
```
Note the IPv4 address (e.g., 192.168.1.100)

**Step 3:** Start the receiver
```bash
cd e:\Projects\steganography
python network_receiver_standalone.py
```

Press Enter when asked for port (uses 9999)

**You'll see:**
```
============================================================
🔐 BLOCKCHAIN STEGANOGRAPHY - NETWORK RECEIVER
============================================================
📡 Listening on port: 9999
🔑 Encryption: AES-256-CBC
⏰ Started: 2024-12-20 15:30:00
============================================================

✅ Receiver is ready! Waiting for messages...
```

**Leave this running!** Don't close the terminal.

---

### COMPUTER A (Sender) - Do This Second

**Step 1:** Start web app
```bash
cd e:\Projects\steganography
python blockchain_web_app.py
```

**Step 2:** Open wizard
```
http://localhost:5000/simple-wizard
```

**Step 3:** Follow wizard steps:
1. **STEP 1:** Sender address → Next
2. **STEP 2:** Select "Network Receiver" → Enter Computer B's IP (192.168.1.100) → Next
3. **STEP 3:** Select features → Next
4. **STEP 4:** Type message → Next
5. **STEP 5:** Click "🚀 SEND MESSAGE"

---

### COMPUTER B (Receiver) - See the Result

**The terminal will show:**
```
📨 Incoming connection from: 192.168.1.50:54321

============================================================
📬 MESSAGE RECEIVED
============================================================
From: 0x627306090abaB3A6e1400e9345bC60c78a8BEf57
Time: 2024-12-20 15:35:42
Features Used: 3 of 10

🔓 Decrypted Message:
   Your secret message here

📋 Feature Details:
   ✓ Blockchain Key: Block #5
   ✓ Authentication: Verified
   ✓ Forensic Record: Block #6
============================================================

✅ Waiting for next message...
```

**The message is automatically decrypted and displayed!** ✅

---

## 🎬 Real Example

### Computer B (Home Computer - 192.168.1.100)
```bash
> cd e:\Projects\steganography
> python network_receiver_standalone.py

Enter port to listen on (default 9999): [Press Enter]

📡 Listening on port: 9999
✅ Receiver is ready! Waiting for messages...
```

### Computer A (Office Computer)
```bash
> cd e:\Projects\steganography
> python blockchain_web_app.py
> Open browser: http://localhost:5000/simple-wizard

Wizard Steps:
STEP 1: Sender → 0x627306090abaB3A6e1400e9345bC60c78a8BEf57
STEP 2: Network Receiver → IP: 192.168.1.100
STEP 3: Features → Blockchain Keys, Authentication
STEP 4: Message → "Hello from office"
STEP 5: SEND!
```

### Computer B Shows:
```
📬 MESSAGE RECEIVED
🔓 Decrypted Message: Hello from office
✓ Blockchain Key: Block #5
✓ Authentication: Verified
```

---

## 🔑 Key Points

1. **Receiver must be running FIRST** - Start `network_receiver_standalone.py` before sending
2. **Note the IP address** - Use `ipconfig` to find it
3. **Same network** - Both computers should be on same WiFi/LAN
4. **Port 9999** - Receiver listens on this port
5. **Automatic decryption** - Receiver decrypts and displays message
6. **Keep running** - Receiver can receive multiple messages

---

## 📁 Files You Need

### On Receiver Computer (Computer B):
- `network_receiver_standalone.py` ✅ (I created this)
- `start_receiver.bat` ✅ (Quick start for Windows)
- `start_receiver.sh` ✅ (Quick start for Linux/Mac)

### On Sender Computer (Computer A):
- `blockchain_web_app.py` ✅ (Already exists)
- Web browser to access wizard

---

## 🚨 Troubleshooting

### "Connection refused"
- ✅ Make sure receiver is running on Computer B
- ✅ Check IP address is correct
- ✅ Verify both computers on same network

### "Connection timeout"
- ✅ Ping Computer B: `ping 192.168.1.100`
- ✅ Check firewall settings
- ✅ Ensure port 9999 is not blocked

### Receiver not showing messages
- ✅ Check terminal is still running
- ✅ Look for "Incoming connection" message
- ✅ Verify no errors in terminal

---

## ✅ Summary

**Your Question:** How to receive messages on another computer?

**The Answer:**
1. On Computer B: Run `python network_receiver_standalone.py`
2. Note Computer B's IP address
3. On Computer A: Use wizard, select "Network Receiver", enter IP
4. Send message
5. Computer B's terminal shows the decrypted message automatically!

**Files Created:**
- ✅ `network_receiver_standalone.py` - The receiver script
- ✅ `start_receiver.bat` - Windows quick start
- ✅ `start_receiver.sh` - Linux/Mac quick start
- ✅ `NETWORK_RECEIVER_GUIDE.md` - Detailed guide
- ✅ `QUICK_START_NETWORK.md` - Quick reference

**That's it!** 🎉
