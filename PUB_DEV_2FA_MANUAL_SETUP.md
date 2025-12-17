# راهنمای تفصیلی: حل مشکل pub.dev با 2FA

## 📌 خلاصه مشکل و حل

### مشکل ریشه‌ای
- حساب Google شما **2-Factor Authentication** فعال دارد
- Dart pub client نمی‌تواند **interactively** کد 2FA وارد کند
- Flutter tool هر بار می‌کوشد pub.dev را access کند → مشکل Authorization

### حل
**App-Specific Password** استفاده کنید (نه رمز اصلی Google)

---

## 🔐 مراحل حل

### مرحله 1: ایجاد App Password

1. **لاگین به Google Account**
   - https://myaccount.google.com/security
   - 2FA code را وارد کنید

2. **رفتن به App Passwords**
   - سمت چپ: "Security"
   - پیدا کنید: "App passwords" (فقط اگر 2FA فعال باشد)

3. **ایجاد Password**
   - App: "Other (custom name)"
   - Name: `flutter-pub`
   - Device: `Windows`
   - کلیک: "Generate"

4. **کپی کردن**
   - Google یک **16-character password** می‌دهد
   - **مثال**: `abcd efgh ijkl mnop`
   - کپی این رو (بدون space)

---

### مرحله 2: ذخیره Credentials Manually

**چون Flutter tool pub upgrade می‌کند، باید credentials مستقل ذخیره کنیم.**

1. **ایجاد credentials directory**

```powershell
# Windows
$credDir = "$env:USERPROFILE\.pubrc.json"
# یا
$credDir = "$env:APPDATA\dart_pub"
```

2. **ایجاد credentials file**

```powershell
# File path
$filePath = "$env:USERPROFILE\.pubrc.json"

# Content (YAML format)
$content = @"
# pub.dev credentials
hosted:
  - url: "https://pub.dev"
    token: "oauth2/YOUR_TOKEN_HERE"
"@

# Save
Set-Content -Path $filePath -Value $content
```

**اما** بهتر است direct method استفاده کنیم:

---

### ✅ سادهترین راه: استفاده از Pub Cache

**حالا بگذا مخزن credentials رو احاطه کنیم:**

```powershell
# موقعیت credentials
$pubCache = "$env:PUB_CACHE"
if (!$pubCache) {
    $pubCache = "$env:USERPROFILE\.pub-cache"
}

# Credentials location
$credPath = "$pubCache\credentials.json"

# Show current
if (Test-Path $credPath) {
    Write-Host "Credentials file: $credPath"
    Get-Content $credPath | Select-Object -First 5
}
```

---

### 🔧 درجه یک: Direct Configuration

```powershell
# Navigate
cd d:\AvicennaAI\mobile

# Skip Flutter updates
$env:FLUTTER_SKIP_UPDATE_CHECK = "true"
$env:FLUTTER_NO_ANALYTICS = "true"

# Try pub get
dart pub get --verbose 2>&1 | Select-Object -First 50
```

---

## 📝 تمام خطوات برای شما

### Step 1: Google Setup (5 min)

```
1. https://myaccount.google.com/security
2. Login + 2FA code
3. Click "App passwords"
4. Select:
   - App: Other
   - Device: Windows
   - Name: flutter-pub
5. Click Generate
6. COPY: abcd efgh ijkl mnop (16 chars, remove space)
```

### Step 2: Dart Token (2 min)

```powershell
cd C:\flutter\bin

# Direct dart (no flutter wrapper)
dart pub token add https://pub.dev

# When asked:
# Email: your-email@gmail.com
# Password: [Paste the 16-char without space: abcdefghijklmnop]
```

### Step 3: Test (1 min)

```bash
cd d:\AvicennaAI\mobile

# Clear everything
flutter clean
dart pub cache clean

# Get dependencies
flutter pub get
# Expected: "Got dependencies!" ✅

# If works, build APK
flutter build apk --release
# Expected: ✓ Built build/.../app-release.apk ✅
```

---

## 🐛 Troubleshooting

### اگر "Building flutter tool..." می‌آید

**مشکل**: Flutter wrapper pub upgrade انجام می‌دهد  
**حل**: Skip flutter tool initialization

```powershell
$env:FLUTTER_SKIP_UPDATE_CHECK = "true"
$env:FLUTTER_NO_ANALYTICS = "true"
$env:FLUTTER_ENVIRONMENT = "offline"

# Then try
dart pub get
```

### اگر credentials نگذاشته شد

**کجا ذخیره می‌شوند:**
```
Windows: %USERPROFILE%\.pub-cache\credentials.json
Linux:   ~/.pub-cache/credentials.json
Mac:     ~/.pub-cache/credentials.json
```

**چک کنید:**
```powershell
$pubCache = if ($env:PUB_CACHE) { $env:PUB_CACHE } else { "$env:USERPROFILE\.pub-cache" }
Get-Content "$pubCache\credentials.json" 2>$null
```

### اگر "Invalid credentials"

```powershell
# Remove old token
dart pub token remove https://pub.dev

# Generate NEW app password from Google
# https://myaccount.google.com/apppasswords

# Add again
dart pub token add https://pub.dev
```

---

## ✨ خلاصه

| چیز | وضعیت |
|-----|--------|
| مشکل | 2FA blocks non-interactive pub access |
| حل | App-specific password |
| زمان | 10 دقیقه |
| نتیجه | `flutter build apk` ✅ کار می‌کند |

---

## 🚀 بعد از حل

```bash
cd d:\AvicennaAI\mobile

# 1. Build APK
flutter build apk --release

# 2. Wait 15-20 minutes for build
# ✅ Release APK ready

# 3. Install on phone
adb devices
adb install -r build\app\outputs\flutter-apk\app-release.apk

# 4. Test app
# • Splash screen ✓
# • Login ✓
# • Health analysis ✓
```

**و کار تمام است!** 🎉

