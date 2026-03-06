@echo off
echo ======================================================================
echo BLOCKCHAIN NETWORK STEGANOGRAPHY - AUTOMATED TEST
echo ======================================================================
echo.
echo This will:
echo 1. Start receiver in background
echo 2. Wait 2 seconds
echo 3. Send message
echo 4. Show results
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo Starting receiver in background...
start /B python network_receiver.py timing 30 > receiver_output.txt 2>&1

echo Waiting 3 seconds for receiver to initialize...
timeout /t 3 /nobreak > nul

echo.
echo Sending message...
python network_sender.py 127.0.0.1 "Hello World" timing

echo.
echo Waiting for receiver to finish...
timeout /t 5 /nobreak > nul

echo.
echo ======================================================================
echo RECEIVER OUTPUT:
echo ======================================================================
type receiver_output.txt

echo.
echo ======================================================================
echo TEST COMPLETE!
echo ======================================================================
pause
