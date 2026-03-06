# 🔧 Network Receiver Troubleshooting

## ❌ Problem: "Receiver in other computer doesn't get the message"

---

## ✅ Solution

### The receiver computer MUST run the standalone receiver script!

The web receiver (`/receiver` page) only shows messages in the Flask app's memory.
For network messages, you need `network_receiver_standalone.py` running.

---

## 📋 Correct Setup

### Computer B (Receiver):

```bash
cd e:\Projects\steganography
python network_receiver_standalone.py
```

**You should see:**
```
📡 Listening on port: 9999
✅ Receiver is ready! Waiting for messages...
```

**Keep this running!**

---

### Computer A (Sender):

```bash
cd e:\Projects\steganography
python blockchain_web_app.py
```

Open: http://localhost:5000

1. Select "Network"
2. Enter Computer B's IP (e.g., 192.168.1.100)
3. Type message
4. Click Send

---

## 🧪 Test Network Connection

Before sending, test if Computer B is reachable:

```bash
python test_network.py 192.168.1.100
```

This will tell you if:
- ✅ Receiver is running
- ✅ Port 9999 is open
- ✅ Network is working

---

## 🔍 Common Issues

### Issue 1: "Connection Refused"
**Cause:** Receiver script is NOT running on Computer B

**Solution:**
```bash
# On Computer B
python network_receiver_standalone.py
```

---

### Issue 2: "Connection Timeout"
**Cause:** Firewall blocking or wrong IP

**Solution:**
```bash
# Check IP on Computer B
ipconfig

# Test connection from Computer A
ping 192.168.1.100
python test_network.py 192.168.1.100
```

---

### Issue 3: "Web receiver doesn't show network messages"
**Cause:** Web receiver only shows local messages

**Solution:** Use `network_receiver_standalone.py` for network messages

---

## 📊 Receiver Types

| Type | Where | What Shows |
|------|-------|------------|
| **Web Receiver** | http://localhost:5000/receiver | Local messages only (127.0.0.1) |
| **Network Receiver** | Terminal script | Network messages from any IP |

---

## ✅ Working Example

### Computer B (192.168.1.100):
```bash
> python network_receiver_standalone.py
📡 Listening on port: 9999
✅ Receiver is ready!
```

### Computer A:
```bash
> python blockchain_web_app.py
> Open http://localhost:5000
> Select "Network"
> Enter: 192.168.1.100
> Send: "Hello"
```

### Computer B Shows:
```
📬 MESSAGE RECEIVED
🔓 Decrypted Message: Hello
```

---

## 🎯 Quick Checklist

On Computer B (Receiver):
- [ ] `network_receiver_standalone.py` is running
- [ ] Shows "Listening on port: 9999"
- [ ] Terminal is still open

On Computer A (Sender):
- [ ] Flask app is running
- [ ] Selected "Network" (not "Same Computer")
- [ ] Entered correct IP address
- [ ] Clicked Send

Network:
- [ ] Both computers on same WiFi/LAN
- [ ] Can ping Computer B from Computer A
- [ ] Firewall allows port 9999

---

## 🚀 Quick Test

**1. Test connection:**
```bash
python test_network.py 192.168.1.100
```

**2. If test passes, send message!**

**3. If test fails, start receiver on Computer B**

---

**Remember: The standalone receiver script MUST be running on the other computer!**
