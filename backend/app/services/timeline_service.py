"""
Timeline Service for Patient Health Journey
Provides diagnosis history, treatment progress, and evolution tracking
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class TimelineService:
    """Patient health timeline and history service"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ===========================
    # Timeline View
    # ===========================
    
    def get_patient_timeline(self, patient_id: int) -> List[Dict[str, Any]]:
        """Get complete patient health timeline"""
        from app.models.patient_and_diagnosis_data import DiagnosticFinding, HealthRecord
        
        diagnoses = self.db.query(DiagnosticFinding).filter(
            DiagnosticFinding.patient_id == patient_id
        ).order_by(desc(DiagnosticFinding.created_at)).all()
        
        timeline_events = []
        
        for diagnosis in diagnoses:
            # Get feedback for this diagnosis
            feedbacks = self.db.query(HealthRecord).filter(
                HealthRecord.diagnosis_id == diagnosis.id
            ).order_by(desc(HealthRecord.created_at)).all()
            
            event = {
                "id": diagnosis.id,
                "type": "diagnosis",
                "condition": diagnosis.condition,
                "severity": diagnosis.severity,
                "duration_days": diagnosis.duration_days,
                "status": diagnosis.status if hasattr(diagnosis, 'status') else "active",
                "date": diagnosis.created_at.isoformat(),
                "feedback_count": len(feedbacks),
                "average_improvement": sum(f.symptom_improvement for f in feedbacks) / len(feedbacks) if feedbacks else 0,
            }
            timeline_events.append(event)
        
        return sorted(timeline_events, key=lambda x: x['date'], reverse=True)
    
    # ===========================
    # Diagnosis History
    # ===========================
    
    def get_diagnosis_history(self, patient_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get patient's diagnosis history"""
        from app.models.patient_and_diagnosis_data import DiagnosticFinding
        
        diagnoses = self.db.query(DiagnosticFinding).filter(
            DiagnosticFinding.patient_id == patient_id
        ).order_by(desc(DiagnosticFinding.created_at)).limit(limit).all()
        
        return [
            {
                "id": d.id,
                "condition": d.condition,
                "severity": d.severity,
                "duration_days": d.duration_days,
                "mizaj_imbalance": d.mizaj_imbalance,
                "created_at": d.created_at.isoformat(),
                "days_ago": (datetime.utcnow() - d.created_at).days,
            }
            for d in diagnoses
        ]
    
    # ===========================
    # Treatment Progress
    # ===========================
    
    def get_treatment_progress(self, diagnosis_id: int) -> Dict[str, Any]:
        """Get treatment progress for a diagnosis"""
        from app.models.patient_and_diagnosis_data import (
            DiagnosticFinding, HealthRecord, Recommendation
        )
        
        diagnosis = self.db.query(DiagnosticFinding).filter(
            DiagnosticFinding.id == diagnosis_id
        ).first()
        
        if not diagnosis:
            return {}
        
        # Get all feedbacks for this diagnosis
        feedbacks = self.db.query(HealthRecord).filter(
            HealthRecord.diagnosis_id == diagnosis_id
        ).order_by(HealthRecord.created_at).all()
        
        # Calculate progress metrics
        if feedbacks:
            avg_rating = sum(f.rating for f in feedbacks) / len(feedbacks)
            avg_improvement = sum(f.symptom_improvement for f in feedbacks) / len(feedbacks)
            compliance = sum(f.compliance_score for f in feedbacks) / len(feedbacks)
        else:
            avg_rating = avg_improvement = compliance = 0.0
        
        # Get recommendations
        recommendations = self.db.query(Recommendation).limit(5).all()
        
        return {
            "diagnosis_id": diagnosis_id,
            "condition": diagnosis.condition,
            "start_date": diagnosis.created_at.isoformat(),
            "duration_days": diagnosis.duration_days,
            "feedback_count": len(feedbacks),
            "average_rating": avg_rating,
            "average_improvement": avg_improvement,
            "compliance_rate": compliance,
            "recommendations_count": len(recommendations),
            "status": "improving" if avg_improvement > 2 else "stable" if avg_improvement > 1 else "declining",
        }
    
    # ===========================
    # Symptom Evolution
    # ===========================
    
    def get_symptom_evolution(self, diagnosis_id: int) -> List[Dict[str, Any]]:
        """Track symptom improvement over time"""
        from app.models.patient_and_diagnosis_data import HealthRecord
        
        feedbacks = self.db.query(HealthRecord).filter(
            HealthRecord.diagnosis_id == diagnosis_id
        ).order_by(HealthRecord.created_at).all()
        
        evolution = []
        for i, feedback in enumerate(feedbacks):
            evolution.append({
                "day": i + 1,
                "date": feedback.created_at.isoformat(),
                "rating": feedback.rating,
                "symptom_improvement": feedback.symptom_improvement,
                "compliance": feedback.compliance_score,
            })
        
        return evolution
    
    # ===========================
    # Patient Comparison
    # ===========================
    
    def find_similar_patients(
        self,
        patient_id: int,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Find similar patients for comparison"""
        from app.models.patient_and_diagnosis_data import Patient
        
        target_patient = self.db.query(Patient).filter(
            Patient.id == patient_id
        ).first()
        
        if not target_patient:
            return []
        
        # Find patients with same mizaj type and similar age
        similar = self.db.query(Patient).filter(
            and_(
                Patient.id != patient_id,
                Patient.mizaj_type == target_patient.mizaj_type,
            )
        ).limit(limit).all()
        
        return [
            {
                "id": p.id,
                "age": p.age,
                "gender": p.gender,
                "mizaj_type": p.mizaj_type,
                "age_diff": abs(p.age - target_patient.age),
            }
            for p in similar
        ]
    
    def compare_patient_outcomes(
        self,
        patient_id_1: int,
        patient_id_2: int,
    ) -> Dict[str, Any]:
        """Compare health outcomes between two patients"""
        from app.models.patient_and_diagnosis_data import (
            Patient, DiagnosticFinding, HealthRecord
        )
        
        # Get patients
        p1 = self.db.query(Patient).filter(Patient.id == patient_id_1).first()
        p2 = self.db.query(Patient).filter(Patient.id == patient_id_2).first()
        
        if not p1 or not p2:
            return {}
        
        # Get diagnosis counts
        diag1 = self.db.query(func.count(DiagnosticFinding.id)).filter(
            DiagnosticFinding.patient_id == patient_id_1
        ).scalar() or 0
        
        diag2 = self.db.query(func.count(DiagnosticFinding.id)).filter(
            DiagnosticFinding.patient_id == patient_id_2
        ).scalar() or 0
        
        # Get average feedback ratings
        avg_rating1 = self.db.query(func.avg(HealthRecord.rating)).filter(
            HealthRecord.diagnosis_id.in_(
                self.db.query(DiagnosticFinding.id).filter(
                    DiagnosticFinding.patient_id == patient_id_1
                )
            )
        ).scalar() or 0.0
        
        avg_rating2 = self.db.query(func.avg(HealthRecord.rating)).filter(
            HealthRecord.diagnosis_id.in_(
                self.db.query(DiagnosticFinding.id).filter(
                    DiagnosticFinding.patient_id == patient_id_2
                )
            )
        ).scalar() or 0.0
        
        return {
            "patient_1": {
                "id": patient_id_1,
                "age": p1.age,
                "mizaj_type": p1.mizaj_type,
                "diagnoses": diag1,
                "avg_rating": float(avg_rating1),
            },
            "patient_2": {
                "id": patient_id_2,
                "age": p2.age,
                "mizaj_type": p2.mizaj_type,
                "diagnoses": diag2,
                "avg_rating": float(avg_rating2),
            },
        }


from sqlalchemy import and_

def get_timeline_service(db: Session) -> TimelineService:
    """Get timeline service instance"""
    return TimelineService(db)
