#!/bin/bash

# ======================================================================
# STEALTH NETWORK - NATIVE SERVICE ORCHESTRATOR (UBUNTU)
# ======================================================================

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}STEALTH NETWORK - NATIVE STARTUP${NC}"
echo -e "${BLUE}======================================================================${NC}"

# 1. Create logs directory if not exists
mkdir -p logs

# 2. Check for Virtual Environment
if [ -d "venv" ]; then
    echo -e "${BLUE}[*] Activating virtual environment...${NC}"
    source venv/bin/activate
else
    echo -e "${RED}[!] 'venv' directory not found. Running with system python...${NC}"
fi

# 3. Start Services
echo -e "${BLUE}[*] Requesting administrative privileges for network steganography...${NC}"
sudo -v # Ask for sudo password once

echo -e "${BLUE}[1/4] Starting Dashboard (Port 5000)...${NC}"
nohup python3 app.py > logs/dashboard.log 2>&1 &
DASHBOARD_PID=$!

sleep 2

echo -e "${BLUE}[2/4] Starting Receiver Node (Port 5001)...${NC}"
# Receiver needs sudo for Scapy packet sniffing
nohup sudo venv/bin/python3 receiver_web.py > logs/receiver.log 2>&1 &
RECEIVER_PID=$!

sleep 2

echo -e "${BLUE}[3/4] Starting Wallet Auth Service (Port 5002)...${NC}"
nohup python3 wallet_auth_app.py > logs/auth.log 2>&1 &
AUTH_PID=$!

sleep 2

echo -e "${BLUE}[4/4] Starting Sender Node (Port 5003)...${NC}"
# Sender needs sudo for Scapy packet injection
nohup sudo venv/bin/python3 sender_web.py > logs/sender.log 2>&1 &
SENDER_PID=$!

echo -e "${GREEN}======================================================================${NC}"
echo -e "ALL SERVICES INITIATED IN BACKGROUND"
echo -e "Dashboard PID: $DASHBOARD_PID"
echo -e "Receiver PID:  $RECEIVER_PID"
echo -e "Auth PID:      $AUTH_PID"
echo -e "Sender PID:    $SENDER_PID"
echo -e "======================================================================"
echo -e "Check logs in the 'logs/' folder if services fail to start."
echo -e "To stop all services: pkill -f python3"
echo -e "${BLUE}======================================================================${NC}"
