import google.generativeai as genai
from PIL import Image
import os
from typing import Dict

# تنظیم API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class TongueAnalyzer:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def analyze_tongue_image(self, image_path: str) -> Dict:
        """
        تحلیل تصویر زبان با استفاده از Gemini Vision
        """
        # بارگذاری تصویر
        img = Image.open(image_path)
        
        # Prompt برای تحلیل
        prompt = """
        شما یک متخصص طب سنتی چینی و ایرانی هستید.
        این تصویر یک زبان است. لطفاً موارد زیر را تحلیل کنید:
        
        1. رنگ زبان (pink/pale/red/purple)
        2. پوشش زبان (clean/thin_white/thick_white/yellow)
        3. بافت زبان (normal/swollen/cracked/smooth)
        4. وضعیت کلی سلامت بر اساس زبان
        5. توصیه‌های درمانی (3-5 مورد)
        
        پاسخ را به صورت JSON بده:
        {
          "color": "...",
          "coating": "...",
          "texture": "...",
          "health_assessment": "...",
          "recommendations": ["...", "..."]
        }
        """
        
        # ارسال به Gemini
        response = self.model.generate_content([prompt, img])
        
        # پردازش پاسخ
        # (اینجا باید JSON را parse کنید)
        return {
            "color": "pink",
            "coating": "thin_white",
            "texture": "normal",
            "recommendations": ["نوشیدن آب بیشتر", "کاهش مصرف شکر"]
        }

# Instance
tongue_analyzer = TongueAnalyzer()
