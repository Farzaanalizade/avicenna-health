from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from app.models.enums import Gender, MizajType

class PatientBase(BaseModel):
    full_name: str
    email: EmailStr
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    phone_number: Optional[str] = None
    mizaj_type: Optional[MizajType] = MizajType.MOTADEL
    medical_history: Optional[str] = None
    lifestyle_info: Optional[str] = None

class PatientRegister(PatientBase):
    password: str

class PatientLogin(BaseModel):
    email: EmailStr
    password: str

class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    phone_number: Optional[str] = None
    mizaj_type: Optional[MizajType] = None
    medical_history: Optional[str] = None
    lifestyle_info: Optional[str] = None

class PatientCreate(PatientBase):
    """برای ایجاد بیمار جدید"""
    pass

class PatientResponse(PatientBase):
    id: int
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True
