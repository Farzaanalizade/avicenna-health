# APK Build Guide - Avicenna Health

## 📱 ساخت APK برای تست روی گوشی Android

### سیستم‌های مورد نیاز

- ✅ Flutter SDK (نصب شده)
- ✅ Android SDK
- ✅ Java Development Kit (JDK)
- ✅ ADB (Android Debug Bridge)

### راه 1: استفاده از PowerShell Script (سادهترین)

```powershell
cd d:\AvicennaAI\mobile
.\build_apk.ps1
```

### راه 2: استفاده از Batch Script

```cmd
d:\AvicennaAI\mobile\build_apk.bat
```

### راه 3: Manual Commands

```bash
cd d:\AvicennaAI\mobile

# 1. پاک‌سازی build های قدیمی
flutter clean

# 2. دریافت dependencies
flutter pub get

# 3. ساخت APK (Release mode - برای تست بهتره)
flutter build apk --release

# 4. یا Debug APK (سریعتر ولی بزرگتر)
flutter build apk --debug
```

---

## 🚀 نصب APK روی گوشی

### پیش‌نیاز: USB Debugging فعال کنید
1. Settings → About Phone → tap "Build Number" 7 times
2. Back → Developer options → USB Debugging ✓

### اتصال گوشی
```bash
# Check connected devices
adb devices

# Should show:
# List of attached devices
# emulator-5554          device
# OR
# FA7AX1A0501            device
```

### نصب APK

```bash
# Simple install
adb install build\app\outputs\flutter-apk\app-release.apk

# Force reinstall (if already installed)
adb install -r build\app\outputs\flutter-apk\app-release.apk

# Uninstall before install
adb uninstall com.example.avicenna_health
adb install build\app\outputs\flutter-apk\app-release.apk
```

---

## 📊 APK Information

**File Locations:**
```
Release APK: d:\AvicennaAI\mobile\build\app\outputs\flutter-apk\app-release.apk
Debug APK:   d:\AvicennaAI\mobile\build\app\outputs\flutter-apk\app-debug.apk
```

**Package Name:** `com.example.avicenna_health`

**File Size Estimates:**
- Debug APK: 100-150 MB
- Release APK: 30-50 MB

---

## 🔧 اگر مشکل پیش آمد

### مشکل 1: pub.dev authorization error

```powershell
# Solution: Disable pub checks
$env:FLUTTER_SKIP_UPDATE_CHECK = "true"
flutter pub get --offline
```

### مشکل 2: Android SDK not found

```bash
# Check Android SDK location
flutter doctor -v

# Set ANDROID_HOME if needed
set ANDROID_HOME=C:\Users\YourUser\AppData\Local\Android\sdk
```

### مشکل 3: No connected devices

```bash
# List all devices
adb devices

# Reconnect device
adb disconnect
adb connect <device-ip>:5555

# Or use USB cable and enable USB Debugging
```

### مشکل 4: Build failed

```bash
# Deep clean
flutter clean
cd android
./gradlew clean
cd ..

# Try again
flutter pub get
flutter build apk --release -v
```

---

## 💡 Tips برای بهتر کار کردن

### Build Release APK سریع
```bash
cd d:\AvicennaAI\mobile
flutter build apk --release --split-per-abi
# Creates smaller APKs for each architecture (arm64-v8a, armeabi-v7a, x86_64)
```

### Build Debug APK (سریعتر)
```bash
flutter build apk --debug
# فقط برای تست، بسیار سریعتر
```

### View Build Logs
```bash
flutter build apk --release -v
# -v برای verbose output
```

### Test on Emulator
```bash
flutter emulators --launch Pixel_4_API_31
# or
emulator -avd Pixel_4_API_31

# Then run
flutter run
```

---

## 🧪 بعد از نصب - تست کنید

### چک‌لیست
- [ ] اپ روی گوشی نصب شد
- [ ] اپ لانچ می‌شود
- [ ] صفحه‌ی Splash نمایش داده می‌شود
- [ ] Login screen نمایش داده می‌شود
- [ ] Backend address صحیح است (پیش‌فرض: localhost)

### Debug Logs
```bash
# View live logs from device
adb logcat

# Filter logs for your app
adb logcat | grep -i avicenna

# Or use Flutter tools
flutter logs
```

---

## 📡 تنظیم Backend Address

اگر backend روی ماشین شما اجرا می‌شود:

1. **فایل را ویرایش کنید:**
   ```
   d:\AvicennaAI\mobile\lib\config\app_config.dart
   ```

2. **IP Address خود را بجای localhost قرار دهید:**
   ```dart
   static const String apiBaseUrl = 'http://YOUR_PC_IP:8000';
   // مثال: http://192.168.1.100:8000
   ```

3. **Rebuild APK**
   ```bash
   flutter clean
   flutter build apk --release
   ```

---

## 🎯 مراحل خلاصه

1. **Prepare**: `flutter clean`
2. **Get Deps**: `flutter pub get`
3. **Build**: `flutter build apk --release`
4. **Install**: `adb install -r build\app\outputs\flutter-apk\app-release.apk`
5. **Test**: Open app on device
6. **Debug**: `flutter logs` or `adb logcat`

---

## 📱 Test Features

بعد از نصب، می‌توانید این features را تست کنید:

- [ ] Register / Login
- [ ] Capture tongue image
- [ ] Capture eye image
- [ ] Input vital signs
- [ ] Quick health check
- [ ] View history
- [ ] Connect to BLE device (اگر دارید)

---

## ⚙️ Advanced Build Options

```bash
# Build both debug and release
flutter build apk

# Build split APKs by architecture
flutter build apk --split-per-abi

# Build AppBundle (برای Google Play Store)
flutter build appbundle --release

# Specify Dart target version
flutter build apk --target-platform android-arm64
```

---

## 🚨 توجهات مهم

1. **Release APK من APK Debug کوچکتر و سریعتر است**
2. **Backend باید روی شبکه یا localhost قابل دسترس باشد**
3. **USB Debugging باید روی گوشی فعال باشد**
4. **اولین build زمان بر است (10-20 دقیقه)**

---

**Last Updated**: December 2, 2025  
**Status**: Ready to Build ✅
