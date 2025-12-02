# APK Build - روش‌های مختلف

## ✅ روش 1: PowerShell Script (Windows - توصیه شده)

```powershell
cd d:\AvicennaAI\mobile
.\build_apk.ps1
```

**مزایا**: آسان، خودکار، خطا‌های نمایش داده می‌شود  
**زمان**: 10-20 دقیقه اولی، 5 دقیقه بعدی

---

## ✅ روش 2: Batch Script (Windows)

```cmd
d:\AvicennaAI\mobile\build_apk.bat
```

**مزایا**: ساده، بدون PowerShell policy issues  
**زمان**: 10-20 دقیقه اولی، 5 دقیقه بعدی

---

## ✅ روش 3: Manual Commands (Windows)

```powershell
$env:FLUTTER_SKIP_UPDATE_CHECK = "true"
$env:FLUTTER_NO_ANALYTICS = "true"

cd d:\AvicennaAI\mobile

# Clean
flutter clean

# Get dependencies
flutter pub get

# Build (release برای گوشی بهتره)
flutter build apk --release --verbose
```

**مزایا**: کنترل کامل، debug logs بیشتر  
**زمان**: 10-20 دقیقه اولی

---

## ✅ روش 4: Docker (اگر Docker دارید)

```bash
cd d:\AvicennaAI\mobile

# Build Docker image
docker build -t avicenna-apk .

# Run and generate APK
docker run -v $(pwd)/output:/output avicenna-apk

# APK در output/avicenna-health.apk خواهد بود
```

**مزایا**: کامل isolated، pub.dev مشکل نیست  
**نیاز**: Docker نصب باشد  
**زمان**: 30-40 دقیقه (اولی)

---

## ✅ روش 5: Linux/Mac (اگر دسترسی دارید)

```bash
chmod +x mobile/build_apk.sh
./mobile/build_apk.sh
```

**مزایا**: pub.dev معمولاً مشکلی نیست  
**نیاز**: Linux یا macOS  
**زمان**: 10-20 دقیقه

---

## ⚠️ اگر همه روش‌ها ناموفق بودند

### Solution A: استفاده از GitHub Actions

1. Push کد به GitHub
2. استفاده از Flutter Action
3. APK download کنید

```yaml
# .github/workflows/build.yml
name: Build APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter build apk --release
      - uses: actions/upload-artifact@v2
        with:
          name: apk
          path: build/app/outputs/flutter-apk/app-release.apk
```

### Solution B: استفاده از Online APK Builders

- EAS Build (Expo): https://eas.expo.dev
- Codemagic: https://codemagic.io

---

## 📲 بعد از Build - نصب APK

### Step 1: اتصال گوشی

```bash
# Check devices
adb devices

# Output should show:
# emulator-5554      device
# OR
# FA7AX1A0501        device
```

### Step 2: نصب APK

```bash
adb install -r build/app/outputs/flutter-apk/app-release.apk
```

### Step 3: لانچ اپ

```bash
# Automatic
adb shell am start -n com.example.avicenna_health/com.example.avicenna_health.MainActivity

# Or manually from device
```

---

## 🐛 Troubleshooting

### Issue: "pub upgrade failed"
```powershell
$env:FLUTTER_SKIP_UPDATE_CHECK = "true"
flutter pub get --offline
```

### Issue: "Android SDK not found"
```bash
flutter doctor -v
# Check ANDROID_HOME path
```

### Issue: "Gradle build failed"
```bash
flutter clean
cd android
./gradlew clean
cd ..
flutter build apk --release -v
```

### Issue: "No connected devices"
```bash
# USB Debugging را فعال کنید
# Settings → About Phone → tap Build Number 7 times
# Back → Developer options → USB Debugging ON

adb devices  # Should show device now
```

---

## 📊 خلاصه

| روش | سهولت | سرعت | نیاز |
|-----|-------|------|------|
| PowerShell | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Windows |
| Batch | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Windows |
| Manual | ⭐⭐⭐ | ⭐⭐⭐ | Windows |
| Docker | ⭐⭐⭐ | ⭐⭐ | Docker |
| Linux/Mac | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Linux/Mac |
| GitHub Actions | ⭐⭐ | ⭐ | Internet |

---

## 🎯 توصیه

**برای شما**: روش 1 (PowerShell) یا روش 2 (Batch)

```powershell
cd d:\AvicennaAI\mobile
.\build_apk.ps1
```

بعد از موفق build:

```powershell
adb install -r build\app\outputs\flutter-apk\app-release.apk
```

---

**تاریخ**: 2 دسامبر 2025  
**Avicenna Health v1.0.0**
