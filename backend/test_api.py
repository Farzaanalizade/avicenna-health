"""
اسکریپت تست کامل API
برای اجرا: python test_api.py
"""
import requests
import base64
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

def print_section(title):
    """چاپ عنوان بخش"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}\n")

def test_register():
    """تست ثبت‌نام"""
    print_section("🔐 تست Register")
    url = f"{BASE_URL}/api/auth/register"
    
    # ابتدا با داده‌های حداقل تست می‌کنیم
    data_minimal = {
        "full_name": "تست کاربر",
        "email": "test@example.com",
        "password": "test123456"
    }
    
    # سپس با داده‌های کامل
    data_full = {
        "full_name": "تست کاربر",
        "email": "test@example.com",
        "password": "test123456",
        "mizaj_type": "motadel",
        "gender": "male",
        "date_of_birth": "1990-01-15",
        "phone_number": "09123456789"
    }
    
    # استفاده از داده‌های حداقل
    data = data_minimal
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Request Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ ثبت‌نام موفق!")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result
        elif response.status_code == 422:
            # Validation error - جزئیات را نمایش بده
            error_detail = response.json()
            print("❌ خطای Validation:")
            print(json.dumps(error_detail, indent=2, ensure_ascii=False))
            print("\n💡 نکته: فیلدهای اجباری را بررسی کنید:")
            print("   - full_name: string")
            print("   - email: string با فرمت ایمیل")
            print("   - password: string")
            print("\n💡 مقادیر enum معتبر:")
            print("   - gender: 'male', 'female', 'other'")
            print("   - mizaj_type: 'garm', 'sard', 'tar', 'khoshk', 'garm_tar', 'garm_khoshk', 'sard_tar', 'sard_khoshk', 'motadel'")
            return None
        else:
            print(f"❌ خطا: {response.text}")
            return None
    except Exception as e:
        print(f"❌ خطا در اتصال: {e}")
        return None

def test_login(email, password):
    """تست ورود"""
    print_section("🔑 تست Login")
    url = f"{BASE_URL}/api/auth/login"
    data = {"email": email, "password": password}
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            token = result["access_token"]
            print("✅ ورود موفق!")
            print(f"Token: {token[:50]}...")
            print(f"Patient: {result.get('patient', {})}")
            return token
        else:
            print(f"❌ خطا: {response.text}")
            return None
    except Exception as e:
        print(f"❌ خطا در اتصال: {e}")
        return None

def test_tongue_analyze(token, image_path=None):
    """تست تحلیل زبان"""
    print_section("👅 تست تحلیل زبان")
    
    if not image_path or not Path(image_path).exists():
        print("⚠️  تصویر یافت نشد. استفاده از داده نمونه...")
        # استفاده از یک تصویر نمونه (base64 کوچک)
        # در عمل باید یک تصویر واقعی استفاده کنید
        print("💡 برای تست واقعی، یک تصویر زبان را به base64 تبدیل کنید")
        return None
    
    try:
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
            "metadata": {"filename": Path(image_path).name}
        }
        
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ تحلیل موفق!")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result
        else:
            print(f"❌ خطا: {response.text}")
            return None
    except FileNotFoundError:
        print(f"❌ فایل تصویر یافت نشد: {image_path}")
        return None
    except Exception as e:
        print(f"❌ خطا: {e}")
        return None

def test_eye_analyze(token, image_path=None):
    """تست تحلیل چشم"""
    print_section("👁️ تست تحلیل چشم")
    
    if not image_path or not Path(image_path).exists():
        print("⚠️  تصویر یافت نشد. استفاده از داده نمونه...")
        print("💡 برای تست واقعی، یک تصویر چشم را به base64 تبدیل کنید")
        return None
    
    try:
        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        url = f"{BASE_URL}/api/health/eye/analyze"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        data = {
            "image_base64": image_base64,
            "metadata": {"filename": Path(image_path).name}
        }
        
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ تحلیل موفق!")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result
        else:
            print(f"❌ خطا: {response.text}")
            return None
    except FileNotFoundError:
        print(f"❌ فایل تصویر یافت نشد: {image_path}")
        return None
    except Exception as e:
        print(f"❌ خطا: {e}")
        return None

def test_health_check():
    """تست Health Check"""
    print_section("🏥 تست Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ خطا: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  🧪 تست API Avicenna AI")
    print("="*50)
    
    # تست Health Check
    if not test_health_check():
        print("\n❌ سرور در دسترس نیست! لطفاً ابتدا سرور را راه‌اندازی کنید:")
        print("   uvicorn run:app --reload")
        exit(1)
    
    # تست Register
    user = test_register()
    
    if user:
        # تست Login
        email = "test@example.com"
        password = "test123456"
        token = test_login(email, password)
        
        if token:
            print("\n" + "="*50)
            print("  ✅ تست‌های Authentication موفق بودند!")
            print("="*50)
            print("\n💡 برای تست تحلیل تصاویر:")
            print("   1. یک تصویر زبان را در پوشه backend قرار دهید")
            print("   2. یک تصویر چشم را در پوشه backend قرار دهید")
            print("   3. سپس این کد را اجرا کنید:")
            print("\n   test_tongue_analyze(token, 'tongue_image.jpg')")
            print("   test_eye_analyze(token, 'eye_image.jpg')")
            
            # اگر تصاویر موجود باشند، تست کن
            tongue_image = Path("tongue_image.jpg")
            eye_image = Path("eye_image.jpg")
            
            if tongue_image.exists():
                test_tongue_analyze(token, str(tongue_image))
            
            if eye_image.exists():
                test_eye_analyze(token, str(eye_image))
        else:
            print("\n❌ تست Login ناموفق بود")
    else:
        print("\n⚠️  ثبت‌نام ناموفق بود (ممکن است کاربر از قبل وجود داشته باشد)")
        print("   سعی می‌کنیم با همان ایمیل وارد شویم...")
        token = test_login("test@example.com", "test123456")
        
        if token:
            print("\n✅ ورود با کاربر موجود موفق بود!")
    
    print("\n" + "="*50)
    print("  🎉 تست‌ها کامل شدند!")
    print("="*50 + "\n")

