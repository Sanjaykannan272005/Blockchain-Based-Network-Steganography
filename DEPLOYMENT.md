# Stealth Network: Production Deployment Guide

This guide outlines the steps to deploy the **Stealth Network** to a real-world production environment (e.g., Ubuntu 22.04 VPS).

## 1. 🏗️ Server Preparation

### Install Docker & Docker Compose
Connect to your server via SSH and run:
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

---

## 🖥️ VMware / Ubuntu Virtual Machine Setup

If you are deploying on an Ubuntu VM via **VMware Workstation** or **Player**:

### 1. 🌐 Network Configuration (CRITICAL)
For the P2P and Steganography packet-level features to work with other physical machines:
- **Shut down the VM**.
- Go to **Virtual Machine Settings** > **Network Adapter**.
- Select **Bridged: Connect directly to the physical network**.
- Check **Replicate physical network connection state**.
- *Why?* NAT mode hides the VM's true MAC/IP address behind the host, which can block raw steganographic packets.

### 2. 🔌 Prerequisites
Install the capture library on the host Ubuntu to ensure Scapy has full access:
```bash
sudo apt install -y libpcap-dev
```

---

## 2. 📁 Project Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Sanjaykannan272005/steganography.git
   cd steganography
   ```

2. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   nano .env
   ```
   > Fill in your real **RPC_URL**, **OPERATOR_PRIVATE_KEY**, and contract addresses in the `.env` file. These are essential for the system to interact with the blockchain.

---

## 🐧 Native Ubuntu Installation (No Docker)

If you prefer to run the project directly on Ubuntu (recommended for VMware for best networking performance):

### 1. 🛠️ Install System Dependencies
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv libpcap-dev
```

### 2. 🐍 Setup Python Environment
```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. 🚀 Launch the Network
Make the startup script executable and run it:
```bash
chmod +x start_all_services.sh
./start_all_services.sh
```

### 📊 Monitoring Logs
Since services run in the background, you can watch the live logs:
```bash
tail -f logs/dashboard.log
```

---

## 3. 🚀 Launch the Network

Run the entire ecosystem using Docker Compose:
```bash
docker-compose up -d --build
```

### Verify Running Containers
```bash
docker-compose ps
```
You should see 5 services running: `dashboard`, `wallet-auth`, `receiver`, `sender`, and `p2p-node`.

---

## 4. 🌐 Accessing the Interfaces

By default, the following ports are exposed:
- **C2 Dashboard**: `http://YOUR_SERVER_IP:5000`
- **Identity & Auth**: `http://YOUR_SERVER_IP:5002`
- **Target Receiver**: `http://YOUR_SERVER_IP:5001`
- **Covert Sender**: `http://YOUR_SERVER_IP:5003`

---

## 5. 🛡️ Post-Deployment Security

1. **Firewall (UFW)**: Only allow essential traffic.
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 5000:5003/tcp
   sudo ufw allow icmp
   sudo ufw enable
   ```

2. **SSL (Recommended)**: For real production, use a reverse proxy like **Nginx** with **Certbot** to provide HTTPS on these ports.

---

## 💻 Multi-Computer Setup (LAN)

If you are running the project across multiple computers on the same network:

1. **Find your Local IP**:
   - **Windows**: Run `ipconfig` in CMD. Look for `IPv4 Address` (e.g., `192.168.1.15`).
   - **Linux/Mac**: Run `hostname -I` or `ifconfig`.

2. **Sync Configuration**:
   - Ensure the `.env` file on **Computer B** is identical to **Computer A** (same Private Keys, RPC URLs, and Contract Addresses).

3. **Access from Other Computers**:
   - Instead of `localhost`, use the IP of the main computer:
     - Dashboard: `http://[IP_OF_COMP_A]:5000`
     - Receiver: `http://[IP_OF_COMP_A]:5001`
   - **IMPORTANT**: When sending messages in the UI, ensure the "Target IP" corresponds to the real network IP of the receiver machine, not `127.0.0.1`.

4. **Firewall Access**:
   - Ensure Windows Firewall or your router is not blocking the ports (5000-5003).

---

## 🛠️ Troubleshooting

- **Check Logs**: `docker-compose logs -f [service_name]`
- **Restart All**: `docker-compose restart`
- **Permission Denied (Scapy)**: Docker containers are granted `NET_ADMIN` and `NET_RAW` capabilities in `docker-compose.yml`, which is required for network steganography.
