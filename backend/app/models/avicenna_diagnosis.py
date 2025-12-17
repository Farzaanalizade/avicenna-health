"""
مدل‌های تشخیصی بر اساس اصول ابوعلی سینا
شامل: اصول تشخیصی (زبان، نبض، ادرار، مزاج)
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float, JSON, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum


class PulseType(str, Enum):
    """انواع نبض بر اساس فلسفه سینا"""
    KABIR = "kabir"  # پر (بزرگ)
    SAGHIR = "saghir"  # کوچک
    TAVIL = "tavil"  # طویل
    QASIR = "qasir"  # کوتاه
    SARE_EN = "sare_en"  # سریع
    BETH_IN = "beth_in"  # آهسته
    MONTEM_EN = "montem_en"  # منتظم
    NAAMONTEM = "naamontem"  # نامنتظم
    QAVI = "qavi"  # قوی
    ZAEEF = "zaeef"  # ضعیف
    GARM = "garm"  # گرم
    SARD = "sard"  # سرد


class UrineDensity(str, Enum):
    """چگالی ادرار"""
    KHAFIF = "khafif"  # سبک
    MOTAVASSETA = "motavasseta"  # متوسط
    SAQIL = "saqil"  # سنگین


class UrineColor(str, Enum):
    """رنگ ادرار"""
    SEFID = "sefid"  # سفید
    ZARD = "zard"  # زرد
    GHERMEZ = "ghermez"  # قرمز
    GHEBLEH = "ghebleh"  # قهوه‌ای
    TARIK = "tarik"  # تیره
    TABII = "tabii"  # طبیعی


class PulseAnalysis(Base):
    """تحلیل نبض بر اساس روش سینا"""
    __tablename__ = "pulse_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # اطلاعات نبض
    pulse_rate = Column(Integer)  # ضربات در دقیقه
    primary_type = Column(SQLEnum(PulseType), nullable=True)  # نوع اولیه نبض
    secondary_types = Column(JSON, default={})  # انواع ثانویه
    
    # مشخصات نبض
    strength = Column(String)  # قوت نبض: ضعیف، متوسط، قوی
    rhythm = Column(String)  # ریتم: منتظم، نامنتظم
    temperature = Column(Float)  # دمای احساسی نبض
    
    # تحلیل سینایی
    mizaj_indicator = Column(String)  # نشان دهنده مزاج بر اساس نبض
    condition_assessment = Column(Text)  # ارزیابی وضعیت بدن
    
    # آناتومی ضربان
    location = Column(String)  # محل پیگیری: مچ، گردن، شقیق
    depth = Column(String)  # عمق: سطحی، متوسط، عمیق
    width = Column(String)  # عرض: باریک، متوسط، پهن
    
    detailed_analysis = Column(JSON)
    ai_assessment = Column(Text)
    confidence_score = Column(Float)
    
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    analyzed_by = Column(String(100))  # نام پزشک یا سیستم
    
    patient = relationship("Patient", back_populates="pulse_analyses")


class UrineAnalysis(Base):
    """تحلیل ادرار بر اساس روش سینا"""
    __tablename__ = "urine_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # مشخصات ادرار
    color = Column(SQLEnum(UrineColor), nullable=True)
    density = Column(SQLEnum(UrineDensity), nullable=True)
    odor = Column(String)  # بو: معطر، بی‌بو، بدبو
    clarity = Column(String)  # وضوح: شفاف، نیمه‌شفاف، تیره
    foam = Column(String)  # کف: کم، متوسط، زیاد
    
    # مکونات و نشانگرها
    sediment_present = Column(Boolean, default=False)  # رسوب
    crystals_present = Column(Boolean, default=False)  # کریستال
    blood_present = Column(Boolean, default=False)  # خون
    protein_level = Column(String)  # سطح پروتئین
    sugar_level = Column(String)  # سطح قند
    
    # تحلیل سینایی
    mizaj_indicator = Column(String)  # نشان دهنده مزاج
    temperature_indication = Column(String)  # نشان دهنده گرما/سردی
    moisture_indication = Column(String)  # نشان دهنده رطوبت/خشکی
    
    health_status = Column(Text)  # وضعیت سلامت براساس تحلیل
    potential_conditions = Column(JSON)  # بیماری‌های احتمالی
    
    collection_time = Column(String)  # زمان جمع‌آوری: صبح، بعد، شب
    storage_duration = Column(Integer)  # مدت ذخیره‌سازی (ساعت)
    
    detailed_analysis = Column(JSON)
    ai_assessment = Column(Text)
    confidence_score = Column(Float)
    
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    analyzed_by = Column(String(100))
    
    patient = relationship("Patient", back_populates="urine_analyses")


class TongueCoating(Base):
    """تحلیل زبان (پوشش و رطوبت)"""
    __tablename__ = "tongue_coatings"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # مشخصات پوشش زبان
    coating_color = Column(String)  # رنگ پوشش
    coating_thickness = Column(String)  # ضخامت: نازک، متوسط، ضخیم
    coating_distribution = Column(String)  # پخش: کامل، جزئی، ریشه فقط
    
    # بدن زبان
    body_color = Column(String)  # رنگ بدن زبان
    body_shape = Column(String)  # شکل: عادی، متورم، نازک
    body_size = Column(String)  # اندازه: طبیعی، بزرگ، کوچک
    
    # نشانگرهای سینایی
    moisture_level = Column(String)  # رطوبت: خشک، طبیعی، مرطوب
    temperature_feeling = Column(String)  # احساس گرما/سردی
    
    # ویژگی‌های خاص
    cracks_pattern = Column(String)  # الگوی ترک: خطی، شبکه‌ای، نقطه‌ای
    tooth_marks = Column(Boolean, default=False)  # اثر دندان
    bumps_or_papillae = Column(String)  # نوک‌ها: نرمال، برجسته، صاف
    
    # تحلیل سینایی
    mizaj_type = Column(String)  # نوع مزاج
    organ_indicators = Column(JSON)  # نشانگرهای اعضای مختلف
    disease_indicators = Column(JSON)  # نشانگرهای بیماری
    
    detailed_analysis = Column(JSON)
    ai_assessment = Column(Text)
    confidence_score = Column(Float)
    
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    analyzed_by = Column(String(100))
    
    patient = relationship("Patient", back_populates="tongue_coatings")


class DiagnosticFinding(Base):
    """یافته‌های تشخیصی جمع‌بندی شده"""
    __tablename__ = "diagnostic_findings"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # منابع تشخیصی
    pulse_analysis_id = Column(Integer, ForeignKey("pulse_analyses.id"), nullable=True)
    urine_analysis_id = Column(Integer, ForeignKey("urine_analyses.id"), nullable=True)
    tongue_coating_id = Column(Integer, ForeignKey("tongue_coatings.id"), nullable=True)
    
    # خلاصه تشخیص
    primary_mizaj = Column(String)  # مزاج اولیه تشخیص‌شده
    secondary_mizaj = Column(String)  # مزاج ثانویه
    
    # نتیجه‌گیری کلی
    overall_health_status = Column(Text)
    affected_organs = Column(JSON)  # اعضای تحت تأثیر
    identified_imbalances = Column(JSON)  # عدم‌تعادل‌های شناسایی شده
    
    # توصیه‌های درمانی
    recommended_treatments = Column(JSON)
    lifestyle_recommendations = Column(JSON)
    dietary_recommendations = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(100))
    
    patient = relationship("Patient", back_populates="diagnostic_findings")
