from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict
from app.database import get_db
from app.models.patient import Patient
from app.schemas.patient import PatientRegister, PatientLogin, PatientResponse
from app.models.enums import MizajType
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=PatientResponse)
def register_patient(patient_data: PatientRegister, db: Session = Depends(get_db)):
    """ثبت‌نام بیمار جدید"""
    # بررسی وجود ایمیل
    existing_patient = db.query(Patient).filter(Patient.email == patient_data.email).first()
    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="این ایمیل قبلاً ثبت شده است"
        )
    
    # ایجاد بیمار جدید
    db_patient = Patient(
        full_name=patient_data.full_name,
        email=patient_data.email,
        password_hash=get_password_hash(patient_data.password),
        date_of_birth=patient_data.date_of_birth,
        gender=patient_data.gender,
        phone_number=patient_data.phone_number,
        mizaj_type=patient_data.mizaj_type if patient_data.mizaj_type else MizajType.MOTADEL,
        medical_history=patient_data.medical_history,
        lifestyle_info=patient_data.lifestyle_info
    )
    
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    return PatientResponse(
        id=db_patient.id,
        full_name=db_patient.full_name,
        email=db_patient.email,
        date_of_birth=db_patient.date_of_birth,
        gender=db_patient.gender,
        phone_number=db_patient.phone_number,
        mizaj_type=db_patient.mizaj_type,
        medical_history=db_patient.medical_history,
        lifestyle_info=db_patient.lifestyle_info,
        is_active=db_patient.is_active,
        created_at=db_patient.created_at
    )

@router.post("/login")
def login(login_data: PatientLogin, db: Session = Depends(get_db)) -> Dict:
    """ورود بیمار"""
    # جستجوی بیمار
    patient = db.query(Patient).filter(Patient.email == login_data.email).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ایمیل یا رمز عبور نادرست است"
        )
    
    # بررسی رمز عبور
    if not verify_password(login_data.password, patient.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ایمیل یا رمز عبور نادرست است"
        )
    
    # ایجاد توکن
    access_token = create_access_token(data={"sub": patient.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "patient": {
            "id": patient.id,
            "full_name": patient.full_name,
            "email": patient.email,
            "mizaj_type": patient.mizaj_type
        }
    }

