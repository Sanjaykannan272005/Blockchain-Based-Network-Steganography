@echo off
REM Wallet Authentication Service Launcher
REM Windows batch file to start the wallet authentication app

echo.
echo ========================================================
echo           Wallet Authentication Service
echo ========================================================
echo.
echo Starting wallet_auth_app.py...
echo.
echo Open browser: http://localhost:5002
echo.
echo Press Ctrl+C to stop the service
echo.
echo ========================================================
echo.

python wallet_auth_app.py

if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to start wallet authentication service
    echo.
    echo Troubleshooting:
    echo   1. Make sure Python is installed and in PATH
    echo   2. Install dependencies: pip install -r requirements.txt
    echo   3. Check blockchain_config.json exists
    echo   4. Check flask is installed: pip install flask
    echo.
    pause
)
