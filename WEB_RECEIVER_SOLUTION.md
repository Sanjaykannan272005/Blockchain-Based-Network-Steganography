# ✅ WEB RECEIVER SETUP - FINAL SOLUTION

## The Issue
`network_receiver_standalone.py` works, but web interface doesn't show messages.

## Why?
Each computer runs its own Flask app with separate memory.
- Computer A's Flask: Has messages it sent
- Computer B's Flask: Empty (needs network listener)

## ✅ SOLUTION

### Computer B (Receiver):

**Step 1: Close standalone receiver**
```bash
# If network_receiver_standalone.py is running, press Ctrl+C
```

**Step 2: Start Flask with network listener**
```bash
cd e:\Projects\steganography
python blockchain_web_app.py
```

**You MUST see this:**
```
============================================================
📡 NETWORK RECEIVER ACTIVE
Port: 9999
Status: Listening for incoming messages
============================================================

Visit: http://localhost:5000
```

**Step 3: Open web receiver**
```
http://localhost:5000/receiver
```

Click "Start Listening"

---

### Computer A (Sender):

```bash
python blockchain_web_app.py
```

Open: http://localhost:5000
- Select "Network"
- Enter Computer B's IP
- Send message

---

### Computer B Will Show:

**In Terminal:**
```
📨 Incoming connection from 10.71.214.20:50548
✅ Message received and stored!
   From: 0x627306090abaB3A6e1400e9345...
   Message: your message...
   Total messages: 1
```

**In Web Browser (http://localhost:5000/receiver):**
```
📨 Message 1
your message
From: 0x627306090abaB3A6e1400e9345...
Time: 2024-12-20 15:30:00
```

---

## 🔧 Troubleshooting

### "Port 9999 already in use"
**Cause:** `network_receiver_standalone.py` is still running

**Solution:**
```bash
# Find and close it
# Then restart Flask
python blockchain_web_app.py
```

### "No messages in web interface"
**Check:**
1. ✅ Flask terminal shows "NETWORK RECEIVER ACTIVE"
2. ✅ Flask terminal shows "Message received and stored!"
3. ✅ Web page shows "Start Listening" was clicked
4. ✅ Wait 2 seconds for auto-refresh

### "Terminal shows message but web doesn't"
**Solution:** Refresh the web page or click "Start Listening" again

---

## 📊 What Should Happen

| Step | Computer B Terminal | Computer B Web |
|------|---------------------|----------------|
| 1. Start Flask | "NETWORK RECEIVER ACTIVE" | - |
| 2. Open /receiver | - | "No messages yet" |
| 3. Click "Start Listening" | - | "Listening..." |
| 4. Computer A sends | "Message received!" | - |
| 5. Wait 2 seconds | - | Message appears! ✅ |

---

## ✅ Quick Test

**Computer B:**
```bash
python blockchain_web_app.py
# See "NETWORK RECEIVER ACTIVE"? ✅
# Open: http://localhost:5000/receiver
# Click "Start Listening"
```

**Computer A:**
```bash
# Open: http://localhost:5000
# Network → Computer B IP → Send
```

**Computer B Terminal:**
```
📨 Incoming connection...
✅ Message received!
```

**Computer B Web:**
```
(2 seconds later)
📨 Message appears! ✅
```

---

## 🎯 Key Points

1. **Only ONE program on port 9999**
   - Either Flask OR standalone receiver
   - NOT both!

2. **Flask must show "NETWORK RECEIVER ACTIVE"**
   - If not, network listener didn't start
   - Restart Flask

3. **Web receiver auto-refreshes every 2 seconds**
   - Be patient
   - Messages appear automatically

4. **Each Flask instance has its own memory**
   - Computer A's Flask ≠ Computer B's Flask
   - Network listener fills Computer B's memory

---

**Restart Flask on Computer B and watch for "NETWORK RECEIVER ACTIVE"!**
