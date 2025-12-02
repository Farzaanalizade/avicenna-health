#!/usr/bin/env powershell
# Build APK Script for Avicenna Health
# اسکریپت ساخت APK برای اویسنا سلامت

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Avicenna Health - APK Builder" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Set environment variables
$env:FLUTTER_SKIP_UPDATE_CHECK = "true"
$env:FLUTTER_NO_ANALYTICS = "true"
$env:PUB_HOSTED_URL = "https://pub.dev"
$env:FLUTTER_STORAGE_BASE_URL = "https://storage.googleapis.com/flutter_infra_release/releases/stable"

# Change to mobile directory
Set-Location -Path "d:\AvicennaAI\mobile"

Write-Host "[1/4] Checking Flutter installation..." -ForegroundColor Yellow
& C:\flutter\bin\flutter.bat --version

Write-Host ""
Write-Host "[2/4] Cleaning previous builds..." -ForegroundColor Yellow
& C:\flutter\bin\flutter.bat clean

Write-Host ""
Write-Host "[3/4] Getting dependencies..." -ForegroundColor Yellow
try {
    Write-Host "  Trying offline mode first..." -ForegroundColor Gray
    & C:\flutter\bin\flutter.bat pub get --offline 2>&1
} catch {
    Write-Host "  Offline mode failed, trying online..." -ForegroundColor Gray
    & C:\flutter\bin\flutter.bat pub get
}

Write-Host ""
Write-Host "[4/4] Building APK (Release mode)..." -ForegroundColor Yellow
& C:\flutter\bin\flutter.bat build apk --release --verbose

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan

# Check if APK was built successfully
$apkPath = "build\app\outputs\flutter-apk\app-release.apk"
if (Test-Path $apkPath) {
    Write-Host "✓ APK built successfully!" -ForegroundColor Green
    Write-Host "Location: $(Resolve-Path $apkPath)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Install on device with ADB:" -ForegroundColor Cyan
    Write-Host "  adb install $apkPath" -ForegroundColor White
    Write-Host ""
    Write-Host "Or for reinstall (force update):" -ForegroundColor Cyan
    Write-Host "  adb install -r $apkPath" -ForegroundColor White
} else {
    Write-Host "✗ APK build failed" -ForegroundColor Red
    exit 1
}

Write-Host "======================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit"
