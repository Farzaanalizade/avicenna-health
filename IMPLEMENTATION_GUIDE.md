# 📘 راهنمای پیاده‌سازی کامل Avicenna AI

## 🎯 فهرست مطالب

1. [نصب و راه‌اندازی](#نصب-و-راه‌اندازی)
2. [پیکربندی](#پیکربندی)
3. [پیاده‌سازی Gemini API](#پیاده‌سازی-gemini-api)
4. [تکمیل سرویس AI](#تکمیل-سرویس-ai)
5. [تست و Debug](#تست-و-debug)
6. [Deployment](#deployment)

---

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

```bash
# Python 3.10+
python --version

# Node.js 18+ (برای Mobile)
node --version

# Git
git --version
```

### نصب Backend

```bash
cd backend

# ایجاد Virtual Environment
python -m venv venv

# فعال‌سازی (Windows)
venv\Scripts\activate

# فعال‌سازی (Linux/Mac)
source venv/bin/activate

# نصب پکیج‌ها
pip install -r requirements.txt

# ایجاد فایل .env
cp .env.example .env
```

### تنظیم .env

```env
# Database
DATABASE_URL=sqlite:///./avicenna.db
# یا برای PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/avicenna

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production-2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI APIs
GEMINI_API_KEY=your-gemini-api-key-here
OPENAI_API_KEY=your-openai-api-key-here  # اختیاری
ANTHROPIC_API_KEY=your-anthropic-api-key-here  # اختیاری

# Application
DEBUG=True
APP_NAME=Avicenna Health Monitor
APP_VERSION=1.0.0

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### راه‌اندازی سرور

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## ⚙️ پیکربندی

### ساختار فایل‌های پیکربندی

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py      # تنظیمات اصلی
│   │   ├── security.py     # امنیت
│   │   └── dependencies.py # Dependencies
│   └── ...
└── .env                    # متغیرهای محیطی
```

### بررسی پیکربندی

```python
# backend/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    DATABASE_URL: str = "sqlite:///./avicenna.db"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 🤖 پیاده‌سازی Gemini API

### ایجاد سرویس Gemini

```python
# backend/app/services/gemini_service.py
import google.generativeai as genai
from PIL import Image
import base64
import io
import json
import re
from typing import Dict, Any, Optional
from app.core.config import settings

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def analyze_tongue_image(self, image_base64: str) -> Dict[str, Any]:
        """تحلیل تصویر زبان با Gemini"""
        
        # Decode image
        try:
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
        except Exception as e:
            return {"error": f"خطا در پردازش تصویر: {str(e)}"}
        
        # Prompt برای تحلیل
        prompt = """
        شما یک متخصص طب سنتی ایرانی (بوعلی سینا) و چینی هستید.
        این تصویر زبان یک بیمار است. لطفاً با دقت تحلیل کنید.
        
        تحلیل موارد زیر:
        
        1. رنگ زبان (صورتی/قرمز/زرد/سفید/بنفش)
        2. پوشش زبان (نوع، ضخامت، درصد پوشش)
        3. بافت (ترک‌ها، لکه‌ها، تورم)
        4. رطوبت (خشک/نرمال/مرطوب)
        
        پاسخ را به صورت JSON دقیق بده:
        {
          "color": "رنگ اصلی",
          "coating": {
            "type": "نوع پوشش",
            "thickness": "ضخامت",
            "coverage_percentage": عدد
          },
          "texture": {
            "cracks": true/false,
            "spots": true/false,
            "swelling": true/false
          },
          "moisture": "وضعیت رطوبت",
          "mizaj_assessment": "مزاج احتمالی",
          "health_indicators": ["نشانه 1", "نشانه 2"],
          "recommendations": ["توصیه 1", "توصیه 2"],
          "confidence": 0.0-1.0
        }
        """
        
        try:
            response = self.model.generate_content([prompt, image])
            
            # استخراج JSON از پاسخ
            json_text = self._extract_json(response.text)
            if json_text:
                result = json.loads(json_text)
                return result
            else:
                return self._parse_text_response(response.text)
                
        except Exception as e:
            return {
                "error": f"خطا در تحلیل: {str(e)}",
                "color": "نامشخص",
                "coating": {"type": "نامشخص"},
                "mizaj_assessment": "نامشخص"
            }
    
    async def analyze_eye_image(self, image_base64: str) -> Dict[str, Any]:
        """تحلیل تصویر چشم"""
        # Similar implementation
        pass
    
    def _extract_json(self, text: str) -> Optional[str]:
        """استخراج JSON از متن"""
        # جستجوی JSON در متن
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if json_match:
            return json_match.group()
        return None
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """تبدیل پاسخ متنی به ساختار"""
        # Parse text response
        return {
            "color": "نامشخص",
            "coating": {"type": "نامشخص"},
            "mizaj_assessment": "نامشخص",
            "health_indicators": [],
            "recommendations": ["مشاوره با پزشک"]
        }
```

### اتصال به AIService

```python
# backend/app/services/ai_service.py
from app.services.gemini_service import GeminiService

class AIService:
    def __init__(self):
        self.tongue_analyzer = TongueAnalyzer()
        self.eye_analyzer = EyeAnalyzer()
        self.voice_analyzer = VoiceAnalyzer()
        self.gemini_service = GeminiService()  # اضافه کردن
    
    async def analyze_tongue(self, image_base64: str) -> Dict[str, Any]:
        """تحلیل زبان با Gemini"""
        
        # استفاده از Gemini برای تحلیل دقیق
        gemini_result = await self.gemini_service.analyze_tongue_image(image_base64)
        
        # ترکیب با تحلیل محلی
        local_analysis = self.tongue_analyzer.analyze_image(image_base64)
        
        # ترکیب نتایج
        return {
            "color": gemini_result.get("color") or local_analysis.get("color", {}).get("primary"),
            "coating": gemini_result.get("coating", {}).get("type") or local_analysis.get("coating", {}).get("type"),
            "cracks": "بله" if gemini_result.get("texture", {}).get("cracks") else "خیر",
            "humidity": gemini_result.get("moisture") or local_analysis.get("moisture"),
            "avicenna_diagnosis": f"مزاج: {gemini_result.get('mizaj_assessment', 'نامشخص')}",
            "recommendations": {
                "immediate": gemini_result.get("recommendations", []),
                "lifestyle": [],
                "dietary": []
            }
        }
```

---

## 🧪 تست و Debug

### تست API Endpoints

```bash
# تست Health Check
curl http://localhost:8000/health

# تست Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# تست تحلیل زبان (با token)
curl -X POST http://localhost:8000/api/health/tongue/analyze \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "BASE64_IMAGE_DATA"}'
```

### تست با Python

```python
# test_api.py
import requests
import base64

# Login
response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={"email": "test@example.com", "password": "password123"}
)
token = response.json()["access_token"]

# تحلیل زبان
with open("tongue_image.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()

response = requests.post(
    "http://localhost:8000/api/health/tongue/analyze",
    headers={"Authorization": f"Bearer {token}"},
    json={"image_base64": image_base64}
)

print(response.json())
```

### Debug Mode

```python
# فعال‌سازی logging
import logging
logging.basicConfig(level=logging.DEBUG)

# در کد
logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.error("Error message")
```

---

## 🚢 Deployment

### Docker

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/avicenna
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=avicenna
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Production Checklist

- [ ] تغییر SECRET_KEY
- [ ] استفاده از PostgreSQL
- [ ] فعال‌سازی HTTPS
- [ ] تنظیم CORS
- [ ] Backup Database
- [ ] Monitoring & Logging
- [ ] Rate Limiting
- [ ] Error Handling

---

## 📝 نکات مهم

1. **امنیت**: همیشه از HTTPS استفاده کنید
2. **Rate Limiting**: محدودیت درخواست‌ها
3. **Error Handling**: مدیریت خطاها
4. **Logging**: ثبت تمام فعالیت‌ها
5. **Testing**: تست کامل قبل از Production

---

**آخرین بروزرسانی: 2024**

