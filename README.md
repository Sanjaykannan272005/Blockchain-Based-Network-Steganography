# 🔐 Stealth Network Dashboard (Unified C2 Center)

## 📡 Project Overview
The **Stealth Network Dashboard** is a military-grade, decentralized communication platform designed for high-stakes covert operations. It integrates advanced steganography with a blockchain-backed P2P mesh network to ensure message plausible deniability, transmission resilience, and operator anonymity.

### 🎯 Problem Statement
Standard encrypted communication (like Signal or Telegram) is easily detectable by state-level firewalls. While the content is hidden, the *fact* that a conversation is happening is visible. Our system solves this by blending message traffic into standard network protocols and utilizing decentralized "dead-drops" to eliminate traceable sender-receiver paths.

---

## 🛠️ Technology Stack
- **Dashboard Interface**: HTML5, Vanilla CSS, JS (Bootstrap 5, Chart.js, Mermaid.js)
- **Backend Logic**: Python 3.x, Flask, Pyshark (Packet Sniffing)
- **Encryption Engine**: AES-256-GCM, Onion Routing Encryption
- **Steganography Layers**: LSB (Image-based) + Timing/Padding (Network-based)
- **Blockchain Layer**: Ethereum/EVM (Solidity Smart Contracts), Web3.py
- **P2P Networking**: Custom Mesh Protocol, Node-to-Node Forwarding

---

## 🧱 Core Modules

### 1. Unified Dashboard (C2 Center)
A centralized command-and-control interface for real-time network monitoring.
- **Real-Time Terminal**: Live stream of system logs and background activity.
- **P2P Topology Map**: Interactive visualizer of the active node mesh.
- **Security Simulator**: Red-team tool providing statistical detection probability (KS-Tests).

### 2. Covert Transmitter (Hybrid Sender)
Multi-layered steganography engine for data transmission.
- **Onion Encryption**: Successive layers of encryption for node-hop security.
- **Adaptive Protocol**: Toggles between timing-delay and packet-padding methods based on network jitter.
- **Blockchain Dead-Drop**: Syncs message fragments directly to the blockchain for asynchronous retrieval.

### 3. Identity & Resilience Layer
Advanced security protocols for operator and node protection.
- **RBAC (Role Based Access Control)**: Wallet-authenticated administrative controls.
- **Auto-Kill Switch**: Nodes self-destruct (wipe local buffers) if reputation drops below a safety threshold.
- **Dead-Man's Switch**: Automatic time-locked emergency broadcasts if operator inactivity is detected.

---

## 📦 Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd steganography
   ```

2. **Initialize Environment**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Blockchain**:
   - Update `blockchain_config.json` with your RPC URL and Contract Addresses.
   - Deploy contracts in the `/contracts` folder using Remix or Hardhat.

4. **Launch Dashboard**:
   ```bash
   python app.py
   ```
   Navigate to `http://localhost:5000/dashboard`.

---

## 🛡️ Security Considerations
- **Metadata Protection**: The system strips all EXIF data from cover images.
- **Plausible Deniability**: Traffic patterns are mathematically modeled to mimic standard background noise (Entropy matching).
- **Decentralized Reputation**: Node health is managed through on-chain consensus, preventing sybil attacks on the mesh.

---

## 📝 License
This project is intended for educational research and authorized professional testing. Unauthorized use in restricted jurisdictions is strictly prohibited.

---
*Developed for the Google DeepMind Advanced Agentic Coding project.*