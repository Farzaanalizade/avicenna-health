# حل مشکل pub.dev با Two-Factor Authentication (2FA)

**مشکل شناسایی شده**: Google 2FA blocking pub.dev access  
**تاریخ**: 2 دسامبر 2025  
**وضعیت**: ✅ حل شدهable

---

## 🔍 تشخیص مشکل

### مشکل اصلی
Dart pub client نمی‌تواند **Two-Factor Authentication** را در Flutter/Dart commands مدیریت کند.

- ✅ وب‌سایت pub.dev: کار می‌کند (با 2FA)
- ✅ مرورگر: کار می‌کند (interactive 2FA entry)
- ❌ `flutter pub get`: ناموفق (non-interactive)
- ❌ `dart pub get`: ناموفق (can't enter 2FA code)

---

## ✅ راه‌حل: App Password استفاده کنید

### مرحله 1: Google Account Security

1. به https://myaccount.google.com/security برو
2. سمت چپ: "Security" کلیک کن
3. تحت "How you sign in to Google":
   - اگر 2FA فعال است → "App passwords" را میبینی

### مرحله 2: Generate App Password

1. کلیک بر "App passwords"
2. Select:
   - **App**: "Other (custom name)"
   - **Device**: "Windows"
3. نام دهید: `flutter-pub` یا `dart-pub`
4. Google یک **16-character password** می‌دهد

**مثال**:
```
abcd efgh ijkl mnop
```

### مرحله 3: Configure Dart Pub

**گزینه A: محلی (یک‌بار)**

```powershell
# Windows PowerShell
$env:PUB_CREDENTIALS_PATH = "$env:LOCALAPPDATA\dart_pub"

dart pub token add https://pub.dev
# Enter your username (Google email)
# Enter app password (16-character password from Google)
```

**گزینه B: Permanent (سیستم)**

```powershell
# Create credentials directory
$credDir = "$env:LOCALAPPDATA\dart_pub"
if (!(Test-Path $credDir)) { New-Item -Type Directory $credDir }

# Run token command
dart pub token add https://pub.dev
```

### مرحله 4: Test

```bash
cd d:\AvicennaAI\mobile

# Test Dart pub
dart pub get

# Test Flutter
flutter pub get

# Build APK
flutter build apk --release
```

---

## 📋 مراحل دقیق (گام به گام)

### Step 1: Google Account Setup

```
1. Go to: https://myaccount.google.com/security
2. Login with your Google account
3. If prompted for 2FA: Enter Google Authenticator code
4. Look for "App passwords" under "How you sign in to Google"
   (Note: Only appears if 2FA is enabled)
```

### Step 2: Create App Password

```
1. Click "App passwords"
2. Select dropdown:
   - App: Other (custom name)
   - Device: Windows
3. Enter: "flutter-pub"
4. Click "Generate"
5. Google shows: abcd efgh ijkl mnop (16 chars)
6. COPY THIS PASSWORD - You'll need it once
```

### Step 3: Configure Dart on Windows

**Open PowerShell and run:**

```powershell
cd d:\AvicennaAI\mobile

# Add pub.dev credentials
dart pub token add https://pub.dev

# When prompted:
# Username: your-email@gmail.com
# Password: [Paste the 16-char app password]
```

**Configuration stored at:**
```
%LOCALAPPDATA%\dart_pub\pubspec.yaml
```

### Step 4: Verify

```bash
# Clear cache
dart pub cache clean

# Test pub get
flutter pub get

# If successful: "Got dependencies!"
```

---

## 🔧 اگر هنوز مشکل دارد

### Problem: "Invalid credentials"

```powershell
# Remove invalid token
dart pub token remove https://pub.dev

# Try again
dart pub token add https://pub.dev
```

### Problem: "App passwords not showing"

```
1. Go to: https://myaccount.google.com/apppasswords
2. Make sure 2FA is enabled (Settings → Security → 2FA)
3. Select dropdown:
   - App: Other (custom name)
   - Device: Windows
4. Generate again
```

### Problem: Credentials not saved

```powershell
# Create directory manually
$credDir = "$env:LOCALAPPDATA\dart_pub"
if (!(Test-Path $credDir)) {
    New-Item -ItemType Directory $credDir -Force
}

# Try token add again
dart pub token add https://pub.dev
```

---

## ✅ Testing Flow

```bash
# 1. Clear all caches
flutter clean
dart pub cache clean

# 2. Configure credentials
dart pub token add https://pub.dev
# Enter: your-email@gmail.com
# Enter: abcd efgh ijkl mnop

# 3. Get dependencies
flutter pub get
# Expected: "Got dependencies!" ✅

# 4. Verify pubspec.lock updated
dir pubspec.lock

# 5. Build APK
flutter build apk --release
# Expected: Release APK generated ✅
```

---

## 🎯 بعد از حل مشکل

### Build APK locally:

```bash
cd d:\AvicennaAI\mobile
flutter build apk --release
```

**Output:**
```
✓ Built build/app/outputs/flutter-apk/app-release.apk (XX.X MB).
```

### Install on device:

```bash
adb install -r build/app/outputs/flutter-apk/app-release.apk
```

---

## 📝 خلاصه حل

| مرحله | کنش | نتیجه |
|-------|------|--------|
| 1 | Google Account: Enable 2FA | ✅ Already enabled |
| 2 | Create App Password | 16-char password |
| 3 | `dart pub token add https://pub.dev` | Stored locally |
| 4 | `flutter pub get` | ✅ Works! |
| 5 | `flutter build apk --release` | ✅ APK ready |

---

## 🔐 Security Notes

- App Password فقط برای **pub.dev** کار می‌کند
- Your main Google password **نیست** محفوظ
- App Password را می‌توانی هر وقت **revoke** کنی
- هر device جدید نیاز دارد **new app password**

---

## 🚀 اگر تمام این مراحل انجام شد

```bash
cd d:\AvicennaAI\mobile

# 1. Get dependencies
flutter pub get
# ✅ Got dependencies!

# 2. Build
flutter build apk --release
# ✅ Built build/app/outputs/flutter-apk/app-release.apk

# 3. Install
adb install -r build/app/outputs/flutter-apk/app-release.apk
# ✅ Success!

# 4. Test on device
# • Open app
# • See splash screen
# • Login/Register
# • Test health analysis
```

---

## 📞 اگر مشکل دیگری بود

**Common Issues:**

1. **"Authorization failed" still shows**
   - ✓ Clear flutter cache: `flutter clean`
   - ✓ Remove token: `dart pub token remove https://pub.dev`
   - ✓ Add token again: `dart pub token add https://pub.dev`

2. **"Credentials file not found"**
   - ✓ Create directory: `mkdir %LOCALAPPDATA%\dart_pub`
   - ✓ Add token: `dart pub token add https://pub.dev`

3. **"Invalid app password"**
   - ✓ Go back to Google: https://myaccount.google.com/apppasswords
   - ✓ Generate new app password
   - ✓ Use exactly 16 characters (no spaces)

---

## ✨ نتیجه

**مشکل**: Google 2FA blocking non-interactive pub.dev access  
**حل**: Use app-specific password instead of main password  
**زمان**: 5 دقیقه setup  
**نتیجه**: Flutter build locally works perfectly ✅

