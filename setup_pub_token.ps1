# Setup pub.dev Token with Google 2FA
# هدف: Add dart pub token برای pub.dev

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║        PUB.DEV TOKEN SETUP (with Google 2FA)         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Step 1: آگاهی دهنده
Write-Host "📌 Step 1: Google App Password Generation" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Yellow
Write-Host "`n⚠️  لطفا این مراحل را در مرورگر انجام دهید:`n"
Write-Host "1️⃣  رفتن به: https://myaccount.google.com/apppasswords" -ForegroundColor Green
Write-Host "2️⃣  وارد شوید با 2FA code" -ForegroundColor Green
Write-Host "3️⃣  انتخاب کنید: App: Other (custom name) | Device: Windows" -ForegroundColor Green
Write-Host "4️⃣  نام دهید: flutter-pub" -ForegroundColor Green
Write-Host "5️⃣  کپی کنید: 16-character app password (بدون space)" -ForegroundColor Green
Write-Host "`n💾 App Password مثال: abcdefghijklmnop`n" -ForegroundColor Cyan

# Step 2: Input
Write-Host "📌 Step 2: Enter Your Credentials" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Yellow

$email = Read-Host "`n📧 Google Email Address (example: user@gmail.com)"
$appPassword = Read-Host "🔐 16-Char App Password (paste from Google)"

# Validate
if ($email -notmatch "@") {
    Write-Host "❌ Invalid email format" -ForegroundColor Red
    exit 1
}

if ($appPassword.Length -ne 16) {
    Write-Host "⚠️  Warning: App password should be 16 characters" -ForegroundColor Yellow
    Write-Host "   Current length: $($appPassword.Length)" -ForegroundColor Yellow
}

# Step 3: تنظیم محیط
Write-Host "`n📌 Step 3: Setting Environment Variables" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Yellow

$env:FLUTTER_SKIP_UPDATE_CHECK = "true"
$env:FLUTTER_NO_ANALYTICS = "true"
$env:PUB_SKIP_VERSION_CHECK = "true"

Write-Host "✓ Environment variables set" -ForegroundColor Green

# Step 4: محل کار
Write-Host "`n📌 Step 4: Navigate to Mobile Directory" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Yellow

cd d:\AvicennaAI\mobile
Write-Host "✓ Changed to: $(Get-Location)" -ForegroundColor Green

# Step 5: Token addition
Write-Host "`n📌 Step 5: Adding pub.dev Token" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Yellow
Write-Host "⏳ Running: dart pub token add https://pub.dev`n" -ForegroundColor Cyan

# Use echo to pipe credentials
Write-Host "$email`n$appPassword" | dart pub token add https://pub.dev

# Check result
if ($?) {
    Write-Host "`n✅ Token successfully added!" -ForegroundColor Green
} else {
    Write-Host "`n⚠️  Token addition may have issues" -ForegroundColor Yellow
}

# Step 6: Verification
Write-Host "`n📌 Step 6: Verification" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Yellow

$credFile = "$env:USERPROFILE\.pub-cache\credentials.json"
if (Test-Path $credFile) {
    Write-Host "✅ Credentials file exists at: $credFile" -ForegroundColor Green
    Write-Host "   File size: $((Get-Item $credFile).Length) bytes" -ForegroundColor Green
} else {
    Write-Host "⚠️  Credentials file not found yet (may appear after first use)" -ForegroundColor Yellow
}

# Step 7: Test pub get
Write-Host "`n📌 Step 7: Testing pub get" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Yellow
Write-Host "⏳ Running: flutter pub get (first time may be slow)...`n" -ForegroundColor Cyan

flutter pub get

if ($?) {
    Write-Host "`n✅ Dependencies downloaded successfully!" -ForegroundColor Green
} else {
    Write-Host "`n❌ pub get failed - check credentials" -ForegroundColor Red
}

# Final summary
Write-Host "`n╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║              SETUP COMPLETE!                          ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "📋 اگر همه چیز موفق بود:" -ForegroundColor Cyan
Write-Host "   1. flutter clean" -ForegroundColor White
Write-Host "   2. flutter build apk --release" -ForegroundColor White
Write-Host "   3. adb install -r build\app\outputs\flutter-apk\app-release.apk" -ForegroundColor White

Write-Host "`n⚠️  اگر مشکل پیش آمد:" -ForegroundColor Yellow
Write-Host "   • dart pub token remove https://pub.dev" -ForegroundColor White
Write-Host "   • دوباره اپ پسورد بسازید" -ForegroundColor White
Write-Host "   • اسکریپت را مجدد اجرا کنید" -ForegroundColor White

Write-Host ""
