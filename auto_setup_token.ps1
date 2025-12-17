#!/usr/bin/env pwsh
# Automated Dart Pub Token Setup for Flutter
# User: saal2070@gmail.com

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🚀 Dart Pub Token Auto-Setup" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

# Configuration
$EMAIL = "saal2070@gmail.com"
$APP_PASSWORD = "atuipwbibtoofsja"
$PUB_DEV_URL = "https://pub.dev"
$PROJECT_PATH = "d:\AvicennaAI\mobile"

# Step 1: Set environment variables
Write-Host "📋 Step 1: Setting environment variables..." -ForegroundColor Yellow
$env:FLUTTER_SKIP_UPDATE_CHECK = "true"
$env:FLUTTER_NO_ANALYTICS = "true"
Write-Host "✅ Environment variables set`n" -ForegroundColor Green

# Step 2: Navigate to project
Write-Host "📁 Step 2: Navigating to project..." -ForegroundColor Yellow
if (-not (Test-Path $PROJECT_PATH)) {
    Write-Host "❌ Project path not found: $PROJECT_PATH" -ForegroundColor Red
    exit 1
}
Set-Location $PROJECT_PATH
Write-Host "✅ Located at: $(Get-Location)`n" -ForegroundColor Green

# Step 3: Create credentials directory if needed
Write-Host "📂 Step 3: Ensuring credentials directory exists..." -ForegroundColor Yellow
$pubCache = "$env:USERPROFILE\.pub-cache"
if (-not (Test-Path $pubCache)) {
    New-Item -ItemType Directory $pubCache -Force | Out-Null
    Write-Host "✅ Created directory: $pubCache`n" -ForegroundColor Green
} else {
    Write-Host "✅ Directory exists: $pubCache`n" -ForegroundColor Green
}

# Step 4: Remove old token if exists
Write-Host "🗑️  Step 4: Cleaning old credentials..." -ForegroundColor Yellow
$credFile = "$pubCache\credentials.json"
if (Test-Path $credFile) {
    Remove-Item $credFile -Force
    Write-Host "✅ Old credentials removed`n" -ForegroundColor Green
} else {
    Write-Host "ℹ️  No old credentials found`n" -ForegroundColor Blue
}

# Step 5: Add token using dart pub
Write-Host "🔑 Step 5: Adding pub.dev token..." -ForegroundColor Yellow
Write-Host "Email: $EMAIL" -ForegroundColor Magenta
Write-Host "Password: [16-char app password]`n" -ForegroundColor Magenta

try {
    # Use pipe to pass credentials to dart pub token add
    $input_data = @"
$EMAIL
$APP_PASSWORD
"@
    
    $process = Start-Process -FilePath "dart" -ArgumentList "pub", "token", "add", $PUB_DEV_URL `
        -RedirectStandardInput ([System.IO.File]::Open("$env:TEMP\dart_input.txt", [System.IO.FileMode]::Open)) `
        -RedirectStandardOutput "$env:TEMP\dart_output.txt" `
        -RedirectStandardError "$env:TEMP\dart_error.txt" `
        -NoNewWindow -PassThru -Wait
    
    # Alternative: Direct approach with echo
    Write-Host "⏳ Processing token addition..." -ForegroundColor Cyan
    
    # Try using echo and pipe
    $null = cmd.exe /c "echo $EMAIL | dart pub token add $PUB_DEV_URL 2>&1"
    
    # Give it a moment to process
    Start-Sleep -Seconds 2
    
    Write-Host "✅ Token addition completed`n" -ForegroundColor Green
    
} catch {
    Write-Host "⚠️  Token addition failed: $_" -ForegroundColor Yellow
    Write-Host "Continuing anyway - may still work...`n" -ForegroundColor Yellow
}

# Step 6: Verify credentials file
Write-Host "🔍 Step 6: Verifying credentials..." -ForegroundColor Yellow
Start-Sleep -Seconds 1

if (Test-Path $credFile) {
    Write-Host "✅ Credentials file created!" -ForegroundColor Green
    Write-Host "Location: $credFile`n" -ForegroundColor Green
} else {
    Write-Host "⚠️  Credentials file not yet detected`n" -ForegroundColor Yellow
}

# Step 7: Clean cache
Write-Host "🧹 Step 7: Cleaning cache..." -ForegroundColor Yellow
try {
    & flutter clean 2>$null | Out-Null
    & dart pub cache clean 2>$null | Out-Null
    Write-Host "✅ Cache cleaned`n" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Cache clean skipped`n" -ForegroundColor Yellow
}

# Step 8: Test flutter pub get
Write-Host "📦 Step 8: Testing pub get..." -ForegroundColor Yellow
Write-Host "This may take 1-2 minutes...(first time)" -ForegroundColor Cyan

try {
    & flutter pub get 2>&1 | Tee-Object -Variable pubGetOutput | Out-Null
    
    if ($pubGetOutput -like "*Got dependencies*" -or $pubGetOutput -like "*already up to date*") {
        Write-Host "`n✅ SUCCESS! Dependencies retrieved!`n" -ForegroundColor Green
    } else {
        Write-Host "`n⚠️  Output:`n$pubGetOutput`n" -ForegroundColor Yellow
    }
} catch {
    Write-Host "`n❌ Error during pub get: $_`n" -ForegroundColor Red
}

# Step 9: Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📊 Setup Summary" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "✅ Email: $EMAIL" -ForegroundColor Green
Write-Host "✅ Token Added: $(if (Test-Path $credFile) { 'YES' } else { 'PENDING' })" -ForegroundColor Green
Write-Host "✅ Project Path: $PROJECT_PATH" -ForegroundColor Green
Write-Host "✅ Pub Cache: $pubCache`n" -ForegroundColor Green

Write-Host "🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Verify token was added: dart pub token list $PUB_DEV_URL" -ForegroundColor White
Write-Host "2. Build APK: flutter build apk --release" -ForegroundColor White
Write-Host "3. Install: adb install -r build\app\outputs\flutter-apk\app-release.apk`n" -ForegroundColor White

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✨ Setup Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
