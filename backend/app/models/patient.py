from sqlalchemy import Column, Integer, String, Date, Text, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.enums import Gender, MizajType

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(SQLEnum(Gender), nullable=True)
    phone_number = Column(String(15), nullable=True)
    
    mizaj_type = Column(SQLEnum(MizajType), default=MizajType.MOTADEL)
    
    medical_history = Column(Text, nullable=True)
    lifestyle_info = Column(Text, nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # روابط با سوابق سلامت
    health_records = relationship("HealthRecord", back_populates="patient", cascade="all, delete-orphan")
    tongue_analyses = relationship("TongueAnalysis", back_populates="patient", cascade="all, delete-orphan")
    eye_analyses = relationship("EyeAnalysis", back_populates="patient", cascade="all, delete-orphan")
    vital_signs = relationship("VitalSigns", back_populates="patient", cascade="all, delete-orphan")
    audio_analyses = relationship("AudioAnalysis", back_populates="patient", cascade="all, delete-orphan")
    skin_analyses = relationship("SkinAnalysis", back_populates="patient", cascade="all, delete-orphan")
    health_reports = relationship("HealthReport", back_populates="patient", cascade="all, delete-orphan")
    
    # روابط با اصول تشخیصی سینا
    pulse_analyses = relationship("PulseAnalysis", back_populates="patient", cascade="all, delete-orphan")
    urine_analyses = relationship("UrineAnalysis", back_populates="patient", cascade="all, delete-orphan")
    tongue_coatings = relationship("TongueCoating", back_populates="patient", cascade="all, delete-orphan")
    diagnostic_findings = relationship("DiagnosticFinding", back_populates="patient", cascade="all, delete-orphan")
    
    # روابط با برنامه‌های درمانی مزاج
    mizaj_treatments = relationship("MizajBalanceTreatment", back_populates="patient", cascade="all, delete-orphan")
