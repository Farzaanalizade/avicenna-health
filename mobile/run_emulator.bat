@echo off
REM Start Android Emulator
REM ======================

echo.
echo ========================================
echo Starting Android Emulator
echo ========================================
echo.

cd /d d:\AvicennaAI\mobile

echo Available Emulators:
flutter emulators

echo.
echo.
echo Starting Pixel_6_API_33 (modify if needed)...
echo.

flutter emulators --launch Pixel_6_API_33

echo.
echo Emulator is starting... please wait 30-60 seconds
echo.
pause
