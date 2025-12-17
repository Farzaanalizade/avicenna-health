from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta
from typing import List

from app.database import get_db
from app.models.sensor_and_diagnostic_data import (
    SensorData, WearableDevice, PulseAnalysis, UrineAnalysis, 
    TongueCoating, DiagnosticFinding, MizajBalanceTreatment
)
from app.models.patient import Patient
from app.schemas.sensor_diagnostic_schemas import (
    SensorDataCreate, SensorDataResponse, SensorDataUpdate,
    WearableDeviceCreate, WearableDeviceResponse, WearableDeviceUpdate,
    PulseAnalysisCreate, PulseAnalysisResponse,
    UrineAnalysisCreate, UrineAnalysisResponse,
    TongueCoatingCreate, TongueCoatingResponse,
    DiagnosticFindingCreate, DiagnosticFindingResponse,
    MizajBalanceTreatmentCreate, MizajBalanceTreatmentUpdate, MizajBalanceTreatmentResponse
)
from app.utils.security import get_current_user

router = APIRouter(
    prefix="/api/v1",
    tags=["sensor_diagnostic"]
)


# ==================== SENSOR DATA ====================

@router.post("/sensor-data/upload", response_model=SensorDataResponse)
def upload_sensor_data(
    patient_id: int,
    sensor_data: SensorDataCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """بارگذاری داده سنسور"""
    # بررسی اینکه بیمار موجود است
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    
    # ایجاد داده سنسور
    db_sensor_data = SensorData(
        patient_id=patient_id,
        sensor_type=sensor_data.sensor_type,
        raw_value=sensor_data.raw_value,
        unit=sensor_data.unit,
        device_info=sensor_data.device_info,
        confidence_score=sensor_data.confidence_score,
        timestamp=datetime.utcnow()
    )
    
    db.add(db_sensor_data)
    db.commit()
    db.refresh(db_sensor_data)
    
    return db_sensor_data


@router.post("/sensor-data/batch-upload")
def batch_upload_sensor_data(
    patient_id: int,
    sensor_readings: List[SensorDataCreate],
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """بارگذاری دسته‌ای داده‌های سنسور"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    
    uploaded_count = 0
    
    for sensor_data in sensor_readings:
        db_sensor_data = SensorData(
            patient_id=patient_id,
            sensor_type=sensor_data.sensor_type,
            raw_value=sensor_data.raw_value,
            unit=sensor_data.unit,
            device_info=sensor_data.device_info,
            confidence_score=sensor_data.confidence_score,
            timestamp=sensor_data.timestamp or datetime.utcnow()
        )
        db.add(db_sensor_data)
        uploaded_count += 1
    
    db.commit()
    
    return {
        "message": f"{uploaded_count} داده سنسور بارگذاری شد",
        "count": uploaded_count
    }


@router.get("/sensor-data/patient/{patient_id}", response_model=List[SensorDataResponse])
def get_patient_sensor_data(
    patient_id: int,
    sensor_type: str = None,
    days: int = 7,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """دریافت داده‌های سنسور بیمار"""
    # بررسی بیمار
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    
    # تاریخ شروع
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(SensorData).filter(
        SensorData.patient_id == patient_id,
        SensorData.created_at >= start_date
    )
    
    if sensor_type:
        query = query.filter(SensorData.sensor_type == sensor_type)
    
    return query.order_by(desc(SensorData.created_at)).all()


@router.patch("/sensor-data/{sensor_id}", response_model=SensorDataResponse)
def update_sensor_data(
    sensor_id: int,
    update_data: SensorDataUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """به‌روزرسانی داده سنسور"""
    db_sensor = db.query(SensorData).filter(SensorData.id == sensor_id).first()
    if not db_sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="داده سنسور یافت نشد"
        )
    
    if update_data.processed_value is not None:
        db_sensor.processed_value = update_data.processed_value
    if update_data.confidence_score is not None:
        db_sensor.confidence_score = update_data.confidence_score
    if update_data.is_valid is not None:
        db_sensor.is_valid = update_data.is_valid
    if update_data.validation_notes is not None:
        db_sensor.validation_notes = update_data.validation_notes
    
    db.commit()
    db.refresh(db_sensor)
    
    return db_sensor


# ==================== WEARABLE DEVICE ====================

@router.post("/wearable/register", response_model=WearableDeviceResponse)
def register_wearable_device(
    patient_id: int,
    device_data: WearableDeviceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """ثبت دستگاه پوشیدنی جدید"""
    # بررسی بیمار
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    
    # بررسی تکراری بودن device_id
    existing = db.query(WearableDevice).filter(
        WearableDevice.device_id == device_data.device_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="این دستگاه قبلاً ثبت شده است"
        )
    
    db_device = WearableDevice(
        patient_id=patient_id,
        device_type=device_data.device_type,
        device_model=device_data.device_model,
        device_id=device_data.device_id,
        device_name=device_data.device_name,
        api_token=device_data.api_token,
        api_url=device_data.api_url,
        sync_frequency=device_data.sync_frequency or 300
    )
    
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    
    return db_device


@router.get("/wearable/devices/{patient_id}", response_model=List[WearableDeviceResponse])
def get_patient_wearables(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """دریافت دستگاه‌های پوشیدنی بیمار"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    
    return db.query(WearableDevice).filter(
        WearableDevice.patient_id == patient_id
    ).all()


@router.patch("/wearable/{device_id}", response_model=WearableDeviceResponse)
def update_wearable_device(
    device_id: int,
    update_data: WearableDeviceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """به‌روزرسانی وضعیت دستگاه پوشیدنی"""
    db_device = db.query(WearableDevice).filter(WearableDevice.id == device_id).first()
    if not db_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="دستگاه یافت نشد"
        )
    
    if update_data.connection_status:
        db_device.connection_status = update_data.connection_status
        if update_data.connection_status == "CONNECTED":
            db_device.last_sync = datetime.utcnow()
    
    if update_data.battery_level is not None:
        db_device.battery_level = update_data.battery_level
    
    if update_data.is_active is not None:
        db_device.is_active = update_data.is_active
    
    if update_data.sync_frequency:
        db_device.sync_frequency = update_data.sync_frequency
    
    db.commit()
    db.refresh(db_device)
    
    return db_device


# ==================== PULSE ANALYSIS ====================

@router.post("/pulse-analysis", response_model=PulseAnalysisResponse)
def create_pulse_analysis(
    patient_id: int,
    pulse_data: PulseAnalysisCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """ثبت تحلیل نبض"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    
    db_pulse = PulseAnalysis(
        patient_id=patient_id,
        pulse_rate=pulse_data.pulse_rate,
        pulse_rhythm=pulse_data.pulse_rhythm,
        pulse_strength=pulse_data.pulse_strength,
        pulse_depth=pulse_data.pulse_depth,
        measurement_location=pulse_data.measurement_location,
        mizaj_indication=pulse_data.mizaj_indication,
        organ_involved=pulse_data.organ_involved,
        disease_indication=pulse_data.disease_indication,
        audio_recording_path=pulse_data.audio_recording_path,
        clinical_notes=pulse_data.clinical_notes
    )
    
    db.add(db_pulse)
    db.commit()
    db.refresh(db_pulse)
    
    return db_pulse


@router.get("/pulse-analysis/patient/{patient_id}", response_model=List[PulseAnalysisResponse])
def get_patient_pulse_analyses(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """دریافت تحلیل‌های نبض بیمار"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    
    return db.query(PulseAnalysis).filter(
        PulseAnalysis.patient_id == patient_id
    ).order_by(desc(PulseAnalysis.created_at)).all()


# ==================== URINE ANALYSIS ====================

@router.post("/urine-analysis", response_model=UrineAnalysisResponse)
def create_urine_analysis(
    patient_id: int,
    urine_data: UrineAnalysisCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """ثبت تحلیل ادرار"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    
    db_urine = UrineAnalysis(
        patient_id=patient_id,
        color=urine_data.color,
        transparency=urine_data.transparency,
        smell=urine_data.smell,
        consistency=urine_data.consistency,
        temperature=urine_data.temperature,
        volume=urine_data.volume,
        ph_level=urine_data.ph_level,
        specific_gravity=urine_data.specific_gravity,
        protein_level=urine_data.protein_level,
        glucose_level=urine_data.glucose_level,
        ketones=urine_data.ketones,
        blood_present=urine_data.blood_present,
        bacteria_present=urine_data.bacteria_present,
        mizaj_indication=urine_data.mizaj_indication,
        organ_involved=urine_data.organ_involved,
        disease_indication=urine_data.disease_indication,
        image_path=urine_data.image_path,
        clinical_notes=urine_data.clinical_notes
    )
    
    db.add(db_urine)
    db.commit()
    db.refresh(db_urine)
    
    return db_urine


@router.get("/urine-analysis/patient/{patient_id}", response_model=List[UrineAnalysisResponse])
def get_patient_urine_analyses(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """دریافت تحلیل‌های ادرار بیمار"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    
    return db.query(UrineAnalysis).filter(
        UrineAnalysis.patient_id == patient_id
    ).order_by(desc(UrineAnalysis.created_at)).all()


# ==================== TONGUE COATING ====================

@router.post("/tongue-coating", response_model=TongueCoatingResponse)
def create_tongue_coating(
    patient_id: int,
    tongue_data: TongueCoatingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """ثبت تحلیل پوشش زبان"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    
    db_tongue = TongueCoating(
        patient_id=patient_id,
        body_color=tongue_data.body_color,
        coating_type=tongue_data.coating_type,
        coating_color=tongue_data.coating_color,
        coating_distribution=tongue_data.coating_distribution,
        texture=tongue_data.texture,
        moisture=tongue_data.moisture,
        thickness=tongue_data.thickness,
        cracks_present=tongue_data.cracks_present,
        cracks_pattern=tongue_data.cracks_pattern,
        teeth_marks=tongue_data.teeth_marks,
        tremor=tongue_data.tremor,
        nodules_present=tongue_data.nodules_present,
        pimples_present=tongue_data.pimples_present,
        swollen_papillae=tongue_data.swollen_papillae,
        mizaj_indication=tongue_data.mizaj_indication,
        heat_cold_index=tongue_data.heat_cold_index,
        dryness_wetness_index=tongue_data.dryness_wetness_index,
        chinese_medicine_signs=tongue_data.chinese_medicine_signs,
        ayurvedic_signs=tongue_data.ayurvedic_signs,
        potential_diseases=tongue_data.potential_diseases,
        image_path=tongue_data.image_path,
        clinical_notes=tongue_data.clinical_notes
    )
    
    db.add(db_tongue)
    db.commit()
    db.refresh(db_tongue)
    
    return db_tongue


@router.get("/tongue-coating/patient/{patient_id}", response_model=List[TongueCoatingResponse])
def get_patient_tongue_coatings(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """دریافت تحلیل‌های پوشش زبان بیمار"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    
    return db.query(TongueCoating).filter(
        TongueCoating.patient_id == patient_id
    ).order_by(desc(TongueCoating.created_at)).all()


# ==================== DIAGNOSTIC FINDING ====================

@router.post("/diagnostic-finding", response_model=DiagnosticFindingResponse)
def create_diagnostic_finding(
    patient_id: int,
    finding_data: DiagnosticFindingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """ایجاد یافتۀ تشخیصی"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    
    db_finding = DiagnosticFinding(
        patient_id=patient_id,
        finding_type=finding_data.finding_type,
        avicenna_diagnosis=finding_data.avicenna_diagnosis,
        affected_organs=finding_data.affected_organs,
        affected_humors=finding_data.affected_humors,
        severity_level=finding_data.severity_level,
        prognosis=finding_data.prognosis,
        expected_duration=finding_data.expected_duration,
        root_cause=finding_data.root_cause,
        contributing_factors=finding_data.contributing_factors,
        recommended_treatment=finding_data.recommended_treatment,
        dietary_recommendations=finding_data.dietary_recommendations,
        lifestyle_recommendations=finding_data.lifestyle_recommendations,
        traditional_medicines=finding_data.traditional_medicines,
        prevention_measures=finding_data.prevention_measures,
        complications_if_untreated=finding_data.complications_if_untreated,
        requires_doctor_consultation=finding_data.requires_doctor_consultation,
        urgency_level=finding_data.urgency_level or "routine",
        specialist_type=finding_data.specialist_type,
        physician_notes=finding_data.physician_notes
    )
    
    db.add(db_finding)
    db.commit()
    db.refresh(db_finding)
    
    return db_finding


@router.get("/diagnostic-finding/patient/{patient_id}", response_model=List[DiagnosticFindingResponse])
def get_patient_diagnostic_findings(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """دریافت یافته‌های تشخیصی بیمار"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    
    return db.query(DiagnosticFinding).filter(
        DiagnosticFinding.patient_id == patient_id
    ).order_by(desc(DiagnosticFinding.created_at)).all()


# ==================== MIZAJ BALANCE TREATMENT ====================

@router.post("/mizaj-treatment", response_model=MizajBalanceTreatmentResponse)
def create_mizaj_treatment(
    patient_id: int,
    treatment_data: MizajBalanceTreatmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """ایجاد برنامۀ درمانی تعادل مزاج"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    
    db_treatment = MizajBalanceTreatment(
        patient_id=patient_id,
        current_mizaj=treatment_data.current_mizaj,
        target_mizaj=treatment_data.target_mizaj,
        duration_days=treatment_data.duration_days,
        dietary_treatments=treatment_data.dietary_treatments,
        herbal_treatments=treatment_data.herbal_treatments,
        lifestyle_treatments=treatment_data.lifestyle_treatments,
        natural_treatments=treatment_data.natural_treatments,
        physical_treatments=treatment_data.physical_treatments,
        spiritual_treatments=treatment_data.spiritual_treatments,
        forbidden_items=treatment_data.forbidden_items,
        physician_notes=treatment_data.physician_notes
    )
    
    db.add(db_treatment)
    db.commit()
    db.refresh(db_treatment)
    
    return db_treatment


@router.get("/mizaj-treatment/patient/{patient_id}", response_model=List[MizajBalanceTreatmentResponse])
def get_patient_mizaj_treatments(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """دریافت برنامه‌های درمانی تعادل مزاج بیمار"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    
    return db.query(MizajBalanceTreatment).filter(
        MizajBalanceTreatment.patient_id == patient_id,
        MizajBalanceTreatment.status == "active"
    ).order_by(desc(MizajBalanceTreatment.created_at)).all()


@router.patch("/mizaj-treatment/{treatment_id}", response_model=MizajBalanceTreatmentResponse)
def update_mizaj_treatment(
    treatment_id: int,
    update_data: MizajBalanceTreatmentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """به‌روزرسانی برنامۀ درمانی"""
    db_treatment = db.query(MizajBalanceTreatment).filter(
        MizajBalanceTreatment.id == treatment_id
    ).first()
    
    if not db_treatment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="برنامۀ درمانی یافت نشد"
        )
    
    if update_data.status:
        db_treatment.status = update_data.status
    
    if update_data.progress_tracking:
        db_treatment.progress_tracking = update_data.progress_tracking
    
    if update_data.physician_notes:
        db_treatment.physician_notes = update_data.physician_notes
    
    if update_data.confidence_score is not None:
        db_treatment.confidence_score = update_data.confidence_score
    
    db.commit()
    db.refresh(db_treatment)
    
    return db_treatment
