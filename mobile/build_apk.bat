@echo off
REM Build APK Script for Avicenna Health
REM اسکریپت ساخت APK برای اویسنا سلامت

setlocal enabledelayedexpansion

echo ======================================
echo  Avicenna Health - APK Builder
echo ======================================
echo.

REM Set Flutter environment variables to skip pub checks
set FLUTTER_SKIP_UPDATE_CHECK=true
set FLUTTER_NO_ANALYTICS=true
set PUB_HOSTED_URL=https://pub.dev
set FLUTTER_STORAGE_BASE_URL=https://storage.googleapis.com/flutter_infra_release/releases/stable

cd /d d:\AvicennaAI\mobile

echo [1/4] Checking Flutter installation...
C:\flutter\bin\flutter.bat --version

echo.
echo [2/4] Cleaning previous builds...
C:\flutter\bin\flutter.bat clean

echo.
echo [3/4] Getting dependencies (offline mode if available)...
REM Try pub get with offline mode first
C:\flutter\bin\flutter.bat pub get --offline 2>nul || C:\flutter\bin\flutter.bat pub get

echo.
echo [4/4] Building APK (Release mode)...
C:\flutter\bin\flutter.bat build apk --release

echo.
echo ======================================
if exist "build\app\outputs\flutter-apk\app-release.apk" (
    echo ✓ APK built successfully!
    echo Location: build\app\outputs\flutter-apk\app-release.apk
    echo.
    echo Install on device:
    echo adb install build\app\outputs\flutter-apk\app-release.apk
) else (
    echo ✗ APK build failed
    exit /b 1
)
echo ======================================

pause
