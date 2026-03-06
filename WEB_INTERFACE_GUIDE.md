# 🌐 WEB INTERFACE - QUICK START

## 🚀 Start Web Interface:

```bash
python web_network_blockchain.py
```

Or double-click: `start_web.bat`

Then open: **http://localhost:5000**

---

## ✨ Features:

### 📤 Send Messages:
- Enter message in text area
- Specify receiver host/port
- Click "Send Encrypted Message"
- Message encrypted & sent over network
- Key stored on blockchain automatically

### 📥 Receive Messages:
- Auto-refreshes every 3 seconds
- Shows decrypted messages
- Displays transaction hash
- Shows encrypted preview

### 💰 Wallet Info:
- View wallet address
- Check ETH balance
- Refresh balance button

---

## 💡 How to Use:

### Single Machine (Testing):

1. **Start web interface:**
   ```bash
   python web_network_blockchain.py
   ```

2. **Open browser:**
   ```
   http://localhost:5000
   ```

3. **Send message to yourself:**
   - Message: "Hello World"
   - Host: localhost
   - Port: 9999
   - Click "Send"

4. **Watch it appear in "Received Messages"!**

---

### Two Machines (Real Usage):

**Machine 1 (Receiver):**
```bash
python web_network_blockchain.py
```
Open: http://localhost:5000

**Machine 2 (Sender):**
```bash
python web_network_blockchain.py
```
Open: http://localhost:5000

In sender's browser:
- Message: "Secret message"
- Host: `<Machine 1 IP>`
- Port: 9999
- Click "Send"

Machine 1 will receive and decrypt automatically!

---

## 🎯 Advantages:

✅ **User-Friendly** - No command line needed
✅ **Real-Time** - Auto-refresh received messages
✅ **Visual** - See balance, transactions, messages
✅ **Integrated** - Send & receive in one interface
✅ **Background Receiver** - Always listening

---

## 📊 What You'll See:

### Sending:
```
✅ Sent!
TX: 3218c6b9c410e902...
```

### Receiving:
```
📩 Hello World
TX: 3218c6b9c410e902...
Encrypted: FYt+Zx4XvxyUfdD0...
```

---

## 🔧 Configuration:

Edit `web_network_blockchain.py`:

```python
# Change receiver port
sock.bind(('localhost', 9999))  # Change 9999

# Change web port
app.run(debug=True, port=5000)  # Change 5000
```

---

## 🌐 Remote Access:

To access from other devices:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

Then access: `http://<your-ip>:5000`

---

**Web interface ready!** 🚀

Start: `python web_network_blockchain.py`
Open: http://localhost:5000
