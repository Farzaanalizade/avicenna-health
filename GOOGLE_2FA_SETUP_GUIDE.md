# 🎯 مراحل نهایی: حل مشکل Google 2FA برای pub.dev

**وضعیت**: Ready for manual 2FA setup  
**تاریخ**: 2 دسامبر 2025

---

## ✅ قدم‌های بعدی (در سه مرحله)

### مرحله اول: ایجاد App Password از Google

**مهم**: شما باید این کار را انجام دهید (من نمی‌توانم)

1. **وارد شوید به Google Account**
   ```
   https://myaccount.google.com/security
   ```
   - کد 2FA را وارد کنید

2. **نمایش امنیت**
   - سمت چپ > "Security"
   - جستجو کنید: "App passwords"
   - (اگر نمی‌بینید، 2FA فعال نیست)

3. **ایجاد App Password**
   ```
   Select app: Other (custom name)
   Enter name: flutter-pub
   
   Select device: Windows
   
   Click: Generate
   ```

4. **کپی رمز**
   ```
   Google نمایش می‌دهد: abcd efgh ijkl mnop
   
   کپی کنید (بدون space):
   abcdefghijklmnop
   ```

**⏱️ زمان**: 5 دقیقه

---

### مرحله دوم: ثبت Token در Dart

**اکنون این دستورات را اجرا کنید:**

```powershell
# 1. تنظیم environment
$env:FLUTTER_SKIP_UPDATE_CHECK = "true"
$env:FLUTTER_NO_ANALYTICS = "true"

# 2. نوشتار مشخصات
cd d:\AvicennaAI\mobile

# 3. اضافه کردن token
dart pub token add https://pub.dev

# وقتی سوال شد:
# Username: [your-email@gmail.com]
# Password: [abcdefghijklmnop - رمز 16 کاراکتری از Google]
```

**آنچه انتظار می‌رود:**
```
> Enter username for pub.dev: your-email@gmail.com
> Enter password: [paste 16-char password]
✓ Token saved!
```

**⏱️ زمان**: 1 دقیقه

---

### مرحله سوم: آزمایش و Build

```powershell
cd d:\AvicennaAI\mobile

# 1. پاک کردن cache
flutter clean
dart pub cache clean

# 2. دریافت dependencies
flutter pub get
# Expected: "Got dependencies!" ✅

# 3. ساخت APK (اگر pub get موفق شد)
flutter build apk --release
# Expected: ✓ Built build/app/outputs/flutter-apk/app-release.apk ✅

# 4. نصب روی گوشی
adb devices
adb install -r build\app\outputs\flutter-apk\app-release.apk
```

**⏱️ زمان**: 20 دقیقه (build اول طولانی است)

---

## 🔍 بررسی اینکه همه چیز درست شد

```powershell
# چک کنید که token ذخیره شد
$credFile = "$env:USERPROFILE\.pub-cache\credentials.json"
if (Test-Path $credFile) {
    Write-Host "✅ Credentials file exists"
    Get-Content $credFile | Select-Object -First 3
} else {
    Write-Host "❌ Credentials file not found"
}
```

---

## 🐛 اگر مشکل پیش آمد

### خطا: "Invalid credentials"

```powershell
# 1. حذف token قدیم
dart pub token remove https://pub.dev

# 2. رفتن دوباره به Google
# https://myaccount.google.com/apppasswords
# Generate APP PASSWORD جدید

# 3. اضافه کردن دوباره
dart pub token add https://pub.dev
```

### خطا: "Building flutter tool..."

```powershell
# تنظیم variables و سعی مجدد
$env:FLUTTER_SKIP_UPDATE_CHECK = "true"
$env:FLUTTER_NO_ANALYTICS = "true"

# خالی کردن
flutter clean
dart pub cache clean

# تلاش دوباره
flutter pub get --verbose
```

### خطا: "Credentials directory not found"

```powershell
# ایجاد directory
$pubCache = "$env:USERPROFILE\.pub-cache"
if (!(Test-Path $pubCache)) {
    New-Item -ItemType Directory $pubCache -Force
}

# سعی مجدد
dart pub token add https://pub.dev
```

---

## 📊 خلاصه فرآیند

| مرحله | کنش | تخمین زمان |
|-------|------|----------|
| **1** | Google App Password | 5 دقیقه |
| **2** | `dart pub token add` | 1 دقیقه |
| **3** | `flutter pub get` | 2 دقیقه |
| **4** | `flutter build apk` | 15 دقیقه |
| **5** | `adb install` | 3 دقیقه |
| | **کل** | **~30 دقیقه** |

---

## ✨ نتیجه نهایی

### بعد از انجام موفق:

1. ✅ Flutter pub.dev متصل است
2. ✅ تمام dependencies دانلود شد
3. ✅ APK ساخته شد
4. ✅ APK روی گوشی نصب شد
5. ✅ اپ کار می‌کند! 🎉

---

## 🔗 مراجع

| منبع | URL |
|------|-----|
| Google Account Security | https://myaccount.google.com/security |
| App Passwords | https://myaccount.google.com/apppasswords |
| Flutter Docs | https://flutter.dev |
| Dart Pub | https://pub.dev |

---

## 📌 نکات مهم

1. **App Password ≠ Google Password**
   - App Password فقط برای pub.dev
   - رمز اصلی محفوظ است

2. **16 کاراکتر بدون فاصلہ**
   ```
   ✅ صحیح: abcdefghijklmnop
   ❌ اشتباه: abcd efgh ijkl mnop
   ```

3. **Token ذخیره می‌شود محلی**
   ```
   C:\Users\[USERNAME]\.pub-cache\credentials.json
   ```

4. **می‌توانید token را revoke کنید**
   - Google Account
   - App passwords
   - Remove app password

---

## 🚀 شروع کنید!

**اکنون:**

1. رفتن به: https://myaccount.google.com/apppasswords
2. ایجاد "flutter-pub" app password
3. Copy 16-char password
4. اجرای: `dart pub token add https://pub.dev`
5. وارد کردن email و password

**سپس:**

```bash
cd d:\AvicennaAI\mobile
flutter pub get
flutter build apk --release
```

**و اپ آماده است!** ✅

