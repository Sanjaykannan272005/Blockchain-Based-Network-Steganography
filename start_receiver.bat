@echo off
echo.
echo ========================================================
echo   BLOCKCHAIN STEGANOGRAPHY - NETWORK RECEIVER
echo ========================================================
echo.
echo This computer will receive encrypted messages
echo.

REM Get local IP address
echo Your IP addresses:
ipconfig | findstr /i "IPv4"
echo.

REM Start receiver
python network_receiver_standalone.py

pause
