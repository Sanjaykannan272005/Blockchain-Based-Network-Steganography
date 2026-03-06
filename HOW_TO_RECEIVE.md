# 📥 HOW TO RECEIVE MESSAGES

## 🎯 The web interface has a BUILT-IN receiver!

When you start the web interface, it automatically:
1. ✅ Starts listening on port 9999
2. ✅ Receives encrypted messages from network
3. ✅ Retrieves keys from blockchain
4. ✅ Decrypts messages automatically
5. ✅ Displays them in "Received Messages" section

---

## 🚀 Quick Start:

### Start Web Interface:
```bash
python web_network_blockchain.py
```

### Open Browser:
```
http://localhost:5000
```

### That's it! You can now:
- **Send messages** (left side)
- **Receive messages** (right side - auto-updates every 3 seconds)

---

## 💡 Test It Yourself:

1. **Start web interface:**
   ```bash
   python web_network_blockchain.py
   ```

2. **Open browser:** http://localhost:5000

3. **Send message to yourself:**
   - Message: `Hello World`
   - Host: `localhost`
   - Port: `9999`
   - Click "Send Encrypted Message"

4. **Watch the right side:**
   - After ~15-30 seconds (blockchain confirmation)
   - Message appears in "Received Messages"
   - Shows: "📩 Hello World"

---

## 🔄 How It Works:

```
WEB INTERFACE (Single Process)
├── Flask Web Server (port 5000)
│   └── Serves web page
│
├── Background Receiver Thread
│   └── Listens on port 9999
│   └── Receives encrypted messages
│   └── Gets keys from blockchain
│   └── Decrypts automatically
│
└── Web Page
    ├── Send messages (left)
    └── View received (right - auto-refresh)
```

---

## 📊 What You'll See:

### After Sending:
```
Left Side (Send):
✅ Sent!
TX: 3218c6b9c410e902...

Right Side (Received):
📩 Hello World
TX: 3218c6b9c410e902...
Encrypted: FYt+Zx4XvxyUfdD0...
```

---

## 🌐 Two Machines:

### Machine 1 (Receiver):
```bash
python web_network_blockchain.py
```
Open: http://localhost:5000
- Just wait for messages
- They appear automatically in "Received Messages"

### Machine 2 (Sender):
```bash
python web_network_blockchain.py
```
Open: http://localhost:5000
- Enter message
- Host: `<Machine 1 IP address>`
- Port: `9999`
- Click "Send"

Machine 1 will show the decrypted message!

---

## ⚡ Key Points:

✅ **No separate receiver needed** - Built into web interface
✅ **Auto-refresh** - Messages appear automatically every 3 seconds
✅ **Background thread** - Receiver runs in background
✅ **Always listening** - Ready to receive anytime

---

## 🔧 Troubleshooting:

### Messages not appearing?
1. Wait 30 seconds (blockchain confirmation time)
2. Click "Refresh" button
3. Check browser console for errors

### Want to see receiver logs?
Check the terminal where you ran `python web_network_blockchain.py`

---

**The web interface does EVERYTHING automatically!** 🚀

Just start it and use the browser - sending and receiving both work!
