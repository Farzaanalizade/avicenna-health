# 🎯 راهنمای سریع اجرای Both (Backend + Mobile)

## ✅ وضعیت فعلی
- ✅ Backend Python: **3.14.0** - OK
- ✅ Backend FastAPI: **0.115.0** - OK
- ✅ Mobile Flutter: **3.38.3** - OK
- ✅ Mobile Dependencies: **Resolved** - OK
- ❌ Backend Server: **نیاز به manual start**
- ❌ Android Emulator: **نیاز به manual start**

---

## 🚀 اجرای Manual (ساده‌تر)

### 1️⃣ **منو Terminal یا CMD جدید باز کنید** 

```bash
Win + R
cmd
```

---

### 2️⃣ **Backend را شروع کنید:**

```bash
cd d:\AvicennaAI\backend
d:\AvicennaAI\backend\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

**منتظر بمانید تا ببینید:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

---

### 3️⃣ **Terminal دوم را باز کنید و Emulator راه بیندازید:**

```bash
cd d:\AvicennaAI\mobile
flutter emulators --launch Pixel_6_API_33
```

اگر emulator موجود نیست:
```bash
flutter emulators
```

این فهرست emulator‌های موجود را نشان می‌دهد.

---

### 4️⃣ **Terminal سوم - Mobile App:**

```bash
cd d:\AvicennaAI\mobile
flutter run
```

---

## 📊 نتیجه نهایی

**شما باید سه terminal دیدید:**

```
Terminal 1 - Backend:
✓ INFO: Uvicorn running on http://127.0.0.1:8000
✓ INFO: Application startup complete

Terminal 2 - Emulator:
✓ emulator: Waiting for emulator to start...
✓ emulator started

Terminal 3 - Mobile:
✓ Running lib/main.dart on emulator
✓ Flutter app is running
```

---

## 🧪 تست Connectivity

**Terminal 4 (optional):**

```bash
# Test Backend API
curl http://localhost:8000/docs

# یا در مرورگر:
http://localhost:8000/docs
```

---

## 🔗 Mobile → Backend Connection

**فایل config:**
- `mobile/lib/config/app_config.dart`

**بررسی کنید:**
```dart
static const String apiBaseUrl = 'http://10.0.2.2:8000';
```

✅ `10.0.2.2` = localhost از نظر Emulator
✅ `:8000` = Backend Port

---

## ⚠️ اگر مشکل پیش آمد

### Backend نمی‌شود شروع:

```bash
# مطمئن شوید venv در جای درست است
dir d:\AvicennaAI\backend\venv\Scripts\python.exe

# اگر خطا داد:
pip install -r requirements.txt
```

### Emulator نمی‌شود شروع:

```bash
# بررسی کنید emulator‌های موجود
flutter emulators

# یکی را انتخاب و راه بیندازید
flutter emulators --launch <name>
```

### Mobile بروی emulator نمی‌رود:

```bash
# ابتدا device متصل است؟
flutter devices

# اگر کاری نبود:
flutter clean
flutter pub get
flutter run
```

---

## 📌 نکات مهم

1. **هر Terminal جداگانه:**
   - Terminal 1: Backend فقط
   - Terminal 2: Emulator فقط
   - Terminal 3: Mobile فقط

2. **ترتیب اجرا:**
   - ابتدا Backend
   - سپس Emulator
   - آخر Mobile

3. **منتظر بمانید:**
   - Backend: 2-3 ثانیه
   - Emulator: 30-60 ثانیه
   - Mobile: 30-45 ثانیه

4. **Logs را دنبال کنید:**
   - Backend: در Terminal 1
   - Mobile: در Terminal 3

---

## 🎮 تست در Mobile App

**وقتی app روی emulator اجرا شد:**

1. **صفحه اول** - Splash screen
2. **صفحه دوم** - Auth/Login
3. **صفحه سوم** - Dashboard
4. **کلیک بر Diagnostic** → پالس وارد کنید → Submit

**نتیجه مورد انتظار:**
- ✅ API call به Backend
- ✅ Analysis نتیجه می‌دهد
- ✅ UI نتیجه را نشان می‌دهد

---

## 📞 Need Help?

**بررسی کنید:**
1. Backend running? `curl http://localhost:8000/docs`
2. Emulator running? `flutter devices`
3. Mobile app logs? `Terminal 3 output`
4. Network? `ping 10.0.2.2` (from emulator terminal)

---

**سفارش ویژه:** Terminal‌ها را **کنار هم** بگذارید تا logs را راحت‌تر ببینید! 🎯
