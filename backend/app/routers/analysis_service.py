"""
API Routes برای سرویس‌های تحلیل و توصیه
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
import os

from app.dependencies import get_db
from app.models.patient import Patient
from app.models.avicenna_diagnosis import DiagnosticFinding
from app.services.avicenna_analysis import AvicennaAnalysisEngine
from app.services.image_analysis import ImageAnalysisService
from app.services.personalized_recommendations import PersonalizedRecommendationService
from app.crud import patient as patient_crud

router = APIRouter(prefix="/api/v1/analysis", tags=["تحلیل و توصیه"])

# فولدر برای ذخیره تصاویر
UPLOAD_DIR = "uploads/diagnostic_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ============ تحلیل جامع ============
@router.post("/comprehensive/{patient_id}")
def comprehensive_analysis(
    patient_id: int,
    pulse_data: dict,
    urine_data: dict,
    tongue_data: dict,
    db: Session = Depends(get_db)
):
    """تحلیل جامع تمام داده‌های تشخیصی"""
    
    try:
        # تحلیل نبض
        from app.models.avicenna_diagnosis import PulseAnalysis
        pulse = PulseAnalysis(**pulse_data, patient_id=patient_id)
        pulse_analysis = AvicennaAnalysisEngine.analyze_pulse(pulse, db)
        
        # تحلیل ادرار
        from app.models.avicenna_diagnosis import UrineAnalysis
        urine = UrineAnalysis(**urine_data, patient_id=patient_id)
        urine_analysis = AvicennaAnalysisEngine.analyze_urine(urine, db)
        
        # تحلیل زبان
        from app.models.avicenna_diagnosis import TongueCoating
        tongue = TongueCoating(**tongue_data, patient_id=patient_id)
        tongue_analysis = AvicennaAnalysisEngine.analyze_tongue(tongue, db)
        
        # ترکیب نتایج
        diagnosis = AvicennaAnalysisEngine.synthesize_diagnosis(
            pulse_analysis,
            urine_analysis,
            tongue_analysis
        )
        
        # توصیه درمان‌ها
        recommended_remedies = AvicennaAnalysisEngine.recommend_treatments(
            diagnosis["primary_mizaj"],
            diagnosis["secondary_mizaj"],
            db
        )
        
        # توصیه‌های سبک زندگی
        lifestyle_recommendations = AvicennaAnalysisEngine.recommend_lifestyle_changes(
            diagnosis["primary_mizaj"]
        )
        
        # توصیه‌های غذایی
        dietary_recommendations = AvicennaAnalysisEngine.recommend_dietary_changes(
            diagnosis["primary_mizaj"]
        )
        
        return {
            "patient_id": patient_id,
            "pulse_analysis": pulse_analysis,
            "urine_analysis": urine_analysis,
            "tongue_analysis": tongue_analysis,
            "diagnosis": diagnosis,
            "recommended_remedies": [
                {
                    "id": r.id,
                    "name": r.name_fa,
                    "type": r.remedy_type,
                    "usage": r.usage_method,
                    "dosage": r.dosage
                }
                for r in recommended_remedies
            ],
            "lifestyle_recommendations": lifestyle_recommendations,
            "dietary_recommendations": dietary_recommendations,
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"خطا در تحلیل: {str(e)}"
        )


# ============ تحلیل تصاویر ============
@router.post("/analyze-tongue-image/{patient_id}")
async def analyze_tongue_image(
    patient_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """تحلیل تصویر زبان"""
    
    try:
        # ذخیره تصویر
        file_path = f"{UPLOAD_DIR}/tongue_{patient_id}_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # تحلیل
        analysis = ImageAnalysisService.analyze_tongue_image(file_path)
        abnormalities = ImageAnalysisService.detect_tongue_abnormalities(analysis)
        organ_indicators = ImageAnalysisService.correlate_tongue_with_organs(analysis)
        
        return {
            "patient_id": patient_id,
            "image_path": file_path,
            "analysis": analysis,
            "abnormalities": abnormalities,
            "organ_indicators": organ_indicators,
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"خطا در تحلیل تصویر: {str(e)}"
        )


@router.post("/analyze-eye-image/{patient_id}")
async def analyze_eye_image(
    patient_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """تحلیل تصویر چشم"""
    
    try:
        # ذخیره تصویر
        file_path = f"{UPLOAD_DIR}/eye_{patient_id}_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # تحلیل
        analysis = ImageAnalysisService.analyze_eye_image(file_path)
        abnormalities = ImageAnalysisService.detect_eye_abnormalities(analysis)
        
        return {
            "patient_id": patient_id,
            "image_path": file_path,
            "analysis": analysis,
            "abnormalities": abnormalities,
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"خطا در تحلیل تصویر: {str(e)}"
        )


# ============ توصیه‌های شخصی‌شده ============
@router.get("/personalized-plan/{patient_id}")
def get_personalized_plan(
    patient_id: int,
    db: Session = Depends(get_db)
):
    """دریافت برنامه درمانی شخصی‌شده"""
    
    try:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="بیمار یافت نشد"
            )
        
        plan = PersonalizedRecommendationService.generate_personalized_plan(patient, db)
        return plan
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/weekly-schedule/{patient_id}")
def get_weekly_schedule(
    patient_id: int,
    db: Session = Depends(get_db)
):
    """دریافت برنامه هفتگی"""
    
    try:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="بیمار یافت نشد"
            )
        
        schedule = PersonalizedRecommendationService.generate_weekly_schedule(patient, db)
        return schedule
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/dietary-plan/{patient_id}")
def get_dietary_plan(
    patient_id: int,
    mizaj: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """دریافت برنامه غذایی"""
    
    try:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="بیمار یافت نشد"
            )
        
        # اگر mizaj تعیین نشده باشد از mizaj بیمار استفاده کن
        if not mizaj:
            mizaj = patient.mizaj_type or "motadel"
        
        plan = PersonalizedRecommendationService.generate_monthly_dietary_plan(
            patient, mizaj, db
        )
        return plan
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/self-monitoring-guide/{patient_id}")
def get_self_monitoring_guide(
    patient_id: int,
    db: Session = Depends(get_db)
):
    """دریافت راهنمای خود مراقبتی"""
    
    try:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="بیمار یافت نشد"
            )
        
        guide = PersonalizedRecommendationService.generate_self_monitoring_guide(
            patient, db
        )
        return guide
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ============ توصیه‌های تصویری ============
@router.post("/image-recommendations/{patient_id}")
async def get_image_recommendations(
    patient_id: int,
    tongue_file: Optional[UploadFile] = File(None),
    eye_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """دریافت توصیه‌های براساس تحلیل تصاویر"""
    
    try:
        tongue_analysis = None
        eye_analysis = None
        
        # تحلیل تصویر زبان
        if tongue_file:
            file_path = f"{UPLOAD_DIR}/tongue_{patient_id}.jpg"
            with open(file_path, "wb") as f:
                f.write(await tongue_file.read())
            tongue_analysis = ImageAnalysisService.analyze_tongue_image(file_path)
        
        # تحلیل تصویر چشم
        if eye_file:
            file_path = f"{UPLOAD_DIR}/eye_{patient_id}.jpg"
            with open(file_path, "wb") as f:
                f.write(await eye_file.read())
            eye_analysis = ImageAnalysisService.analyze_eye_image(file_path)
        
        # استخراج توصیه‌ها
        recommendations = ImageAnalysisService.get_health_recommendations(
            tongue_analysis or {},
            eye_analysis or {}
        )
        
        return {
            "patient_id": patient_id,
            "tongue_analysis": tongue_analysis,
            "eye_analysis": eye_analysis,
            "recommendations": recommendations,
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ============ گزارش جامع ============
@router.get("/full-report/{patient_id}")
def get_full_report(
    patient_id: int,
    db: Session = Depends(get_db)
):
    """دریافت گزارش جامع برای بیمار"""
    
    try:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="بیمار یافت نشد"
            )
        
        report = {
            "patient_info": {
                "id": patient.id,
                "name": patient.full_name,
                "age": 30,  # محاسبه از تاریخ تولد
                "mizaj": patient.mizaj_type,
            },
            "recent_findings": [],  # TODO: Implement get_comprehensive_report
            "personalized_plan": PersonalizedRecommendationService.generate_personalized_plan(
                patient, db
            ),
            "weekly_schedule": PersonalizedRecommendationService.generate_weekly_schedule(
                patient, db
            ),
            "dietary_plan": PersonalizedRecommendationService.generate_monthly_dietary_plan(
                patient, patient.mizaj_type or "motadel", db
            ),
            "self_monitoring_guide": PersonalizedRecommendationService.generate_self_monitoring_guide(
                patient, db
            ),
        }
        
        return report
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
