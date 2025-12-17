@echo off
REM Master Script - Run Both Backend + Mobile
REM ==========================================

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   Avicenna AI - Full Stack Startup                        ║
echo ║   Backend + Mobile Both Together                          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo.
echo ✓ Step 1: Backend Server
echo   Location: backend\run_backend.bat
echo   Port: 8000
echo   Command: uvicorn app.main:app --reload
echo.

echo.
echo ✓ Step 2: Android Emulator
echo   Location: mobile\run_emulator.bat
echo   Command: flutter emulators --launch Pixel_6_API_33
echo.

echo.
echo ✓ Step 3: Mobile App
echo   Location: mobile\run_mobile.bat
echo   Command: flutter run
echo.

echo.
echo ════════════════════════════════════════════════════════════
echo Please follow these steps:
echo ════════════════════════════════════════════════════════════
echo.

echo 1. Open Terminal/CMD Window 1:
echo    Run: backend\run_backend.bat
echo    Wait for: "Application startup complete"
echo.

echo 2. Open Terminal/CMD Window 2:
echo    Run: mobile\run_emulator.bat
echo    Wait for: Emulator appears (30-60 seconds)
echo.

echo 3. Open Terminal/CMD Window 3:
echo    Run: mobile\run_mobile.bat
echo    Wait for: App appears on emulator
echo.

echo ════════════════════════════════════════════════════════════
echo.

echo Opening Backend...
cd /d d:\AvicennaAI\backend
start run_backend.bat

timeout /t 3

echo Opening Emulator...
cd /d d:\AvicennaAI\mobile
start run_emulator.bat

timeout /t 5

echo Opening Mobile App...
cd /d d:\AvicennaAI\mobile
start run_mobile.bat

echo.
echo All processes started! Check each window for status.
echo.

pause
