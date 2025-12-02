# 🧪 راهنمای تست API Endpoints

## 📋 فهرست مطالب

1. [تست Authentication](#تست-authentication)
2. [تست تحلیل زبان](#تست-تحلیل-زبان)
3. [تست تحلیل چشم](#تست-تحلیل-چشم)
4. [استفاده از Swagger UI](#استفاده-از-swagger-ui)

---

## 🔐 تست Authentication

### 1. ثبت‌نام (Register)

#### با cURL:

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"full_name\": \"علی احمدی\",
    \"email\": \"ali@example.com\",
    \"password\": \"password123\",
    \"date_of_birth\": \"1990-01-15\",
    \"gender\": \"male\",
    \"phone_number\": \"09123456789\",
    \"mizaj_type\": \"motadel\",
    \"medical_history\": \"سابقه بیماری خاصی ندارد\",
    \"lifestyle_info\": \"ورزش منظم، رژیم متعادل\"
  }"
```

**⚠️ توجه:** در Windows PowerShell از `\"` استفاده کنید نه `'`

**مقادیر معتبر برای enum ها:**
- `gender`: `"male"`, `"female"`, `"other"`
- `mizaj_type`: `"garm"`, `"sard"`, `"tar"`, `"khoshk"`, `"garm_tar"`, `"garm_khoshk"`, `"sard_tar"`, `"sard_khoshk"`, `"motadel"`

#### با Python (requests):

```python
import requests

url = "http://localhost:8000/api/auth/register"

# داده‌های حداقل (فقط فیلدهای اجباری)
data_minimal = {
    "full_name": "علی احمدی",
    "email": "ali@example.com",
    "password": "password123"
}

# داده‌های کامل
data_full = {
    "full_name": "علی احمدی",
    "email": "ali@example.com",
    "password": "password123",
    "date_of_birth": "1990-01-15",  # فرمت: YYYY-MM-DD
    "gender": "male",  # مقادیر معتبر: "male", "female", "other"
    "phone_number": "09123456789",
    "mizaj_type": "motadel",  # مقادیر معتبر: "garm", "sard", "tar", "khoshk", "garm_tar", "garm_khoshk", "sard_tar", "sard_khoshk", "motadel"
    "medical_history": "سابقه بیماری خاصی ندارد",
    "lifestyle_info": "ورزش منظم، رژیم متعادل"
}

# استفاده از داده‌های حداقل
response = requests.post(url, json=data_minimal)
print(f"Status Code: {response.status_code}")
if response.status_code != 200:
    print(f"Error: {response.text}")
else:
    print(response.json())
```

#### پاسخ موفق:

```json
{
  "id": 1,
  "full_name": "علی احمدی",
  "email": "ali@example.com",
  "date_of_birth": "1990-01-15",
  "gender": "male",
  "phone_number": "09123456789",
  "mizaj_type": "motadel",
  "medical_history": "سابقه بیماری خاصی ندارد",
  "lifestyle_info": "ورزش منظم، رژیم متعادل",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00"
}
```

---

### 2. ورود (Login)

#### با cURL:

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "ali@example.com",
    "password": "password123"
  }'
```

#### با Python:

```python
import requests

url = "http://localhost:8000/api/auth/login"
data = {
    "email": "ali@example.com",
    "password": "password123"
}

response = requests.post(url, json=data)
result = response.json()

if response.status_code == 200:
    token = result["access_token"]
    print(f"✅ Login successful!")
    print(f"Token: {token[:50]}...")
    print(f"Patient: {result['patient']}")
else:
    print(f"❌ Login failed: {result}")
```

#### پاسخ موفق:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "patient": {
    "id": 1,
    "full_name": "علی احمدی",
    "email": "ali@example.com",
    "mizaj_type": "motadel"
  }
}
```

**⚠️ مهم:** این `access_token` را برای تست endpoint های دیگر ذخیره کنید!

---

## 👅 تست تحلیل زبان

### آماده‌سازی تصویر

ابتدا باید یک تصویر زبان را به base64 تبدیل کنید:

#### با Python:

```python
import base64
import requests

# خواندن تصویر و تبدیل به base64
with open("tongue_image.jpg", "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

# دریافت token از login
login_url = "http://localhost:8000/api/auth/login"
login_data = {
    "email": "ali@example.com",
    "password": "password123"
}
login_response = requests.post(login_url, json=login_data)
token = login_response.json()["access_token"]

# ارسال برای تحلیل
url = "http://localhost:8000/api/health/tongue/analyze"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
data = {
    "image_base64": image_base64,
    "metadata": {
        "filename": "tongue_image.jpg",
        "timestamp": "2024-01-15T10:30:00"
    }
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

#### با cURL:

```bash
# ابتدا تصویر را به base64 تبدیل کنید (در Linux/Mac)
IMAGE_BASE64=$(base64 -i tongue_image.jpg)

# یا در Windows PowerShell:
$imageBytes = [System.IO.File]::ReadAllBytes("tongue_image.jpg")
$imageBase64 = [System.Convert]::ToBase64String($imageBytes)

# سپس ارسال کنید
curl -X POST "http://localhost:8000/api/health/tongue/analyze" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"image_base64\": \"$IMAGE_BASE64\",
    \"metadata\": {
      \"filename\": \"tongue_image.jpg\"
    }
  }"
```

#### آپلود مستقیم فایل:

```python
import requests

# دریافت token
login_response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={"email": "ali@example.com", "password": "password123"}
)
token = login_response.json()["access_token"]

# آپلود فایل
url = "http://localhost:8000/api/health/tongue/upload"
headers = {"Authorization": f"Bearer {token}"}

with open("tongue_image.jpg", "rb") as f:
    files = {"file": ("tongue_image.jpg", f, "image/jpeg")}
    response = requests.post(url, headers=headers, files=files)

print(response.json())
```

#### پاسخ نمونه:

```json
{
  "color": "صورتی",
  "coating": "نازک",
  "cracks": "خیر",
  "humidity": "نرمال",
  "avicenna_diagnosis": "مزاج: معتدل",
  "recommendations": {
    "immediate": [
      "مصرف غذاهای متعادل",
      "نوشیدن آب کافی"
    ],
    "lifestyle": [],
    "dietary": []
  }
}
```

---

## 👁️ تست تحلیل چشم

### با Python:

```python
import base64
import requests

# خواندن تصویر چشم
with open("eye_image.jpg", "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

# دریافت token
login_response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={"email": "ali@example.com", "password": "password123"}
)
token = login_response.json()["access_token"]

# ارسال برای تحلیل
url = "http://localhost:8000/api/health/eye/analyze"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
data = {
    "image_base64": image_base64,
    "metadata": {
        "filename": "eye_image.jpg"
    }
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### با cURL:

```bash
# تبدیل تصویر به base64
IMAGE_BASE64=$(base64 -i eye_image.jpg)

curl -X POST "http://localhost:8000/api/health/eye/analyze" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"image_base64\": \"$IMAGE_BASE64\",
    \"metadata\": {
      \"filename\": \"eye_image.jpg\"
    }
  }"
```

### آپلود مستقیم:

```python
import requests

token = "YOUR_ACCESS_TOKEN"  # از login دریافت کنید

url = "http://localhost:8000/api/health/eye/upload"
headers = {"Authorization": f"Bearer {token}"}

with open("eye_image.jpg", "rb") as f:
    files = {"file": ("eye_image.jpg", f, "image/jpeg")}
    response = requests.post(url, headers=headers, files=files)

print(response.json())
```

#### پاسخ نمونه:

```json
{
  "iris_color": "قهوه‌ای",
  "sclera_condition": "سفید",
  "avicenna_diagnosis": "وضعیت صلبیه: سفید",
  "recommendations": {
    "immediate": [],
    "lifestyle": [],
    "medical": []
  }
}
```

---

## 🌐 استفاده از Swagger UI

ساده‌ترین روش تست، استفاده از Swagger UI است:

### دسترسی:
1. سرور را اجرا کنید: `uvicorn run:app --reload`
2. به آدرس بروید: http://localhost:8000/docs
3. در صفحه Swagger UI:

#### تست Register:
1. روی `/api/auth/register` کلیک کنید
2. روی "Try it out" کلیک کنید
3. داده‌های نمونه را وارد کنید:
```json
{
  "full_name": "علی احمدی",
  "email": "ali@example.com",
  "password": "password123",
  "mizaj_type": "motadel"
}
```
4. روی "Execute" کلیک کنید

#### تست Login:
1. روی `/api/auth/login` کلیک کنید
2. "Try it out" را بزنید
3. ایمیل و رمز عبور را وارد کنید
4. Token را از پاسخ کپی کنید

#### تست Tongue Analysis:
1. ابتدا Login کنید و Token را دریافت کنید
2. در بالای صفحه Swagger، روی "Authorize" کلیک کنید
3. Token را وارد کنید (با فرمت: `Bearer YOUR_TOKEN`)
4. روی `/api/health/tongue/analyze` کلیک کنید
5. "Try it out" را بزنید
6. تصویر را به base64 تبدیل کرده و وارد کنید
   - یا از `/api/health/tongue/upload` استفاده کنید

---

## 📝 اسکریپت تست کامل (Python)

فایل `test_api.py` را ایجاد کنید:

```python
import requests
import base64
import json

BASE_URL = "http://localhost:8000"

def test_register():
    """تست ثبت‌نام"""
    url = f"{BASE_URL}/api/auth/register"
    data = {
        "full_name": "تست کاربر",
        "email": "test@example.com",
        "password": "test123456",
        "mizaj_type": "motadel"
    }
    response = requests.post(url, json=data)
    print("✅ Register:", response.status_code)
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json() if response.status_code == 200 else None

def test_login(email, password):
    """تست ورود"""
    url = f"{BASE_URL}/api/auth/login"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    print("✅ Login:", response.status_code)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"Token: {token[:50]}...")
        return token
    return None

def test_tongue_analyze(token, image_path):
    """تست تحلیل زبان"""
    # تبدیل تصویر به base64
    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    url = f"{BASE_URL}/api/health/tongue/analyze"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "image_base64": image_base64,
        "metadata": {"filename": image_path}
    }
    
    response = requests.post(url, json=data, headers=headers)
    print("✅ Tongue Analyze:", response.status_code)
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json() if response.status_code == 200 else None

def test_eye_analyze(token, image_path):
    """تست تحلیل چشم"""
    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    url = f"{BASE_URL}/api/health/eye/analyze"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "image_base64": image_base64,
        "metadata": {"filename": image_path}
    }
    
    response = requests.post(url, json=data, headers=headers)
    print("✅ Eye Analyze:", response.status_code)
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.json() if response.status_code == 200 else None

if __name__ == "__main__":
    print("🧪 شروع تست API...\n")
    
    # تست Register
    user = test_register()
    print()
    
    if user:
        # تست Login
        token = test_login("test@example.com", "test123456")
        print()
        
        if token:
            # تست Tongue (اگر تصویر دارید)
            # test_tongue_analyze(token, "tongue_image.jpg")
            
            # تست Eye (اگر تصویر دارید)
            # test_eye_analyze(token, "eye_image.jpg")
            pass
```

اجرا:
```bash
cd backend
python test_api.py
```

---

## ⚠️ نکات مهم

1. **Token Expiration:** Token ها بعد از 7 روز منقضی می‌شوند (قابل تنظیم در config)

2. **Image Size:** حداکثر اندازه تصویر 5MB است

3. **Image Format:** فرمت‌های مجاز:
   - JPEG (.jpg, .jpeg)
   - PNG (.png)
   - WebP (.webp)

4. **Base64 Encoding:** مطمئن شوید که base64 string کامل است (شامل prefix `data:image/jpeg;base64,` نیست)

5. **Error Handling:** همیشه status code را چک کنید:
   - `200`: موفق
   - `400`: خطای درخواست
   - `401`: نیاز به authentication
   - `404`: یافت نشد
   - `500`: خطای سرور

---

## 🔍 Debug Tips

اگر خطا دیدید:

1. **401 Unauthorized:**
   - Token را دوباره دریافت کنید
   - مطمئن شوید header به درستی ارسال می‌شود: `Authorization: Bearer TOKEN`

2. **400 Bad Request:**
   - فرمت JSON را چک کنید
   - فیلدهای اجباری را بررسی کنید

3. **500 Internal Server Error:**
   - لاگ‌های سرور را بررسی کنید
   - مطمئن شوید Gemini API Key تنظیم شده است

---

**آخرین بروزرسانی: 2024**

