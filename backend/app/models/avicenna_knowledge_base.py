"""
Avicenna (Ibn Sina) Medical Knowledge Models
طب بوعلی سینا و فلسفۀ پزشکی اسلامی

Based on:
- القانون في الطب (Canon of Medicine)
- کتاب الشفا (Book of Healing)
- رساله‌های پزشکی مختلف
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, Boolean, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from app.database import Base


class MizajType(str, Enum):
    """چهار مزاج اساسی در فلسفۀ پزشکی سینایی"""
    GARM_TAR = "garm_tar"          # گرم و تر (خون/خوی)
    GARM_KHOSHK = "garm_khoshk"    # گرم و خشک (صفرا/سیاہ)
    SARD_TAR = "sard_tar"          # سرد و تر (بلغم/آب)
    SARD_KHOSHK = "sard_khoshk"    # سرد و خشک (سوداء/خاک)
    MOTADEL = "motadel"            # متعادل


class HumorType(str, Enum):
    """چهار خلط اساسی بدن"""
    KHOON = "khoon"                # خون (Blood) - GARM_TAR
    SAFRA = "safra"                # صفرا (Yellow Bile) - GARM_KHOSHK
    BALGHAM = "balgham"            # بلغم (Phlegm) - SARD_TAR
    SOUDAA = "soudaa"              # سوداء (Black Bile) - SARD_KHOSHK


class AvicennaDisease(Base):
    """بیماری‌های شناخت‌شده در طب سینایی"""
    __tablename__ = "avicenna_diseases"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # نام بیماری
    persian_name = Column(String(255), nullable=False)
    arabic_name = Column(String(255), nullable=True)
    latin_name = Column(String(255), nullable=True)
    modern_equivalent = Column(String(255), nullable=True)  # معادل طب مدرن
    
    # تصنیف
    category = Column(String(100), nullable=False)  # "fever", "respiratory", "digestive"
    severity = Column(String(50))  # "minor", "moderate", "severe", "critical"
    
    # مزاج و خلط‌ها
    related_mizaj = Column(String(50), nullable=False)  # MizajType
    involved_humors = Column(JSON)  # [{"humor": "khoon", "excess": true, "deficiency": false}]
    
    # علائم و نشانه‌ها
    symptoms = Column(JSON)  # [{"symptom": "تب", "severity": "high", "frequency": "constant"}]
    tongue_signs = Column(JSON)  # علائم روی زبان
    eye_signs = Column(JSON)  # علائم روی چشم
    pulse_signs = Column(JSON)  # علائم نبض
    
    # علل و عوامل
    causes = Column(JSON)  # [{"cause": "غذای گرم", "type": "dietary", "weight": 0.7}]
    predisposing_factors = Column(JSON)  # عوامل آسیب‌پذیری
    
    # درمان‌ها
    treatments = Column(JSON)  # [{"name": "داروی...", "type": "herbal", "dosage": "..."}]
    dietary_recommendations = Column(JSON)  # توصیه‌های غذایی
    lifestyle_recommendations = Column(JSON)  # توصیه‌های زندگی
    
    # دوران و پیش‌آگهی
    expected_duration = Column(String(100))  # مثلاً "3-7 days"
    prognosis = Column(Text)
    
    # منابع
    source_books = Column(JSON)  # ["canon", "shifa", "rasalah"]
    reference_text = Column(Text)  # متن اصلی
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # روابط
    tongue_diagnoses = relationship("AvicennaTongueDiagnosis", back_populates="disease")
    eye_diagnoses = relationship("AvicennaEyeDiagnosis", back_populates="disease")
    pulse_diagnoses = relationship("AvicennaPulseDiagnosis", back_populates="disease")
    treatments_rel = relationship("AvicennaTreatment", back_populates="disease")


class AvicennaTongueDiagnosis(Base):
    """معیارهای تشخیصی از روی زبان در طب سینایی"""
    __tablename__ = "avicenna_tongue_diagnosis"
    
    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("avicenna_diseases.id"), nullable=False)
    
    # رنگ زبان
    color_category = Column(String(50), nullable=False)  # "pale", "red", "crimson", "purple", "dark"
    color_mizaj = Column(String(50))  # مزاج مربوطه
    color_description = Column(Text)  # توضیح
    
    # پوشش زبان
    coating_type = Column(String(50))  # "none", "thin", "thick", "greasy"
    coating_color = Column(String(50))  # "white", "yellow", "gray", "brown"
    coating_meaning = Column(Text)  # معنی پوشش
    
    # بافت
    texture = Column(String(50))  # "smooth", "rough", "bumpy", "cracked"
    moisture = Column(String(50))  # "dry", "normal", "wet", "sticky"
    swelling = Column(Boolean, default=False)  # متورم بودن
    
    # نشانه‌های ویژه
    special_signs = Column(JSON)  # [{sign: "شکاف", meaning: "...", mizaj: "..."}]
    
    # ارتباط مزاج
    related_mizaj = Column(String(50), nullable=False)
    
    # سطح قطعیت
    confidence = Column(Float, default=0.7)  # 0-1
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # روابط
    disease = relationship("AvicennaDisease", back_populates="tongue_diagnoses")


class AvicennaEyeDiagnosis(Base):
    """معیارهای تشخیصی از روی چشم در طب سینایی"""
    __tablename__ = "avicenna_eye_diagnosis"
    
    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("avicenna_diseases.id"), nullable=False)
    
    # رنگ چشم
    eye_color_indicator = Column(String(50))  # نشانه از رنگ چشم
    color_mizaj = Column(String(50))  # مزاج مربوطه
    
    # سفیدی چشم
    sclera_color = Column(String(50))  # "white", "yellow", "red", "dark"
    sclera_meaning = Column(Text)
    
    # حدقه (مردمک)
    pupil_size = Column(String(50))  # "normal", "dilated", "constricted"
    pupil_meaning = Column(Text)
    
    # نشانه‌های ویژه
    special_signs = Column(JSON)  # [{sign: "سیاہ لکے", meaning: "...", mizaj: "..."}]
    
    # چمک و تاب
    brightness = Column(String(50))  # "bright", "dull", "dark"
    brightness_meaning = Column(Text)
    
    # ارتباط مزاج
    related_mizaj = Column(String(50), nullable=False)
    
    # سطح قطعیت
    confidence = Column(Float, default=0.6)  # 0-1
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # روابط
    disease = relationship("AvicennaDisease", back_populates="eye_diagnoses")


class AvicennaPulseDiagnosis(Base):
    """معیارهای تشخیصی از روی نبض در طب سینایی"""
    __tablename__ = "avicenna_pulse_diagnosis"
    
    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("avicenna_diseases.id"), nullable=False)
    
    # ضربان
    pulse_rate_range = Column(String(50))  # "slow", "normal", "fast", "very_fast"
    pulse_rate_min = Column(Integer)
    pulse_rate_max = Column(Integer)
    
    # نوع نبض
    pulse_rhythm = Column(String(50))  # "regular", "irregular", "thready", "bounding"
    rhythm_meaning = Column(Text)
    
    # قوت و ضعف
    pulse_strength = Column(String(50))  # "weak", "moderate", "strong", "bounding"
    strength_meaning = Column(Text)
    
    # عمق نبض
    pulse_depth = Column(String(50))  # "superficial", "moderate", "deep"
    depth_meaning = Column(Text)
    
    # نرمی و سختی
    pulse_texture = Column(String(50))  # "soft", "moderate", "hard", "wiry"
    texture_meaning = Column(Text)
    
    # مکان بهتر
    location = Column(String(100))  # "radial", "temporal", "carotid"
    
    # ارتباط مزاج
    related_mizaj = Column(String(50), nullable=False)
    
    # سطح قطعیت
    confidence = Column(Float, default=0.8)  # 0-1
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # روابط
    disease = relationship("AvicennaDisease", back_populates="pulse_diagnoses")


class AvicennaTreatment(Base):
    """درمان‌های پیشنهادی در طب سینایی"""
    __tablename__ = "avicenna_treatments"
    
    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("avicenna_diseases.id"), nullable=False)
    
    # نوع درمان
    treatment_type = Column(String(50), nullable=False)  # "herbal", "dietary", "lifestyle", "bloodletting"
    
    # درمان‌های گیاهی
    herbal_name = Column(String(255), nullable=True)
    herbal_english = Column(String(255), nullable=True)
    herbal_parts = Column(String(255), nullable=True)  # "leaf", "root", "seed", "flower"
    herbal_preparation = Column(String(255), nullable=True)  # "decoction", "infusion", "powder"
    
    # خواص دارویی
    potency = Column(String(50), nullable=True)  # "warm", "cold", degree
    moisture = Column(String(50), nullable=True)  # "moist", "dry"
    
    # دوز و نحوۀ استفاده
    dosage = Column(String(255), nullable=True)
    administration_method = Column(String(255), nullable=True)  # "oral", "topical", "inhalation"
    frequency = Column(String(255), nullable=True)  # "3 times daily", "before sleep"
    duration = Column(String(255), nullable=True)  # "7 days", "until recovery"
    
    # غذاهای توصیه‌شده
    recommended_foods = Column(JSON)  # [{food, property, benefit}]
    
    # غذاهای ممنوعه
    forbidden_foods = Column(JSON)  # [{food, reason}]
    
    # سبک زندگی
    lifestyle_advice = Column(JSON)  # [{activity, frequency, benefit}]
    
    # احتیاطات
    precautions = Column(JSON)  # [{precaution, reason}]
    contraindications = Column(JSON)  # موارد مخالفه
    
    # مرحلۀ درمان
    stage = Column(String(50))  # "acute", "subacute", "chronic", "recovery"
    
    # مأخذ و منبع
    source_reference = Column(Text)  # متن اصلی یا منبع
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # روابط
    disease = relationship("AvicennaDisease", back_populates="treatments_rel")


class AvicennaMizajBalanceGuide(Base):
    """راهنمای تعادل مزاج و نگهداری سلامت"""
    __tablename__ = "avicenna_mizaj_balance_guide"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # مزاج
    mizaj = Column(String(50), nullable=False, unique=True)  # MizajType
    
    # خصوصیات
    persian_name = Column(String(100))
    english_name = Column(String(100))
    
    # خلط غالب
    dominant_humor = Column(String(50))  # HumorType
    
    # ویژگی‌های منطقی
    logical_properties = Column(JSON)  # [{property, value}]
    
    # معادل در طب دیگر
    tcm_equivalent = Column(String(100))  # معادل در طب چینی
    ayurveda_equivalent = Column(String(100))  # معادل در آیورودا
    
    # غذاهای مناسب
    recommended_foods = Column(JSON)  # [{food, benefit, frequency}]
    
    # فصل‌های مناسب
    favorable_seasons = Column(JSON)  # ["spring", "summer"]
    
    # فعالیت‌های توصیه‌شده
    recommended_activities = Column(JSON)  # [{activity, frequency, benefit}]
    
    # ساعات بهتر روز
    optimal_hours = Column(JSON)  # [{time, activity, benefit}]
    
    # احتیاطات
    precautions = Column(JSON)
    
    # بیماری‌های احتمالی اگر نامتعادل شود
    potential_diseases = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AvicennaHerbalRemedyDictionary(Base):
    """فرهنگ دارو‌های گیاهی در طب سینایی"""
    __tablename__ = "avicenna_herbal_remedies"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # نام دارو
    persian_name = Column(String(255), nullable=False)
    arabic_name = Column(String(255), nullable=True)
    english_name = Column(String(255), nullable=False)
    latin_botanical_name = Column(String(255), nullable=True)
    
    # نوع گیاه
    plant_family = Column(String(100))
    plant_parts_used = Column(JSON)  # ["leaf", "root", "seed", "flower", "bark"]
    
    # خواص دارویی
    potency = Column(String(50), nullable=False)  # "warm", "cold", "1st", "2nd", "3rd", "4th" degree
    moisture_property = Column(String(50), nullable=False)  # "moist", "dry"
    
    # تأثیرات
    effects = Column(JSON)  # [{effect, strength, reliability}]
    
    # بیماری‌های درمان‌شونده
    treats_diseases = Column(JSON)  # [{"disease": "تب", "efficacy": 0.8, "stage": "acute"}]
    
    # روش تهیه
    preparation_methods = Column(JSON)  # [{method: "decoction", description: "..."}]
    
    # دوز توصیه‌شده
    recommended_dosage = Column(String(255))
    dosage_frequency = Column(String(255))
    
    # موارد مخالفه
    contraindications = Column(JSON)  # [{condition, reason}]
    side_effects = Column(JSON)  # [{effect, severity}]
    
    # تعاملات دارویی
    drug_interactions = Column(JSON)  # [{herb, interaction}]
    
    # نکات ذخیره‌سازی
    storage_notes = Column(Text)
    shelf_life = Column(String(100))
    
    # منبع و اثر
    avicenna_reference = Column(Text)  # ارجاع به آثار سینایی
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
