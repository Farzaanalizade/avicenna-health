"""
سرویس Gemini AI برای تحلیل تصاویر و داده‌های پزشکی
"""
import logging
from typing import Dict, Any, Optional

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except (ImportError, TypeError) as e:
    # Python 3.14 compatibility: protobuf metaclass issue
    GENAI_AVAILABLE = False
    logging.warning(f"Google Generative AI not available: {e}")

from PIL import Image
import base64
import io
import json
import re
from app.core.config import settings

logger = logging.getLogger(__name__)

class GeminiService:
    """سرویس Gemini برای تحلیل تصاویر"""
    
    def __init__(self):
        """Initialize Gemini service"""
        self.model = None
        self.genai_available = GENAI_AVAILABLE
        
        if not GENAI_AVAILABLE:
            logger.warning("Google Generative AI not available (Python 3.14 compatibility issue)")
            return
        
        try:
            if not settings.GEMINI_API_KEY:
                logger.warning("GEMINI_API_KEY not set. Gemini features will be disabled.")
                self.model = None
            else:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("Gemini service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Gemini: {e}")
            self.model = None
    
    async def analyze_tongue_image(self, image_base64: str) -> Dict[str, Any]:
        """تحلیل تصویر زبان با Gemini"""
        
        if not self.model:
            return self._get_default_tongue_response()
        
        # Decode image
        try:
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
        except Exception as e:
            logger.error(f"Error decoding image: {e}")
            return self._get_default_tongue_response()
        
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
            logger.error(f"Error in Gemini analysis: {e}")
            return self._get_default_tongue_response()
    
    async def analyze_eye_image(self, image_base64: str) -> Dict[str, Any]:
        """تحلیل تصویر چشم"""
        
        if not self.model:
            return self._get_default_eye_response()
        
        try:
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
        except Exception as e:
            logger.error(f"Error decoding image: {e}")
            return self._get_default_eye_response()
        
        prompt = """
        شما یک متخصص طب سنتی هستید. این تصویر چشم یک بیمار است.
        
        تحلیل کنید:
        
        1. صلبیه (سفیدی چشم): رنگ، وضوح، لکه‌ها
        2. عنبیه: رنگ، الگو، یکنواختی
        3. مردمک: اندازه، شکل
        4. عروق: وضوح، الگو، التهاب
        
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
          "warnings": ["هشدار 1"],
          "recommendations": ["توصیه 1"],
          "confidence": 0.0-1.0
        }
        """
        
        try:
            response = self.model.generate_content([prompt, image])
            json_text = self._extract_json(response.text)
            if json_text:
                return json.loads(json_text)
            return self._get_default_eye_response()
        except Exception as e:
            logger.error(f"Error in eye analysis: {e}")
            return self._get_default_eye_response()
    
    def _extract_json(self, text: str) -> Optional[str]:
        """استخراج JSON از متن"""
        # جستجوی JSON در متن
        patterns = [
            r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # ساده
            r'```json\s*(\{.*?\})\s*```',  # با markdown
            r'```\s*(\{.*?\})\s*```',  # بدون json
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                json_str = match.group(1) if match.groups() else match.group()
                try:
                    # تست اعتبار JSON
                    json.loads(json_str)
                    return json_str
                except:
                    continue
        
        return None
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """تبدیل پاسخ متنی به ساختار"""
        # Extract key information from text
        result = {
            "color": "نامشخص",
            "coating": {"type": "نامشخص"},
            "mizaj_assessment": "نامشخص",
            "health_indicators": [],
            "recommendations": ["مشاوره با پزشک"],
            "confidence": 0.5
        }
        
        # Try to extract color
        if "قرمز" in text or "red" in text.lower():
            result["color"] = "قرمز"
        elif "صورتی" in text or "pink" in text.lower():
            result["color"] = "صورتی"
        elif "زرد" in text or "yellow" in text.lower():
            result["color"] = "زرد"
        elif "سفید" in text or "white" in text.lower():
            result["color"] = "سفید"
        
        return result
    
    def _get_default_tongue_response(self) -> Dict[str, Any]:
        """پاسخ پیش‌فرض برای زبان"""
        return {
            "color": "نامشخص",
            "coating": {"type": "نامشخص", "thickness": "نامشخص", "coverage_percentage": 0},
            "texture": {"cracks": False, "spots": False, "swelling": False},
            "moisture": "نامشخص",
            "mizaj_assessment": "نامشخص",
            "health_indicators": [],
            "recommendations": ["Gemini API غیرفعال است - لطفاً API Key را تنظیم کنید"],
            "confidence": 0.0
        }
    
    def _get_default_eye_response(self) -> Dict[str, Any]:
        """پاسخ پیش‌فرض برای چشم"""
        return {
            "sclera": {"color": "نامشخص", "clarity": "نامشخص", "yellowness": 0.0, "redness": 0.0},
            "iris": {"color": "نامشخص", "pattern": "نامشخص", "uniformity": 0.0},
            "pupil": {"size": "نامشخص", "shape": "نامشخص"},
            "health_assessment": "نامشخص",
            "warnings": [],
            "recommendations": ["Gemini API غیرفعال است"],
            "confidence": 0.0
        }

