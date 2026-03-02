@echo off
setlocal enabledelayedexpansion
title Stealth Network Launcher

:: Configuration
set PYTHON_EXE=C:\Users\ELCOT\AppData\Local\Python\bin\python3.exe
set PYTHONUTF8=1
chcp 65001 > nul

:MENU
cls
echo ======================================================================
echo           STEALTH NETWORK - UNIFIED PROJECT LAUNCHER
echo ======================================================================
echo.
echo  [1] START FULL WEB SYSTEM (Dashboard, Receiver, Auth, Sender)
echo  [2] START CLI RECEIVER (UDP Fallback Mode - Recommended)
echo  [3] START CLI SENDER   (UDP Fallback Mode - Recommended)
echo  [4] RUN SYSTEM DIAGNOSTICS
echo  [5] EXIT
echo.
set /p choice="Select an option (1-5): "

if "%choice%"=="1" goto START_WEB
if "%choice%"=="2" goto START_RECV
if "%choice%"=="3" goto START_SEND
if "%choice%"=="4" goto DIAG
if "%choice%"=="5" exit
goto MENU

:START_WEB
echo Starting all services...
start "Dashboard" cmd /k "chcp 65001 > nul && %PYTHON_EXE% app.py"
timeout /t 1 > nul
start "Receiver"  cmd /k "chcp 65001 > nul && %PYTHON_EXE% receiver_web.py"
timeout /t 1 > nul
start "WalletAuth" cmd /k "chcp 65001 > nul && %PYTHON_EXE% wallet_auth_app.py"
timeout /t 1 > nul
start "Sender"    cmd /k "chcp 65001 > nul && %PYTHON_EXE% sender_web.py"
echo.
echo All services launched! 
echo Access Dashboard at: http://localhost:5000/dashboard
pause
goto MENU

:START_RECV
set /p dur="Duration to listen (seconds, default 60): "
if "!dur!"=="" set dur=60
cls
echo Starting Receiver with UDP Fallback...
%PYTHON_EXE% network_receiver.py timing !dur! --force-fallback
pause
goto MENU

:START_SEND
set /p tip="Target IP Address: "
set /p msg="Message to Send: "
cls
echo Sending via UDP Fallback...
%PYTHON_EXE% network_sender.py !tip! "!msg!" timing --force-fallback
pause
goto MENU

:DIAG
cls
echo Running Project Verification...
%PYTHON_EXE% validate_system.py
pause
goto MENU
