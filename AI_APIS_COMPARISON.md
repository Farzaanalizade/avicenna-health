# 🤖 مقایسه جامع API های هوش مصنوعی برای پروژه Avicenna AI

## 📊 جدول مقایسه سریع

| ویژگی | Gemini 1.5 Pro | Gemini 1.5 Flash | GPT-4 Vision | Claude Sonnet 4 | Custom Models |
|------|----------------|------------------|--------------|-----------------|--------------|
| **قیمت (Input)** | $1.25/1M tokens | $0.075/1M tokens | $10/1M tokens | $3/1M tokens | هزینه GPU |
| **قیمت (Output)** | $5/1M tokens | $0.30/1M tokens | $30/1M tokens | $15/1M tokens | - |
| **Context Window** | 1M tokens | 1M tokens | 128K tokens | 200K tokens | نامحدود |
| **Vision Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Multimodal** | ✅ کامل | ✅ کامل | ✅ تصویر+متن | ⚠️ محدود | ⚠️ نیاز به توسعه |
| **زبان فارسی** | ✅ عالی | ✅ عالی | ✅ خوب | ⚠️ متوسط | ✅ کامل |
| **Rate Limit** | 60 RPM | 60 RPM | متغیر | متغیر | نامحدود |
| **JSON Mode** | ✅ | ✅ | ✅ | ✅ | - |
| **استدلال** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🏆 توصیه نهایی: ترکیب Gemini Flash + GPT-4 (برای موارد پیچیده)

### استراتژی پیشنهادی:

#### 1. **Gemini 1.5 Flash** (Primary - 80% استفاده)
- ✅ **تحلیل تصاویر زبان و چشم** - سریع و دقیق
- ✅ **تفسیر اولیه** - بر اساس دانش طب سنتی
- ✅ **تولید توصیه‌ها** - شخصی‌سازی شده
- ✅ **هزینه پایین** - مناسب برای استفاده زیاد

**موارد استفاده:**
- تحلیل روزانه تصاویر
- تفسیر نتایج سنسورها
- تولید توصیه‌های اولیه

#### 2. **GPT-4 Vision** (Secondary - 15% استفاده)
- ✅ **تحلیل‌های پیچیده** - زمانی که Gemini مطمئن نیست
- ✅ **استدلال پزشکی پیشرفته** - ترکیب چندین نشانه
- ✅ **تشخیص بیماری‌های نادر**

**موارد استفاده:**
- موارد مشکوک یا پیچیده
- ترکیب چندین نشانه برای تشخیص
- بررسی دوم (Second Opinion)

#### 3. **Claude Sonnet 4** (Tertiary - 5% استفاده)
- ✅ **تحلیل متنی** - ترکیب نتایج
- ✅ **تولید گزارش‌های جامع**
- ✅ **استدلال منطقی**

**موارد استفاده:**
- تولید گزارش‌های نهایی
- ترکیب و تحلیل نتایج چندین منبع

---

## 💻 پیاده‌سازی Gemini API

### نصب و راه‌اندازی

```bash
pip install google-generativeai pillow
```

### کد نمونه - تحلیل تصویر زبان

```python
import google.generativeai as genai
from PIL import Image
import base64
import io
from typing import Dict, Any

class GeminiTongueAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def analyze_tongue(self, image_base64: str) -> Dict[str, Any]:
        """تحلیل تصویر زبان با Gemini"""
        
        # Decode image
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        
        # Prompt برای تحلیل
        prompt = """
        شما یک متخصص طب سنتی ایرانی و چینی هستید. این تصویر زبان یک بیمار است.
        
        لطفاً موارد زیر را با دقت تحلیل کنید:
        
        1. **رنگ زبان:**
           - صورتی (طبیعی)
           - قرمز (گرم مزاج، التهاب)
           - قرمز تیره (التهاب شدید)
           - زرد (مشکل کبدی/صفراوی)
           - سفید (سرد مزاج، ضعف)
           - بنفش/کبود (مشکل گردش خون)
        
        2. **پوشش زبان:**
           - بدون پوشش (خشکی)
           - پوشش سفید نازک (طبیعی)
           - پوشش سفید ضخیم (رطوبت زیاد)
           - پوشش زرد (حرارت/صفرا)
           - پوشش قهوه‌ای (مشکل گوارشی)
        
        3. **بافت و شکل:**
           - ترک‌ها (خشکی)
           - لکه‌ها (مشکلات احتمالی)
           - تورم (رطوبت)
           - علائم دندان (رطوبت زیاد)
        
        4. **رطوبت:**
           - خشک
           - نرمال
           - مرطوب
           - بسیار مرطوب
        
        پاسخ را به صورت JSON دقیق بده:
        {
          "color": "رنگ اصلی",
          "coating": {
            "type": "نوع پوشش",
            "thickness": "ضخامت (نازک/متوسط/ضخیم)",
            "coverage": "درصد پوشش"
          },
          "texture": {
            "cracks": true/false,
            "spots": true/false,
            "swelling": true/false
          },
          "moisture": "وضعیت رطوبت",
          "mizaj_assessment": "مزاج احتمالی (گرم/سرد/تر/خشک/معتدل)",
          "health_indicators": ["نشانه 1", "نشانه 2"],
          "recommendations": ["توصیه 1", "توصیه 2"]
        }
        """
        
        try:
            response = self.model.generate_content([prompt, image])
            
            # Parse JSON response
            import json
            import re
            
            # استخراج JSON از پاسخ
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result
            else:
                # اگر JSON پیدا نشد، ساختار دستی بساز
                return self._parse_text_response(response.text)
                
        except Exception as e:
            print(f"Error in Gemini analysis: {e}")
            return self._get_default_response()
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """تبدیل پاسخ متنی به JSON"""
        # این متد می‌تواند پاسخ متنی را parse کند
        return {
            "color": "نامشخص",
            "coating": {"type": "نامشخص"},
            "mizaj_assessment": "نامشخص",
            "health_indicators": [],
            "recommendations": ["مشاوره با پزشک"]
        }
    
    def _get_default_response(self) -> Dict[str, Any]:
        """پاسخ پیش‌فرض در صورت خطا"""
        return {
            "color": "نامشخص",
            "coating": {"type": "نامشخص"},
            "mizaj_assessment": "نامشخص",
            "health_indicators": [],
            "recommendations": ["خطا در تحلیل - لطفاً دوباره تلاش کنید"]
        }
```

### کد نمونه - تحلیل تصویر چشم

```python
class GeminiEyeAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def analyze_eye(self, image_base64: str) -> Dict[str, Any]:
        """تحلیل تصویر چشم"""
        
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        
        prompt = """
        شما یک متخصص طب سنتی هستید. این تصویر چشم یک بیمار است.
        
        تحلیل کنید:
        
        1. **صلبیه (سفیدی چشم):**
           - رنگ (سفید طبیعی، زرد، قرمز)
           - وضوح
           - لکه‌ها یا تغییر رنگ
        
        2. **عنبیه:**
           - رنگ
           - الگو
           - یکنواختی
        
        3. **مردمک:**
           - اندازه
           - شکل
           - تقارن
        
        4. **عروق:**
           - وضوح
           - الگو
           - قرمزی یا التهاب
        
        پاسخ JSON:
        {
          "sclera": {
            "color": "رنگ",
            "clarity": "وضوح",
            "yellowness": 0.0-1.0,
            "redness": 0.0-1.0
          },
          "iris": {
            "color": "رنگ",
            "pattern": "الگو",
            "uniformity": 0.0-1.0
          },
          "pupil": {
            "size": "اندازه",
            "shape": "شکل"
          },
          "health_assessment": "ارزیابی کلی",
          "warnings": ["هشدار 1", "هشدار 2"],
          "recommendations": ["توصیه 1"]
        }
        """
        
        try:
            response = self.model.generate_content([prompt, image])
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return self._get_default_response()
        except Exception as e:
            print(f"Error: {e}")
            return self._get_default_response()
```

---

## 🔄 پیاده‌سازی ترکیبی (Gemini + GPT-4)

```python
class HybridAIService:
    def __init__(self, gemini_key: str, openai_key: str):
        self.gemini_analyzer = GeminiTongueAnalyzer(gemini_key)
        self.openai_client = openai.OpenAI(api_key=openai_key)
    
    async def analyze_with_fallback(self, image_base64: str) -> Dict[str, Any]:
        """تحلیل با fallback به GPT-4"""
        
        # ابتدا با Gemini تحلیل کن
        result = await self.gemini_analyzer.analyze_tongue(image_base64)
        
        # اگر confidence پایین بود، از GPT-4 استفاده کن
        if result.get("confidence", 1.0) < 0.7:
            gpt4_result = await self._analyze_with_gpt4(image_base64)
            
            # ترکیب نتایج
            return self._merge_results(result, gpt4_result)
        
        return result
    
    async def _analyze_with_gpt4(self, image_base64: str) -> Dict[str, Any]:
        """تحلیل با GPT-4 Vision"""
        # Implementation with OpenAI API
        pass
```

---

## 📈 بهینه‌سازی هزینه

### استراتژی‌های کاهش هزینه:

1. **Caching**
   - ذخیره نتایج تحلیل‌های مشابه
   - استفاده از hash تصویر

2. **Batch Processing**
   - پردازش دسته‌ای در ساعات کم‌ترافیک

3. **Smart Routing**
   - استفاده از Gemini برای 80% موارد
   - GPT-4 فقط برای موارد پیچیده

4. **Compression**
   - فشرده‌سازی تصاویر قبل از ارسال
   - کاهش حجم داده

---

## 🔐 امنیت و حریم خصوصی

### نکات مهم:

1. **رمزگذاری داده‌ها**
   - تمام تصاویر باید رمزگذاری شوند
   - استفاده از HTTPS

2. **عدم ذخیره‌سازی**
   - تصاویر پس از تحلیل حذف شوند
   - فقط نتایج تحلیل ذخیره شوند

3. **GDPR/HIPAA Compliance**
   - رعایت قوانین حریم خصوصی
   - امکان حذف داده‌ها

---

## 📝 نتیجه‌گیری

**بهترین ترکیب برای پروژه Avicenna AI:**

1. **Gemini 1.5 Flash** - Primary (80%)
   - سریع، ارزان، دقیق
   - مناسب برای استفاده روزانه

2. **GPT-4 Vision** - Secondary (15%)
   - برای موارد پیچیده
   - استدلال پیشرفته

3. **Claude Sonnet 4** - Tertiary (5%)
   - تحلیل متنی
   - تولید گزارش

**هزینه ماهانه تخمینی:**
- Gemini Flash: ~$50-100 (برای 1000 کاربر فعال)
- GPT-4: ~$20-50 (برای موارد پیچیده)
- Claude: ~$10-20 (برای گزارش‌ها)

**کل: ~$80-170/ماه**

---

**آخرین بروزرسانی: 2024**

