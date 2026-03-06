@echo off
echo ======================================================================
echo STEALTH NETWORK - FULL ECOSYSTEM STARTUP
echo ======================================================================
echo.

echo [1/4] Starting Dashboard (Port 5000)...
start "Dashboard" cmd /k "python app.py"

timeout /t 2 /nobreak

echo [2/4] Starting Receiver Node (Port 5001)...
start "Receiver" cmd /k "python receiver_web.py"

timeout /t 2 /nobreak

echo [3/4] Starting Wallet Auth Service (Port 5002)...
start "WalletAuth" cmd /k "python wallet_auth_app.py"

timeout /t 2 /nobreak

echo [4/4] Starting Sender Node (Port 5003)...
start "Sender" cmd /k "python sender_web.py"

echo.
echo ======================================================================
echo ALL SERVICES INITIATED
echo Dashboard: http://localhost:5000/dashboard
echo Receiver:  http://localhost:5001
echo WalletAuth: http://localhost:5002
echo Sender:    http://localhost:5003
echo ======================================================================
echo.
pause
