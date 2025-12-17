# 🚀 راهنمای اجرای Backend + Mobile - گام به گام

## 📱 مرحله 1: Android Emulator راه بیندازید

### گزینه A: از Android Studio
```
1. Android Studio را باز کنید
2. Tools → Device Manager
3. یک device انتخاب کنید (یا ایجاد کنید)
4. بر روی ▶️ کلیک کنید
```

### گزینه B: از Terminal
```bash
# فهرست emulator‌های موجود
flutter emulators

# Pixel 6 را اگر موجود است راه بیندازید
flutter emulators --launch Pixel_6_API_33

# یا هر emulator دیگری را:
flutter emulators --launch <emulator_name>
```

---

## 🖥️ مرحله 2: Backend Server راه بیندازید

### Terminal 1 (Backend)

```bash
# به پوشه backend برید
cd d:\AvicennaAI\backend

# Virtual environment را فعال کنید
.\venv\Scripts\Activate.ps1

# ستقیم دستور را اجرا کنید (بدون powershell wrapper)
set PYTHONPATH=d:\AvicennaAI\backend
python -m uvicorn app.main:app --reload --port 8000
```

**یا اگر خطا داد:**

```bash
cd d:\AvicennaAI\backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

**انتظار بکشید تا:**
```
✓ Application startup complete [uvicorn]
✓ Uvicorn running on http://127.0.0.1:8000
```

---

## 📲 مرحله 3: Mobile App را اجرا کنید

### Terminal 2 (Mobile)

```bash
# به پوشه mobile برید
cd d:\AvicennaAI\mobile

# اپ را اجرا کنید
flutter run
```

**یا verbose mode برای دیباگ:**
```bash
flutter run -v
```

---

## ✅ تست اتصال

### هنگام اجرای Both:

**Terminal 3 (اختیاری - برای تست API)**
```bash
# API را تست کنید
curl http://localhost:8000/docs

# یا در مرورگر:
# http://localhost:8000/docs
```

---

## 🐛 معمولی Errors و حل‌ها

### ❌ Error: "Android SDK not found"
**حل:** Android Studio را نصب کنید یا مسیر SDK را تنظیم کنید:
```bash
flutter config --android-sdk <path-to-android-sdk>
```

### ❌ Error: "No emulator/device found"
**حل:** 
```bash
flutter emulators  # ببینید چه emulator‌هایی موجود است
flutter emulators --launch <name>  # یکی را راه بیندازید
```

### ❌ Error: Port 8000 in use
**حل:**
```bash
# پیدا کنید کدام process درحال استفاده است
netstat -ano | findstr :8000

# یا استفاده کنید از port دیگری
python -m uvicorn app.main:app --reload --port 8001
```

### ❌ Error: "Module not found"
**حل:**
```bash
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 🎯 چک‌لیست اجرا

```
☐ Android Emulator راه افتاده
☐ Backend port 8000 آماده است
☐ Swagger UI در http://localhost:8000/docs کار می‌کند
☐ Mobile app روی emulator اجرا می‌شود
☐ هیچ error در console نیست
```

---

## 📊 نتیجه مورد انتظار

```
Terminal 1 (Backend):
✓ INFO:     Uvicorn running on http://127.0.0.1:8000
✓ INFO:     Reload disabled.

Terminal 2 (Mobile):
✓ Flutter app running on device/emulator
✓ App displays correctly
✓ No console errors
```

---

## 💡 نکات مهم

1. **Terminal‌ها جداگانه بمانند**
   - Backend در Terminal 1
   - Mobile در Terminal 2

2. **اگر Backend restart شود**
   - Mobile خودکار reconnect می‌کند

3. **اگر Mobile crash کند**
   - Backend هنوز اجرا است
   - از Terminal 2 `flutter run` را دوباره اجرا کنید

4. **برای توقف**
   - Backend: `Ctrl+C` در Terminal 1
   - Mobile: `q` در Terminal 2

---

## 🚀 بعد از اجرا موفق

هنگامی که هر دو اجرا شدند:

1. **Backend API test کنید:**
   ```
   http://localhost:8000/docs
   ```

2. **Mobile app test کنید:**
   - Diagnostic screen باز کنید
   - داده‌های pulse وارد کنید
   - دکمه submit را بزنید
   - نتیجه را ببینید

3. **Check logs:**
   - Backend logs در Terminal 1
   - Mobile logs در Terminal 2

---

**اگر مشکل پیش آمد، این راهنمای خطاهای معمول را دنبال کنید!**
