import base64
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import numpy as np
from PIL import Image
import io
import logging

# تنظیم لاگر
logger = logging.getLogger(__name__)

# Import Gemini Service
try:
    from app.services.gemini_service import GeminiService
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Gemini service not available")

class TongueAnalyzer:
    """تحلیلگر تصاویر زبان با استفاده از پردازش تصویر و AI"""
    
    def __init__(self):
        self.color_ranges = {
            "صورتی": {"h": (340, 20), "s": (20, 60), "v": (70, 100)},
            "قرمز": {"h": (0, 10), "s": (50, 100), "v": (50, 100)},
            "قرمز تیره": {"h": (350, 10), "s": (60, 100), "v": (30, 70)},
            "زرد": {"h": (20, 40), "s": (30, 100), "v": (60, 100)},
            "سفید": {"h": (0, 360), "s": (0, 20), "v": (80, 100)},
            "بنفش": {"h": (270, 330), "s": (20, 100), "v": (30, 90)}
        }
        
        self.coating_patterns = {
            "بدون پوشش": {"thickness": 0, "coverage": 0},
            "نازک": {"thickness": 1, "coverage": 30},
            "متوسط": {"thickness": 2, "coverage": 60},
            "ضخیم": {"thickness": 3, "coverage": 90}
        }
    
    def analyze_image(self, image_base64: str) -> Dict[str, Any]:
        """تحلیل تصویر زبان"""
        try:
            # Decode base64 image
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # تحلیل‌های پایه (این‌ها نمونه هستند - در عمل با مدل AI جایگزین می‌شوند)
            analysis = {
                "color": self._analyze_color(image),
                "coating": self._analyze_coating(image),
                "moisture": self._analyze_moisture(image),
                "texture": self._analyze_texture(image),
                "shape": self._analyze_shape(image),
                "cracks": self._detect_cracks(image),
                "spots": self._detect_spots(image)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing tongue image: {e}")
            return self._get_default_analysis()
    
    def _analyze_color(self, image: Image.Image) -> Dict[str, Any]:
        """تحلیل رنگ زبان"""
        # نمونه پیاده‌سازی ساده
        return {
            "primary": "صورتی",
            "secondary": None,
            "uniformity": 0.85,
            "abnormal_areas": []
        }
    
    def _analyze_coating(self, image: Image.Image) -> Dict[str, Any]:
        """تحلیل پوشش زبان"""
        return {
            "type": "نازک",
            "color": "سفید",
            "thickness": 1,
            "coverage_percentage": 20,
            "distribution": "یکنواخت"
        }
    
    def _analyze_moisture(self, image: Image.Image) -> str:
        """تحلیل رطوبت زبان"""
        return "نرمال"
    
    def _analyze_texture(self, image: Image.Image) -> Dict[str, Any]:
        """تحلیل بافت زبان"""
        return {
            "smoothness": 0.8,
            "roughness_areas": [],
            "papillae_visible": True
        }
    
    def _analyze_shape(self, image: Image.Image) -> Dict[str, Any]:
        """تحلیل شکل زبان"""
        return {
            "symmetry": 0.95,
            "swelling": False,
            "tooth_marks": False,
            "size": "نرمال"
        }
    
    def _detect_cracks(self, image: Image.Image) -> List[Dict[str, Any]]:
        """تشخیص ترک‌های زبان"""
        return []
    
    def _detect_spots(self, image: Image.Image) -> List[Dict[str, Any]]:
        """تشخیص لکه‌های زبان"""
        return []
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """تحلیل پیش‌فرض در صورت خطا"""
        return {
            "color": {"primary": "نامشخص", "uniformity": 0},
            "coating": {"type": "نامشخص", "thickness": 0},
            "moisture": "نامشخص",
            "texture": {"smoothness": 0},
            "shape": {"symmetry": 0},
            "cracks": [],
            "spots": []
        }
    
    def interpret_for_mizaj(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """تفسیر نتایج بر اساس مزاج در طب سنتی"""
        interpretation = {
            "mizaj_indication": "",
            "imbalances": [],
            "recommendations": []
        }
        
        color = analysis.get("color", {}).get("primary", "")
        coating = analysis.get("coating", {})
        moisture = analysis.get("moisture", "")
        
        # تعیین مزاج بر اساس رنگ
        if color == "قرمز" or color == "قرمز تیره":
            interpretation["mizaj_indication"] = "گرم"
            interpretation["imbalances"].append("افزایش حرارت بدن")
            interpretation["recommendations"].append("مصرف غذاهای سرد مزاج")
        elif color == "صورتی":
            interpretation["mizaj_indication"] = "معتدل"
        elif color == "سفید" or color == "رنگ پریده":
            interpretation["mizaj_indication"] = "سرد"
            interpretation["imbalances"].append("کمبود حرارت بدن")
            interpretation["recommendations"].append("مصرف غذاهای گرم مزاج")
        
        # تحلیل بر اساس پوشش
        if coating.get("thickness", 0) > 2:
            interpretation["imbalances"].append("رطوبت زیاد")
            interpretation["recommendations"].append("کاهش مصرف غذاهای چرب و سنگین")
        
        # تحلیل رطوبت
        if moisture == "خشک":
            interpretation["imbalances"].append("خشکی بدن")
            interpretation["recommendations"].append("افزایش مصرف مایعات")
        elif moisture == "بسیار مرطوب":
            interpretation["imbalances"].append("رطوبت زیاد")
            
        return interpretation


class EyeAnalyzer:
    """تحلیلگر تصاویر چشم"""
    
    def analyze_image(self, image_base64: str) -> Dict[str, Any]:
        """تحلیل تصویر چشم"""
        try:
            # Decode base64 image
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            
            analysis = {
                "sclera": self._analyze_sclera(image),
                "iris": self._analyze_iris(image),
                "pupil": self._analyze_pupil(image),
                "vessels": self._analyze_vessels(image),
                "overall_health": self._assess_overall_health(image)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing eye image: {e}")
            return self._get_default_analysis()
    
    def _analyze_sclera(self, image: Image.Image) -> Dict[str, Any]:
        """تحلیل صلبیه (سفیدی چشم)"""
        return {
            "color": "سفید",
            "clarity": "صاف",
            "yellowness": 0.05,
            "redness": 0.1,
            "spots": []
        }
    
    def _analyze_iris(self, image: Image.Image) -> Dict[str, Any]:
        """تحلیل عنبیه"""
        return {
            "pattern": "نرمال",
            "color_uniformity": 0.9,
            "density": "متوسط",
            "abnormalities": []
        }
    
    def _analyze_pupil(self, image: Image.Image) -> Dict[str, Any]:
        """تحلیل مردمک"""
        return {
            "size": "نرمال",
            "shape": "گرد",
            "response": "نرمال"
        }
    
    def _analyze_vessels(self, image: Image.Image) -> Dict[str, Any]:
        """تحلیل عروق چشم"""
        return {
            "visibility": "نرمال",
            "pattern": "منظم",
            "congestion": False
        }
    
    def _assess_overall_health(self, image: Image.Image) -> List[str]:
        """ارزیابی سلامت کلی بر اساس چشم"""
        return ["سلامت عمومی خوب", "عدم وجود نشانه‌های التهاب"]
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        return {
            "sclera": {"color": "نامشخص"},
            "iris": {"pattern": "نامشخص"},
            "pupil": {"size": "نامشخص"},
            "vessels": {"visibility": "نامشخص"},
            "overall_health": []
        }


class VoiceAnalyzer:
    """تحلیلگر صدا و سرفه"""
    
    def analyze_audio(self, audio_base64: str, audio_format: str) -> Dict[str, Any]:
        """تحلیل فایل صوتی"""
        try:
            # در اینجا می‌توان از کتابخانه‌هایی مثل librosa استفاده کرد
            # فعلاً نتایج نمونه برمی‌گردانیم
            
            analysis = {
                "voice_characteristics": {
                    "pitch": "نرمال",
                    "tone": "صاف",
                    "clarity": 0.85,
                    "hoarseness": 0.1
                },
                "respiratory_indicators": {
                    "wheezing": False,
                    "congestion": False,
                    "breath_sounds": "نرمال"
                },
                "cough_analysis": {
                    "type": "خشک",
                    "severity": "خفیف",
                    "frequency": "گاهی"
                }
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing audio: {e}")
            return self._get_default_analysis()
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        return {
            "voice_characteristics": {"pitch": "نامشخص"},
            "respiratory_indicators": {"breath_sounds": "نامشخص"},
            "cough_analysis": {"type": "نامشخص"}
        }


class AIService:
    """سرویس اصلی هوش مصنوعی"""
    
    def __init__(self):
        self.tongue_analyzer = TongueAnalyzer()
        self.eye_analyzer = EyeAnalyzer()
        self.voice_analyzer = VoiceAnalyzer()
        
        # Initialize Gemini Service
        if GEMINI_AVAILABLE:
            try:
                self.gemini_service = GeminiService()
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
                self.gemini_service = None
        else:
            self.gemini_service = None
    
    async def analyze_tongue(self, image_base64: str) -> Dict[str, Any]:
        """تحلیل کامل زبان با Gemini و تحلیل محلی"""
        
        # استفاده از Gemini برای تحلیل دقیق (اگر در دسترس باشد)
        gemini_result = None
        if self.gemini_service:
            try:
                gemini_result = await self.gemini_service.analyze_tongue_image(image_base64)
            except Exception as e:
                logger.error(f"Gemini analysis failed: {e}")
        
        # تحلیل محلی به عنوان fallback
        image_analysis = self.tongue_analyzer.analyze_image(image_base64)
        traditional_interpretation = self.tongue_analyzer.interpret_for_mizaj(image_analysis)
        
        # ترکیب نتایج (اولویت با Gemini)
        if gemini_result and gemini_result.get("confidence", 0) > 0.5:
            color = gemini_result.get("color", "نامشخص")
            coating_data = gemini_result.get("coating", {})
            coating = coating_data.get("type", "نامشخص") if isinstance(coating_data, dict) else "نامشخص"
            texture = gemini_result.get("texture", {})
            cracks = "بله" if texture.get("cracks", False) else "خیر"
            humidity = gemini_result.get("moisture", "نامشخص")
            mizaj = gemini_result.get("mizaj_assessment", "نامشخص")
            recommendations_list = gemini_result.get("recommendations", [])
        else:
            # استفاده از نتایج محلی
            color = image_analysis.get("color", {}).get("primary", "نامشخص")
            coating = image_analysis.get("coating", {}).get("type", "نامشخص")
            cracks = "بله" if image_analysis.get("cracks") else "خیر"
            humidity = image_analysis.get("moisture", "نامشخص")
            mizaj = traditional_interpretation.get("mizaj_indication", "نامشخص")
            recommendations_list = traditional_interpretation.get("recommendations", [])
        
        # ساخت تشخیص بوعلی
        avicenna_diagnosis = f"مزاج: {mizaj}"
        if traditional_interpretation.get("imbalances"):
            avicenna_diagnosis += f" | عدم تعادل: {', '.join(traditional_interpretation['imbalances'])}"
        
        return {
            "color": color,
            "coating": coating,
            "cracks": cracks,
            "humidity": humidity,
            "avicenna_diagnosis": avicenna_diagnosis,
            "recommendations": {
                "immediate": recommendations_list,
                "lifestyle": [],
                "dietary": []
            }
        }
    
    async def analyze_eye(self, image_base64: str) -> Dict[str, Any]:
        """تحلیل کامل چشم با Gemini و تحلیل محلی"""
        
        # استفاده از Gemini (اگر در دسترس باشد)
        gemini_result = None
        if self.gemini_service:
            try:
                gemini_result = await self.gemini_service.analyze_eye_image(image_base64)
            except Exception as e:
                logger.error(f"Gemini eye analysis failed: {e}")
        
        # تحلیل محلی
        analysis = self.eye_analyzer.analyze_image(image_base64)
        health_indicators = self._interpret_ey_for_health(analysis)
        
        # ترکیب نتایج
        if gemini_result and gemini_result.get("confidence", 0) > 0.5:
            iris_data = gemini_result.get("iris", {})
            iris_color = iris_data.get("color", "نامشخص") if isinstance(iris_data, dict) else "نامشخص"
            sclera_data = gemini_result.get("sclera", {})
            sclera_condition = sclera_data.get("color", "نامشخص") if isinstance(sclera_data, dict) else "نامشخص"
            recommendations_list = gemini_result.get("recommendations", [])
            warnings_list = gemini_result.get("warnings", [])
        else:
            iris_color = analysis.get("iris", {}).get("pattern", "نامشخص")
            sclera_condition = analysis.get("sclera", {}).get("color", "نامشخص")
            recommendations_list = health_indicators.get("recommendations", [])
            warnings_list = health_indicators.get("warnings", [])
        
        # ساخت تشخیص بوعلی
        avicenna_diagnosis = f"وضعیت صلبیه: {sclera_condition}"
        if warnings_list:
            avicenna_diagnosis += f" | هشدارها: {', '.join(warnings_list)}"
        
        return {
            "iris_color": iris_color,
            "sclera_condition": sclera_condition,
            "avicenna_diagnosis": avicenna_diagnosis,
            "recommendations": {
                "immediate": recommendations_list,
                "lifestyle": [],
                "medical": []
            }
        }
    
    async def analyze_voice(self, audio_base64: str, audio_format: str) -> Dict[str, Any]:
        """تحلیل صدا"""
        analysis = self.voice_analyzer.analyze_audio(audio_base64, audio_format)
        
        # تفسیر برای سلامت
        health_assessment = self._interpret_voice_for_health(analysis)
        
        # ساخت نتیجه مطابق با schema
        voice_chars = analysis.get("voice_characteristics", {})
        pitch_value = voice_chars.get("pitch", "نرمال")
        if isinstance(pitch_value, str):
            pitch = None
        else:
            pitch = float(pitch_value) if pitch_value else None
        
        tone_quality = voice_chars.get("tone", "نامشخص")
        speech_rate = None  # در صورت نیاز می‌توان محاسبه کرد
        
        # ساخت تشخیص بوعلی
        avicenna_diagnosis = f"کیفیت صدا: {tone_quality}"
        if health_assessment.get("warnings"):
            avicenna_diagnosis += f" | هشدارها: {', '.join(health_assessment['warnings'])}"
        
        return {
            "pitch": pitch,
            "tone_quality": tone_quality,
            "speech_rate": speech_rate,
            "avicenna_diagnosis": avicenna_diagnosis,
            "recommendations": {
                "immediate": health_assessment.get("recommendations", []),
                "lifestyle": [],
                "medical": []
            }
        }
    
    def _interpret_ey_for_health(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """تفسیر نتایج چشم برای سلامت"""
        indicators = {
            "overall_status": "خوب",
            "warnings": [],
            "recommendations": []
        }
        
        sclera = analysis.get("sclera", {})
        if sclera.get("yellowness", 0) > 0.1:
            indicators["warnings"].append("زردی احتمالی صلبیه - بررسی کبد")
            indicators["recommendations"].append("مشاوره با پزشک")
        
        if sclera.get("redness", 0) > 0.3:
            indicators["warnings"].append("قرمزی چشم - احتمال التهاب")
            indicators["recommendations"].append("استراحت و کمپرس سرد")
        
        return indicators
    
    def _interpret_voice_for_health(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """تفسیر نتایج صدا برای سلامت"""
        assessment = {
            "status": "نرمال",
            "warnings": [],
            "recommendations": []
        }
        
        voice_chars = analysis.get("voice_characteristics", {})
        if voice_chars.get("hoarseness", 0) > 0.3:
            assessment["warnings"].append("خشونت صدا - احتمال التهاب حنجره")
            assessment["recommendations"].append("استراحت صوتی و نوشیدن مایعات گرم")
        
        respiratory = analysis.get("respiratory_indicators", {})
        if respiratory.get("wheezing", False):
            assessment["warnings"].append("صدای ویز - احتمال مشکل تنفسی")
            assessment["recommendations"].append("مشاوره فوری با پزشک")
        
        return assessment
    
    async def quick_health_check(
        self, 
        symptoms: List[str], 
        vitals: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """بررسی سریع سلامت"""
        # این متد باید با AI تکمیل شود
        probable_conditions = []
        recommendations = {
            "immediate": [],
            "lifestyle": [],
            "dietary": []
        }
        
        # تحلیل اولیه علائم
        if "تب" in symptoms or "fever" in [s.lower() for s in symptoms]:
            probable_conditions.append("عفونت احتمالی")
            recommendations["immediate"].append("استراحت و مصرف مایعات")
        
        if "سرفه" in symptoms or "cough" in [s.lower() for s in symptoms]:
            probable_conditions.append("مشکل تنفسی")
            recommendations["immediate"].append("نوشیدن مایعات گرم")
        
        return {
            "probable_conditions": probable_conditions,
            "recommendations": recommendations,
            "urgency": "routine" if len(probable_conditions) == 0 else "soon"
        }
