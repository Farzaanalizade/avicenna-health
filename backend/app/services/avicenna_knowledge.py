from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass
import json

class MizajType(str, Enum):
    """انواع مزاج در طب سنتی"""
    GARM = "گرم"
    SARD = "سرد"
    TAR = "تر"
    KHOSHK = "خشک"
    GARM_TAR = "گرم و تر"
    GARM_KHOSHK = "گرم و خشک"
    SARD_TAR = "سرد و تر"
    SARD_KHOSHK = "سرد و خشک"
    MOTADEL = "معتدل"

@dataclass
class FoodItem:
    """مشخصات غذا در طب سنتی"""
    name: str
    mizaj: MizajType
    benefits: List[str]
    harms: List[str]
    islah: Optional[str] = None  # مصلح

@dataclass
class HerbalMedicine:
    """مشخصات داروی گیاهی"""
    name: str
    scientific_name: str
    mizaj: MizajType
    properties: List[str]
    uses: List[str]
    dosage: str
    warnings: List[str]

class AvicennaKnowledge:
    """پایگاه دانش طب سنتی ابن سینا"""
    """پایگاه دانش طب سنتی ابن سینا"""
    
    # دانش تحلیل زبان
    TONGUE_COLOR_MEANINGS = {
        "قرمز روشن": {
            "mizaj": "گرم",
            "indication": "افزایش حرارت بدن",
            "recommendations": ["مصرف غذاهای سرد", "نوشیدن آب خنک", "استراحت"]
        },
        "قرمز تیره": {
            "mizaj": "گرم و خشک",
            "indication": "التهاب یا عفونت",
            "recommendations": ["مصرف شربت‌های خنک", "پرهیز از غذاهای گرم"]
        },
        "صورتی": {
            "mizaj": "معتدل",
            "indication": "سلامت عمومی خوب",
            "recommendations": ["ادامه رژیم متعادل"]
        },
        "سفید": {
            "mizaj": "سرد",
            "indication": "ضعف یا کم‌خونی",
            "recommendations": ["مصرف غذاهای مقوی", "گوشت قرمز", "عسل"]
        },
        "زرد": {
            "mizaj": "گرم و خشک (صفراوی)",
            "indication": "مشکل کبدی یا صفراوی",
            "recommendations": ["مصرف کاسنی", "سکنجبین", "غذاهای سبک"]
        },
        "بنفش یا کبود": {
            "mizaj": "سرد و خشک",
            "indication": "مشکل گردش خون",
            "recommendations": ["ورزش", "ماساژ", "غذاهای گرم"]
        }
    }
    
    TONGUE_COATING_ANALYSIS = {
        "بدون پوشش": {
            "indication": "خشکی بدن یا ضعف معده",
            "recommendations": ["نوشیدن مایعات", "غذاهای مرطوب"]
        },
        "پوشش سفید نازک": {
            "indication": "وضعیت طبیعی",
            "recommendations": ["ادامه عادات سالم"]
        },
        "پوشش سفید ضخیم": {
            "indication": "رطوبت و بلغم زیاد",
            "recommendations": ["کاهش لبنیات", "مصرف ادویه‌های گرم"]
        },
        "پوشش زرد": {
            "indication": "حرارت و صفرا",
            "recommendations": ["غذاهای خنک", "پرهیز از سرخ‌کردنی"]
        },
        "پوشش قهوه‌ای": {
            "indication": "مشکل گوارشی شدید",
            "recommendations": ["رژیم سبک", "مشاوره پزشکی"]
        }
    }
    
    # دانش غذاها
    FOODS_DATABASE = {
        "گندم": FoodItem(
            name="گندم",
            mizaj=MizajType.GARM_TAR,
            benefits=["مقوی", "ملین", "مفید برای ریه"],
            harms=["نفاخ", "دیرهضم برای معده ضعیف"],
            islah="زنجبیل"
        ),
        "برنج": FoodItem(
            name="برنج",
            mizaj=MizajType.SARD_KHOSHK,
            benefits=["قابض", "مفید برای اسهال", "آرام‌بخش"],
            harms=["یبوست‌آور", "کاهش میل جنسی"],
            islah="عسل و دارچین"
        ),
        "عسل": FoodItem(
            name="عسل",
            mizaj=MizajType.GARM_KHOSHK,
            benefits=["مقوی قلب", "ضدعفونی", "ملین", "مفید برای سرفه"],
            harms=["مضر برای صفراوی‌مزاج‌ها"],
            islah="سرکه"
        ),
        "سیب": FoodItem(
            name="سیب",
            mizaj=MizajType.SARD_TAR,
            benefits=["مقوی قلب", "مفید برای معده", "ضد تب"],
            harms=["نفاخ"],
            islah="عسل"
        ),
        "انار": FoodItem(
            name="انار",
            mizaj=MizajType.SARD,
            benefits=["قابض", "مقوی معده", "ضد عطش"],
            harms=["مضر برای سینه و ریه"],
            islah="عسل یا شکر"
        ),
        "زعفران": FoodItem(
            name="زعفران",
            mizaj=MizajType.GARM_KHOSHK,
            benefits=["مقوی قلب", "ضد افسردگی", "مقوی حافظه"],
            harms=["سردرد در مصرف زیاد"],
            islah="کافور"
        ),
        "گوشت گوسفند": FoodItem(
            name="گوشت گوسفند",
            mizaj=MizajType.GARM_TAR,
            benefits=["مقوی", "مولد خون", "مفید برای لاغری"],
            harms=["سنگین", "مولد بلغم"],
            islah="سرکه و نعناع"
        ),
        "ماهی": FoodItem(
            name="ماهی",
            mizaj=MizajType.SARD_TAR,
            benefits=["سبک", "مفید برای مغز", "ملین"],
            harms=["مولد بلغم"],
            islah="فلفل و زنجبیل"
        ),
        "خیار": FoodItem(
            name="خیار",
            mizaj=MizajType.SARD_TAR,
            benefits=["رفع عطش", "خنک‌کننده", "مدر"],
            harms=["دیرهضم", "مضر برای معده سرد"],
            islah="نمک و نعناع"
        ),
        "هویج": FoodItem(
            name="هویج",
            mizaj=MizajType.GARM,
            benefits=["مقوی بینایی", "مدر", "مفید برای کبد"],
            harms=["نفاخ"],
            islah="سیاه‌دانه"
        )
    }
    
    # دانش داروهای گیاهی
    HERBAL_MEDICINES = {
        "زنجبیل": HerbalMedicine(
            name="زنجبیل",
            scientific_name="Zingiber officinale",
            mizaj=MizajType.GARM_KHOSHK,
            properties=["ضد تهوع", "گرم‌کننده", "هاضم", "ضد التهاب"],
            uses=["سرماخوردگی", "مشکلات گوارشی", "دردهای مفصلی"],
            dosage="3-5 گرم پودر در روز",
            warnings=["احتیاط در بارداری", "تداخل با داروهای ضد انعقاد"]
        ),
        "زعفران": HerbalMedicine(
            name="زعفران",
            scientific_name="Crocus sativus",
            mizaj=MizajType.GARM_KHOSHK,
            properties=["ضد افسردگی", "مقوی قلب", "تنظیم قاعدگی"],
            uses=["افسردگی", "اضطراب", "مشکلات قاعدگی"],
            dosage="30-50 میلی‌گرم در روز",
            warnings=["عدم مصرف زیاد", "احتیاط در بارداری"]
        ),
        "گل گاوزبان": HerbalMedicine(
            name="گل گاوزبان",
            scientific_name="Echium amoenum",
            mizaj=MizajType.GARM_TAR,
            properties=["آرام‌بخش", "ضد اضطراب", "مقوی اعصاب"],
            uses=["اضطراب", "بی‌خوابی", "تپش قلب عصبی"],
            dosage="دم‌کرده 5-10 گرم در روز",
            warnings=["عدم مصرف طولانی مدت"]
        ),
        "نعناع": HerbalMedicine(
            name="نعناع",
            scientific_name="Mentha piperita",
            mizaj=MizajType.GARM_KHOSHK,
            properties=["ضد نفخ", "هاضم", "ضد تشنج"],
            uses=["مشکلات گوارشی", "سردرد", "سرماخوردگی"],
            dosage="دم‌کرده 3-5 گرم سه بار در روز",
            warnings=["احتیاط در رفلاکس معده"]
        ),
        "بابونه": HerbalMedicine(
            name="بابونه",
            scientific_name="Matricaria chamomilla",
            mizaj=MizajType.GARM,
            properties=["ضد التهاب", "آرام‌بخش", "ضد اسپاسم"],
            uses=["بی‌خوابی", "دل‌درد", "التهاب"],
            dosage="دم‌کرده 3-5 گرم در روز",
            warnings=["حساسیت در افراد آلرژیک"]
        )
    }
    
    # سیستم توصیه بر اساس مزاج
    MIZAJ_RECOMMENDATIONS = {
        MizajType.GARM: {
            "suitable_foods": ["خیار", "کاهو", "ماست", "انار", "هندوانه"],
            "avoid_foods": ["فلفل", "زنجبیل", "گوشت قرمز", "عسل"],
            "lifestyle": ["خواب کافی", "محیط خنک", "ورزش ملایم"],
            "herbs": ["گل گاوزبان", "بیدمشک", "گلاب"]
        },
        MizajType.SARD: {
            "suitable_foods": ["عسل", "خرما", "گوشت", "زنجبیل", "دارچین"],
            "avoid_foods": ["خیار", "هندوانه", "دوغ", "کاهو"],
            "lifestyle": ["ورزش منظم", "محیط گرم", "ماساژ با روغن گرم"],
            "herbs": ["زنجبیل", "دارچین", "فلفل سیاه"]
        },
        MizajType.TAR: {
            "suitable_foods": ["نخود", "عدس", "گوشت بدون چربی"],
            "avoid_foods": ["شیر", "ماست", "برنج", "موز"],
            "lifestyle": ["ورزش هوازی", "سونا", "کاهش خواب"],
            "herbs": ["زیره", "زنیان", "پونه"]
        },
        MizajType.KHOSHK: {
            "suitable_foods": ["شیر", "کره", "بادام", "کنجد", "روغن زیتون"],
            "avoid_foods": ["عدس", "چای", "قهوه"],
            "lifestyle": ["خواب کافی", "حمام آب گرم", "ماساژ با روغن"],
            "herbs": ["بنفشه", "خاکشیر", "اسفرزه"]
        }
    }
    
    @classmethod
    def analyze_mizaj_from_symptoms(cls, symptoms: Dict[str, Any]) -> MizajType:
        """تعیین مزاج بر اساس علائم"""
        score = {"garm": 0, "sard": 0, "tar": 0, "khoshk": 0}
        
        # تحلیل دمای بدن
        if symptoms.get("body_temperature", "normal") == "warm":
            score["garm"] += 1
        elif symptoms.get("body_temperature") == "cold":
            score["sard"] += 1
        
        # تحلیل پوست
        if symptoms.get("skin_condition") == "dry":
            score["khoshk"] += 1
        elif symptoms.get("skin_condition") == "oily":
            score["tar"] += 1
        
        # تحلیل خواب
        if symptoms.get("sleep_quality") == "light":
            score["garm"] += 1
            score["khoshk"] += 1
        elif symptoms.get("sleep_quality") == "heavy":
            score["sard"] += 1
            score["tar"] += 1
        
        # تحلیل اشتها
        if symptoms.get("appetite") == "high":
            score["garm"] += 1
        elif symptoms.get("appetite") == "low":
            score["sard"] += 1
        
        # تحلیل تعریق
        if symptoms.get("sweating") == "high":
            score["tar"] += 1
        elif symptoms.get("sweating") == "low":
            score["khoshk"] += 1
        
        # تعیین مزاج غالب
        max_score = max(score.values())
        if max_score == 0:
            return MizajType.MOTADEL
        
        # ترکیب مزاج‌ها
        dominant = [k for k, v in score.items() if v == max_score]
        
        if len(dominant) == 1:
            if dominant[0] == "garm":
                return MizajType.GARM
            elif dominant[0] == "sard":
                return MizajType.SARD
            elif dominant[0] == "tar":
                return MizajType.TAR
            else:
                return MizajType.KHOSHK
        elif len(dominant) == 2:
            if "garm" in dominant and "tar" in dominant:
                return MizajType.GARM_TAR
            elif "garm" in dominant and "khoshk" in dominant:
                return MizajType.GARM_KHOSHK
            elif "sard" in dominant and "tar" in dominant:
                return MizajType.SARD_TAR
            elif "sard" in dominant and "khoshk" in dominant:
                return MizajType.SARD_KHOSHK
        
        return MizajType.MOTADEL
    
    @classmethod
    def get_food_recommendations(cls, mizaj: MizajType, health_condition: Optional[str] = None) -> Dict[str, List[str]]:
        """توصیه‌های غذایی بر اساس مزاج و وضعیت سلامت"""
        recommendations = cls.MIZAJ_RECOMMENDATIONS.get(mizaj, {})
        
        # اضافه کردن توصیه‌های خاص برای شرایط سلامت
        if health_condition:
            if health_condition == "سرماخوردگی":
                recommendations["herbs"] = recommendations.get("herbs", []) + ["زنجبیل", "نعناع"]
                recommendations["suitable_foods"] = recommendations.get("suitable_foods", []) + ["سوپ مرغ", "عسل"]
            elif health_condition == "یبوست":
                recommendations["suitable_foods"] = recommendations.get("suitable_foods", []) + ["انجیر", "آلو", "روغن زیتون"]
            elif health_condition == "بی‌خوابی":
                recommendations["herbs"] = recommendations.get("herbs", []) + ["بابونه", "گل گاوزبان"]
        
        return recommendations
    
    @classmethod
    def get_herbal_medicine_info(cls, herb_name: str) -> Optional[HerbalMedicine]:
        """دریافت اطلاعات داروی گیاهی"""
        return cls.HERBAL_MEDICINES.get(herb_name)
    
    @classmethod
    def get_food_info(cls, food_name: str) -> Optional[FoodItem]:
        """دریافت اطلاعات غذا"""
        return cls.FOODS_DATABASE.get(food_name)
    
    @classmethod
    def analyze_tongue_color(cls, color: str) -> Dict[str, Any]:
        """تحلیل رنگ زبان"""
        return cls.TONGUE_COLOR_MEANINGS.get(color, {
            "mizaj": "نامشخص",
            "indication": "نیاز به بررسی بیشتر",
            "recommendations": ["مشاوره با متخصص"]
        })
    
    @classmethod
    def analyze_tongue_coating(cls, coating_type: str) -> Dict[str, Any]:
        """تحلیل پوشش زبان"""
        return cls.TONGUE_COATING_ANALYSIS.get(coating_type, {
            "indication": "نیاز به بررسی بیشتر",
            "recommendations": ["مشاوره با متخصص"]
        })
    
    @classmethod
    def get_personalized_recommendations(cls, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """توصیه‌های شخصی‌سازی شده بر اساس وضعیت بیمار"""
        mizaj = patient_data.get("mizaj", MizajType.MOTADEL)
        age = patient_data.get("age", 30)
        gender = patient_data.get("gender", "unknown")
        conditions = patient_data.get("conditions", [])
        
        recommendations = {
            "dietary": cls.get_food_recommendations(mizaj),
            "herbal": [],
            "lifestyle": [],
            "warnings": []
        }
        
        # توصیه‌های سنی
        if age > 60:
            recommendations["dietary"]["suitable_foods"] = recommendations["dietary"].get("suitable_foods", []) + ["شیر", "عسل", "بادام"]
            recommendations["lifestyle"].append("ورزش ملایم روزانه")
        elif age < 20:
            recommendations["dietary"]["suitable_foods"] = recommendations["dietary"].get("suitable_foods", []) + ["گوشت", "تخم‌مرغ", "حبوبات"]
        
        # توصیه‌های جنسیتی
        if gender == "female":
            recommendations["herbal"].append("زعفران برای تنظیم قاعدگی")
            recommendations["dietary"]["suitable_foods"] = recommendations["dietary"].get("suitable_foods", []) + ["خرما", "کنجد"]
        
        # توصیه‌های بر اساس شرایط خاص
        for condition in conditions:
            if "دیابت" in condition:
                recommendations["warnings"].append("محدودیت مصرف قند و کربوهیدرات")
                recommendations["dietary"]["avoid_foods"] = recommendations["dietary"].get("avoid_foods", []) + ["خرما", "عسل", "انگور"]
            elif "فشار خون" in condition:
                recommendations["warnings"].append("محدودیت مصرف نمک")
                recommendations["lifestyle"].append("مدیریت استرس")
        
        return recommendations

# Alias for backward compatibility
AvicennaKnowledgeBase = AvicennaKnowledge
