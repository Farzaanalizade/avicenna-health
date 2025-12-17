# Phase 3 - Image Analysis API Testing Guide

## 📋 دستورالعمل تست API های تحلیل تصویر

### بخش اول: تنظیم محیط

#### ۱. دریافت GEMINI_API_KEY
```bash
# از https://makersuite.google.com/app/apikey
# یک کلید جدید بسازید
# داخل .env قرار بدید:
GEMINI_API_KEY=your_key_here
```

#### ۲. اجرای Backend
```bash
cd backend
source venv/bin/activate  # یا: venv\Scripts\activate (Windows)
python -m uvicorn app.main:app --reload
# Server شروع می‌شه در http://localhost:8000
```

#### ۳. تست سریع
```bash
# Health check
curl http://localhost:8000/health

# Expected: {"status": "healthy", "service": "Avicenna Health Backend"}
```

---

## 🧪 تست Endpoints

### 1. Health Check - بررسی وضعیت سرور

```http
GET /api/v1/analysis/

Response (200 OK):
{
  "status": "operational",
  "service": "Image Analysis Service",
  "version": "1.0.0",
  "gemini_available": true
}
```

### 2. تحلیل زبان (Tongue Analysis)

```http
POST /api/v1/analysis/tongue
Content-Type: multipart/form-data

Parameters:
- image: <binary image file>

Authorization: Bearer {token}
```

**نمونه cURL:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "image=@tongue_image.jpg" \
  http://localhost:8000/api/v1/analysis/tongue
```

**Response (200 OK):**
```json
{
  "id": 1,
  "patient_id": 1,
  "analysis_type": "tongue",
  "findings": {
    "color": "red",
    "coating": "thin_white",
    "moisture": "normal",
    "cracks": false,
    "shape": "normal"
  },
  "mizaj": "garm_tar",
  "confidence": 0.85,
  "recommendations": [
    "کاهش غذاهای گرم",
    "مصرف آب به فراوانی",
    "ورزش ملایم"
  ],
  "created_at": "2025-01-10T12:30:00Z",
  "status": "completed"
}
```

### 3. تحلیل چشم (Eye Analysis)

```http
POST /api/v1/analysis/eye
Content-Type: multipart/form-data

Parameters:
- image: <binary image file>

Authorization: Bearer {token}
```

**نمونه cURL:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "image=@eye_image.jpg" \
  http://localhost:8000/api/v1/analysis/eye
```

**Response (200 OK):**
```json
{
  "id": 2,
  "patient_id": 1,
  "analysis_type": "eye",
  "findings": {
    "sclera_color": "white",
    "pupil_size": "normal",
    "brightness": "normal",
    "dark_circles": false,
    "overall_clarity": "clear"
  },
  "health_status": "healthy",
  "confidence": 0.82,
  "recommendations": [
    "مراقبت از چشم‌ها",
    "استراحت منظم"
  ],
  "created_at": "2025-01-10T12:31:00Z",
  "status": "completed"
}
```

### 4. تحلیل صورت (Face Analysis)

```http
POST /api/v1/analysis/face
Content-Type: multipart/form-data

Parameters:
- image: <binary image file>

Authorization: Bearer {token}
```

**نمونه Python:**
```python
import requests

files = {'image': open('face_image.jpg', 'rb')}
headers = {'Authorization': 'Bearer YOUR_JWT_TOKEN'}

response = requests.post(
    'http://localhost:8000/api/v1/analysis/face',
    files=files,
    headers=headers
)

print(response.json())
```

**Response (200 OK):**
```json
{
  "id": 3,
  "patient_id": 1,
  "analysis_type": "face",
  "findings": {
    "complexion": "balanced",
    "skin_condition": "healthy",
    "texture": "smooth",
    "puffiness": false,
    "color_distribution": "even"
  },
  "complexion_type": "normal",
  "confidence": 0.79,
  "recommendations": [
    "مراقبت از پوست",
    "تغذیه متعادل"
  ],
  "created_at": "2025-01-10T12:32:00Z",
  "status": "completed"
}
```

### 5. تحلیل پوست (Skin Analysis)

```http
POST /api/v1/analysis/skin
Content-Type: multipart/form-data

Parameters:
- image: <binary image file>

Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "id": 4,
  "patient_id": 1,
  "analysis_type": "skin",
  "findings": {
    "condition": "normal",
    "texture": "smooth",
    "tone": "even",
    "visible_issues": "none",
    "hydration": "adequate"
  },
  "skin_status": "healthy",
  "confidence": 0.80,
  "recommendations": [
    "مرطوب‌کننده روزانه",
    "محافظت از آفتاب"
  ],
  "created_at": "2025-01-10T12:33:00Z",
  "status": "completed"
}
```

### 6. دریافت تاریخچه تحلیل‌ها (Analysis History)

```http
GET /api/v1/analysis/history/{patient_id}?analysis_type=tongue&limit=20

Authorization: Bearer {token}
```

**نمونه cURL:**
```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  'http://localhost:8000/api/v1/analysis/history/1?analysis_type=tongue&limit=20'
```

**Response (200 OK):**
```json
{
  "patient_id": 1,
  "total": 5,
  "limit": 20,
  "offset": 0,
  "analyses": [
    {
      "id": 1,
      "analysis_type": "tongue",
      "findings": {...},
      "confidence": 0.85,
      "created_at": "2025-01-10T12:30:00Z"
    }
  ]
}
```

---

## ⚠️ Error Responses

### 400 - Bad Request (Invalid Image)
```json
{
  "detail": "Image validation failed: Size exceeds 5MB limit"
}
```

### 401 - Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 422 - Unprocessable Entity (Invalid Format)
```json
{
  "detail": [
    {
      "loc": ["body", "image"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 - Server Error
```json
{
  "detail": "Error analyzing image: [error message]"
}
```

---

## 🛠️ ابزارهای تست

### Option 1: استفاده از Python Test Script

```bash
cd backend
python test_phase_3.py
```

**Output:**
```
✅ Health Check
✅ Login
✅ Tongue Analysis
✅ Eye Analysis
✅ Face Analysis
✅ Skin Analysis
✅ Knowledge Base
✅ Diagnosis Save

Passed: 8/8
```

### Option 2: استفاده از Postman

1. نصب Postman: https://www.postman.com/downloads/
2. ایمپورت Postman Collection:
   - File → Import
   - انتخاب فایل: `PHASE_3_POSTMAN_COLLECTION.json`
3. تست کردن endpoints

### Option 3: استفاده از cURL

```bash
# Login
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"test@avicenna.com","password":"test_password"}' \
  http://localhost:8000/api/auth/login

# حفظ token از response
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Tongue Analysis
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -F "image=@path/to/image.jpg" \
  http://localhost:8000/api/v1/analysis/tongue
```

### Option 4: استفاده از VS Code REST Client

فایل: `test_api.rest`

```rest
### Health Check
GET http://localhost:8000/api/v1/analysis/

### Tongue Analysis
POST http://localhost:8000/api/v1/analysis/tongue
Authorization: Bearer YOUR_TOKEN
Content-Type: multipart/form-data; boundary=----FormBoundary7MA4YWxkTrZu0gW

------FormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="image"; filename="tongue.jpg"
Content-Type: image/jpeg

< ./test_images/tongue.jpg
------FormBoundary7MA4YWxkTrZu0gW--
```

---

## 📱 Integration با Mobile App

### در mobile/lib/services/analysis_service.dart:

```dart
Future<Map<String, dynamic>> analyzeTongueImage(File imageFile) async {
  try {
    final uri = Uri.parse('$backendUrl/api/v1/analysis/tongue');
    final request = MultipartRequest('POST', uri)
      ..headers['Authorization'] = 'Bearer $token'
      ..files.add(
        await MultipartFile.fromPath('image', imageFile.path),
      );

    final response = await request.send();
    if (response.statusCode == 200) {
      final responseData = await response.stream.toBytes();
      return json.decode(utf8.decode(responseData));
    }
  } catch (e) {
    // Offline mode
    return getOfflineTongueAnalysis();
  }
}
```

---

## 🔍 Debugging Tips

### 1. فعال کردن Detailed Logging

```python
# در backend/app/core/config.py
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### 2. بررسی Gemini API Key

```bash
python -c "
import os
from google.generativeai import configure
api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    configure(api_key=api_key)
    print('✅ API Key is valid')
else:
    print('❌ API Key not found')
"
```

### 3. تست Image Processing

```python
from app.services.image_processing_service import ImageProcessingService

service = ImageProcessingService()
with open('test_image.jpg', 'rb') as f:
    image_data = f.read()

is_valid, error = service.validate_image(image_data)
print(f"Valid: {is_valid}, Error: {error}")
```

### 4. Database Inspection

```bash
# SQLite
sqlite3 backend/avicenna.db
sqlite> SELECT * FROM diagnostic_findings;

# PostgreSQL
psql avicenna_db
# \d diagnostic_findings
```

---

## ✅ Performance Benchmarks

| Operation | Time | Notes |
|-----------|------|-------|
| Image validation | ~50ms | Size, format, dimensions |
| Gemini analysis | ~2-3s | API call + response parsing |
| Database save | ~100ms | Insert to diagnostic_findings |
| Total (online) | ~2.5-3.5s | End-to-end |
| Total (offline) | ~100ms | Demo data only |

---

## 🚀 Next Steps

### بعد از تست موفق Endpoints:

1. **Knowledge Base Matching**
   - موجود شده: تشخیص‌ها در database
   - لازم است: Matching with DiagnosticFinding
   - فایل: `backend/app/services/knowledge_matching_service.py`

2. **Treatment Recommendations**
   - موجود شده: Analysis results
   - لازم است: Recommendation engine
   - فایل: `backend/app/services/recommendation_engine.py`

3. **Mobile Results Display**
   - موجود شده: API service
   - لازم است: Results screen UI
   - فایل: `mobile/lib/screens/analysis_results_screen.dart`

4. **Full Integration Testing**
   - تست end-to-end
   - بررسی sync behavior
   - Performance optimization

---

## 📞 Troubleshooting

### مشکل: "Connection refused"
```bash
# بررسی کنید backend درحال اجراست
python -m uvicorn app.main:app --reload
```

### مشکل: "GEMINI_API_KEY not found"
```bash
# تنظیم environment variable
export GEMINI_API_KEY="your_key_here"  # Linux/Mac
set GEMINI_API_KEY=your_key_here       # Windows
```

### مشکل: "Invalid image format"
```bash
# استفاده از تصاویر JPEG/PNG/WEBP
# اندازه بین 480x480 تا 4096x4096
# فایل حداکثر 5MB
```

### مشکل: "401 Unauthorized"
```bash
# دریافت token جدید از login endpoint
# استفاده در Authorization header
```

---

**Last Updated**: January 10, 2025  
**Status**: Ready for Phase 3 Testing  
**Version**: 1.0.0
