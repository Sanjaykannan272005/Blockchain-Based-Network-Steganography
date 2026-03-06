#!/usr/bin/env python3
"""
Quick Start Wallet Authentication
Run this to get started with MetaMask wallet authentication
"""

import sys
import subprocess
import json
import os

def create_startup_bat():
    """Create Windows batch file to start wallet auth"""
    bat_content = """@echo off
echo Starting Wallet Authentication Service...
python wallet_auth_app.py
pause
"""
    with open('start_wallet_auth.bat', 'w') as f:
        f.write(bat_content)
    print("✅ Created start_wallet_auth.bat")

def create_startup_sh():
    """Create Unix shell script to start wallet auth"""
    sh_content = """#!/bin/bash
echo "Starting Wallet Authentication Service..."
python3 wallet_auth_app.py
"""
    with open('start_wallet_auth.sh', 'w') as f:
        f.write(sh_content)
    os.chmod('start_wallet_auth.sh', 0o755)
    print("✅ Created start_wallet_auth.sh")

def check_dependencies():
    """Check if all required packages are installed"""
    required = {
        'web3': 'web3',
        'eth_account': 'eth-account',
        'flask': 'flask'
    }
    
    missing = []
    for package_name, pip_name in required.items():
        try:
            __import__(package_name)
            print(f"✅ {pip_name} is installed")
        except ImportError:
            missing.append(pip_name)
            print(f"❌ {pip_name} is NOT installed")
    
    if missing:
        print(f"\n⚠️  Install missing packages:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True

def check_config():
    """Check if blockchain_config.json exists"""
    if os.path.exists('blockchain_config.json'):
        print("✅ blockchain_config.json exists")
        
        with open('blockchain_config.json', 'r') as f:
            config = json.load(f)
        
        print(f"   RPC URL: {config.get('rpc_url', 'NOT SET')[:50]}...")
        print(f"   Access Control Contract: {config.get('access_control_contract', 'NOT SET')}")
        
        return True
    else:
        print("❌ blockchain_config.json NOT FOUND")
        print("\nCreate it with:")
        print(json.dumps({
            "rpc_url": "https://sepolia.infura.io/v3/YOUR_INFURA_KEY",
            "access_control_contract": "0x0000000000000000000000000000000000000000",
            "owner_address": "0x0000000000000000000000000000000000000000"
        }, indent=2))
        return False

def check_templates():
    """Check if template files exist"""
    if os.path.exists('templates/wallet_auth.html'):
        print("✅ wallet_auth.html template exists")
        return True
    else:
        print("❌ wallet_auth.html NOT FOUND")
        return False

def print_startup_info():
    """Print important startup information"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                   🔐 WALLET AUTHENTICATION                    ║
║              MetaMask + Smart Contract Access Control         ║
╚═══════════════════════════════════════════════════════════════╝

📋 FEATURES ENABLED:
  ✅ MetaMask wallet connection
  ✅ ECDSA message signing
  ✅ Cryptographic sender verification
  ✅ Smart contract whitelist control
  ✅ Time-based permissions (1 day - 1 year)
  ✅ Revocable access
  ✅ On-chain access audit trail

🚀 STARTUP:
  Windows: python wallet_auth_app.py
  Linux:   python3 wallet_auth_app.py
  
  OR use the startup scripts:
  Windows: start_wallet_auth.bat
  Linux:   ./start_wallet_auth.sh

🌐 WEB INTERFACE:
  URL: http://localhost:5002
  
  Features:
  - 🪙 Connect MetaMask wallet
  - ✍️  Sign messages to prove identity
  - 👥 Manage sender whitelist
  - ⏰ Set time-based permissions
  - 📋 Monitor active permissions

⚙️  CONFIGURATION:
  Edit: blockchain_config.json
  
  Required fields:
  - rpc_url: Your Infura/Alchemy RPC endpoint
  - access_control_contract: Deployed contract address
  - owner_address: Your wallet address

📚 DOCUMENTATION:
  Read: WALLET_AUTH_GUIDE.md
  
  Topics covered:
  - Complete setup instructions
  - API reference
  - Security features
  - Integration examples
  - Troubleshooting

🔐 SECURITY:
  - ECDSA signatures (secp256k1)
  - EIP-191 message signing
  - On-chain access control
  - Immutable audit trail
  - Revocable permissions

💡 NEXT STEPS:
  1. Deploy SenderAccessControl.sol smart contract
  2. Update blockchain_config.json with contract address
  3. Start wallet_auth_app.py
  4. Open http://localhost:5002
  5. Connect MetaMask wallet
  6. Try signing a message

📞 SUPPORT:
  Issues: Check WALLET_AUTH_GUIDE.md troubleshooting section
  Questions: Review inline code comments

╔═══════════════════════════════════════════════════════════════╗
║                   Ready to start! 🚀                         ║
╚═══════════════════════════════════════════════════════════════╝
""")

def main():
    print("\n🔐 Wallet Authentication Quick Setup\n")
    
    print("Checking dependencies...")
    if not check_dependencies():
        print("\n⚠️  Please install missing dependencies first:")
        print("   pip install -r requirements.txt")
        return False
    
    print("\nChecking configuration...")
    if not check_config():
        print("\n⚠️  Please update blockchain_config.json")
        return False
    
    print("\nChecking templates...")
    if not check_templates():
        print("\n⚠️  Missing template files")
        return False
    
    print("\nCreating startup scripts...")
    create_startup_bat()
    create_startup_sh()
    
    print("\n" + "="*60)
    print_startup_info()
    
    print("\n✅ Setup complete! Ready to start wallet authentication.\n")
    
    # Ask if user wants to start now
    if sys.platform.startswith('win'):
        start = input("Start wallet_auth_app.py now? (y/n): ").lower()
        if start == 'y':
            import wallet_auth_app
    
    return True

if __name__ == '__main__':
    main()
