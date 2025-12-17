# Flutter pub.dev مشکل - راه‌حل‌های جامع

**وضعیت**: ❌ مشکل pub.dev ادامه دارد  
**تاریخ**: 2 دسامبر 2025  
**شناسایی شده**: Error 69 - Authorization failed

---

## 🔍 بررسی انجام‌شده

✅ **Network Test**: موفق - Ping to pub.dev کار می‌کند (135ms)  
✅ **HTTPS Connection**: موفق - HTTP 200 response  
❌ **Dart Pub**: ناموفق - Authorization error  
❌ **Flutter Tool**: ناموفق - pub upgrade fails  
❌ **Cache Clear**: ناموفق - مشکل باقی  

---

## 🎯 راه‌حل‌های ممکن

### 1. **VPN/Proxy Disabled Check**

```powershell
# Check if using proxy
netsh winhttp show proxy

# Check environment variables
$env:HTTP_PROXY
$env:HTTPS_PROXY
```

اگر proxy دیدی:
- VPN را خاموش کن
- Proxy را disable کن
- دوباره سعی کن

---

### 2. **Corporate Firewall/SSL Inspection**

اگر شرکتی محیط هستی:

```powershell
# Try with alternate pub server
$env:PUB_HOSTED_URL = "https://pub.mirrors.aliyun.com"
flutter pub get
```

یا برای کشورهای دیگر:
- China: `https://pub.mirrors.aliyun.com`
- Google: `https://pub.dev`

---

### 3. **Fresh Flutter Installation**

```bash
# Download Flutter SDK completely fresh
flutter doctor -v

# Remove Flutter cache
rm -r ~/.flutter/  # Linux/Mac
rmdir %USERPROFILE%\.flutter /s  # Windows
```

---

### 4. **System Dart (Bypass Flutter Tool)**

```bash
cd d:\AvicennaAI\mobile

# Use system Dart directly
dart pub get

# Then build with Flutter
flutter build apk --release --no-pub
```

---

### 5. **GitHub Actions Cloud Build** ⭐ **RECOMMENDED**

شبکه‌ای مشکل دارد؟ ابری build کن!

```bash
# Push code to GitHub
git push

# GitHub Actions خودکار build می‌کند
# 15-20 دقیقه صبر کن
# APK downloaded from artifacts
```

**فایل workflow**: `.github/workflows/build-apk.yml`

---

### 6. **Codemagic Alternative**

```bash
# Visit: https://codemagic.io
# Sign up
# Connect GitHub repo
# Build automatically
```

---

## 🔧 Advanced Troubleshooting

### Dart Version Conflict

```bash
dart --version
flutter --version

# Check if dart is in PATH
where dart
```

### Clear All Caches

```powershell
# Flutter cache
flutter clean

# Dart cache
dart pub cache clean

# System temp
rm -r $env:TEMP\pub* 2>$null

# Full reinstall
flutter clean
Remove-Item -Path "$env:USERPROFILE\.flutter" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.pub-cache" -Recurse -Force
```

### Check Dart Pub Configuration

```bash
dart pub config --list
```

---

## 📋 تصمیم گیری

| وضعیت | راه‌حل | زمان |
|------|--------|------|
| 🟢 Network OK | GitHub Actions | 20 دقیقه |
| 🟡 Corporate VPN | Codemagic | 20 دقیقه |
| 🔴 هنوز مشکل | System Dart | 15 دقیقه |
| 🟣 فوری نیاز | Docker Build | 30 دقیقه |

---

## ✅ اگر مشکل حل شد

```bash
cd d:\AvicennaAI\mobile

# Test
flutter pub get

# اگر OK → Build کن
flutter build apk --release

# Check output
dir build\app\outputs\flutter-apk\
```

---

## 🚀 بهترین کنش

**1. ابتدا**: GitHub Actions (هیچ مشکل محلی نیست)
```bash
git push origin main
# Go to GitHub Actions
# Run workflow
```

**2. اگر ترجیح محلی**: System Dart
```bash
dart pub get
flutter build apk --release --no-pub
```

**3. اگر هنوز مشکل**: Codemagic
```bash
# Visit codemagic.io
# Sign up + connect
```

---

## 📞 Support

- Flutter Issues: https://github.com/flutter/flutter/issues
- Pub.dev Help: https://pub.dev/help
- Dart Forum: https://stackoverflow.com/questions/tagged/dart

