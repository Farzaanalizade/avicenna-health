@echo off
REM Initialize Flutter project with Android support (bypasses pub.dev)

setlocal enabledelayedexpansion

echo.
echo ========================================
echo  Flutter Android Initialization
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Disabling Flutter tool update check...
set FLUTTER_SKIP_UPDATE_CHECK=true
set FLUTTER_NO_ANALYTICS=true

echo Step 2: Cleaning cache...
rmdir /s /q .dart_tool 2>nul
rmdir /s /q android 2>nul
rmdir /s /q ios 2>nul
rmdir /s /q build 2>nul

echo Step 3: Getting pubspec.yaml dependencies...
call flutter pub get 2>&1

echo Step 4: Creating Android folder structure...
if not exist "android" (
    call flutter create android --platforms android
)

echo Step 5: Updating Android project...
call flutter pub upgrade 2>&1

echo.
echo Setup complete. You can now try building.
echo.

endlocal
