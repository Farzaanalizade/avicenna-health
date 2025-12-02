from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class HealthRecord(Base):
    __tablename__ = "health_records"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # اطلاعات ضبط شده
    record_type = Column(String(50))  # tongue, eye, voice, pulse
    analysis_data = Column(JSON)
    
    # نتایج تحلیل
    mizaj_assessment = Column(String(50))
    health_status = Column(Text)
    recommendations = Column(JSON)
    
    # اطلاعات علائم حیاتی
    blood_pressure_systolic = Column(Float)
    blood_pressure_diastolic = Column(Float)
    heart_rate = Column(Float)
    body_temperature = Column(Float)
    
    # متادیتا
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    analyzed_by = Column(String(100))  # AI or practitioner name
    
    # رابطه با جدول بیماران
    patient = relationship("Patient", back_populates="health_records")
