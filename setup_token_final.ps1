#!/usr/bin/env pwsh
# Force kill all Flutter/Dart processes
Get-Process dart -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process flutter -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3

# Navigate to project
Set-Location d:\AvicennaAI\mobile

# Set environment
$env:FLUTTER_SKIP_UPDATE_CHECK = "true"
$env:FLUTTER_NO_ANALYTICS = "true"

# Try to add token directly with input
$credentials = @"
saal2070@gmail.com
atuipwbibtoofsja
"@

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🔑 Adding pub.dev token..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Use cmd.exe to run dart with input redirection
$credFile = "d:\AvicennaAI\pub_credentials.txt"
Set-Content -Path $credFile -Value $credentials -Encoding ASCII

# Alternative: Use PowerShell's stdin redirection
$process = Start-Process -FilePath "dart" `
    -ArgumentList "pub", "token", "add", "https://pub.dev" `
    -RedirectStandardInput $credFile `
    -NoNewWindow `
    -PassThru `
    -Wait

Write-Host ""
Write-Host "Process completed with exit code: $($process.ExitCode)"
Write-Host ""

# Verify credentials
$credPath = "$env:USERPROFILE\.pub-cache\credentials.json"
if (Test-Path $credPath) {
    Write-Host "✅ Credentials saved!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Credentials not yet created" -ForegroundColor Yellow
}

# Test flutter pub get
Write-Host ""
Write-Host "📦 Testing flutter pub get..." -ForegroundColor Cyan
flutter pub get

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✨ Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
