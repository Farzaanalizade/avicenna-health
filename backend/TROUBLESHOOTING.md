# 🔧 راهنمای رفع مشکلات (Troubleshooting)

## ❌ خطای 422 Unprocessable Content

### علت:
این خطا زمانی رخ می‌دهد که داده‌های ارسالی با schema تعریف شده مطابقت ندارند.

### راه‌حل:

#### 1. بررسی فیلدهای اجباری

فیلدهای **اجباری** برای Register:
- ✅ `full_name`: string (حداقل 1 کاراکتر)
- ✅ `email`: string با فرمت ایمیل معتبر
- ✅ `password`: string (حداقل 1 کاراکتر)

#### 2. بررسی مقادیر Enum

**Gender (جنسیت):**
- ✅ `"male"`
- ✅ `"female"`
- ✅ `"other"`

**MizajType (مزاج):**
- ✅ `"garm"` - گرم
- ✅ `"sard"` - سرد
- ✅ `"tar"` - تر
- ✅ `"khoshk"` - خشک
- ✅ `"garm_tar"` - گرم و تر
- ✅ `"garm_khoshk"` - گرم و خشک
- ✅ `"sard_tar"` - سرد و تر
- ✅ `"sard_khoshk"` - سرد و خشک
- ✅ `"motadel"` - معتدل (پیش‌فرض)

#### 3. بررسی فرمت تاریخ

فرمت صحیح: `YYYY-MM-DD`
- ✅ `"1990-01-15"`
- ❌ `"15/01/1990"`
- ❌ `"1990-1-15"` (باید با صفر باشد)

#### 4. مثال درست برای Register

```json
{
  "full_name": "علی احمدی",
  "email": "ali@example.com",
  "password": "password123"
}
```

یا با فیلدهای اختیاری:

```json
{
  "full_name": "علی احمدی",
  "email": "ali@example.com",
  "password": "password123",
  "date_of_birth": "1990-01-15",
  "gender": "male",
  "phone_number": "09123456789",
  "mizaj_type": "motadel"
}
```

### تست با Python:

```python
import requests

url = "http://localhost:8000/api/auth/register"

# تست 1: داده‌های حداقل (باید کار کند)
data1 = {
    "full_name": "تست کاربر",
    "email": "test@example.com",
    "password": "test123"
}

response1 = requests.post(url, json=data1)
print(f"Test 1 Status: {response1.status_code}")
if response1.status_code == 422:
    print(f"Validation Errors: {response1.json()}")

# تست 2: با enum اشتباه (باید خطا بدهد)
data2 = {
    "full_name": "تست کاربر",
    "email": "test2@example.com",
    "password": "test123",
    "gender": "invalid_gender"  # ❌ مقدار اشتباه
}

response2 = requests.post(url, json=data2)
print(f"Test 2 Status: {response2.status_code}")
if response2.status_code == 422:
    print(f"Validation Errors: {response2.json()}")
```

### مشاهده جزئیات خطا:

در Swagger UI (http://localhost:8000/docs):
1. روی `/api/auth/register` کلیک کنید
2. "Try it out" را بزنید
3. داده‌ها را وارد کنید
4. "Execute" را بزنید
5. در بخش "Response body" جزئیات خطا را ببینید

مثال خطا:
```json
{
  "detail": [
    {
      "type": "enum",
      "loc": ["body", "gender"],
      "msg": "Input should be 'male', 'female' or 'other'",
      "input": "invalid_value"
    }
  ]
}
```

---

## ❌ خطای 400 Bad Request

### علت:
- ایمیل قبلاً ثبت شده است
- مشکل در دیتابیس

### راه‌حل:
- از ایمیل دیگری استفاده کنید
- یا کاربر موجود را حذف کنید

---

## ❌ خطای 401 Unauthorized

### علت:
- Token نامعتبر یا منقضی شده
- Header Authorization اشتباه

### راه‌حل:
```python
# ✅ درست
headers = {"Authorization": f"Bearer {token}"}

# ❌ اشتباه
headers = {"Authorization": token}
headers = {"Authorization": f"Token {token}"}
```

---

## ❌ خطای 500 Internal Server Error

### علت:
- مشکل در کد backend
- مشکل در اتصال به دیتابیس
- مشکل در API های خارجی (مثل Gemini)

### راه‌حل:
1. لاگ‌های سرور را بررسی کنید
2. مطمئن شوید دیتابیس در دسترس است
3. مطمئن شوید API Keys تنظیم شده‌اند

---

## 🔍 Debug Tips

### 1. مشاهده Request کامل:

```python
import requests
import json

url = "http://localhost:8000/api/auth/register"
data = {
    "full_name": "تست",
    "email": "test@example.com",
    "password": "test123"
}

# مشاهده request
print("Request URL:", url)
print("Request Data:", json.dumps(data, indent=2, ensure_ascii=False))

response = requests.post(url, json=data)

# مشاهده response کامل
print("Status Code:", response.status_code)
print("Response Headers:", dict(response.headers))
print("Response Body:", response.text)
```

### 2. استفاده از curl با verbose:

```bash
curl -v -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"full_name":"تست","email":"test@example.com","password":"test123"}'
```

### 3. بررسی Schema در Swagger:

در http://localhost:8000/docs:
- روی endpoint کلیک کنید
- بخش "Request body" را ببینید
- مثال‌های موجود را استفاده کنید

---

## 📝 چک‌لیست رفع مشکل

- [ ] فیلدهای اجباری (`full_name`, `email`, `password`) ارسال شده‌اند
- [ ] فرمت ایمیل صحیح است
- [ ] مقادیر enum صحیح هستند (`gender`, `mizaj_type`)
- [ ] فرمت تاریخ صحیح است (`YYYY-MM-DD`)
- [ ] Content-Type header صحیح است (`application/json`)
- [ ] JSON معتبر است (بررسی syntax)
- [ ] سرور در حال اجرا است
- [ ] دیتابیس در دسترس است

---

**آخرین بروزرسانی: 2024**

