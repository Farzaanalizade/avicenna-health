"""
سرویس‌های AI برای تحلیل خودکار داده‌های تشخیصی
"""
import json
from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.avicenna_diagnosis import (
    PulseAnalysis, UrineAnalysis, TongueCoating, DiagnosticFinding
)
from app.models.avicenna_diseases import Disease, Symptom, TraditionalRemedy
from app.crud.avicenna_diseases import DiseaseOps, TraditionalRemedyOps


class AvicennaAnalysisEngine:
    """موتور تحلیل بر اساس اصول سینا"""
    
    # جدول تطابق نبض و مزاج
    PULSE_MIZAJ_MAP = {
        "kabir": ["garm", "tar"],          # پر
        "saghir": ["sard", "khoshk"],      # کوچک
        "tavil": ["tar"],                   # طویل
        "qasir": ["khoshk"],                # کوتاه
        "sare_en": ["garm"],                # سریع
        "beth_in": ["sard"],                # آهسته
        "qavi": ["garm"],                   # قوی
        "zaeef": ["sard", "khoshk"],        # ضعیف
    }
    
    # جدول تطابق ادرار و مزاج
    URINE_COLOR_MIZAJ_MAP = {
        "zard": ["garm"],                   # زرد = گرم
        "ghermez": ["garm_tar"],            # قرمز = گرم تر
        "sefid": ["sard", "khoshk"],        # سفید = سرد خشک
        "tarik": ["sard"],                  # تیره = سرد
    }
    
    URINE_DENSITY_MIZAJ_MAP = {
        "saqil": ["garm"],                  # سنگین = گرم
        "motavasseta": ["motadel"],         # متوسط = متعادل
        "khafif": ["sard"],                 # سبک = سرد
    }
    
    # جدول تطابق زبان و مزاج
    TONGUE_COLOR_MIZAJ_MAP = {
        "ghermez": ["garm"],                # قرمز = گرم
        "pale": ["sard"],                   # رنگ‌پریده = سرد
        "pink": ["motadel"],                # صورتی = متعادل
    }
    
    @staticmethod
    def analyze_pulse(pulse: PulseAnalysis, db: Session) -> Dict:
        """تحلیل نبض و استخراج نشانگرهای مزاج"""
        
        mizaj_scores = {
            "garm": 0,
            "sard": 0,
            "tar": 0,
            "khoshk": 0,
        }
        
        # تحلیل بر اساس نوع نبض
        if pulse.primary_type and pulse.primary_type in AvicennaAnalysisEngine.PULSE_MIZAJ_MAP:
            for mizaj in AvicennaAnalysisEngine.PULSE_MIZAJ_MAP[pulse.primary_type]:
                mizaj_scores[mizaj] += 2
        
        # تحلیل بر اساس قوت
        if pulse.strength == "قوی":
            mizaj_scores["garm"] += 1
        elif pulse.strength == "ضعیف":
            mizaj_scores["sard"] += 1
        
        # تحلیل بر اساس سرعت (مستفاد از ریتم)
        if pulse.rhythm == "سریع":
            mizaj_scores["garm"] += 1
        elif pulse.rhythm == "آهسته":
            mizaj_scores["sard"] += 1
        
        # تحلیل بر اساس دما
        if pulse.temperature:
            if pulse.temperature > 37.5:
                mizaj_scores["garm"] += 2
            elif pulse.temperature < 36.5:
                mizaj_scores["sard"] += 2
        
        # تحلیل بر اساس عمق (سطحی = تر، عمیق = خشک)
        if pulse.depth == "سطحی":
            mizaj_scores["tar"] += 1
        elif pulse.depth == "عمیق":
            mizaj_scores["khoshk"] += 1
        
        # تحلیل بر اساس عرض (پهن = تر، باریک = خشک)
        if pulse.width == "پهن":
            mizaj_scores["tar"] += 1
        elif pulse.width == "باریک":
            mizaj_scores["khoshk"] += 1
        
        # محاسبه مزاج غالب
        dominant_mizaj = max(mizaj_scores, key=mizaj_scores.get)
        
        return {
            "scores": mizaj_scores,
            "dominant_mizaj": dominant_mizaj,
            "confidence": min(mizaj_scores[dominant_mizaj] / 10, 1.0),
            "assessment": AvicennaAnalysisEngine._get_pulse_assessment(pulse)
        }
    
    @staticmethod
    def analyze_urine(urine: UrineAnalysis, db: Session) -> Dict:
        """تحلیل ادرار و استخراج نشانگرهای مزاج"""
        
        mizaj_scores = {
            "garm": 0,
            "sard": 0,
            "tar": 0,
            "khoshk": 0,
        }
        
        # تحلیل رنگ
        if urine.color and urine.color in AvicennaAnalysisEngine.URINE_COLOR_MIZAJ_MAP:
            for mizaj in AvicennaAnalysisEngine.URINE_COLOR_MIZAJ_MAP[urine.color]:
                mizaj_scores[mizaj] += 2
        
        # تحلیل چگالی
        if urine.density and urine.density in AvicennaAnalysisEngine.URINE_DENSITY_MIZAJ_MAP:
            for mizaj in AvicennaAnalysisEngine.URINE_DENSITY_MIZAJ_MAP[urine.density]:
                mizaj_scores[mizaj] += 1
        
        # تحلیل شفافیت (شفاف = سالم، تیره = مریض)
        if urine.clarity == "شفاف":
            pass  # نشانگر خوب
        elif urine.clarity == "تیره":
            mizaj_scores["garm"] += 1  # نشانگر بیماری
        
        # تحلیل کف (کف زیاد = رطوبت زیاد)
        if urine.foam == "زیاد":
            mizaj_scores["tar"] += 1
        
        # تحلیل رسوب (رسوب = بیماری)
        if urine.sediment_present:
            mizaj_scores["sard"] += 1
        
        # تحلیل پروتئین (پروتئین = بیماری)
        if urine.protein_level and urine.protein_level != "منفی":
            mizaj_scores["garm"] += 1
        
        # محاسبه مزاج غالب
        dominant_mizaj = max(mizaj_scores, key=mizaj_scores.get)
        
        return {
            "scores": mizaj_scores,
            "dominant_mizaj": dominant_mizaj,
            "confidence": min(mizaj_scores[dominant_mizaj] / 10, 1.0),
            "health_status": AvicennaAnalysisEngine._get_urine_health_status(urine)
        }
    
    @staticmethod
    def analyze_tongue(tongue: TongueCoating, db: Session) -> Dict:
        """تحلیل زبان و استخراج نشانگرهای مزاج"""
        
        mizaj_scores = {
            "garm": 0,
            "sard": 0,
            "tar": 0,
            "khoshk": 0,
        }
        
        # تحلیل رنگ
        if tongue.body_color and tongue.body_color in AvicennaAnalysisEngine.TONGUE_COLOR_MIZAJ_MAP:
            for mizaj in AvicennaAnalysisEngine.TONGUE_COLOR_MIZAJ_MAP[tongue.body_color]:
                mizaj_scores[mizaj] += 2
        
        # تحلیل پوشش
        if tongue.coating_color == "زرد":
            mizaj_scores["garm"] += 1
        elif tongue.coating_color == "سفید":
            mizaj_scores["sard"] += 1
        
        # تحلیل ضخامت پوشش (پوشش ضخیم = تر)
        if tongue.coating_thickness == "ضخیم":
            mizaj_scores["tar"] += 1
        elif tongue.coating_thickness == "نازک":
            mizaj_scores["khoshk"] += 1
        
        # تحلیل رطوبت
        if tongue.moisture_level == "مرطوب":
            mizaj_scores["tar"] += 1
        elif tongue.moisture_level == "خشک":
            mizaj_scores["khoshk"] += 1
        
        # تحلیل ترک‌های زبان (ترک = خشکی)
        if tongue.cracks_pattern:
            mizaj_scores["khoshk"] += 1
        
        # تحلیل اثر دندان (اثر = تورم)
        if tongue.tooth_marks:
            mizaj_scores["tar"] += 1
        
        # تحلیل نوک‌های زبان (برجسته = گرم)
        if tongue.bumps_or_papillae == "برجسته":
            mizaj_scores["garm"] += 1
        
        # محاسبه مزاج غالب
        dominant_mizaj = max(mizaj_scores, key=mizaj_scores.get)
        
        return {
            "scores": mizaj_scores,
            "dominant_mizaj": dominant_mizaj,
            "confidence": min(mizaj_scores[dominant_mizaj] / 10, 1.0),
            "organ_indicators": AvicennaAnalysisEngine._get_tongue_organ_indicators(tongue)
        }
    
    @staticmethod
    def synthesize_diagnosis(
        pulse_analysis: Dict,
        urine_analysis: Dict,
        tongue_analysis: Dict
    ) -> Dict:
        """ترکیب تحلیل‌های نبض، ادرار و زبان برای تشخیص جامع"""
        
        # میانگین‌گیری از سه تحلیل
        combined_scores = {
            "garm": 0,
            "sard": 0,
            "tar": 0,
            "khoshk": 0,
        }
        
        for mizaj in combined_scores:
            combined_scores[mizaj] = (
                pulse_analysis["scores"].get(mizaj, 0) +
                urine_analysis["scores"].get(mizaj, 0) +
                tongue_analysis["scores"].get(mizaj, 0)
            ) / 3
        
        # تحدید مزاج اولیه و ثانویه
        sorted_mizajs = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        primary_mizaj = sorted_mizajs[0][0]
        secondary_mizaj = sorted_mizajs[1][0] if len(sorted_mizajs) > 1 else None
        
        return {
            "combined_scores": combined_scores,
            "primary_mizaj": primary_mizaj,
            "secondary_mizaj": secondary_mizaj,
            "overall_confidence": (
                pulse_analysis["confidence"] +
                urine_analysis["confidence"] +
                tongue_analysis["confidence"]
            ) / 3
        }
    
    @staticmethod
    def _get_pulse_assessment(pulse: PulseAnalysis) -> str:
        """ارزیابی وضعیت براساس نبض"""
        if pulse.strength == "قوی" and pulse.rhythm == "منتظم":
            return "وضعیت سالم و متعادل"
        elif pulse.strength == "ضعیف":
            return "ضعف عمومی و خستگی"
        elif pulse.rhythm == "نامنتظم":
            return "اختلال در گردش و بی‌نظمی"
        return "وضعیت نیاز به بررسی بیشتر"
    
    @staticmethod
    def _get_urine_health_status(urine: UrineAnalysis) -> str:
        """ارزیابی سلامت براساس ادرار"""
        status = "وضعیت سالم"
        
        if urine.sediment_present or urine.crystals_present:
            status = "نشانگر اختلال کلیوی"
        if urine.blood_present:
            status = "نشانگر خونریزی"
        if urine.protein_level and urine.protein_level != "منفی":
            status = "نشانگر اختلال کلیوی"
        
        return status
    
    @staticmethod
    def _get_tongue_organ_indicators(tongue: TongueCoating) -> Dict:
        """استخراج نشانگرهای اعضای مختلف از زبان"""
        indicators = {}
        
        if tongue.coating_color == "زرد":
            indicators["liver"] = "اختلال کبد"
        if tongue.coating_color == "سفید":
            indicators["spleen"] = "اختلال طحال"
        if tongue.body_color == "ghermez":
            indicators["heart"] = "اختلال قلب"
        if tongue.moisture_level == "خشک":
            indicators["kidney"] = "اختلال کلیه"
        if tongue.cracks_pattern:
            indicators["lung"] = "اختلال ریه"
        
        return indicators
    
    @staticmethod
    def recommend_treatments(
        primary_mizaj: str,
        secondary_mizaj: Optional[str],
        db: Session
    ) -> List[TraditionalRemedy]:
        """توصیه درمان‌های سنتی براساس مزاج"""
        
        remedies = []
        
        # درمان برای مزاج اولیه
        if primary_mizaj:
            primary_remedies = TraditionalRemedyOps.get_for_mizaj(db, primary_mizaj)
            remedies.extend(primary_remedies[:3])  # ۳ درمان برتر
        
        # درمان برای مزاج ثانویه
        if secondary_mizaj:
            secondary_remedies = TraditionalRemedyOps.get_for_mizaj(db, secondary_mizaj)
            remedies.extend(secondary_remedies[:2])  # ۲ درمان برتر
        
        # حذف تکراری‌ها
        unique_remedies = list(set(remedies))
        
        return unique_remedies
    
    @staticmethod
    def recommend_lifestyle_changes(primary_mizaj: str) -> List[str]:
        """توصیه‌های سبک زندگی براساس مزاج"""
        
        lifestyle_map = {
            "garm": [
                "کاهش فعالیت بدنی شدید",
                "خواب کافی و استراحت",
                "پرهیز از غذاهای گرم و تیز",
                "حمام آب سرد",
                "محیط خنک و تازهوا"
            ],
            "sard": [
                "افزایش فعالیت بدنی معمول",
                "غذاهای گرم و تقویت‌کننده",
                "نور آفتاب کافی",
                "حمام آب گرم",
                "محیط گرم و مناسب"
            ],
            "tar": [
                "دهکی و تعریق محدود",
                "غذاهای خشک",
                "پرهیز از غذاهای آبکی",
                "خواب کافی",
                "محیط خشک"
            ],
            "khoshk": [
                "نرم‌کننده‌های طبیعی",
                "غذاهای روغنی و چرب",
                "هیدراسیون مناسب",
                "روغن‌کشی پوست",
                "محیط مرطوب"
            ]
        }
        
        return lifestyle_map.get(primary_mizaj, [])
    
    @staticmethod
    def recommend_dietary_changes(primary_mizaj: str) -> List[str]:
        """توصیه‌های غذایی براساس مزاج"""
        
        dietary_map = {
            "garm": [
                "آب و میوه‌های سرد",
                "خیار و کدو",
                "دوغ و شیرخام",
                "گوشت مرغ بجای گوشت قرمز",
                "پرهیز از ادویه و غذاهای تیز"
            ],
            "sard": [
                "گوشت قرمز و پرچرب",
                "غذاهای گرم و دم‌شده",
                "ادویه و فلفل",
                "چای و قهوه",
                "عسل و خشکبار"
            ],
            "tar": [
                "نان خشک",
                "گوشت بریان",
                "سبزیجات خام",
                "پرهیز از آب و نوشیدنی‌های آب‌کی",
                "میوه‌های خشک"
            ],
            "khoshk": [
                "روغن زیتون",
                "دوغ و شیرخام",
                "غذاهای مرطوب",
                "آب‌میوه طازه",
                "شیرینی‌های نرم"
            ]
        }
        
        return dietary_map.get(primary_mizaj, [])
