@echo off
title Vehicle Service Centre Management System Server
cd /d "%~dp0backend"
echo ========================================================
echo   Vehicle Service Centre Management System (Autocare Pro)
echo   Starting local server on http://127.0.0.1:8000 ...
echo ========================================================
start "" "http://127.0.0.1:8000"
.\venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
pause
