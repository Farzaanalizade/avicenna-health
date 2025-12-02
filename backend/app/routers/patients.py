from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.patient import Patient
from app.schemas.patient import PatientResponse, PatientUpdate
from app.core.dependencies import get_current_patient

router = APIRouter(prefix="/api/patients", tags=["Patients"])

@router.get("/me", response_model=PatientResponse)
def get_current_patient_info(current_patient: Patient = Depends(get_current_patient)):
    """دریافت اطلاعات بیمار جاری"""
    return current_patient

@router.put("/me", response_model=PatientResponse)
def update_current_patient(
    patient_update: PatientUpdate,
    db: Session = Depends(get_db),
    current_patient: Patient = Depends(get_current_patient)
):
    """به‌روزرسانی اطلاعات بیمار جاری"""
    # به‌روزرسانی فیلدهایی که ارسال شده‌اند
    update_data = patient_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_patient, field, value)
    
    db.commit()
    db.refresh(current_patient)
    return current_patient

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_patient: Patient = Depends(get_current_patient)
):
    """دریافت اطلاعات یک بیمار خاص (فقط برای ادمین یا خود بیمار)"""
    # بررسی دسترسی
    if current_patient.id != patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="شما اجازه دسترسی به این اطلاعات را ندارید"
        )
    
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیمار یافت نشد"
        )
    return patient

@router.delete("/me")
def delete_current_patient(
    db: Session = Depends(get_db),
    current_patient: Patient = Depends(get_current_patient)
):
    """حذف حساب کاربری بیمار"""
    db.delete(current_patient)
    db.commit()
    return {"message": "حساب کاربری با موفقیت حذف شد"}
