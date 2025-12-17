# 📱 ANDROID SDK SETUP - نصب اپ روی گوشی

## ✅ مراحل نصب

### مرحله 1: Android Studio دانلود و نصب

1. برو به: https://developer.android.com/studio
2. دانلود Android Studio
3. نصب کن (اجازه بده تمام SDK components install بشود)

---

### مرحله 2: Environment Variable تنظیم

**Windows:**

```powershell
# PowerShell رو Run as Administrator بازکن
$androidSdkPath = "$env:LOCALAPPDATA\Android\Sdk"
[Environment]::SetEnvironmentVariable("ANDROID_HOME", $androidSdkPath, "User")
[Environment]::SetEnvironmentVariable("PATH", "$env:PATH;$androidSdkPath\tools;$androidSdkPath\platform-tools", "User")

# Verify
echo $env:ANDROID_HOME
```

---

### مرحله 3: USB Debugging فعال کن

**روی گوشی Android:**

1. **Settings → About Phone** برو
2. **Build Number** رو **7 بار** تاب کن
3. **Developer Options** ظاهر میشه
4. برگرد به **Settings → Developer Options**
5. **USB Debugging** رو **ON** کن ✅

---

### مرحله 4: گوشی رو PC وصل کن

1. گوشی رو USB cable با کامپیوتر وصل کن
2. **USB Debugging** dialog رو قبول کن (روی گوشی)
3. **Transfer files** انتخاب کن (نه صرفاً charging)

---

### مرحله 5: Device رو Verify کن

```bash
flutter devices
```

**انتظار:** گوشی رو لیست بشود مثل:
```
android • device-id • android-arm64 • Android 14
```

---

## 🚀 اپ رو روی گوشی Install کن

### Option 1: Flutter Run (Best for Development)
```bash
cd c:\Project\AvicennaAI\mobile
flutter run
# یا مشخص
flutter run -d <device-id>
```

### Option 2: Build APK ابتدا
```bash
cd c:\Project\AvicennaAI\mobile
flutter build apk --debug
# Output: build/app/outputs/flutter-apk/app-debug.apk

# سپس install کن
flutter install
```

### Option 3: Direct APK Install
```bash
adb install build/app/outputs/flutter-apk/app-debug.apk
```

---

## 📊 مثال کامل

```bash
# 1. Flutter دانلود/update کن
flutter doctor

# 2. گوشی رو check کن
flutter devices

# 3. اپ رو روی گوشی run کن
flutter run

# 4. Hot reload (کد change کی)
# Terminal میں: 'r' بزن و Enter
# یا: Ctrl + Shift + R
```

---

## 🔍 Troubleshooting

### مشکل: "No Android SDK found"
```bash
# Android SDK path رو مشخص کن
flutter config --android-sdk /path/to/android/sdk
```

### مشکل: Device detect نمیشه
```bash
# 1. USB cable check کن (data cable نه charging only)
# 2. USB Debugging ON باشه
# 3. PC اجازه gave باشه (روی گوشی prompt قبول کن)

# 4. ADB restart کن:
adb kill-server
adb start-server
flutter devices
```

### مشکل: Build fail
```bash
flutter clean
flutter pub get
flutter run -v  # verbose output ببین
```

---

## 📱 Testing Checklist

- [ ] Android Studio نصب شد
- [ ] Android SDK set شد
- [ ] USB Debugging فعال است
- [ ] گوشی detect میشه (`flutter devices`)
- [ ] APK build successful
- [ ] اپ روی گوشی install شد
- [ ] اپ launch شد
- [ ] Features work کنند

---

## 🎯 بعد از اینکه اپ روی گوشی بود:

### دوباره کد تغییر بده (Hot Reload)
```bash
# Terminal میں 'r' بزن:
r

# یا Ctrl+Shift+R برای hot restart
```

### Logs رو ببین
```bash
flutter logs
```

### Full Restart
```bash
# Terminal میں 'R' بزن:
R
```

---

## ✅ اگر همه چی درست شد:

```
✅ گوشی detect شد
✅ APK build شد
✅ اپ install شد
✅ اپ روی گوشی run میشه
✅ تمام features test شد
```

**Ready for real device testing! 🎉**

---

**Next Steps:**
1. Android Studio نصب کن
2. USB Debugging فعال کن
3. `flutter run` اجرا کن
4. اپ رو روی گوشی test کن
5. Feedback collect کن

---

