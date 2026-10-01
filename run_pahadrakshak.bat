@echo off
title PahadRakshak Server Launcher (HTTPS + HTTP)
echo ========================================================
echo   🏔️ PahadRakshak — Emergency Response System
echo ========================================================
echo [1/3] Navigating to project directory...
cd /d "C:\Users\bhatt\.gemini\antigravity\scratch\pahadrakshak"

echo [2/3] Starting HTTPS Server for Real Mobile Hardware GPS Access...
start "PahadRakshak HTTPS Server" .\venv\Scripts\python.exe -m uvicorn backend.app.main:app --port 8443 --host 0.0.0.0 --ssl-keyfile key.pem --ssl-certfile cert.pem

echo [3/3] Opening Web App in default browser...
start "" "http://127.0.0.1:8000/app/index.html"

.\venv\Scripts\python.exe -m uvicorn backend.app.main:app --port 8000 --host 0.0.0.0
pause
