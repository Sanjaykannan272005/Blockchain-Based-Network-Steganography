# 🌐 Network Receiver Setup Guide

## How to Receive Messages on Another Computer

---

## 📋 Overview

When you select **"Network Receiver"** in the Simple Wizard, the message is sent over the network to another computer. Here's how to set it up.

---

## 🎯 Two Computers Setup

### Computer A (Sender)
- Runs the web interface
- Sends encrypted messages

### Computer B (Receiver)
- Runs the network receiver script
- Receives and decrypts messages

---

## 🚀 Step-by-Step Setup

### STEP 1: Setup Receiver Computer (Computer B)

#### 1.1 Copy the receiver script
Copy `network_receiver_standalone.py` to Computer B

#### 1.2 Install dependencies on Computer B
```bash
pip install pycryptodomex
```

#### 1.3 Find Computer B's IP address

**Windows:**
```bash
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

**Linux/Mac:**
```bash
ifconfig
# or
ip addr show
```
Look for "inet" address (e.g., 192.168.1.100)

#### 1.4 Start the receiver on Computer B
```bash
cd e:\Projects\steganography
python network_receiver_standalone.py
```

**Output:**
```
╔════════════════════════════════════════════════════════════╗
║     BLOCKCHAIN STEGANOGRAPHY - NETWORK RECEIVER            ║
║     Run this on the computer that will receive messages    ║
╚════════════════════════════════════════════════════════════╝

Enter port to listen on (default 9999): 
```

Press Enter to use default port 9999.

**Receiver will show:**
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

---

### STEP 2: Send Message from Computer A

#### 2.1 Start web interface on Computer A
```bash
cd e:\Projects\steganography
python blockchain_web_app.py
```

#### 2.2 Open Simple Wizard
Visit: http://localhost:5000/simple-wizard

#### 2.3 Follow the wizard steps:

**STEP 1: Configure Sender**
- Enter sender address
- Click "Next"

**STEP 2: Configure Receiver**
- Select: **"Network Receiver (Different Computer)"**
- Enter Computer B's IP address (e.g., 192.168.1.100)
- Click "Next"

**STEP 3: Select Features**
- Choose features (e.g., Blockchain Keys, Authentication)
- Click "Next"

**STEP 4: Write Message**
- Type: "Hello from Computer A"
- Click "Next"

**STEP 5: Review & Send**
- Review settings
- Click "🚀 SEND MESSAGE"

---

### STEP 3: Receive Message on Computer B

**Computer B terminal will show:**

```
📨 Incoming connection from: 192.168.1.50:54321

============================================================
📬 MESSAGE RECEIVED
============================================================
From: 0x627306090abaB3A6e1400e9345bC60c78a8BEf57
Time: 2024-12-20 15:35:42
Features Used: 3 of 10

🔓 Decrypted Message:
   Hello from Computer A

📋 Feature Details:
   ✓ Blockchain Key: Block #5
   ✓ Authentication: Verified
   ✓ Forensic Record: Block #6
============================================================

✅ Waiting for next message...
```

---

## 🔧 Network Configuration

### Same Network (LAN)
- Both computers on same WiFi/Ethernet
- Use local IP (192.168.x.x)
- No firewall configuration needed (usually)

### Different Networks (Internet)
- Need public IP or port forwarding
- Configure router to forward port 9999
- May need firewall rules

---

## 🛡️ Firewall Configuration

### Windows Firewall (Computer B)

**Allow incoming connections on port 9999:**

```powershell
# Run as Administrator
netsh advfirewall firewall add rule name="Blockchain Receiver" dir=in action=allow protocol=TCP localport=9999
```

### Linux Firewall (Computer B)

**UFW:**
```bash
sudo ufw allow 9999/tcp
```

**iptables:**
```bash
sudo iptables -A INPUT -p tcp --dport 9999 -j ACCEPT
```

---

## 🧪 Testing

### Test 1: Same Computer (Localhost)
**Receiver IP:** 127.0.0.1
- Start receiver on same computer
- Send message to 127.0.0.1
- Should work immediately

### Test 2: Same Network (LAN)
**Receiver IP:** 192.168.1.100 (example)
- Start receiver on Computer B
- Find Computer B's local IP
- Send message to that IP
- Should work if firewall allows

### Test 3: Different Networks (Internet)
**Receiver IP:** Public IP + Port Forwarding
- Configure router port forwarding
- Use public IP address
- May require VPN or advanced setup

---

## 🔍 Troubleshooting

### Problem: "Connection refused"

**Solution:**
1. ✅ Check receiver is running on Computer B
2. ✅ Verify IP address is correct
3. ✅ Check firewall allows port 9999
4. ✅ Ensure both computers on same network

### Problem: "Connection timeout"

**Solution:**
1. ✅ Ping Computer B from Computer A
   ```bash
   ping 192.168.1.100
   ```
2. ✅ Check network connectivity
3. ✅ Verify no VPN blocking connection

### Problem: "Decryption failed"

**Solution:**
1. ✅ Ensure both use same password
2. ✅ Check `BlockchainStego2024` password matches
3. ✅ Verify message wasn't corrupted

### Problem: Receiver not showing messages

**Solution:**
1. ✅ Check receiver terminal is running
2. ✅ Look for "Incoming connection" message
3. ✅ Verify no errors in terminal

---

## 📊 Complete Example

### Scenario: Send "Secret Mission" from Office to Home

**Home Computer (Receiver):**
```bash
# 1. Find IP address
ipconfig
# Result: 192.168.1.100

# 2. Start receiver
python network_receiver_standalone.py
# Press Enter for port 9999

# 3. Wait for messages...
```

**Office Computer (Sender):**
```bash
# 1. Start web app
python blockchain_web_app.py

# 2. Open browser
http://localhost:5000/simple-wizard

# 3. Configure:
STEP 1: Sender address (default)
STEP 2: Network Receiver → IP: 192.168.1.100
STEP 3: Select features (Blockchain Keys, Authentication)
STEP 4: Message: "Secret Mission"
STEP 5: Send!
```

**Home Computer Shows:**
```
📬 MESSAGE RECEIVED
From: 0x627306090abaB3A6e1400e9345bC60c78a8BEf57
🔓 Decrypted Message: Secret Mission
✓ Blockchain Key: Block #5
✓ Authentication: Verified
```

---

## 🎯 Quick Reference

### Receiver Computer (Computer B)
```bash
# Install dependencies
pip install pycryptodomex

# Find IP address
ipconfig  # Windows
ifconfig  # Linux/Mac

# Start receiver
python network_receiver_standalone.py
# Press Enter for default port 9999
```

### Sender Computer (Computer A)
```bash
# Start web app
python blockchain_web_app.py

# Open wizard
http://localhost:5000/simple-wizard

# In STEP 2:
- Select: Network Receiver
- Enter: Computer B's IP address
```

---

## 🔐 Security Notes

1. **Same Password:** Both computers use `BlockchainStego2024`
2. **Encryption:** AES-256-CBC (military-grade)
3. **Network:** Messages encrypted before transmission
4. **Firewall:** Only port 9999 needs to be open
5. **Local Network:** Safest on trusted LAN

---

## ✅ Summary

**To receive messages on another computer:**

1. ✅ Copy `network_receiver_standalone.py` to Computer B
2. ✅ Install `pycryptodomex` on Computer B
3. ✅ Find Computer B's IP address
4. ✅ Run receiver script on Computer B
5. ✅ In wizard, select "Network Receiver"
6. ✅ Enter Computer B's IP address
7. ✅ Send message!
8. ✅ Computer B shows decrypted message in terminal

**That's it!** 🎉
