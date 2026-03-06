@echo off
echo ======================================================================
echo BLOCKCHAIN NETWORK STEGANOGRAPHY - SIMULTANEOUS TEST
echo ======================================================================
echo.
echo Starting receiver and sender simultaneously...
echo.

REM Start receiver in background
start "Receiver" cmd /k "python network_receiver.py timing 60"

REM Wait 5 seconds for receiver to initialize
timeout /t 5 /nobreak

REM Start sender
start "Sender" cmd /k "python network_sender.py 127.0.0.1 \"Hello World\" timing"

echo.
echo Both windows opened!
echo Watch the Receiver window for results.
echo.
pause
