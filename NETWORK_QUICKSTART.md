# 🚀 QUICK START - Real Network Steganography

## What You Need (5 minutes setup)

```bash
# Install required package
python -m pip install scapy pycryptodome
```

That's it! No blockchain setup needed for testing.

---

## 🎯 Send Your First Secret Message (2 minutes)

### **Step 1: Start Receiver (Computer A or Terminal 1)**

```bash
# Run as Administrator/root
python network_receiver.py timing 60
```

You'll see:
```
🔐 BLOCKCHAIN-CONTROLLED NETWORK STEGANOGRAPHY - RECEIVER
📡 Getting decryption key from blockchain...
✅ Key derived from blockchain
🌐 Capturing network packets...
👂 Listening for TIMING channel (duration: 60s)...
   Waiting for packets...
```

### **Step 2: Send Message (Computer B or Terminal 2)**

```bash
# Run as Administrator/root
python network_sender.py 127.0.0.1 "Hello World" timing
```

You'll see:
```
🔐 BLOCKCHAIN-CONTROLLED NETWORK STEGANOGRAPHY - SENDER
📡 Getting encryption key from blockchain...
✅ Key derived from blockchain
🔒 Encrypting message with AES-256...
✅ Message encrypted
🌐 Sending via network steganography...
🚀 Sending via TIMING channel to 127.0.0.1
✅ Sent 704 bits via timing channel
✅ MESSAGE SENT SUCCESSFULLY!
```

### **Step 3: See Result (Receiver Terminal)**

```
✅ Captured 88 packets, extracted 704 bits
✅ Data extracted
🔓 Decrypting message with AES-256...

======================================================================
✅ MESSAGE RECEIVED:
   Hello World
======================================================================
```

---

## 🎉 That's It! You Just Sent a Secret Message Over the Network!

**What happened:**
1. ✅ Message encrypted with blockchain-derived key
2. ✅ Hidden in network packet timing delays
3. ✅ Sent over network (looks like normal ICMP pings)
4. ✅ Receiver captured packets
5. ✅ Extracted hidden data from timing
6. ✅ Decrypted with same blockchain key

---

## 🌐 Send to Another Computer

### **Find Receiver's IP:**

```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

Look for IPv4 address (e.g., 192.168.1.100)

### **Send Message:**

```bash
# On sender computer
python network_sender.py 192.168.1.100 "Secret message" timing
```

### **Receive Message:**

```bash
# On receiver computer
python network_receiver.py timing 60
```

---

## 🎭 Try Different Channels

### **Timing Channel (Default)**
- Hides data in packet delays
- Most covert
- Slower

```bash
# Sender
python network_sender.py 127.0.0.1 "Secret" timing

# Receiver
python network_receiver.py timing
```

### **Size Channel**
- Hides data in packet sizes
- Balanced
- Medium speed

```bash
# Sender
python network_sender.py 127.0.0.1 "Secret" size

# Receiver
python network_receiver.py size
```

### **TTL Channel**
- Hides data in TTL field
- Very stealthy
- Fast

```bash
# Sender
python network_sender.py 127.0.0.1 "Secret" ttl

# Receiver
python network_receiver.py ttl
```

---

## 🔑 How Blockchain Controls It

### **Automatic Key Generation**
```
Both sender & receiver:
↓
Query blockchain (simulated locally)
↓
Get current block data
↓
Derive SAME encryption key
↓
No key exchange needed!
```

### **Time-Based Keys**
- Keys change every minute
- Both sides automatically sync
- Old keys expire
- No manual key management

### **In Production**
- Connect to real blockchain (Ethereum, Polygon)
- Smart contracts control access
- On-chain authentication
- Forensic records

---

## 🚨 Troubleshooting

### **"Permission denied"**
```bash
# Windows: Run terminal as Administrator
# Right-click PowerShell → Run as Administrator

# Linux/Mac: Use sudo
sudo python network_sender.py ...
```

### **"No data extracted"**
- Make sure receiver is running FIRST
- Use same channel on both sides
- Check firewall allows ICMP
- Try 127.0.0.1 for local testing

### **"Decryption failed"**
- Keys must be generated at same time (within 1 minute)
- Start receiver, then sender immediately
- Both must use same blockchain time

### **"Scapy not installed"**
```bash
python -m pip install scapy
```

---

## 📊 What Makes This Special

1. **Real Network:** Actually sends packets over network
2. **Blockchain Keys:** Keys derived from blockchain, never transmitted
3. **Automatic Sync:** Both sides get same key automatically
4. **Looks Normal:** Packets appear as regular ICMP pings
5. **No Setup:** Works out of the box
6. **Multiple Channels:** Choose timing/size/TTL
7. **Encrypted:** AES-256 military-grade encryption

---

## 🎓 Next Steps

1. ✅ Test locally (127.0.0.1)
2. ✅ Test on same network (192.168.x.x)
3. ✅ Try different channels
4. ✅ Read REAL_NETWORK_GUIDE.md for details
5. ✅ Connect to real blockchain
6. ✅ Deploy smart contracts

---

## 📝 Command Reference

### **Sender**
```bash
python network_sender.py <target_ip> <message> [channel]

Examples:
python network_sender.py 127.0.0.1 "Hello"
python network_sender.py 192.168.1.100 "Secret" timing
python network_sender.py 10.0.0.5 "Attack at dawn" ttl
```

### **Receiver**
```bash
python network_receiver.py <channel> [duration]

Examples:
python network_receiver.py timing
python network_receiver.py size 120
python network_receiver.py ttl 60
```

---

## 🔒 Security Notes

- **For Learning:** This is educational
- **For Production:** Connect to real blockchain
- **Keys:** Change every minute automatically
- **Stealth:** Packets look like normal traffic
- **Encryption:** AES-256 military-grade

---

**Ready to send secret messages over the network!** 🚀🔐

Just run:
```bash
# Terminal 1 (Receiver)
python network_receiver.py timing

# Terminal 2 (Sender)
python network_sender.py 127.0.0.1 "Your secret message" timing
```

**No blockchain setup needed - it works immediately!** 🎉
