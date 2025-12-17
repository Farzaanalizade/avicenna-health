"""
API Routes برای اصول تشخیصی سینا
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies import get_db
from app.schemas.avicenna_diagnosis import (
    PulseAnalysisCreate, PulseAnalysisResponse,
    UrineAnalysisCreate, UrineAnalysisResponse,
    TongueCoatingCreate, TongueCoatingResponse,
    DiagnosticFindingCreate, DiagnosticFindingResponse
)
from app.crud.avicenna_diagnosis import (
    PulseAnalysisOps, UrineAnalysisOps, TongueCoatingOps, DiagnosticFindingOps
)

router = APIRouter(prefix="/api/v1/diagnosis", tags=["تشخیصی"])


# ============ نبض ============
@router.post("/pulse", response_model=PulseAnalysisResponse)
def create_pulse_analysis(
    pulse_data: PulseAnalysisCreate,
    db: Session = Depends(get_db)
):
    """ایجاد تحلیل نبض جدید"""
    return PulseAnalysisOps.create(db, pulse_data)


@router.get("/pulse/{pulse_id}", response_model=PulseAnalysisResponse)
def get_pulse_analysis(pulse_id: int, db: Session = Depends(get_db)):
    """دریافت تحلیل نبض با ID"""
    pulse = PulseAnalysisOps.get_by_id(db, pulse_id)
    if not pulse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="نبض یافت نشد")
    return pulse


@router.get("/pulse/patient/{patient_id}", response_model=List[PulseAnalysisResponse])
def get_patient_pulses(patient_id: int, db: Session = Depends(get_db)):
    """دریافت تمام تحلیل‌های نبض برای بیمار"""
    return PulseAnalysisOps.get_by_patient(db, patient_id)


@router.get("/pulse/patient/{patient_id}/latest", response_model=Optional[PulseAnalysisResponse])
def get_latest_pulse(patient_id: int, db: Session = Depends(get_db)):
    """دریافت آخرین تحلیل نبض"""
    return PulseAnalysisOps.get_latest_by_patient(db, patient_id)


@router.put("/pulse/{pulse_id}", response_model=PulseAnalysisResponse)
def update_pulse_analysis(
    pulse_id: int,
    pulse_data: dict,
    db: Session = Depends(get_db)
):
    """به‌روزرسانی تحلیل نبض"""
    updated_pulse = PulseAnalysisOps.update(db, pulse_id, pulse_data)
    if not updated_pulse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="نبض یافت نشد")
    return updated_pulse


@router.delete("/pulse/{pulse_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pulse_analysis(pulse_id: int, db: Session = Depends(get_db)):
    """حذف تحلیل نبض"""
    if not PulseAnalysisOps.delete(db, pulse_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="نبض یافت نشد")


# ============ ادرار ============
@router.post("/urine", response_model=UrineAnalysisResponse)
def create_urine_analysis(
    urine_data: UrineAnalysisCreate,
    db: Session = Depends(get_db)
):
    """ایجاد تحلیل ادرار جدید"""
    return UrineAnalysisOps.create(db, urine_data)


@router.get("/urine/{urine_id}", response_model=UrineAnalysisResponse)
def get_urine_analysis(urine_id: int, db: Session = Depends(get_db)):
    """دریافت تحلیل ادرار با ID"""
    urine = UrineAnalysisOps.get_by_id(db, urine_id)
    if not urine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ادرار یافت نشد")
    return urine


@router.get("/urine/patient/{patient_id}", response_model=List[UrineAnalysisResponse])
def get_patient_urines(patient_id: int, db: Session = Depends(get_db)):
    """دریافت تمام تحلیل‌های ادرار برای بیمار"""
    return UrineAnalysisOps.get_by_patient(db, patient_id)


@router.get("/urine/patient/{patient_id}/latest", response_model=Optional[UrineAnalysisResponse])
def get_latest_urine(patient_id: int, db: Session = Depends(get_db)):
    """دریافت آخرین تحلیل ادرار"""
    return UrineAnalysisOps.get_latest_by_patient(db, patient_id)


@router.put("/urine/{urine_id}", response_model=UrineAnalysisResponse)
def update_urine_analysis(
    urine_id: int,
    urine_data: dict,
    db: Session = Depends(get_db)
):
    """به‌روزرسانی تحلیل ادرار"""
    updated_urine = UrineAnalysisOps.update(db, urine_id, urine_data)
    if not updated_urine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ادرار یافت نشد")
    return updated_urine


# ============ زبان ============
@router.post("/tongue", response_model=TongueCoatingResponse)
def create_tongue_coating(
    tongue_data: TongueCoatingCreate,
    db: Session = Depends(get_db)
):
    """ایجاد تحلیل زبان جدید"""
    return TongueCoatingOps.create(db, tongue_data)


@router.get("/tongue/{tongue_id}", response_model=TongueCoatingResponse)
def get_tongue_coating(tongue_id: int, db: Session = Depends(get_db)):
    """دریافت تحلیل زبان با ID"""
    tongue = TongueCoatingOps.get_by_id(db, tongue_id)
    if not tongue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="زبان یافت نشد")
    return tongue


@router.get("/tongue/patient/{patient_id}", response_model=List[TongueCoatingResponse])
def get_patient_tongues(patient_id: int, db: Session = Depends(get_db)):
    """دریافت تمام تحلیل‌های زبان برای بیمار"""
    return TongueCoatingOps.get_by_patient(db, patient_id)


@router.get("/tongue/patient/{patient_id}/latest", response_model=Optional[TongueCoatingResponse])
def get_latest_tongue(patient_id: int, db: Session = Depends(get_db)):
    """دریافت آخرین تحلیل زبان"""
    return TongueCoatingOps.get_latest_by_patient(db, patient_id)


@router.put("/tongue/{tongue_id}", response_model=TongueCoatingResponse)
def update_tongue_coating(
    tongue_id: int,
    tongue_data: dict,
    db: Session = Depends(get_db)
):
    """به‌روزرسانی تحلیل زبان"""
    updated_tongue = TongueCoatingOps.update(db, tongue_id, tongue_data)
    if not updated_tongue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="زبان یافت نشد")
    return updated_tongue


# ============ یافته‌های تشخیصی ============
@router.post("/findings", response_model=DiagnosticFindingResponse)
def create_diagnostic_finding(
    finding_data: DiagnosticFindingCreate,
    db: Session = Depends(get_db)
):
    """ایجاد یافته تشخیصی جدید"""
    return DiagnosticFindingOps.create(db, finding_data)


@router.get("/findings/{finding_id}", response_model=DiagnosticFindingResponse)
def get_diagnostic_finding(finding_id: int, db: Session = Depends(get_db)):
    """دریافت یافته تشخیصی با ID"""
    finding = DiagnosticFindingOps.get_by_id(db, finding_id)
    if not finding:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="یافته یافت نشد")
    return finding


@router.get("/findings/patient/{patient_id}", response_model=List[DiagnosticFindingResponse])
def get_patient_findings(patient_id: int, db: Session = Depends(get_db)):
    """دریافت تمام یافته‌های تشخیصی برای بیمار"""
    return DiagnosticFindingOps.get_by_patient(db, patient_id)


@router.get("/findings/patient/{patient_id}/latest", response_model=Optional[DiagnosticFindingResponse])
def get_latest_finding(patient_id: int, db: Session = Depends(get_db)):
    """دریافت آخرین یافته تشخیصی"""
    return DiagnosticFindingOps.get_latest_by_patient(db, patient_id)


@router.put("/findings/{finding_id}", response_model=DiagnosticFindingResponse)
def update_diagnostic_finding(
    finding_id: int,
    finding_data: dict,
    db: Session = Depends(get_db)
):
    """به‌روزرسانی یافته تشخیصی"""
    updated_finding = DiagnosticFindingOps.update(db, finding_id, finding_data)
    if not updated_finding:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="یافته یافت نشد")
    return updated_finding


@router.get("/report/patient/{patient_id}")
def get_diagnostic_report(patient_id: int, db: Session = Depends(get_db)):
    """دریافت گزارش تشخیصی جامع برای بیمار"""
    report = DiagnosticFindingOps.get_comprehensive_report(db, patient_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="گزارشی یافت نشد")
    return report
