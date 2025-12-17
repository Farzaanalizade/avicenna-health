"""
CRUD operations برای تشخیصی سینا
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.avicenna_diagnosis import (
    PulseAnalysis, UrineAnalysis, TongueCoating, DiagnosticFinding
)
from app.schemas.avicenna_diagnosis import (
    PulseAnalysisCreate, UrineAnalysisCreate, TongueCoatingCreate, DiagnosticFindingCreate
)


# ============ نبض ============
class PulseAnalysisOps:
    @staticmethod
    def create(db: Session, pulse_data: PulseAnalysisCreate) -> PulseAnalysis:
        """ایجاد تحلیل نبض جدید"""
        db_pulse = PulseAnalysis(**pulse_data.dict())
        db.add(db_pulse)
        db.commit()
        db.refresh(db_pulse)
        return db_pulse

    @staticmethod
    def get_by_id(db: Session, pulse_id: int) -> Optional[PulseAnalysis]:
        """دریافت تحلیل نبض با ID"""
        return db.query(PulseAnalysis).filter(PulseAnalysis.id == pulse_id).first()

    @staticmethod
    def get_by_patient(db: Session, patient_id: int) -> List[PulseAnalysis]:
        """دریافت تمام تحلیل‌های نبض برای بیمار"""
        return db.query(PulseAnalysis).filter(PulseAnalysis.patient_id == patient_id).order_by(
            PulseAnalysis.recorded_at.desc()
        ).all()

    @staticmethod
    def get_latest_by_patient(db: Session, patient_id: int) -> Optional[PulseAnalysis]:
        """دریافت آخرین تحلیل نبض"""
        return db.query(PulseAnalysis).filter(
            PulseAnalysis.patient_id == patient_id
        ).order_by(PulseAnalysis.recorded_at.desc()).first()

    @staticmethod
    def update(db: Session, pulse_id: int, pulse_data: dict) -> Optional[PulseAnalysis]:
        """به‌روزرسانی تحلیل نبض"""
        db_pulse = PulseAnalysisOps.get_by_id(db, pulse_id)
        if db_pulse:
            for key, value in pulse_data.items():
                if value is not None:
                    setattr(db_pulse, key, value)
            db.commit()
            db.refresh(db_pulse)
        return db_pulse

    @staticmethod
    def delete(db: Session, pulse_id: int) -> bool:
        """حذف تحلیل نبض"""
        db_pulse = PulseAnalysisOps.get_by_id(db, pulse_id)
        if db_pulse:
            db.delete(db_pulse)
            db.commit()
            return True
        return False


# ============ ادرار ============
class UrineAnalysisOps:
    @staticmethod
    def create(db: Session, urine_data: UrineAnalysisCreate) -> UrineAnalysis:
        """ایجاد تحلیل ادرار جدید"""
        db_urine = UrineAnalysis(**urine_data.dict())
        db.add(db_urine)
        db.commit()
        db.refresh(db_urine)
        return db_urine

    @staticmethod
    def get_by_id(db: Session, urine_id: int) -> Optional[UrineAnalysis]:
        """دریافت تحلیل ادرار با ID"""
        return db.query(UrineAnalysis).filter(UrineAnalysis.id == urine_id).first()

    @staticmethod
    def get_by_patient(db: Session, patient_id: int) -> List[UrineAnalysis]:
        """دریافت تمام تحلیل‌های ادرار برای بیمار"""
        return db.query(UrineAnalysis).filter(UrineAnalysis.patient_id == patient_id).order_by(
            UrineAnalysis.recorded_at.desc()
        ).all()

    @staticmethod
    def get_latest_by_patient(db: Session, patient_id: int) -> Optional[UrineAnalysis]:
        """دریافت آخرین تحلیل ادرار"""
        return db.query(UrineAnalysis).filter(
            UrineAnalysis.patient_id == patient_id
        ).order_by(UrineAnalysis.recorded_at.desc()).first()

    @staticmethod
    def update(db: Session, urine_id: int, urine_data: dict) -> Optional[UrineAnalysis]:
        """به‌روزرسانی تحلیل ادرار"""
        db_urine = UrineAnalysisOps.get_by_id(db, urine_id)
        if db_urine:
            for key, value in urine_data.items():
                if value is not None:
                    setattr(db_urine, key, value)
            db.commit()
            db.refresh(db_urine)
        return db_urine


# ============ زبان ============
class TongueCoatingOps:
    @staticmethod
    def create(db: Session, tongue_data: TongueCoatingCreate) -> TongueCoating:
        """ایجاد تحلیل زبان جدید"""
        db_tongue = TongueCoating(**tongue_data.dict())
        db.add(db_tongue)
        db.commit()
        db.refresh(db_tongue)
        return db_tongue

    @staticmethod
    def get_by_id(db: Session, tongue_id: int) -> Optional[TongueCoating]:
        """دریافت تحلیل زبان با ID"""
        return db.query(TongueCoating).filter(TongueCoating.id == tongue_id).first()

    @staticmethod
    def get_by_patient(db: Session, patient_id: int) -> List[TongueCoating]:
        """دریافت تمام تحلیل‌های زبان برای بیمار"""
        return db.query(TongueCoating).filter(TongueCoating.patient_id == patient_id).order_by(
            TongueCoating.recorded_at.desc()
        ).all()

    @staticmethod
    def get_latest_by_patient(db: Session, patient_id: int) -> Optional[TongueCoating]:
        """دریافت آخرین تحلیل زبان"""
        return db.query(TongueCoating).filter(
            TongueCoating.patient_id == patient_id
        ).order_by(TongueCoating.recorded_at.desc()).first()

    @staticmethod
    def update(db: Session, tongue_id: int, tongue_data: dict) -> Optional[TongueCoating]:
        """به‌روزرسانی تحلیل زبان"""
        db_tongue = TongueCoatingOps.get_by_id(db, tongue_id)
        if db_tongue:
            for key, value in tongue_data.items():
                if value is not None:
                    setattr(db_tongue, key, value)
            db.commit()
            db.refresh(db_tongue)
        return db_tongue


# ============ یافته‌های تشخیصی ============
class DiagnosticFindingOps:
    @staticmethod
    def create(db: Session, finding_data: DiagnosticFindingCreate) -> DiagnosticFinding:
        """ایجاد یافته تشخیصی جدید"""
        db_finding = DiagnosticFinding(**finding_data.dict())
        db.add(db_finding)
        db.commit()
        db.refresh(db_finding)
        return db_finding

    @staticmethod
    def get_by_id(db: Session, finding_id: int) -> Optional[DiagnosticFinding]:
        """دریافت یافته تشخیصی با ID"""
        return db.query(DiagnosticFinding).filter(DiagnosticFinding.id == finding_id).first()

    @staticmethod
    def get_by_patient(db: Session, patient_id: int) -> List[DiagnosticFinding]:
        """دریافت تمام یافته‌های تشخیصی برای بیمار"""
        return db.query(DiagnosticFinding).filter(DiagnosticFinding.patient_id == patient_id).order_by(
            DiagnosticFinding.created_at.desc()
        ).all()

    @staticmethod
    def get_latest_by_patient(db: Session, patient_id: int) -> Optional[DiagnosticFinding]:
        """دریافت آخرین یافته تشخیصی"""
        return db.query(DiagnosticFinding).filter(
            DiagnosticFinding.patient_id == patient_id
        ).order_by(DiagnosticFinding.created_at.desc()).first()

    @staticmethod
    def update(db: Session, finding_id: int, finding_data: dict) -> Optional[DiagnosticFinding]:
        """به‌روزرسانی یافته تشخیصی"""
        db_finding = DiagnosticFindingOps.get_by_id(db, finding_id)
        if db_finding:
            for key, value in finding_data.items():
                if value is not None:
                    setattr(db_finding, key, value)
            db.commit()
            db.refresh(db_finding)
        return db_finding

    @staticmethod
    def get_comprehensive_report(db: Session, patient_id: int) -> dict:
        """دریافت گزارش جامع تشخیصی برای بیمار"""
        latest_pulse = PulseAnalysisOps.get_latest_by_patient(db, patient_id)
        latest_urine = UrineAnalysisOps.get_latest_by_patient(db, patient_id)
        latest_tongue = TongueCoatingOps.get_latest_by_patient(db, patient_id)
        latest_finding = DiagnosticFindingOps.get_latest_by_patient(db, patient_id)

        return {
            "latest_pulse": latest_pulse,
            "latest_urine": latest_urine,
            "latest_tongue": latest_tongue,
            "latest_finding": latest_finding,
            "all_findings": DiagnosticFindingOps.get_by_patient(db, patient_id)
        }
