@echo off
REM Automated Dart Pub Token Setup
setlocal enabledelayedexpansion

cd /d d:\AvicennaAI\mobile

echo.
echo ========================================
echo 🚀 Dart Pub Token Setup
echo ========================================
echo.

REM Kill any running flutter/dart processes
taskkill /F /IM dart.exe >nul 2>&1
taskkill /F /IM flutter.bat >nul 2>&1
timeout /t 2 /nobreak >nul

echo 📋 Step 1: Setting environment variables...
set FLUTTER_SKIP_UPDATE_CHECK=true
set FLUTTER_NO_ANALYTICS=true
echo ✅ Environment set
echo.

echo 🔑 Step 2: Adding pub.dev token...
echo Please enter credentials when prompted:
echo Username: saal2070@gmail.com
echo Password: atuipwbibtoofsja
echo.

REM Run dart pub token add
dart pub token add https://pub.dev < d:\AvicennaAI\pub_input.txt

echo.
echo 🔍 Step 3: Verifying token...
if exist "%USERPROFILE%\.pub-cache\credentials.json" (
    echo ✅ Credentials file created!
) else (
    echo ⚠️  Credentials file not found yet
)

echo.
echo 📦 Step 4: Testing flutter pub get...
flutter pub get

echo.
echo ========================================
echo ✨ Setup Complete!
echo ========================================
pause
