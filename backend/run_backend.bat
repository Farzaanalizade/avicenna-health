@echo off
REM Run Backend Server
REM ==================

echo.
echo ========================================
echo Starting Avicenna AI Backend Server
echo ========================================
echo.

cd /d d:\AvicennaAI\backend

echo Checking Python...
d:\AvicennaAI\backend\venv\Scripts\python.exe --version

echo.
echo Starting FastAPI + Uvicorn on port 8000...
echo.

d:\AvicennaAI\backend\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000

pause
