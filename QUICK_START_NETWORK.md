# 🚀 QUICK START - Network Messaging

## 📱 Send Message to Another Computer

---

## ⚡ Super Quick Setup (3 Steps)

### 1️⃣ On Receiver Computer (Computer B)

**Windows:**
```bash
cd e:\Projects\steganography
start_receiver.bat
```

**Linux/Mac:**
```bash
cd /path/to/steganography
chmod +x start_receiver.sh
./start_receiver.sh
```

**Note the IP address shown** (e.g., 192.168.1.100)

---

### 2️⃣ On Sender Computer (Computer A)

```bash
cd e:\Projects\steganography
python blockchain_web_app.py
```

Open: http://localhost:5000/simple-wizard

---

### 3️⃣ Send Message

In the wizard:
1. **STEP 1:** Enter sender address → Next
2. **STEP 2:** Select "Network Receiver" → Enter IP from Step 1 → Next
3. **STEP 3:** Select features → Next
4. **STEP 4:** Type message → Next
5. **STEP 5:** Click "🚀 SEND MESSAGE"

**Done!** Computer B shows the message instantly! ✅

---

## 📋 What You Need

### On Both Computers:
- ✅ Python 3.x installed
- ✅ `pycryptodomex` package
  ```bash
  pip install pycryptodomex
  ```

### Network:
- ✅ Both computers on same network (WiFi/LAN)
- ✅ Firewall allows port 9999 (optional)

---

## 🎯 Example

**Computer B (Home - 192.168.1.100):**
```
> start_receiver.bat

Your IP addresses:
   IPv4 Address: 192.168.1.100

📡 Listening on port: 9999
✅ Receiver is ready! Waiting for messages...
```

**Computer A (Office):**
```
> python blockchain_web_app.py
> Open http://localhost:5000/simple-wizard

STEP 2: Network Receiver
Enter IP: 192.168.1.100
Send message: "Meeting at 3pm"
```

**Computer B Shows:**
```
📬 MESSAGE RECEIVED
From: 0x627306090abaB3A6e1400e9345bC60c78a8BEf57
🔓 Decrypted Message: Meeting at 3pm
✓ Blockchain Key: Block #5
```

---

## 🔧 Troubleshooting

### Can't connect?

**1. Check IP address:**
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

**2. Test connection:**
```bash
ping 192.168.1.100
```

**3. Check firewall:**
```bash
# Windows (as Admin)
netsh advfirewall firewall add rule name="Receiver" dir=in action=allow protocol=TCP localport=9999
```

**4. Verify receiver is running:**
- Should see "Listening on port: 9999"

---

## 📊 Modes Comparison

| Mode | Receiver Location | Setup |
|------|------------------|-------|
| **GUI Receiver** | Same computer | None - automatic |
| **Network Receiver** | Different computer | Run receiver script |

---

## 🎓 Tips

1. **Test locally first:** Use 127.0.0.1 on same computer
2. **Same network:** Easiest with both on same WiFi
3. **Check firewall:** May need to allow port 9999
4. **Keep receiver running:** Must be active to receive
5. **Note the IP:** Write down receiver's IP address

---

## 📁 Files

- `network_receiver_standalone.py` - Receiver script
- `start_receiver.bat` - Windows quick start
- `start_receiver.sh` - Linux/Mac quick start
- `NETWORK_RECEIVER_GUIDE.md` - Detailed guide

---

## ✅ Checklist

**Receiver Computer:**
- [ ] Python installed
- [ ] pycryptodomex installed
- [ ] Receiver script running
- [ ] IP address noted
- [ ] Firewall allows port 9999

**Sender Computer:**
- [ ] Python installed
- [ ] Web app running
- [ ] Wizard opened
- [ ] Receiver IP entered
- [ ] Message sent

---

## 🎉 That's It!

**Receiver Computer:** Run `start_receiver.bat`
**Sender Computer:** Use wizard with receiver's IP
**Result:** Encrypted message delivered! 🔐

---

## 📞 Quick Commands

```bash
# Receiver Computer
cd e:\Projects\steganography
start_receiver.bat

# Sender Computer  
cd e:\Projects\steganography
python blockchain_web_app.py
# Open: http://localhost:5000/simple-wizard
```

**Simple as that!** 🚀
