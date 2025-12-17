"""
مدل‌های بیماری‌ها، علائم و درمان‌های سنتی بر اساس تعاليم سینا
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float, JSON, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum


class DiseaseCategory(str, Enum):
    """دسته‌بندی بیماری‌ها"""
    NEUROLOGICAL = "neurological"  # عصبی
    DIGESTIVE = "digestive"  # گوارشی
    RESPIRATORY = "respiratory"  # تنفسی
    CIRCULATORY = "circulatory"  # گردشی
    FEVER = "fever"  # تب
    SKIN = "skin"  # پوستی
    JOINT = "joint"  # مفصلی
    MENTAL = "mental"  # روانی
    METABOLIC = "metabolic"  # متابولیکی


class TreatmentType(str, Enum):
    """انواع درمان"""
    HERBAL = "herbal"  # گیاهی
    MINERAL = "mineral"  # معدنی
    DIETARY = "dietary"  # غذایی
    BEHAVIORAL = "behavioral"  # رفتاری
    PHYSICAL_THERAPY = "physical_therapy"  # فیزیوتراپی
    BLOODLETTING = "bloodletting"  # فصادگیری (تاریخی)
    CUPPING = "cupping"  # حجامت
    MASSAGE = "massage"  # ماساژ


class Disease(Base):
    """مدل بیماری‌ها بر اساس تعاليم سینا"""
    __tablename__ = "diseases"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # معلومات پایه‌ای
    name_fa = Column(String(150), nullable=False)  # نام فارسی
    name_ar = Column(String(150), nullable=True)  # نام عربی (از متون سینا)
    name_latin = Column(String(150), nullable=True)  # نام لاتین
    
    # دسته‌بندی
    category = Column(SQLEnum(DiseaseCategory))
    
    # وابستگی به مزاج
    related_mizaj = Column(JSON)  # مزاج‌های مرتبط
    primary_affected_organs = Column(JSON)  # اعضای اول دست‌تحت تأثیر
    secondary_affected_organs = Column(JSON)  # اعضای ثانیه تحت‌تأثیر
    
    # توضیح کلی
    description = Column(Text)
    avicenna_description = Column(Text)  # توضیح از متون سینا
    
    # علائم کلیدی
    key_symptoms = Column(JSON)  # علائم اصلی
    secondary_symptoms = Column(JSON)  # علائم فرعی
    
    # تشخیص
    diagnostic_signs = Column(JSON)  # علائم تشخیصی (زبان، نبض، ادرار)
    pulse_characteristics = Column(JSON)  # خصوصیات نبض
    urine_characteristics = Column(JSON)  # خصوصیات ادرار
    tongue_characteristics = Column(JSON)  # خصوصیات زبان
    
    # عوامل خطر و علل
    etiology = Column(Text)  # علل بیماری
    risk_factors = Column(JSON)
    
    # سطح شدت
    severity_levels = Column(JSON)  # سطوح شدت بیماری
    
    # مدت زمان و پیامدها
    typical_duration = Column(String)  # مدت معمول
    potential_complications = Column(JSON)  # پیامدهای احتمالی
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)


class Symptom(Base):
    """علائم منفرد"""
    __tablename__ = "symptoms"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # معلومات
    name_fa = Column(String(100), nullable=False)
    name_ar = Column(String(100), nullable=True)
    description = Column(Text)
    
    # دسته‌بندی
    symptom_type = Column(String(50))  # سرگیجه، درد، تورم، الغری و...
    severity_range = Column(String)  # خفیف، متوسط، شدید
    
    # مرتبط با مزاج
    mizaj_related = Column(JSON)  # مزاج‌های مرتبط
    
    # مرتبط با اعضا
    affected_areas = Column(JSON)  # مناطق تحت تأثیر
    
    # مشاهده زمانی
    when_observed = Column(String)  # زمان مشاهده: صبح، بعد، شب، هنگام غذا
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DiseaseSymptomRelation(Base):
    """رابطه بین بیماری و علائم"""
    __tablename__ = "disease_symptom_relations"
    
    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=False)
    symptom_id = Column(Integer, ForeignKey("symptoms.id"), nullable=False)
    
    # میزان ارتباط
    is_primary = Column(Boolean, default=False)  # علامت اولیه
    prevalence = Column(Float)  # درصد شیوع
    severity_contribution = Column(Float)  # سهم در شدت کلی
    
    appearance_stage = Column(String)  # مرحله ظهور: ابتدا، میانی، پایانی
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TraditionalRemedy(Base):
    """درمان‌های سنتی بر اساس تعاليم سینا"""
    __tablename__ = "traditional_remedies"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # معلومات پایه‌ای
    name_fa = Column(String(150), nullable=False)
    name_ar = Column(String(150), nullable=True)
    remedy_type = Column(SQLEnum(TreatmentType))
    
    # اجزاء
    ingredients = Column(JSON)  # لیست اجزاء
    quantities = Column(JSON)  # مقادیر اجزاء
    preparation_method = Column(Text)  # روش تهیه
    
    # استفاده
    usage_method = Column(String)  # نحوه استفاده
    dosage = Column(String)  # دوز
    duration = Column(String)  # مدت درمان
    frequency = Column(String)  # فراوانی: روزی یک‌بار، سه‌بار و...
    
    # موارد استفاده
    used_for_diseases = Column(JSON)  # برای درمان کدام بیماری‌ها
    used_for_conditions = Column(JSON)  # برای بهبود کدام شرایط
    
    # خصوصیات سینایی
    effect_on_mizaj = Column(JSON)  # تأثیر بر مزاج
    temperature_nature = Column(String)  # ماهیت ترموتراپی: گرم، سرد
    moisture_nature = Column(String)  # ماهیت رطوبتی: تر، خشک
    
    # اثربخشی و ایمنی
    effectiveness_level = Column(String)  # سطح اثربخشی
    safety_notes = Column(Text)  # نکات ایمنی
    contraindications = Column(JSON)  # موارد مخالف
    side_effects = Column(JSON)  # عوارض
    interactions = Column(JSON)  # تعاملات با سایر دارو‌ها
    
    # منابع
    references = Column(JSON)  # منابع (متون سینا و...)
    avicenna_reference = Column(String)  # منبع دقیق در کتاب سینا
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)


class DiseaseRemediRelation(Base):
    """رابطه بین بیماری و درمان"""
    __tablename__ = "disease_remedy_relations"
    
    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=False)
    remedy_id = Column(Integer, ForeignKey("traditional_remedies.id"), nullable=False)
    
    # معلومات درمان برای این بیماری
    effectiveness_rate = Column(Float)  # درصد اثربخشی
    stage_of_disease = Column(String)  # مرحله بیماری: ابتدایی، متوسط، پیشرفته
    is_primary_treatment = Column(Boolean, default=False)  # درمان اولیه
    treatment_priority = Column(Integer)  # اولویت درمان
    
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MizajBalanceTreatment(Base):
    """درمان برای تعادل مزاج"""
    __tablename__ = "mizaj_balance_treatments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # مزاج فعلی و هدف
    current_mizaj = Column(String)
    target_mizaj = Column(String)
    
    # درمان‌های پیشنهادی
    recommended_remedies = Column(JSON)  # لیست درمان‌های توصیه‌شده
    dietary_recommendations = Column(JSON)  # توصیه‌های غذایی
    lifestyle_changes = Column(JSON)  # تغییرات سبک زندگی
    
    # جزئیات
    treatment_plan = Column(JSON)  # برنامه درمانی تفصیلی
    expected_duration = Column(String)  # مدت تقریبی
    
    # پیگیری
    follow_up_date = Column(DateTime(timezone=True))
    is_completed = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(100))
    
    patient = relationship("Patient", back_populates="mizaj_treatments")


class MedicalPlant(Base):
    """گیاهان دارویی بر اساس تعاليم سینا"""
    __tablename__ = "medical_plants"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # معلومات
    name_fa = Column(String(100), nullable=False)
    name_ar = Column(String(100), nullable=True)
    name_scientific = Column(String(100), nullable=True)
    name_common = Column(String(100), nullable=True)
    
    # خصوصیات
    plant_part_used = Column(String)  # بخش استفاده شده: ریشه، برگ، میوه، گل
    active_compounds = Column(JSON)  # ترکیبات فعال
    
    # طبیعت سینایی
    temperature_nature = Column(String)  # گرم/سرد
    moisture_nature = Column(String)  # تر/خشک
    degree_of_strength = Column(String)  # درجه قوت (1-4)
    
    # موارد استفاده
    medicinal_uses = Column(JSON)  # موارد استفاده
    treats_diseases = Column(JSON)  # درمان می‌دهد
    balances_mizaj = Column(JSON)  # مزاج‌های تعادل‌کننده
    
    # تهیه و مصرف
    preparation_methods = Column(JSON)  # روش‌های تهیه
    typical_dosage = Column(String)  # دوز معمول
    
    # ایمنی
    safety_profile = Column(String)
    contraindications = Column(JSON)
    side_effects = Column(JSON)
    
    # منابع
    avicenna_reference = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
