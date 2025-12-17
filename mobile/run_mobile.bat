@echo off
REM Run Flutter Mobile App
REM ======================

echo.
echo ========================================
echo Running Avicenna AI Mobile App
echo ========================================
echo.

cd /d d:\AvicennaAI\mobile

echo Checking Flutter devices...
flutter devices

echo.
echo Starting Mobile App...
echo.

flutter run

pause
