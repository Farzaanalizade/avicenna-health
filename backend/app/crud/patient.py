from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from typing import Optional


def get_patient_by_user_id(db: Session, user_id: int) -> Optional[Patient]:
    """دریافت بیمار با user_id"""
    return db.query(Patient).filter(Patient.user_id == user_id).first()


def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    """دریافت بیمار با id"""
    return db.query(Patient).filter(Patient.id == patient_id).first()


def create_patient(db: Session, patient: PatientCreate, user_id: int) -> Patient:
    """ایجاد پروفایل بیمار جدید"""
    db_patient = Patient(**patient.model_dump(), user_id=user_id)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def update_patient(db: Session, patient_id: int, patient: PatientUpdate) -> Optional[Patient]:
    """به‌روزرسانی پروفایل بیمار"""
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return None
    
    update_data = patient.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_patient, field, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: int) -> bool:
    """حذف پروفایل بیمار"""
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return False
    
    db.delete(db_patient)
    db.commit()
    return True
