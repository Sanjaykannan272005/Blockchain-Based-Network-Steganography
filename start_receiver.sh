#!/bin/bash

echo ""
echo "========================================================"
echo "  BLOCKCHAIN STEGANOGRAPHY - NETWORK RECEIVER"
echo "========================================================"
echo ""
echo "This computer will receive encrypted messages"
echo ""

# Get local IP address
echo "Your IP addresses:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    ifconfig | grep "inet " | grep -v 127.0.0.1
else
    # Linux
    ip addr show | grep "inet " | grep -v 127.0.0.1
fi
echo ""

# Start receiver
python3 network_receiver_standalone.py
