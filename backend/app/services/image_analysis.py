"""
سرویس تحلیل تصاویر - زبان و چشم
"""
import base64
import json
from typing import Dict, Optional, Tuple
from pathlib import Path
import os


class ImageAnalysisService:
    """سرویس تحلیل تصاویر براساس AI"""
    
    def __init__(self):
        """مقدار‌دهی سرویس"""
        self.models_dir = Path(__file__).parent.parent.parent / "ml_models"
        self.tongue_model_path = self.models_dir / "saved_models" / "tongue_analyzer.pkl"
        self.eye_model_path = self.models_dir / "saved_models" / "eye_analyzer.pkl"
    
    @staticmethod
    def encode_image_to_base64(image_path: str) -> str:
        """تبدیل تصویر به base64"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"خطا در بارگذاری تصویر: {e}")
            return ""
    
    @staticmethod
    def decode_base64_to_image(base64_string: str, output_path: str) -> bool:
        """تبدیل base64 به تصویر"""
        try:
            with open(output_path, "wb") as image_file:
                image_file.write(base64.b64decode(base64_string))
            return True
        except Exception as e:
            print(f"خطا در ذخیره تصویر: {e}")
            return False
    
    @staticmethod
    def analyze_tongue_image(image_path: str) -> Dict:
        """
        تحلیل تصویر زبان
        
        Returns:
            {
                "color": str,
                "coating": str,
                "moisture": str,
                "texture": str,
                "cracks_detected": bool,
                "confidence_score": float,
                "potential_conditions": [{name: str, probability: float}],
                "analysis_details": {}
            }
        """
        try:
            # در نسخه عملی، از مدل ML واقعی استفاده می‌شود
            # اینجا شبیه‌سازی است:
            
            analysis = {
                "color": "pink",  # صورتی = سالم
                "coating": "none",  # بدون پوشش = سالم
                "moisture": "normal",  # رطوبت طبیعی
                "texture": "smooth",  # بافت صاف
                "cracks_detected": False,
                "confidence_score": 0.85,
                "potential_conditions": [],
                "analysis_details": {
                    "rgb_analysis": {
                        "red_average": 220,
                        "green_average": 150,
                        "blue_average": 140
                    },
                    "texture_analysis": {
                        "smoothness": 0.9,
                        "uniformity": 0.85
                    },
                    "abnormalities": []
                },
                "recommendation": "وضعیت طبیعی و سالم"
            }
            
            return analysis
            
        except Exception as e:
            print(f"خطا در تحلیل تصویر زبان: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def analyze_eye_image(image_path: str) -> Dict:
        """
        تحلیل تصویر چشم
        
        Returns:
            {
                "redness_level": float,
                "yellowness_detected": bool,
                "pupil_size": str,
                "clarity": str,
                "confidence_score": float,
                "potential_conditions": [{name: str, probability: float}],
                "analysis_details": {}
            }
        """
        try:
            # شبیه‌سازی تحلیل
            
            analysis = {
                "redness_level": 2,  # 0-10 (0 = سفید، 10 = قرمز)
                "yellowness_detected": False,
                "pupil_size": "normal",  # normal, dilated, constricted
                "clarity": "clear",  # clear, cloudy
                "white_color": "clear",  # وضوح سفید چشم
                "confidence_score": 0.82,
                "potential_conditions": [],
                "analysis_details": {
                    "sclera_analysis": {
                        "color": "white",
                        "clarity": 0.9
                    },
                    "pupil_analysis": {
                        "size": "normal",
                        "symmetry": 0.95,
                        "reactivity": "normal"
                    },
                    "iris_analysis": {
                        "color": "brown",
                        "pattern_clarity": 0.88
                    }
                },
                "recommendation": "وضعیت طبیعی و سالم"
            }
            
            return analysis
            
        except Exception as e:
            print(f"خطا در تحلیل تصویر چشم: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def detect_tongue_abnormalities(analysis: Dict) -> list:
        """شناسایی غیرعادی‌های زبان"""
        abnormalities = []
        
        # بررسی رنگ
        if analysis.get("color") == "red":
            abnormalities.append({"type": "رنگ قرمز", "severity": "متوسط", "meaning": "نشانگر گرما"})
        elif analysis.get("color") == "pale":
            abnormalities.append({"type": "رنگ رنگ‌پریده", "severity": "متوسط", "meaning": "نشانگر سردی/خونریزی"})
        
        # بررسی پوشش
        if analysis.get("coating") == "white":
            abnormalities.append({"type": "پوشش سفید", "severity": "خفیف", "meaning": "نشانگر سردی"})
        elif analysis.get("coating") == "yellow":
            abnormalities.append({"type": "پوشش زرد", "severity": "متوسط", "meaning": "نشانگر گرما"})
        elif analysis.get("coating") == "thick":
            abnormalities.append({"type": "پوشش ضخیم", "severity": "متوسط", "meaning": "نشانگر رطوبت زیاد"})
        
        # بررسی رطوبت
        if analysis.get("moisture") == "dry":
            abnormalities.append({"type": "خشک", "severity": "خفیف", "meaning": "نشانگر خشکی"})
        elif analysis.get("moisture") == "wet":
            abnormalities.append({"type": "مرطوب", "severity": "خفیف", "meaning": "نشانگر رطوبت"})
        
        # بررسی ترک
        if analysis.get("cracks_detected"):
            abnormalities.append({"type": "ترک‌های زبان", "severity": "متوسط", "meaning": "نشانگر خشکی طولانی"})
        
        # بررسی بافت
        if analysis.get("texture") == "bumpy":
            abnormalities.append({"type": "بافت نامنظم", "severity": "خفیف", "meaning": "نشانگر التهاب"})
        
        return abnormalities
    
    @staticmethod
    def detect_eye_abnormalities(analysis: Dict) -> list:
        """شناسایی غیرعادی‌های چشم"""
        abnormalities = []
        
        # بررسی قرمزی
        if analysis.get("redness_level", 0) > 5:
            abnormalities.append({
                "type": "قرمزی شدید",
                "severity": "متوسط",
                "meaning": "نشانگر التهاب یا خستگی"
            })
        elif analysis.get("redness_level", 0) > 2:
            abnormalities.append({
                "type": "قرمزی خفیف",
                "severity": "خفیف",
                "meaning": "نشانگر خستگی"
            })
        
        # بررسی زردی
        if analysis.get("yellowness_detected"):
            abnormalities.append({
                "type": "زردی",
                "severity": "شدید",
                "meaning": "نشانگر اختلال کبد"
            })
        
        # بررسی تیرگی
        if analysis.get("clarity") == "cloudy":
            abnormalities.append({
                "type": "تیرگی",
                "severity": "شدید",
                "meaning": "نشانگر عدم‌وضوح"
            })
        
        # بررسی مردمک
        if analysis.get("pupil_size") == "dilated":
            abnormalities.append({
                "type": "مردمک بزرگ",
                "severity": "خفیف",
                "meaning": "نشانگر تنطیم نور ضعیف"
            })
        elif analysis.get("pupil_size") == "constricted":
            abnormalities.append({
                "type": "مردمک کوچک",
                "severity": "خفیف",
                "meaning": "نشانگر نور زیاد یا اختلال"
            })
        
        return abnormalities
    
    @staticmethod
    def correlate_tongue_with_organs(analysis: Dict) -> Dict:
        """تطابق نشانگرهای زبان با اعضای بدن"""
        organ_map = {
            "قلب": {
                "location": "نوک زبان",
                "indicators": ["رنگ قرمز", "سوزش"]
            },
            "ریه": {
                "location": "لبه زبان جلوی",
                "indicators": ["سفید", "رطوبت زیاد"]
            },
            "کبد": {
                "location": "لبه زبان عقب",
                "indicators": ["زردی", "پوشش زرد"]
            },
            "طحال": {
                "location": "وسط زبان",
                "indicators": ["پوشش سفید", "چاقی"]
            },
            "کلیه": {
                "location": "عقب زبان",
                "indicators": ["رنگ تیره", "خشکی"]
            },
            "معده": {
                "location": "لبه زبان وسط",
                "indicators": ["پوشش قیچی‌شکل", "گرما"]
            }
        }
        
        affected_organs = {}
        
        if analysis.get("color") == "red":
            affected_organs["قلب"] = "احتمالی"
        if analysis.get("coating") == "white":
            affected_organs["ریه/طحال"] = "احتمالی"
        if analysis.get("coating") == "yellow":
            affected_organs["کبد"] = "احتمالی"
        if analysis.get("moisture") == "dry":
            affected_organs["کلیه"] = "احتمالی"
        
        return {
            "organ_map": organ_map,
            "affected_organs": affected_organs
        }
    
    @staticmethod
    def get_health_recommendations(tongue_analysis: Dict, eye_analysis: Dict) -> Dict:
        """استخراج توصیه‌های سلامتی از تحلیل‌های تصویری"""
        
        recommendations = {
            "immediate_actions": [],
            "dietary_changes": [],
            "lifestyle_changes": [],
            "medical_consultation": False,
            "urgency_level": "عادی"
        }
        
        # بررسی زبان
        if tongue_analysis.get("cracks_detected"):
            recommendations["dietary_changes"].append("افزایش مصرف آب و رطوبت")
            recommendations["urgency_level"] = "متوسط"
        
        if tongue_analysis.get("coating") == "yellow":
            recommendations["dietary_changes"].append("کاهش غذاهای گرم و چرب")
            recommendations["lifestyle_changes"].append("استراحت بیشتر")
        
        # بررسی چشم
        if eye_analysis.get("redness_level", 0) > 5:
            recommendations["immediate_actions"].append("استراحت چشم از صفحه نمایش")
            recommendations["dietary_changes"].append("مصرف بیشتر سبزیجات سبز")
        
        if eye_analysis.get("yellowness_detected"):
            recommendations["medical_consultation"] = True
            recommendations["urgency_level"] = "فوری"
        
        return recommendations
