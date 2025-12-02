# Avicenna Health - APK Builder (Offline Mode)
# This script builds APK without requiring pub.dev connectivity

Write-Host "`n╔════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     Avicenna Health - APK Offline Builder        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

# Step 1: Clean previous builds
Write-Host "Step 1/4: Cleaning previous builds..." -ForegroundColor Yellow
flutter clean --verbose

# Step 2: Get dependencies with offline mode
Write-Host "`nStep 2/4: Getting dependencies (offline mode)..." -ForegroundColor Yellow
$env:FLUTTER_SKIP_UPDATE_CHECK = "true"
$env:PUB_SKIP_VERSION_CHECK = "true"
$env:FLUTTER_NO_ANALYTICS = "true"

# Try offline first
flutter pub get --offline 2>&1 | out-null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Offline mode failed, trying with system Dart..." -ForegroundColor Yellow
    dart pub get 2>&1 | out-null
}

# Step 3: Build with offline gradle
Write-Host "`nStep 3/4: Building APK (release mode)..." -ForegroundColor Yellow
$buildArgs = @(
    "build", "apk",
    "--release",
    "--verbose",
    "--no-pub"
)

flutter @buildArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nStep 4/4: Verifying APK..." -ForegroundColor Yellow
    $apkPath = "build\app\outputs\flutter-apk\app-release.apk"
    
    if (Test-Path $apkPath) {
        $apkFile = Get-Item $apkPath
        $sizeGB = [math]::Round($apkFile.Length / 1MB, 2)
        
        Write-Host "`n╔════════════════════════════════════════════════════╗" -ForegroundColor Green
        Write-Host "║         ✅ APK BUILD SUCCESSFUL!                  ║" -ForegroundColor Green
        Write-Host "╚════════════════════════════════════════════════════╝`n" -ForegroundColor Green
        
        Write-Host "📦 APK Location: $apkPath" -ForegroundColor Green
        Write-Host "📊 File Size: $sizeGB MB" -ForegroundColor Green
        Write-Host "📅 Created: $($apkFile.LastWriteTime)" -ForegroundColor Green
        Write-Host "✨ Ready to install on your Android device!" -ForegroundColor Green
        
        Write-Host "`n🚀 Next Steps:" -ForegroundColor Cyan
        Write-Host "1. Connect your Android phone via USB" -ForegroundColor White
        Write-Host "2. Enable USB Debugging (Settings → Developer options)" -ForegroundColor White
        Write-Host "3. Run: adb install -r '$apkPath'" -ForegroundColor White
        Write-Host "4. Or use: adb install -r build\app\outputs\flutter-apk\app-release.apk" -ForegroundColor White
    }
    else {
        Write-Host "`n❌ APK file not found at expected location!" -ForegroundColor Red
        Write-Host "Checking for alternative locations..." -ForegroundColor Yellow
        Get-ChildItem -Path "build" -Recurse -Filter "*.apk" | Select-Object FullName
    }
}
else {
    Write-Host "`n❌ APK Build Failed!" -ForegroundColor Red
    Write-Host "Error code: $LASTEXITCODE" -ForegroundColor Red
    exit 1
}
