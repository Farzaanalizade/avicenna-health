# 🚀 راهنمای راه‌اندازی سرور

## ✅ مشکلات حل شده

تمام مشکلات circular import و startup errors برطرف شده‌اند:

1. ✅ Circular import بین models و schemas - حل شد با ایجاد `enums.py`
2. ✅ Import paths نادرست - همه به مسیرهای صحیح تغییر یافتند
3. ✅ Config files تکراری - یکپارچه شدند
4. ✅ Missing model imports - اضافه شدند

## 🏃 راه‌اندازی سرور

### روش 1: با uvicorn مستقیم

```bash
cd backend
uvicorn app.main:app --reload
```

### روش 2: با run command

```bash
cd backend
uvicorn run:app --reload
```

### روش 3: با Python مستقیم

```bash
cd backend
python -m uvicorn app.main:app --reload
```

## 📋 پیش‌نیازها

1. **Virtual Environment فعال باشد:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **Dependencies نصب شده باشند:**
```bash
pip install -r requirements.txt
```

3. **فایل .env (اختیاری):**
```env
DATABASE_URL=sqlite:///./avicenna.db
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
```

## 🔍 بررسی مشکلات احتمالی

### اگر خطای Import دیدید:

1. **مطمئن شوید virtual environment فعال است**
2. **Dependencies را دوباره نصب کنید:**
   ```bash
   pip install -r requirements.txt
   ```

### اگر خطای Database دیدید:

1. **مطمئن شوید فایل database ایجاد می‌شود:**
   - SQLite: `avicenna.db` در پوشه `backend`
   - PostgreSQL: اتصال صحیح باشد

### اگر خطای Config دیدید:

1. **بررسی کنید `app/core/config.py` وجود دارد**
2. **بررسی کنید `.env` در پوشه `backend` است (اختیاری)**

## ✅ تست سرور

بعد از راه‌اندازی، سرور باید در آدرس زیر در دسترس باشد:

- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## 📝 لاگ‌های موفقیت‌آمیز

وقتی سرور با موفقیت راه‌اندازی شود، باید این پیام‌ها را ببینید:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
🔑 SECRET_KEY loaded: your-secre...
```

## 🐛 Debug Mode

برای debug بیشتر:

```bash
uvicorn app.main:app --reload --log-level debug
```

## 📚 مستندات بیشتر

- [FIXES_APPLIED.md](./FIXES_APPLIED.md) - جزئیات تمام تغییرات
- [README.md](../README.md) - راهنمای اصلی پروژه

