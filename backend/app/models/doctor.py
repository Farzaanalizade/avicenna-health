from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # اطلاعات حرفه‌ای
    specialization = Column(String(100), nullable=True)
    medical_license = Column(String(50), unique=True, nullable=True)
    years_of_experience = Column(Integer, nullable=True)
    
    # اطلاعات تماس
    clinic_address = Column(Text, nullable=True)
    consultation_fee = Column(Integer, nullable=True)
    
    # Bio و توضیحات
    bio = Column(Text, nullable=True)
    
    # روابط
    user = relationship("User", back_populates="doctor_profile")
    appointments = relationship("Appointment", back_populates="doctor")

    def __repr__(self):
        return f"<Doctor(id={self.id}, specialization='{self.specialization}')>"
