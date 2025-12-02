from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class TongueAnalysis(Base):
    """تحلیل تصویر زبان"""
    __tablename__ = "tongue_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # مسیر تصویر
    image_path = Column(String, nullable=False)
    
    # نتایج تحلیل
    color = Column(String)  # "pink", "red", "pale", "purple"
    coating = Column(String)  # "none", "white", "yellow", "thick"
    moisture = Column(String)  # "normal", "dry", "wet"
    cracks_detected = Column(Boolean, default=False)
    texture = Column(String)  # "smooth", "rough", "bumpy"
    
    # تحلیل JSON کامل
    detailed_analysis = Column(JSON)
    
    # تشخیص AI
    ai_diagnosis = Column(Text)
    confidence_score = Column(Float)  # 0-100
    
    # برچسب‌های بیماری احتمالی
    potential_conditions = Column(JSON)  # [{"name": "...", "probability": 0.7}]
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # روابط
    patient = relationship("Patient", back_populates="tongue_analyses")

class EyeAnalysis(Base):
    """تحلیل اسکن چشم"""
    __tablename__ = "eye_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    image_path = Column(String, nullable=False)
    
    # نتایج تحلیل
    redness_level = Column(Float)  # 0-10
    yellowness_detected = Column(Boolean, default=False)
    pupil_size = Column(String)  # "normal", "dilated", "constricted"
    clarity = Column(String)  # "clear", "cloudy"
    
    detailed_analysis = Column(JSON)
    ai_diagnosis = Column(Text)
    confidence_score = Column(Float)
    potential_conditions = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="eye_analyses")

class VitalSigns(Base):
    """علائم حیاتی از سنسورها"""
    __tablename__ = "vital_signs"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # داده‌های حیاتی
    heart_rate = Column(Integer)  # bpm
    spo2 = Column(Integer)  # درصد اکسیژن خون
    temperature = Column(Float)  # سانتیگراد
    blood_pressure_systolic = Column(Integer)  # فشار بالا
    blood_pressure_diastolic = Column(Integer)  # فشار پایین
    respiratory_rate = Column(Integer)  # تعداد تنفس در دقیقه
    
    # منبع داده
    source = Column(String)  # "phone", "smartwatch", "manual"
    device_model = Column(String)  # "Apple Watch Series 9"
    
    # یادداشت کاربر
    notes = Column(Text)
    
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="vital_signs")

class AudioAnalysis(Base):
    """تحلیل صداهای بیولوژیک"""
    __tablename__ = "audio_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    audio_path = Column(String, nullable=False)
    audio_type = Column(String)  # "heartbeat", "breathing", "cough"
    duration = Column(Integer)  # ثانیه
    
    # نتایج تحلیل
    heart_rate_detected = Column(Integer)
    rhythm = Column(String)  # "regular", "irregular"
    abnormal_sounds = Column(Boolean, default=False)
    
    detailed_analysis = Column(JSON)
    ai_diagnosis = Column(Text)
    confidence_score = Column(Float)
    potential_conditions = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="audio_analyses")

class SkinAnalysis(Base):
    """تحلیل تصویر پوست و صورت"""
    __tablename__ = "skin_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    image_path = Column(String, nullable=False)
    body_part = Column(String)  # "face", "arm", "hand", etc.
    
    # تحلیل
    skin_tone = Column(String)  # "normal", "pale", "red", "yellow"
    texture = Column(String)
    spots_detected = Column(Boolean, default=False)
    rashes_detected = Column(Boolean, default=False)
    wounds_detected = Column(Boolean, default=False)
    
    detailed_analysis = Column(JSON)
    ai_diagnosis = Column(Text)
    confidence_score = Column(Float)
    potential_conditions = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="skin_analyses")

class HealthReport(Base):
    """گزارش جامع سلامت"""
    __tablename__ = "health_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # ارجاع به داده‌های مختلف
    tongue_analysis_id = Column(Integer, ForeignKey("tongue_analyses.id"))
    eye_analysis_id = Column(Integer, ForeignKey("eye_analyses.id"))
    skin_analysis_id = Column(Integer, ForeignKey("skin_analyses.id"))
    audio_analysis_id = Column(Integer, ForeignKey("audio_analyses.id"))
    vital_signs_ids = Column(JSON)  # لیست IDهای علائم حیاتی
    
    # تشخیص نهایی
    overall_health_score = Column(Float)  # 0-100
    risk_level = Column(String)  # "low", "medium", "high", "critical"
    
    # بیماری‌های احتمالی
    detected_conditions = Column(JSON)  # [{name, probability, severity}]
    
    # توصیه‌ها
    recommendations = Column(JSON)  # [{"type": "diet", "text": "..."}]
    lifestyle_tips = Column(JSON)
    should_see_doctor = Column(Boolean, default=False)
    urgency = Column(String)  # "none", "routine", "soon", "urgent"
    
    # تحلیل AI
    ai_summary = Column(Text)
    ai_reasoning = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # روابط
    patient = relationship("Patient", back_populates="health_reports")
    tongue_analysis = relationship("TongueAnalysis")
    eye_analysis = relationship("EyeAnalysis")
    skin_analysis = relationship("SkinAnalysis")
    audio_analysis = relationship("AudioAnalysis")
