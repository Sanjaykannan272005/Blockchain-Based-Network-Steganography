# 🔧 FIX: Install Npcap for Windows

## ❌ Error You're Seeing:
```
WARNING: No libpcap provider available ! pcap won't be used
ERROR: winpcap is not installed
```

## ✅ Solution: Install Npcap (2 minutes)

### **Step 1: Download Npcap**

Visit: https://npcap.com/#download

Or direct link: https://npcap.com/dist/npcap-1.79.exe

### **Step 2: Install Npcap**

1. Run the downloaded `npcap-xxx.exe` as Administrator
2. **IMPORTANT:** Check these options during installation:
   - ✅ **Install Npcap in WinPcap API-compatible Mode** (MUST CHECK!)
   - ✅ Support raw 802.11 traffic
   - ✅ Install Npcap Loopback Adapter (for 127.0.0.1 testing)

3. Click Install
4. Restart your computer (important!)

### **Step 3: Test It Works**

```bash
python -c "from scapy.all import *; print('✅ Scapy works!')"
```

If you see `✅ Scapy works!` - you're ready!

---

## 🚀 Now Run Your Commands

### **Terminal 1 (Receiver) - Run as Administrator:**
```bash
python network_receiver.py timing 60
```

### **Terminal 2 (Sender) - Run as Administrator:**
```bash
python network_sender.py 127.0.0.1 "Hello World" timing
```

---

## 🎯 Alternative: Use Web Interface (No Npcap Needed!)

If you don't want to install Npcap, use the web interface instead:

```bash
python blockchain_web_app.py
```

Visit: http://localhost:5000

This uses encryption/decryption without raw packet capture.

---

## 🔧 Still Having Issues?

### **Option 1: Use Wireshark (includes Npcap)**

1. Download Wireshark: https://www.wireshark.org/download.html
2. Install it (includes Npcap automatically)
3. Restart computer
4. Try again

### **Option 2: Manual Npcap Installation**

If automatic install fails:

1. Uninstall any existing WinPcap/Npcap
2. Restart computer
3. Install Npcap fresh
4. **Must check "WinPcap API-compatible Mode"**
5. Restart computer again

### **Option 3: Use Linux/WSL**

On Windows Subsystem for Linux:

```bash
# Install WSL if not already
wsl --install

# In WSL terminal
sudo apt update
sudo apt install python3-pip libpcap-dev
pip3 install scapy pycryptodome

# Run with sudo
sudo python3 network_receiver.py timing 60
```

---

## ✅ Verification Checklist

After installing Npcap:

- [ ] Npcap installed with WinPcap compatibility mode
- [ ] Computer restarted
- [ ] Running terminal as Administrator
- [ ] Scapy test command works
- [ ] Ready to send/receive!

---

## 📝 Quick Reference

**Download Npcap:** https://npcap.com/#download

**Must check during install:**
- ✅ Install Npcap in WinPcap API-compatible Mode
- ✅ Install Npcap Loopback Adapter

**After install:**
- Restart computer
- Run terminals as Administrator
- Test with: `python network_receiver.py timing 60`

---

**Once Npcap is installed, everything will work perfectly!** 🚀
