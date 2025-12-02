# 🏥 Avicenna Health - Complete Healthcare AI System

**Combining Traditional Medicine with Modern AI**

## 📌 Project Overview

A comprehensive health monitoring system integrating:
- **Iranian Traditional Medicine** (Avicenna/Ibn Sina)
- **Chinese Traditional Medicine** (TCM)
- **Indian Traditional Medicine** (Ayurveda)
- **Modern Medicine**
- **AI & Machine Learning** (Google Gemini + Local Models)

## ✨ Key Features

- 🔍 **Tongue Analysis** - Assess constitutional type & health indicators
- 👁️ **Eye (Iris) Analysis** - Evaluate health from iris patterns
- 🎤 **Audio Analysis** - Analyze heartbeat, breathing, cough patterns
- 📊 **Sensor Integration** - Heart rate, SpO2, temperature, motion
- 🤖 **Intelligent Diagnosis** - Multi-modal data fusion & analysis
- 💡 **Personalized Recommendations** - Based on traditional medicine principles
- ⌚ **Smartwatch Support** - Bluetooth integration for wearables
- 📱 **Cross-platform App** - iOS & Android via Flutter

## 🚀 شروع سریع

### پیش‌نیازها

- Python 3.10+
- Node.js 18+ (برای Mobile App)
- PostgreSQL (اختیاری - SQLite به صورت پیش‌فرض)
- API Keys:
  - Google Gemini API Key (ضروری)
  - OpenAI API Key (اختیاری)
  - Anthropic API Key (اختیاری)

### نصب Backend

```bash
# Clone repository
git clone <repository-url>
cd AvicennaAI

# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API keys

# Run migrations (if using database)
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

### تنظیم .env

```env
# Database
DATABASE_URL=sqlite:///./avicenna.db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI APIs
GEMINI_API_KEY=your-gemini-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Application
DEBUG=True
```

### تست API

```bash
# Health check
curl http://localhost:8000/health

# API Documentation
open http://localhost:8000/docs
```

## 📁 ساختار پروژه

```
AvicennaAI/
├── backend/                 # Backend API (FastAPI)
│   ├── app/
│   │   ├── core/            # Core configurations
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── routers/         # API routes
│   │   ├── services/        # Business logic
│   │   │   ├── ai_service.py
│   │   │   ├── gemini_service.py
│   │   │   └── avicenna_knowledge.py
│   │   └── main.py
│   ├── requirements.txt
│   └── .env
├── mobile/                   # Mobile App (React Native)
│   ├── src/
│   │   ├── screens/
│   │   ├── components/
│   │   ├── services/
│   │   └── store/
│   └── package.json
├── docs/                     # Documentation
├── ROADMAP.md               # نقشه راه کامل
├── AI_APIS_COMPARISON.md    # مقایسه API های AI
├── IMPLEMENTATION_GUIDE.md  # راهنمای پیاده‌سازی
└── README.md                # این فایل
```

## 📚 مستندات

- [🗺️ نقشه راه کامل](./ROADMAP.md) - مراحل توسعه و Timeline
- [🤖 مقایسه API های هوش مصنوعی](./AI_APIS_COMPARISON.md) - انتخاب بهترین API
- [📘 راهنمای پیاده‌سازی](./IMPLEMENTATION_GUIDE.md) - راهنمای کامل کدنویسی

## 🔧 تکنولوژی‌ها

### Backend
- **FastAPI** - Framework اصلی
- **SQLAlchemy** - ORM
- **PostgreSQL/SQLite** - Database
- **Pydantic** - Validation
- **JWT** - Authentication

### AI/ML
- **Google Gemini 1.5 Flash** - تحلیل تصاویر (Primary)
- **OpenAI GPT-4 Vision** - تحلیل پیشرفته (Secondary)
- **Anthropic Claude** - تحلیل متنی (Tertiary)

### Mobile
- **React Native** - Framework
- **TypeScript** - Language
- **Redux Toolkit** - State Management

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - ثبت نام
- `POST /api/auth/login` - ورود

### Health Analysis
- `POST /api/health/tongue/analyze` - تحلیل زبان
- `POST /api/health/eye/analyze` - تحلیل چشم
- `POST /api/health/voice/analyze` - تحلیل صدا
- `POST /api/health/audio/analyze` - تحلیل صوت (قلب/تنفس)
- `POST /api/health/vital-signs` - ثبت علائم حیاتی
- `GET /api/health/report` - گزارش جامع سلامت

## 🎯 وضعیت پروژه

### ✅ تکمیل شده
- [x] ساختار Backend
- [x] Authentication & Authorization
- [x] Database Models
- [x] API Routes
- [x] سرویس Gemini AI
- [x] پایگاه دانش طب سنتی (مقدماتی)
- [x] تحلیل تصویر زبان (با Gemini)
- [x] تحلیل تصویر چشم (با Gemini)

### 🚧 در حال توسعه
- [ ] تحلیل صدا (قلب و تنفس)
- [ ] اتصال به سنسورها
- [ ] Mobile App
- [ ] تکمیل پایگاه دانش

### 📋 برنامه‌ریزی شده
- [ ] مدل‌های ML Custom
- [ ] Web Frontend
- [ ] Integration با Smartwatch
- [ ] Telemedicine Features

## 🤝 مشارکت

برای مشارکت در پروژه:

1. Fork کنید
2. Branch جدید بسازید (`git checkout -b feature/AmazingFeature`)
3. Commit کنید (`git commit -m 'Add some AmazingFeature'`)
4. Push کنید (`git push origin feature/AmazingFeature`)
5. Pull Request باز کنید

## ⚠️ نکات مهم

1. **این سیستم تشخیص نیست** - فقط کمک‌کننده است
2. **همیشه با پزشک مشورت کنید** - برای تشخیص نهایی
3. **حریم خصوصی** - تمام داده‌ها رمزگذاری می‌شوند
4. **امنیت** - از HTTPS استفاده کنید

## 📝 مجوز

این پروژه تحت مجوز MIT است.

## 📧 تماس

برای سوالات و پیشنهادات:
- Email: [your-email@example.com]
- GitHub Issues: [repository-url]/issues

---

**ساخته شده با ❤️ برای سلامتی همه**

