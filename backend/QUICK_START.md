# Quick Start Guide - راهنمای شروع سریع

## 5 دقیقه برای اجرای سریع

### Step 1: نصب Backend (2 دقیقه)
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: پر کردن داده‌ها (1 دقیقه)
```bash
python seed_data.py
python seed_extended_data.py
```

### Step 3: اجرای سرور (1 دقیقه)
```bash
python -m uvicorn app.main:app --reload
```

سرور شروع می‌شود: `http://localhost:8000`

### Step 4: تست API (1 دقیقه)

```bash
# API Documentation
# Open browser: http://localhost:8000/docs

# یا استفاده از curl:
curl -X GET http://localhost:8000/api/v1/diseases
```

---

## اجرای Mobile

### نصب Flutter
```bash
cd mobile
flutter pub get
flutter run
```

---

## ساختار پایگاه داده

### Pulse Analysis (تحلیل نبض)
```
نبض: 60-90 bpm (طبیعی)
نوع: دقیق، منتظم، کم‌زور
مزاج: گرم/سرد، خشک/تر
```

### Urine Analysis (تحلیل ادرار)
```
رنگ: زرد، قرمز، سیاه
کثافت: سبک، متوسط، سنگین
علائم: صدور بلور، خون، چربی
```

### Tongue Analysis (تحلیل زبان)
```
رنگ: صورتی، سرخ، سفید
پوشش: لیس، سفید، زرد
رطوبت: خشک، معمولی، مرطوب
```

---

## مثال‌های استفاده

### 1. تحلیل جامع
```bash
curl -X POST http://localhost:8000/api/v1/analysis/comprehensive/1 \
  -H "Content-Type: application/json" \
  -d '{
    "pulse_data": {
      "pulse_rate": 72,
      "type": "daqiq",
      "rhythm": "montazem",
      "strength": "motavassset",
      "temperature_sensation": "normal",
      "depth": "surface",
      "width": "normal"
    },
    "urine_data": {
      "color": "zard",
      "density": "motavassset",
      "clarity": "roshan"
    },
    "tongue_data": {
      "body_color": "pink",
      "coating_color": "white",
      "coating_thickness": "thin",
      "moisture": "normal"
    }
  }'
```

### 2. دریافت برنامه درمانی
```bash
curl http://localhost:8000/api/v1/analysis/personalized-plan/1
```

### 3. دریافت برنامه غذایی
```bash
curl http://localhost:8000/api/v1/analysis/dietary-plan/1
```

### 4. دریافت جدول هفتگی
```bash
curl http://localhost:8000/api/v1/analysis/weekly-schedule/1
```

---

## Database Models

### Patient (بیمار)
- `id`, `name`, `age`, `gender`
- `date_of_birth`, `blood_type`
- `medical_history`, `created_at`

### Pulse Analysis (تحلیل نبض)
- `patient_id`, `pulse_rate`, `type`
- `rhythm`, `strength`, `temperature`
- `depth`, `width`, `mizaj_indicators`

### Urine Analysis (تحلیل ادرار)
- `patient_id`, `color`, `density`
- `clarity`, `sediment`, `abnormalities`
- `mizaj_indicators`

### Tongue Analysis (تحلیل زبان)
- `patient_id`, `body_color`, `coating_color`
- `coating_thickness`, `moisture`, `texture`
- `organ_indicators`, `disease_markers`

### Diagnostic Finding (یافته‌ تشخیصی)
- `patient_id`, `pulse_analysis_id`
- `urine_analysis_id`, `tongue_analysis_id`
- `dominant_mizaj`, `health_status`
- `treatment_recommendations`

### Disease (بیماری)
- `id`, `name_persian`, `name_english`
- `category`, `mizaj_type`
- `organ_affected`, `description`

### Remedy (درمان)
- `id`, `name_persian`, `name_english`
- `type`, `ingredients`, `preparation`
- `dosage`, `duration`, `mizaj_effects`

---

## Swagger/OpenAPI Documentation

```
http://localhost:8000/docs
```

تمام endpoints را با مثال‌ها دیده می‌توانید.

---

## خطاها و حل‌ها

### Error: `ModuleNotFoundError`
```bash
pip install -r requirements.txt
```

### Error: `Database connection error`
```bash
# بررسی PostgreSQL یا استفاده از SQLite:
# تغییر DATABASE_URL در .env
DATABASE_URL=sqlite:///./test.db
```

### Error: `CORS error`
```python
# بروزرسانی app/core/config.py
ALLOWED_ORIGINS = ["http://localhost:8100"]
```

---

## فولدرهای مهم

```
backend/
├── app/
│   ├── models/          # Database Models
│   ├── schemas/         # Request/Response Schemas
│   ├── routers/         # API Routes
│   ├── services/        # Business Logic
│   ├── crud/            # Database Operations
│   └── main.py          # FastAPI App
│
├── seed_data.py         # اولیه‌سازی پایگاه داده
└── requirements.txt     # وابستگی‌ها
```

---

## API Routes Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/diagnosis/pulse` | POST | ثبت نبض |
| `/api/v1/diagnosis/urine` | POST | ثبت ادرار |
| `/api/v1/diagnosis/tongue` | POST | ثبت زبان |
| `/api/v1/diseases` | GET | لیست بیماری‌ها |
| `/api/v1/remedies/disease/{id}` | GET | درمان‌های بیماری |
| `/api/v1/analysis/comprehensive/{id}` | POST | تحلیل جامع |
| `/api/v1/analysis/personalized-plan/{id}` | GET | برنامه درمانی |
| `/api/v1/analysis/dietary-plan/{id}` | GET | برنامه غذایی |
| `/api/v1/analysis/weekly-schedule/{id}` | GET | جدول هفتگی |
| `/api/v1/analysis/full-report/{id}` | GET | گزارش جامع |

---

## بعدی؟

1. ✅ Backend راه‌اندازی شد
2. ✅ API Documentation آماده است
3. 👉 Mobile App را اتصال دهید
4. 👉 Seed Data را پر کنید
5. 👉 API را تست کنید
6. 👉 Frontend Integration را انجام دهید

دوست دارید که کدام بخش را بیشتر کار کنیم؟
