@echo off
echo ======================================================================
echo STEALTH NETWORK - FULL ECOSYSTEM STARTUP
echo ======================================================================
echo [0/4] Setting Environment (Unicode Support)...
SET PYTHONUTF8=1
CHCP 65001 > NUL

echo [1/4] Starting Dashboard (Port 5000)...
start "Dashboard" cmd /k "CHCP 65001 > NUL && python app.py"

timeout /t 2 /nobreak

echo [2/4] Starting Receiver Node (Port 5001)...
start "Receiver" cmd /k "CHCP 65001 > NUL && python receiver_web.py"

timeout /t 2 /nobreak

echo [3/4] Starting Wallet Auth Service (Port 5002)...
start "WalletAuth" cmd /k "CHCP 65001 > NUL && python wallet_auth_app.py"

timeout /t 2 /nobreak

echo [4/4] Starting Sender Node (Port 5003)...
start "Sender" cmd /k "CHCP 65001 > NUL && python sender_web.py"

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
