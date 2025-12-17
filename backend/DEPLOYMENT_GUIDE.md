# راهنمای اجرا و استقرار سیستم Avicenna AI

## پیش‌نیازها

### Backend
- Python 3.9+
- PostgreSQL یا SQLite
- pip (Package manager for Python)

### Mobile
- Flutter SDK 3.0+
- Android Studio یا Xcode
- Dart 3.0+

## نصب Backend

### ۱. نصب وابستگی‌ها
```bash
cd backend
pip install -r requirements.txt
```

### ۲. تنظیم متغیرهای محیطی
```bash
# ایجاد فایل .env
cat > .env << EOF
DATABASE_URL=postgresql://user:password@localhost/avicenna_db
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:8100"]
DEBUG=True
EOF
```

### ۳. ایجاد پایگاه داده
```bash
python -m alembic upgrade head
```

یا اگر Alembic راه‌اندازی نشده:
```bash
python backend/app/database.py
```

### ۴. پر کردن داده‌های اولیه
```bash
python backend/seed_data.py
python backend/seed_extended_data.py
```

### ۵ اجرای سرور
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

سرور در `http://localhost:8000` اجرا می‌شود

## نصب Mobile

### ۱. تنظیم Flutter
```bash
cd mobile
flutter pub get
```

### ۲. تنظیم API Server
```dart
// lib/config/app_config.dart
class AppConfig {
  static const String apiBaseUrl = 'http://your-server:8000/api/v1';
}
```

### ۳ اجرا روی شبیه‌ساز
```bash
flutter run
```

### ۴ ساخت APK
```bash
flutter build apk --release
```

## ساختار فایل‌ها

```
avicenna-health/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── avicenna_diagnosis.py      # مدل‌های تشخیصی
│   │   │   ├── avicenna_diseases.py       # مدل‌های بیماری
│   │   │   └── patient.py
│   │   ├── services/
│   │   │   ├── avicenna_analysis.py       # موتور تحلیل
│   │   │   ├── image_analysis.py          # تحلیل تصاویر
│   │   │   └── personalized_recommendations.py
│   │   ├── routers/
│   │   │   ├── avicenna_diagnosis.py      # API روتر تشخیصی
│   │   │   ├── avicenna_diseases.py       # API روتر بیماری
│   │   │   └── analysis_service.py        # API روتر تحلیل
│   │   ├── crud/
│   │   ├── schemas/
│   │   └── main.py                        # FastAPI app
│   ├── seed_data.py                       # داده‌های اولیه
│   ├── seed_extended_data.py              # داده‌های گسترده
│   ├── requirements.txt
│   └── AVICENNA_DATABASE_GUIDE.md         # مستندات پایگاه داده
│
├── mobile/
│   ├── lib/
│   │   ├── screens/
│   │   │   ├── diagnostic_screen.dart      # صفحه تشخیصی
│   │   │   ├── personalized_plan_screen.dart
│   │   │   └── home/
│   │   ├── services/
│   │   │   └── api_service.dart
│   │   └── main.dart
│   └── pubspec.yaml
│
└── docs/
    ├── AVICENNA_DATABASE_GUIDE.md         # مستندات پایگاه داده
    └── SERVICES_DOCUMENTATION.md          # مستندات سرویس‌ها
```

## API Endpoints اصلی

### تشخیصی
- `POST /api/v1/diagnosis/pulse` - ثبت نبض
- `POST /api/v1/diagnosis/urine` - ثبت ادرار
- `POST /api/v1/diagnosis/tongue` - ثبت زبان
- `GET /api/v1/diagnosis/report/patient/{id}` - گزارش تشخیصی

### بیماری و درمان
- `GET /api/v1/diseases` - لیست بیماری‌ها
- `GET /api/v1/remedies/disease/{id}` - درمان‌های بیماری
- `GET /api/v1/symptoms/disease/{id}` - علائم بیماری

### تحلیل و توصیه
- `POST /api/v1/analysis/comprehensive/{id}` - تحلیل جامع
- `GET /api/v1/analysis/personalized-plan/{id}` - برنامه درمانی
- `POST /api/v1/analysis/analyze-tongue-image/{id}` - تحلیل تصویر زبان
- `POST /api/v1/analysis/analyze-eye-image/{id}` - تحلیل تصویر چشم
- `GET /api/v1/analysis/full-report/{id}` - گزارش جامع

## Docker Deployment

### Dockerfile Backend
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: avicenna_db
      POSTGRES_USER: avicenna
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://avicenna:secure_password@db:5432/avicenna_db

volumes:
  postgres_data:
```

### اجرا
```bash
docker-compose up -d
```

## بهینه‌سازی و تنظیم

### حداکثر کردن کارایی
```python
# app/core/config.py
class Settings:
    # Cache settings
    CACHE_TTL = 3600
    
    # Database
    DATABASE_POOL_SIZE = 20
    DATABASE_MAX_OVERFLOW = 40
    
    # Async
    ASYNC_WORKERS = 4
```

### مانیتورینگ
```bash
# نصب tools
pip install prometheus-client
pip install sentry-sdk

# مانیتور کردن
from prometheus_client import Counter, Histogram
```

## Troubleshooting

### خطای اتصال به پایگاه داده
```bash
# بررسی اتصال PostgreSQL
psql -U user -d avicenna_db -h localhost

# یا استفاده از SQLite برای توسعه
DATABASE_URL=sqlite:///./test.db
```

### خطای تصویر
```python
# بررسی فولدر uploads
import os
os.makedirs("uploads/diagnostic_images", exist_ok=True)
```

### خطای محرمانگی CORS
```python
# بروزرسانی ALLOWED_ORIGINS
ALLOWED_ORIGINS = ["http://localhost:8100", "http://your-domain.com"]
```

## تست API

### استفاده از Postman
1. Import `avicenna-api.postman_collection.json`
2. تنظیم متغیرهای محیط
3. اجرای requests

### استفاده از curl
```bash
# تحلیل جامع
curl -X POST http://localhost:8000/api/v1/analysis/comprehensive/1 \
  -H "Content-Type: application/json" \
  -d '{
    "pulse_data": {"pulse_rate": 72},
    "urine_data": {"color": "zard"},
    "tongue_data": {"body_color": "pink"}
  }'

# دریافت برنامه درمانی
curl http://localhost:8000/api/v1/analysis/personalized-plan/1
```

## بروزرسانی و نگهداری

### اجرای Migrations
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### پشتیبان‌گیری از پایگاه داده
```bash
# PostgreSQL
pg_dump avicenna_db > backup.sql

# SQLite
cp test.db backup.db
```

### بازیابی از پشتیبان
```bash
# PostgreSQL
psql avicenna_db < backup.sql

# SQLite
cp backup.db test.db
```

## منابع اضافی

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flutter Documentation](https://flutter.dev/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
