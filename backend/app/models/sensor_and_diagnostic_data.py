from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Enum as SQLEnum, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base

class SensorData(Base):
    """داده‌های مرکزی از سنسورهای مختلف"""
    __tablename__ = "sensor_data"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # نوع سنسور
    sensor_type = Column(String(50), nullable=False)  # "heart_rate", "spo2", "temp", "gyro", etc.
    
    # زمان ثبت
    timestamp = Column(DateTime(timezone=True), nullable=False, default=func.now())
    
    # داده‌های خام
    raw_value = Column(JSON, nullable=False)  # {"value": 72, "unit": "bpm"}
    
    # داده‌های پردازش‌شده
    processed_value = Column(JSON, nullable=True)  # نتایج پردازش
    
    # واحد اندازه‌گیری
    unit = Column(String(20))  # "bpm", "%", "°C", etc.
    
    # اطلاعات دستگاه
    device_info = Column(JSON)  # {"device_id": "...", "device_type": "smartwatch", "model": "Apple Watch"}
    
    # امتیاز اعتماد
    confidence_score = Column(Float, default=0.0)  # 0-100
    
    # وضعیت
    is_valid = Column(Boolean, default=True)
    validation_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # روابط
    patient = relationship("Patient", back_populates="sensor_data")


class WearableDevice(Base):
    """ثبت و مدیریت دستگاه‌های پوشیدنی"""
    __tablename__ = "wearable_devices"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # مشخصات دستگاه
    device_type = Column(String(100), nullable=False)  # "Apple Watch", "Fitbit", "Xiaomi Band", etc.
    device_model = Column(String(100), nullable=True)
    device_id = Column(String(255), unique=True, nullable=False)  # شناسۀ منحصربفرد دستگاه
    device_name = Column(String(255), nullable=True)
    
    # وضعیت اتصال
    connection_status = Column(String(50), default="DISCONNECTED")  # "CONNECTED", "DISCONNECTED", "ERROR"
    last_sync = Column(DateTime(timezone=True), nullable=True)
    
    # سطح باتری
    battery_level = Column(Integer, nullable=True)  # 0-100
    
    # اطلاعات اتصال
    api_token = Column(String(500), nullable=True)
    api_url = Column(String(500), nullable=True)
    
    # تنظیمات همگام‌سازی
    sync_frequency = Column(Integer, default=300)  # ثانیه (5 دقیقه)
    is_active = Column(Boolean, default=True)
    
    # تاریخچه
    paired_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # روابط
    patient = relationship("Patient", back_populates="wearable_devices")
    vital_signs = relationship("VitalSigns", back_populates="wearable_device")


class PulseAnalysis(Base):
    """تحلیل نبض به روش سینایی"""
    __tablename__ = "pulse_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # مشخصات نبض
    pulse_rate = Column(Integer)  # ضربان در دقیقه
    pulse_rhythm = Column(String(50))  # "regular", "irregular", "thready", "bounding"
    pulse_strength = Column(String(50))  # "weak", "normal", "strong"
    pulse_depth = Column(String(50))  # "deep", "moderate", "superficial"
    
    # نقطۀ سنجش
    measurement_location = Column(String(100))  # "right_wrist", "left_wrist", "radial_artery"
    
    # تحلیل سینایی
    mizaj_indication = Column(String(50))  # "hot_dry", "hot_wet", "cold_dry", "cold_wet"
    organ_involved = Column(String(100))  # "heart", "liver", "kidney", etc.
    disease_indication = Column(Text)  # تفسیر سینایی
    
    # پیام‌های بالینی
    clinical_notes = Column(Text, nullable=True)
    
    # امتیاز اعتماد
    confidence_score = Column(Float, default=0.0)
    
    # فایل صوتی (اختیاری)
    audio_recording_path = Column(String(255), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # روابط
    patient = relationship("Patient", back_populates="pulse_analyses")


class UrineAnalysis(Base):
    """تحلیل ادرار به روش سینایی"""
    __tablename__ = "urine_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # مشخصات ادرار
    color = Column(String(50))  # "clear", "pale", "yellow", "amber", "dark", "brown", "red"
    transparency = Column(String(50))  # "clear", "cloudy", "turbid"
    smell = Column(String(100), nullable=True)  # "normal", "sweet", "foul", "ammonia"
    consistency = Column(String(50))  # "thin", "normal", "thick"
    
    # ویژگی‌های فیزیکی
    temperature = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)  # میلی‌لیتر
    
    # نتایج شیمیایی
    ph_level = Column(Float, nullable=True)
    specific_gravity = Column(Float, nullable=True)
    protein_level = Column(String(50), nullable=True)  # "negative", "trace", "1+", "2+", "3+", "4+"
    glucose_level = Column(String(50), nullable=True)
    ketones = Column(String(50), nullable=True)
    blood_present = Column(Boolean, default=False)
    bacteria_present = Column(Boolean, default=False)
    
    # تحلیل سینایی
    mizaj_indication = Column(String(50))  # "hot_dry", "hot_wet", "cold_dry", "cold_wet"
    organ_involved = Column(String(100))  # "kidney", "bladder", "liver", etc.
    disease_indication = Column(Text)  # تفسیر سینایی
    
    # فایل تصویر
    image_path = Column(String(255), nullable=True)
    
    # یادداشت‌های بالینی
    clinical_notes = Column(Text, nullable=True)
    
    # امتیاز اعتماد
    confidence_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # روابط
    patient = relationship("Patient", back_populates="urine_analyses")


class TongueCoating(Base):
    """تحلیل پوشش و تفصیلات زبان به روش سینایی"""
    __tablename__ = "tongue_coatings"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # رنگ زبان
    body_color = Column(String(50))  # "pale", "normal_red", "red", "crimson", "purple", "dark"
    
    # پوشش زبان
    coating_type = Column(String(50))  # "none", "thin", "thick", "sticky"
    coating_color = Column(String(50))  # "white", "yellow", "gray", "brown", "black"
    coating_distribution = Column(String(100))  # "uniform", "root_only", "tip_only", "patches"
    
    # بافت و ظاهر
    texture = Column(String(50))  # "smooth", "rough", "bumpy", "peeled"
    moisture = Column(String(50))  # "normal", "dry", "wet", "sticky"
    thickness = Column(String(50))  # "normal", "thin", "swollen"
    
    # ویژگی‌های سطحی
    cracks_present = Column(Boolean, default=False)
    cracks_pattern = Column(String(100), nullable=True)  # "central", "pattern", "scattered"
    teeth_marks = Column(Boolean, default=False)
    tremor = Column(Boolean, default=False)
    
    # ویژگی‌های خاص
    nodules_present = Column(Boolean, default=False)
    pimples_present = Column(Boolean, default=False)
    swollen_papillae = Column(Boolean, default=False)
    
    # تحلیل سینایی
    mizaj_indication = Column(String(50))  # "hot_dry", "hot_wet", "cold_dry", "cold_wet"
    heat_cold_index = Column(Integer, nullable=True)  # -5 to +5 (سردتر تا گرم‌تر)
    dryness_wetness_index = Column(Integer, nullable=True)  # -5 to +5 (خشک‌تر تا مرطوب‌تر)
    
    # نگاه‌های چینی و هندی
    chinese_medicine_signs = Column(JSON)  # {"pattern": "...", "signs": [...]}
    ayurvedic_signs = Column(JSON)  # {"dosha": "...", "signs": [...]}
    
    # بیماری‌های احتمالی
    potential_diseases = Column(JSON)  # [{"name": "...", "probability": 0.7}]
    
    # فایل تصویر
    image_path = Column(String(255), nullable=True)
    
    # یادداشت‌های بالینی
    clinical_notes = Column(Text, nullable=True)
    
    # امتیاز اعتماد
    confidence_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # روابط
    patient = relationship("Patient", back_populates="tongue_coatings")


class DiagnosticFinding(Base):
    """یافته‌های تشخیصی جامع از تمام داده‌های بیمار"""
    __tablename__ = "diagnostic_findings"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # ارجاعات داده‌های بالینی
    tongue_coating_id = Column(Integer, ForeignKey("tongue_coatings.id"), nullable=True)
    pulse_analysis_id = Column(Integer, ForeignKey("pulse_analyses.id"), nullable=True)
    urine_analysis_id = Column(Integer, ForeignKey("urine_analyses.id"), nullable=True)
    
    # نوع یافته
    finding_type = Column(String(100), nullable=False)  # "diagnosis", "prognosis", "etiology"
    
    # تشخیص سینایی
    avicenna_diagnosis = Column(Text, nullable=True)
    affected_organs = Column(JSON)  # ["heart", "liver", "kidney"]
    affected_humors = Column(JSON)  # [{"humor": "blood", "excess": true}, ...]
    
    # شدت و پیش‌آگهی
    severity_level = Column(String(50))  # "mild", "moderate", "severe"
    prognosis = Column(Text, nullable=True)
    expected_duration = Column(String(100), nullable=True)  # مثلاً "3-7 days"
    
    # علت و ریشه‌یاب
    root_cause = Column(Text, nullable=True)
    contributing_factors = Column(JSON)  # ["stress", "diet", "sleep_deprivation"]
    
    # درمان پیشنهادی
    recommended_treatment = Column(JSON)  # [{"type": "herbal", "remedy": "...", "duration": "..."}]
    dietary_recommendations = Column(JSON)  # [{food, benefit, quantity}]
    lifestyle_recommendations = Column(JSON)  # [{activity, benefit, frequency}]
    
    # دارو‌های سینایی
    traditional_medicines = Column(JSON)  # [{name, ingredients, dosage, duration}]
    
    # توصیه‌های پیشگیری
    prevention_measures = Column(JSON)  # [{measure, frequency}]
    
    # بیماری‌های احتمالی اگر درمان نشود
    complications_if_untreated = Column(JSON)  # [{disease, probability, timeline}]
    
    # نیاز به ملاقات با پزشک
    requires_doctor_consultation = Column(Boolean, default=False)
    urgency_level = Column(String(50), default="routine")  # "routine", "soon", "urgent", "critical"
    specialist_type = Column(String(100), nullable=True)  # "cardiologist", "gastroenterologist"
    
    # امتیاز اعتماد
    confidence_score = Column(Float, default=0.0)
    
    # یادداشت‌های پزشک
    physician_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    # روابط
    patient = relationship("Patient", back_populates="diagnostic_findings")
    tongue_coating = relationship("TongueCoating")
    pulse_analysis = relationship("PulseAnalysis")
    urine_analysis = relationship("UrineAnalysis")


class MizajBalanceTreatment(Base):
    """برنامۀ درمانی برای تعادل مزاج"""
    __tablename__ = "mizaj_balance_treatments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # مزاج فعلی و هدف
    current_mizaj = Column(String(50), nullable=False)  # "hot_dry", "hot_wet", "cold_dry", "cold_wet"
    target_mizaj = Column(String(50), nullable=False)  # "motadel" (متعادل)
    
    # مدت درمان
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)
    duration_days = Column(Integer, nullable=True)
    
    # درمان‌های غذایی
    dietary_treatments = Column(JSON)  # [{food, property, quantity, frequency}]
    
    # درمان‌های گیاهی
    herbal_treatments = Column(JSON)  # [{herb, benefit, form, dosage, frequency}]
    
    # درمان‌های سبک زندگی
    lifestyle_treatments = Column(JSON)  # [{activity, benefit, frequency, duration}]
    
    # درمان‌های طبیعی (آب‌وهوا، حرکت، استراحت)
    natural_treatments = Column(JSON)  # [{therapy, benefit, frequency}]
    
    # درمان‌های فیزیکی
    physical_treatments = Column(JSON)  # [{treatment, benefit, frequency}]
    
    # درمان‌های روحی
    spiritual_treatments = Column(JSON)  # [{practice, benefit, frequency}]
    
    # موارد ممنوع
    forbidden_items = Column(JSON)  # [foods, activities, behaviors]
    
    # پیگیری و بهبود
    progress_tracking = Column(JSON)  # [{date, observation, mizaj_change}]
    
    # وضعیت درمان
    status = Column(String(50), default="active")  # "active", "paused", "completed", "discontinued"
    
    # یادداشت‌های پزشک
    physician_notes = Column(Text, nullable=True)
    
    # امتیاز اعتماد
    confidence_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # روابط
    patient = relationship("Patient", back_populates="mizaj_treatments")
