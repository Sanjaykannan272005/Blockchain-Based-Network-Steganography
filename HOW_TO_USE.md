# HOW TO USE - STEP BY STEP

## ⚠️ IMPORTANT: Start Receiver FIRST!

### Step 1: Open Terminal 1 - Start Receiver
```bash
python network_receiver_blockchain.py
```

You should see:
```
============================================================
NETWORK STEGANOGRAPHY - RECEIVER
============================================================

Listening on localhost:9999...
Waiting for encrypted messages...
```

**Leave this running!**

---

### Step 2: Open Terminal 2 - Send Message
```bash
python network_sender_blockchain.py
```

Enter your message when prompted.

---

## ✅ Expected Output:

### Terminal 1 (Receiver):
```
Connection from ('127.0.0.1', 54321)
Received encrypted message: FYt+Zx4XvxyUfdD0...
TX Hash: 3218c6b9c410e902...

Retrieving key from blockchain...
Key retrieved: bc528783ecd1c3b9...

Decrypting message...

============================================================
DECRYPTED MESSAGE
============================================================

hi

============================================================
```

### Terminal 2 (Sender):
```
Enter secret message: hi

Original Message: hi
Encryption Key: bc528783ecd1c3b9...
Encrypted Message: FYt+Zx4XvxyUfdD0...

Storing key on blockchain...
TX Hash: 3218c6b9c410e902...
Confirmed in block: 10237626

Sending encrypted message to localhost:9999...
Message sent successfully!
```

---

## 🚨 Troubleshooting:

### "Connection refused" error?
**Solution:** Start receiver first (Terminal 1)

### Receiver not showing message?
**Solution:** 
1. Stop receiver (Ctrl+C)
2. Start receiver again
3. Send message again

### Port already in use?
**Solution:**
1. Close other receiver instances
2. Or change PORT in both files

---

## 🎯 Quick Test:

**Terminal 1:**
```bash
python network_receiver_blockchain.py
```

**Terminal 2:**
```bash
python network_sender_blockchain.py
```
Type: `hello world`

**Result:** Terminal 1 shows "hello world" decrypted!

---

**Remember: Receiver must be running BEFORE sending!** 🚀
