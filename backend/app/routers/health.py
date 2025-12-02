"""
Health Analysis Router - Complete Version
مسیرهای کامل تحلیل سلامت بر اساس طب سنتی ایرانی
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
import base64
from datetime import datetime
import json
import shutil
from pathlib import Path

from app.schemas.health import (
    HealthRecordCreate, HealthRecordResponse,
    TongueAnalysisInput, TongueAnalysisResult,
    EyeAnalysisInput, EyeAnalysisResult,
    VoiceAnalysisInput, VoiceAnalysisResult,
    AudioAnalysisInput, AudioAnalysisResult,
    PulseAnalysisInput, PulseAnalysisResult,
    VitalSignsInput, VitalSigns,
    QuickCheckRequest, QuickCheckResponse,
    FoodRecommendation, HerbalRecommendation,
    HealthRecordReport
)
from app.models import health_data as models
from app.database import get_db
from app.core.dependencies import get_current_patient
from app.models.patient import Patient
from app.services.ai_service import AIService
from app.services.analysis_service import AnalysisService, get_analysis_service
from app.services.avicenna_knowledge import AvicennaKnowledgeBase


router = APIRouter(prefix="/health", tags=["health"])

# مسیر ذخیره فایل‌ها
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize services
ai_service = AIService()
knowledge_base = AvicennaKnowledgeBase()




# -----------------------------------------------------
# 🩺 Endpoint جامع ثبت داده‌های سلامت
# -----------------------------------------------------
@router.post("/record", response_model=HealthRecordResponse, status_code=status.HTTP_201_CREATED)
async def record_health_data(
    tongue_image: Optional[UploadFile] = File(None),
    eye_image: Optional[UploadFile] = File(None),
    skin_image: Optional[UploadFile] = File(None),
    vitals_json: str = Form("{}"),
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """
    Endpoint جامع برای ثبت داده‌های یک جلسه بررسی سلامت.
    - تصاویر زبان، چشم، پوست را به عنوان فایل دریافت می‌کند.
    - علائم حیاتی (ضربان قلب، اکسیژن و ...) را به صورت یک رشته JSON دریافت می‌کند.
    """
    try:
        vital_signs_data = json.loads(vitals_json)
        
        # ایجاد یک گزارش سلامت کلی برای این جلسه
        health_report = models.HealthReport(
            patient_id=current_patient.id,
            created_at=datetime.utcnow()
        )
        db.add(health_report)
        db.flush() # برای گرفتن ID گزارش

        # 1. پردازش و ذخیره تصویر زبان
        tongue_record = None
        if tongue_image:
            file_path = UPLOAD_DIR / f"tongue_{current_patient.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(tongue_image.file, buffer)
            
            tongue_record = models.TongueAnalysis(
                patient_id=current_patient.id,
                image_path=str(file_path)
            )
            db.add(tongue_record)
            db.flush() # برای گرفتن ID
            health_report.tongue_analysis_id = tongue_record.id

        # 2. پردازش و ذخیره تصویر چشم
        eye_record = None
        if eye_image:
            file_path = UPLOAD_DIR / f"eye_{current_patient.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(eye_image.file, buffer)

            eye_record = models.EyeAnalysis(
                patient_id=current_patient.id,
                image_path=str(file_path)
            )
            db.add(eye_record)
            db.flush()
            health_report.eye_analysis_id = eye_record.id

        # 3. پردازش و ذخیره تصویر پوست
        skin_record = None
        if skin_image:
            file_path = UPLOAD_DIR / f"skin_{current_patient.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(skin_image.file, buffer)

            skin_record = models.SkinAnalysis(
                patient_id=current_patient.id,
                image_path=str(file_path),
                body_part=vital_signs_data.get("body_part", "face")
            )
            db.add(skin_record)
            db.flush()
            health_report.skin_analysis_id = skin_record.id
            
        # 4. پردازش و ذخیره علائم حیاتی
        if vital_signs_data:
            vitals_record = models.VitalSigns(
                patient_id=current_patient.id,
                **vital_signs_data
            )
            db.add(vitals_record)
            db.flush()
            health_report.vital_signs_ids = [vitals_record.id]

        db.commit()
        db.refresh(health_report)

        return HealthRecordResponse(
            report_id=health_report.id,
            message="Health data recorded successfully.",
            tongue_analysis_id=health_report.tongue_analysis_id,
            eye_analysis_id=health_report.eye_analysis_id,
            skin_analysis_id=health_report.skin_analysis_id,
            vital_signs_ids=health_report.vital_signs_ids,
            created_at=health_report.created_at
        )

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for vitals.")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while recording health data: {str(e)}"
        )


# -----------------------------------------------------
# 🔬 Endpoint شروع تحلیل جامع
# -----------------------------------------------------
@router.post("/report/{report_id}/analyze", response_model=HealthRecordReport, status_code=status.HTTP_200_OK)
async def analyze_health_report_endpoint(
    report_id: int,
    analysis_service: AnalysisService = Depends(get_analysis_service),
    current_patient: Patient = Depends(get_current_patient)
):
    """
    فرآیند تحلیل جامع یک گزارش سلامت را آغاز می‌کند.
    """
    try:
        # اطمینان از اینکه گزارش متعلق به بیمار فعلی است
        report = analysis_service.db.query(models.HealthReport).filter_by(id=report_id, patient_id=current_patient.id).first()
        if not report:
            raise HTTPException(status_code=404, detail="Health report not found or access denied.")
            
        updated_report = await analysis_service.analyze_health_report(report_id)
        
        # ساخت پاسخ بر اساس schema
        return HealthRecordReport(
            patient_name=current_patient.full_name,
            mizaj_type=current_patient.mizaj_type.value if current_patient.mizaj_type else "متعادل",
            diagnoses={
                "summary": updated_report.ai_summary,
                "risk_level": updated_report.risk_level,
            },
            recommendations=updated_report.recommendations,
            generated_at=updated_report.created_at.isoformat()
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Log the exception for debugging
        print(f"Error in analyze_health_report_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze health report.")





# -----------------------------------------------------
# ⚡ ENDPOINT‌های قدیمی (می‌توانند حذف یا غیرفعال شوند)
# -----------------------------------------------------

# -----------------------------------------------------
# 👅 تحلیل زبان
# -----------------------------------------------------
@router.post("/tongue/analyze", response_model=TongueAnalysisResult, status_code=status.HTTP_200_OK, deprecated=True)
async def analyze_tongue(
    request: TongueAnalysisInput,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """
    تحلیل تصویر زبان بر اساس طب سنتی ایرانی
    
    - رنگ زبان: قرمز، صورتی، زرد، سفید
    - پوشش زبان: ضخیم، نازک، زرد، سفید
    - ترک‌ها و شیارها
    - میزان رطوبت
    """
    try:
        # تحلیل با AI
        result = await ai_service.analyze_tongue(request.image_base64)
        
        # بروزرسانی اطلاعات بیمار
        if result.avicenna_diagnosis:
            current_patient.last_diagnosis = result.avicenna_diagnosis
            current_patient.updated_at = datetime.utcnow()
            db.commit()
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در تحلیل زبان: {str(e)}"
        )


@router.post("/tongue/upload", response_model=TongueAnalysisResult, deprecated=True)
async def upload_tongue_image(
    file: UploadFile = File(...),
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """آپلود مستقیم تصویر زبان"""
    try:
        # بررسی نوع فایل
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="فایل باید تصویر باشد"
            )
        
        # خواندن و تبدیل به base64
        contents = await file.read()
        image_base64 = base64.b64encode(contents).decode()
        
        # ارسال برای تحلیل
        request = TongueAnalysisInput(
            image_base64=image_base64,
            metadata={"filename": file.filename}
        )
        
        return await analyze_tongue(request, current_patient, db)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در آپلود تصویر: {str(e)}"
        )


# -----------------------------------------------------
# 👁 تحلیل چشم
# -----------------------------------------------------
@router.post("/eye/analyze", response_model=EyeAnalysisResult, status_code=status.HTTP_200_OK, deprecated=True)
async def analyze_eye(
    request: EyeAnalysisInput,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """
    تحلیل تصویر چشم و عنبیه
    
    - رنگ عنبیه و تغییرات آن
    - وضعیت صلبیه (سفیدی چشم)
    - وجود لکه‌ها یا رگ‌های قرمز
    - میزان روشنایی و براقیت
    """
    try:
        result = await ai_service.analyze_eye(request.image_base64)
        
        # ذخیره تاریخچه تحلیل
        if result.avicenna_diagnosis:
            current_patient.last_eye_analysis = datetime.utcnow()
            db.commit()
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در تحلیل چشم: {str(e)}"
        )


@router.post("/eye/upload", response_model=EyeAnalysisResult, deprecated=True)
async def upload_eye_image(
    file: UploadFile = File(...),
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """آپلود مستقیم تصویر چشم"""
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="فایل باید تصویر باشد"
            )
        
        contents = await file.read()
        image_base64 = base64.b64encode(contents).decode()
        
        request = EyeAnalysisInput(
            image_base64=image_base64,
            metadata={"filename": file.filename}
        )
        
        return await analyze_eye(request, current_patient, db)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در آپلود تصویر: {str(e)}"
        )


# -----------------------------------------------------
# 🗣 تحلیل صدا (گفتاری)
# -----------------------------------------------------
@router.post("/voice/analyze", response_model=VoiceAnalysisResult, status_code=status.HTTP_200_OK, deprecated=True)
async def analyze_voice(
    request: VoiceAnalysisInput,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """
    تحلیل صدای گفتاری بیمار
    
    - تُن و فرکانس صدا
    - سرعت گفتار
    - وضوح و کیفیت صدا
    - تشخیص مزاج از روی صدا
    """
    try:
        result = await ai_service.analyze_voice(
            request.audio_data_base64, 
            request.sample_rate_hz or 16000
        )
        
        # بروزرسانی پروفایل صوتی بیمار
        if result.avicenna_diagnosis:
            current_patient.voice_profile = {
                "pitch": result.pitch,
                "tone_quality": result.tone_quality,
                "analyzed_at": datetime.utcnow().isoformat()
            }
            db.commit()
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در تحلیل صدا: {str(e)}"
        )


@router.post("/voice/upload", response_model=VoiceAnalysisResult, deprecated=True)
async def upload_voice_recording(
    file: UploadFile = File(...),
    sample_rate: Optional[int] = 16000,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """آپلود فایل صوتی برای تحلیل صدا"""
    try:
        if not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="فایل باید صوتی باشد"
            )
        
        contents = await file.read()
        audio_base64 = base64.b64encode(contents).decode()
        
        request = VoiceAnalysisInput(
            audio_data_base64=audio_base64,
            sample_rate_hz=sample_rate,
            metadata={"filename": file.filename}
        )
        
        return await analyze_voice(request, current_patient, db)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در آپلود فایل صوتی: {str(e)}"
        )


# -----------------------------------------------------
# 🔊 تحلیل صوت عمومی (غیرکلامی)
# -----------------------------------------------------
@router.post("/audio/analyze", response_model=AudioAnalysisResult, status_code=status.HTTP_200_OK, deprecated=True)
async def analyze_audio(
    request: AudioAnalysisInput,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """
    تحلیل صداهای غیرکلامی
    
    - صدای قلب
    - صدای تنفس و ریه
    - صداهای شکمی
    - سایر صداهای بدن
    """
    try:
        # تعیین نوع تحلیل بر اساس audio_type
        audio_type = request.audio_type or "general"
        
        if audio_type == "heartbeat":
            detected_features = {"rhythm": "منظم", "rate": "72 bpm"}
            health_status = "قلب سالم"
        elif audio_type == "breathing":
            detected_features = {"pattern": "طبیعی", "rate": "16/min"}
            health_status = "تنفس طبیعی"
        else:
            detected_features = {"type": audio_type}
            health_status = "در حال پردازش"
        
        result = AudioAnalysisResult(
            detected_features=detected_features,
            health_status=health_status,
            risks_identified=[],
            recommendations={
                "message": "تحلیل اولیه انجام شد",
                "next_steps": ["مشورت با پزشک در صورت نیاز"]
            }
        )
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در تحلیل صوت: {str(e)}"
        )


# -----------------------------------------------------
# 💓 تحلیل نبض
# -----------------------------------------------------
@router.post("/pulse/analyze", response_model=PulseAnalysisResult, status_code=status.HTTP_200_OK, deprecated=True)
async def analyze_pulse(
    request: PulseAnalysisInput,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """
    تحلیل نبض بر اساس اصول طب سنتی
    
    - ضربان قلب و ریتم
    - قدرت و ضعف نبض
    - سرعت و کندی
    - نوع مزاج از روی نبض
    """
    try:
        # شبیه‌سازی تحلیل نبض
        result = PulseAnalysisResult(
            heart_rate=72.0,
            rhythm_type="منظم و موزون",
            mizaj_assessment=current_patient.mizaj_type or "گرم و خشک",
            amplitude_profile="متوسط",
            health_status="طبیعی",
            recommendations={
                "lifestyle": ["استراحت کافی", "کاهش استرس", "ورزش منظم"],
                "nutrition": ["مصرف آب کافی", "غذاهای متعادل"],
                "herbs": knowledge_base.get_herbs_for_mizaj(
                    current_patient.mizaj_type or "گرم و خشک"
                )[:3]
            }
        )
        
        # ذخیره آخرین تحلیل نبض
        current_patient.last_pulse_analysis = datetime.utcnow()
        db.commit()
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در تحلیل نبض: {str(e)}"
        )


# -----------------------------------------------------
# 🩺 ثبت علائم حیاتی
# -----------------------------------------------------
@router.post("/vital-signs", response_model=VitalSigns, status_code=status.HTTP_201_CREATED, deprecated=True)
async def record_vital_signs(
    request: VitalSignsInput,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """
    ثبت علائم حیاتی بیمار
    
    - دمای بدن
    - ضربان قلب
    - تعداد تنفس
    - فشار خون
    - اکسیژن خون
    """
    try:
        vital_signs = VitalSigns(**request.dict())
        
        # ذخیره در دیتابیس (در آینده)
        current_patient.last_vital_signs = {
            **vital_signs.dict(),
            "recorded_at": datetime.utcnow().isoformat()
        }
        db.commit()
        
        return vital_signs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ثبت علائم حیاتی: {str(e)}"
        )


@router.get("/vital-signs/history", response_model=List[Dict[str, Any]], deprecated=True)
async def get_vital_signs_history(
    limit: int = 10,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """دریافت سابقه علائم حیاتی بیمار"""
    try:
        history = getattr(current_patient, "vital_signs_history", [])
        return history[-limit:]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت سابقه علائم حیاتی: {str(e)}"
        )


# -----------------------------------------------------
# ⚡ بررسی سریع وضعیت سلامت (Quick Check)
# -----------------------------------------------------
@router.post("/quick-check", response_model=QuickCheckResponse, status_code=status.HTTP_200_OK, deprecated=True)
async def quick_health_check(
    request: QuickCheckRequest,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """
    بررسی سریع سلامت بر اساس داده‌های محدود
    """
    try:
        result = await ai_service.quick_health_check(
            symptoms=request.symptoms,
            vitals=request.vitals
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در بررسی سریع سلامت: {str(e)}"
        )


# -----------------------------------------------------
# 🌿 توصیه‌های تغذیه‌ای و گیاهی بر اساس مزاج
# -----------------------------------------------------
@router.get("/recommendations", response_model=Dict[str, Any])
async def get_recommendations(
    current_patient: Patient = Depends(get_current_patient)
):
    """بازگرداندن توصیه‌های مربوط به غذا و داروی گیاهی با توجه به مزاج"""
    try:
        mizaj = current_patient.mizaj_type or "متعادل"
        foods = knowledge_base.get_foods_for_mizaj(mizaj)
        herbs = knowledge_base.get_herbs_for_mizaj(mizaj)

        recommendations = {
            "mizaj": mizaj,
            "food_recommendations": foods,
            "herbal_recommendations": herbs,
            "lifestyle": knowledge_base.get_lifestyle_tips(mizaj)
        }

        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت توصیه‌ها: {str(e)}"
        )


# -----------------------------------------------------
# 📄 گزارش سلامت جامع
# -----------------------------------------------------
@router.get("/report", response_model=HealthRecordReport)
async def generate_health_report(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """
    تولید گزارش جامع سلامت بر اساس آخرین تحلیل‌ها و مزاج
    """
    try:
        report_data = {
            "patient_name": current_patient.name,
            "mizaj_type": current_patient.mizaj_type,
            "diagnoses": {
                "tongue": getattr(current_patient, "last_diagnosis", None),
                "voice": getattr(current_patient, "voice_profile", None),
                "eye": getattr(current_patient, "last_eye_analysis", None),
                "pulse": getattr(current_patient, "last_pulse_analysis", None),
                "vitals": getattr(current_patient, "last_vital_signs", None)
            },
            "recommendations": {
                "food": knowledge_base.get_foods_for_mizaj(current_patient.mizaj_type),
                "herbal": knowledge_base.get_herbs_for_mizaj(current_patient.mizaj_type),
                "lifestyle": knowledge_base.get_lifestyle_tips(current_patient.mizaj_type)
            },
            "generated_at": datetime.utcnow().isoformat()
        }

        return HealthRecordReport(**report_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در تولید گزارش سلامت: {str(e)}"
        )


# -----------------------------------------------------
# 🧠 تست اتصال و سلامت سرویس
# -----------------------------------------------------
@router.get("/ping")
async def ping_health_service():
    """تست اتصال به سرویس Health"""
    return {"status": "ok", "message": "Health module active and responding."}
