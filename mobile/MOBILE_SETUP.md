# Mobile App Setup Guide - راهنمای راه‌اندازی اپ موبایل

## پیش‌نیازها

- Flutter SDK 3.0+
- Android Studio یا Xcode
- Dart 3.0+
- Git
- Node.js (Optional)

## نصب Flutter

### Windows

```powershell
# 1. دانلود Flutter
# از https://flutter.dev/docs/get-started/install/windows دانلود کنید

# 2. Extract فایل
# به C:\flutter منتقل کنید

# 3. Update PATH
# Environment Variables → User variables → PATH
# اضافه کنید: C:\flutter\bin

# 4. بررسی نصب
flutter --version
dart --version
```

### macOS

```bash
# 1. استفاده از Homebrew
brew install flutter

# 2. بررسی نصب
flutter --version
```

### Linux

```bash
# 1. دانلود و Extract
cd ~
tar xf ~/Downloads/flutter_linux_3.*.tar.xz

# 2. Add PATH
echo 'export PATH="$PATH:~/flutter/bin"' >> ~/.bashrc
source ~/.bashrc

# 3. بررسی
flutter --version
```

## Setup موبایل

### Step 1: نصب وابستگی‌ها

```bash
cd mobile
flutter pub get
```

### Step 2: نصب Flutter Plugins

```bash
flutter pub global activate get_cli
flutter pub add get
```

### Step 3: تشخیص مشکلات

```bash
flutter doctor
```

این دستور تمام مشکلات احتمل را نشان می‌دهد.

## اجرا روی شبیه‌ساز

### Android

```bash
# 1. باز کردن AVD Manager
flutter emulators

# یا از Android Studio
# Tools → Device Manager

# 2. یک شبیه‌ساز ایجاد کنید
# Device: Pixel 6
# OS: Android 13

# 3. شبیه‌ساز را شروع کنید
flutter emulators --launch Pixel_6_API_33

# 4. اجرای اپ
flutter run
```

### iOS (فقط روی macOS)

```bash
# 1. باز کردن Xcode Simulator
open -a Simulator

# 2. اجرای اپ
flutter run
```

## اجرا روی دستگاه واقعی

### Android

```bash
# 1. فعال کردن Developer Mode
# Settings → About Phone → Tap Build Number 7 times

# 2. فعال کردن USB Debugging
# Settings → Developer Options → USB Debugging

# 3. اتصال دستگاه
adb devices

# 4. اجرای اپ
flutter run
```

### iOS

```bash
# 1. وصل کردن دستگاه به Mac

# 2. قابل اعتماد کردن Certificate
# Settings → General → VPN & Device Management

# 3. اجرای اپ
flutter run
```

## تنظیم Backend Connection

### 1. تشخیص IP Address

```bash
# Windows
ipconfig

# macOS/Linux
ifconfig
```

### 2. آپدیت AppConfig

```dart
// lib/config/app_config.dart

class AppConfig {
  // برای دستگاه واقعی
  static const String apiBaseUrl = 'http://192.168.1.X:8000';
  
  // برای شبیه‌ساز
  // static const String apiBaseUrl = 'http://10.0.2.2:8000';
}
```

### 3. تست اتصال

```dart
// lib/services/api_service.dart میتوانید آزمایشی انجام دهید
Future<void> testConnection() async {
  try {
    final response = await http.get(
      Uri.parse('${AppConfig.apiBaseUrl}/api/v1/diseases'),
    );
    print('Connection OK: ${response.statusCode}');
  } catch (e) {
    print('Connection Error: $e');
  }
}
```

## ساختار پروژه

```
mobile/
├── lib/
│   ├── main.dart                    # نقطه ورود
│   ├── config/
│   │   ├── app_config.dart         # تنظیمات اپ
│   │   ├── routes.dart             # مسیرها
│   │   └── theme.dart              # تم
│   ├── controllers/
│   │   ├── auth_controller.dart    # کنترلر احراز
│   │   ├── health_controller.dart  # کنترلر سلامت
│   │   └── diagnostic_controller.dart  # کنترلر تشخیصی
│   ├── services/
│   │   └── api_service.dart        # سرویس API
│   ├── models/
│   │   ├── health_record.dart
│   │   └── patient.dart
│   ├── screens/
│   │   ├── splash_screen.dart
│   │   ├── auth/
│   │   ├── home/
│   │   ├── diagnostic_screen.dart
│   │   ├── personalized_plan_screen.dart
│   │   └── ...
│   └── assets/
│       ├── images/
│       ├── icons/
│       ├── fonts/
│       └── data/
├── android/                         # کد Android
├── ios/                            # کد iOS
├── pubspec.yaml                    # وابستگی‌ها
└── README.md
```

## Testing

### Unit Tests

```bash
flutter test
```

### Integration Tests

```bash
flutter test integration_test
```

### دیباگ مود

```bash
flutter run --debug
```

### Release مود

```bash
flutter run --release
```

## Build کردن

### Debug APK

```bash
flutter build apk --debug
```

### Release APK

```bash
flutter build apk --release
```

### App Bundle (برای Play Store)

```bash
flutter build appbundle --release
```

### Split APKs (برای آرکیتکچرهای مختلف)

```bash
flutter build apk --release --split-per-abi
```

## استقرار بر روی Google Play Store

### مراحل:

1. **ایجاد حساب Developer**
   - [Google Play Console](https://play.google.com/console)
   - هزینه: $25

2. **ایجاد App**
   - نام: Avicenna Health
   - Bundle ID: com.avicenna.health

3. **ایجاد Key Store**
   ```bash
   keytool -genkey -v -keystore ~/avicenna-release-key.keystore \
     -keyalg RSA -keysize 2048 -validity 10000 -alias avicenna-key
   ```

4. **Build Release**
   ```bash
   flutter build appbundle --release
   ```

5. **Upload به Play Store**
   - فایل `.aab` را آپلود کنید
   - اطلاعات اپ را کامل کنید
   - منتشر کنید

## بهینه‌سازی کارایی

### حجم APK کاهش دهید

```bash
flutter build apk --split-per-abi --obfuscate --split-debug-info=./symbols
```

### Runtime Performance

```dart
// استفاده از const
const Text('Avicenna')

// استفاده از RepaintBoundary
RepaintBoundary(
  child: YourWidget(),
)

// استفاده از ListView.builder
ListView.builder(
  itemCount: 100,
  itemBuilder: (context, index) => Item(index),
)
```

## Debugging & Troubleshooting

### مشکلات رایج

#### "Flutter: command not found"
```bash
# بررسی PATH
echo $PATH

# دوباره تنظیم کنید
# Windows: Environment Variables میں flutter\bin شامل کریں
# macOS/Linux: اضافه کنید به ~/.bashrc یا ~/.zshrc
```

#### "ANDROID_HOME not set"
```bash
# Windows
setx ANDROID_HOME "C:\Users\YourUsername\AppData\Local\Android\sdk"

# macOS
export ANDROID_HOME=~/Library/Android/sdk

# Linux
export ANDROID_HOME=~/Android/Sdk
```

#### "Gradle build failed"
```bash
flutter clean
cd android
./gradlew clean
cd ..
flutter pub get
flutter run
```

#### "HTTP: Handshake error"
```dart
// در api_service.dart
HttpClient httpClient = HttpClient();
httpClient.badCertificateCallback = (X509Certificate cert, String host, int port) => true;
```

### Logs و Debugging

```bash
# تفصیلی لاگ
flutter run -v

# Device logs
adb logcat

# اجرا در debug mode
flutter run --debug

# DevTools
flutter pub global activate devtools
dart devtools
```

## منابع مفید

- [Flutter Documentation](https://flutter.dev/docs)
- [Dart Documentation](https://dart.dev/guides)
- [GetX Documentation](https://github.com/jonataslaw/getx)
- [Firebase for Flutter](https://firebase.flutter.dev/)
- [Flutter Awesome](https://flutterawesome.com/)

## دستورات مفید

```bash
# تمیز کردن
flutter clean

# دریافت وابستگی‌ها
flutter pub get

# بهروزرسانی وابستگی‌ها
flutter pub upgrade

# تولید کد
flutter pub run build_runner build

# فرمت کد
dart format .

# تجزیه و تحلیل کد
dart analyze

# درختی شبیه‌ساز‌ها
flutter emulators

# نسخه Flutter
flutter --version

# اطلاعات سیستم
flutter doctor -v
```

## مرحله بعدی

1. ✅ Flutter را نصب کنید
2. ✅ وابستگی‌ها را نصب کنید
3. 👉 Backend را تشکیل دهید (Backend/DEPLOYMENT_GUIDE.md)
4. 👉 اپ را روی شبیه‌ساز اجرا کنید
5. 👉 API endpoints را تست کنید
6. 👉 اپ را برای Play Store آماده کنید
