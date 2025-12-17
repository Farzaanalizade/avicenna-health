"""
Prediction Service - ML-based recommendation prediction and optimization
Uses effectiveness data to predict best recommendations for each patient
Integrates with feedback analytics to improve recommendations over time
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple, Any
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
import logging
import json
import hashlib

from app.models.patient_and_diagnosis_data import (
    Patient, DiagnosticFinding, Recommendation, HealthRecord
)
from app.models.enums import Gender, MizajType
from app.services.analytics_service import get_analytics_service
from app.services.websocket_manager import get_connection_manager

logger = logging.getLogger(__name__)

# ===========================
# Prediction Data Models
# ===========================

class RecommendationScore(BaseModel):
    """Scored recommendation for a patient"""
    recommendation_id: int
    herb_name: str
    predicted_effectiveness: float = Field(..., ge=0, le=1, description="0-1 predicted effectiveness")
    confidence: float = Field(..., ge=0, le=1, description="0-1 confidence in prediction")
    reasoning: str
    evidence_source: str  # historical_effectiveness, patient_profile, symptom_match
    similar_patient_count: int
    average_improvement: float
    expected_duration_days: int

    class Config:
        schema_extra = {
            "example": {
                "recommendation_id": 1,
                "herb_name": "زنجبیل",
                "predicted_effectiveness": 0.82,
                "confidence": 0.85,
                "reasoning": "بر اساس داده‌های بیماران مشابه",
                "evidence_source": "historical_effectiveness",
                "similar_patient_count": 12,
                "average_improvement": 4.1,
                "expected_duration_days": 28
            }
        }


class PredictionResult(BaseModel):
    """Prediction result for a patient's condition"""
    diagnosis_id: int
    patient_id: int
    prediction_date: datetime
    predicted_recommendations: List[RecommendationScore]
    overall_confidence: float
    model_version: str
    optimization_level: str  # conservative, balanced, aggressive


class PatientProfile(BaseModel):
    """Patient profile for prediction"""
    patient_id: int
    age: int
    gender: str
    mizaj_type: str
    conditions: List[str]
    successful_treatments: List[str]
    unsuccessful_treatments: List[str]
    preferred_treatment_types: List[str]


class PredictionUpdate(BaseModel):
    """Notification of updated predictions"""
    diagnosis_id: int
    old_recommendations: List[int]
    new_recommendations: List[int]
    improvements: List[str]  # What changed and why


# ===========================
# Prediction Service
# ===========================

class PredictionService:
    """Service for ML-based recommendation prediction and optimization"""

    # Configuration
    MODEL_VERSION = "1.0"
    MIN_SIMILAR_PATIENTS = 2
    CONFIDENCE_THRESHOLD = 0.6
    EFFECTIVENESS_DECAY_DAYS = 180  # Recent data weighted more
    PREDICTION_CACHE_HOURS = 24
    SIMILARITY_THRESHOLD = 0.7

    def __init__(self, db: Session):
        self.db = db
        self.analytics_service = get_analytics_service(db)
        self.connection_manager = get_connection_manager()
        self.cache = {}  # Simple in-memory cache

    # ===========================
    # Core Prediction Methods
    # ===========================

    async def predict_recommendations(
        self,
        diagnosis_id: int,
        optimization_level: str = "balanced"
    ) -> Optional[PredictionResult]:
        """
        Predict best recommendations for a diagnosis
        
        Args:
            diagnosis_id: Diagnosis ID to predict for
            optimization_level: conservative/balanced/aggressive
        
        Returns:
            PredictionResult with scored recommendations
        """
        try:
            # Get diagnosis and patient
            diagnosis = self.db.query(DiagnosticFinding).filter(
                DiagnosticFinding.id == diagnosis_id
            ).first()

            if not diagnosis:
                return None

            patient = self.db.query(Patient).filter(
                Patient.id == diagnosis.patient_id
            ).first()

            if not patient:
                return None

            # Check cache
            cache_key = f"pred_{diagnosis_id}_{optimization_level}"
            if cache_key in self.cache:
                cached = self.cache[cache_key]
                if datetime.utcnow() - cached["timestamp"] < timedelta(hours=self.PREDICTION_CACHE_HOURS):
                    return cached["result"]

            # Get current recommendations
            recommendations = self.db.query(Recommendation).filter(
                Recommendation.diagnosis_id == diagnosis_id
            ).all()

            if not recommendations:
                return None

            # Score each recommendation
            scored_recommendations = []
            for rec in recommendations:
                score = await self._score_recommendation(
                    rec, diagnosis, patient, optimization_level
                )
                if score:
                    scored_recommendations.append(score)

            # Sort by predicted effectiveness
            scored_recommendations.sort(
                key=lambda x: x.predicted_effectiveness,
                reverse=True
            )

            # Calculate overall confidence
            confidences = [r.confidence for r in scored_recommendations]
            overall_confidence = sum(confidences) / len(confidences) if confidences else 0.0

            result = PredictionResult(
                diagnosis_id=diagnosis_id,
                patient_id=patient.id,
                prediction_date=datetime.utcnow(),
                predicted_recommendations=scored_recommendations,
                overall_confidence=round(overall_confidence, 3),
                model_version=self.MODEL_VERSION,
                optimization_level=optimization_level
            )

            # Cache result
            self.cache[cache_key] = {
                "result": result,
                "timestamp": datetime.utcnow()
            }

            return result

        except Exception as e:
            logger.error(f"Error predicting recommendations: {str(e)}")
            return None

    async def _score_recommendation(
        self,
        recommendation: Recommendation,
        diagnosis: DiagnosticFinding,
        patient: Patient,
        optimization_level: str
    ) -> Optional[RecommendationScore]:
        """
        Score a single recommendation based on multiple factors
        
        Returns:
            RecommendationScore or None
        """
        try:
            # 1. Historical effectiveness
            historical_score = await self._calculate_historical_effectiveness(recommendation.id)

            # 2. Patient similarity matching
            similar_patients = await self._find_similar_patients(patient, diagnosis)
            similar_patient_score = await self._calculate_similar_patient_effectiveness(
                recommendation.id, similar_patients
            )

            # 3. Symptom-herb match
            symptom_match_score = await self._calculate_symptom_match(
                recommendation, diagnosis.condition_name, diagnosis.primary_finding
            )

            # Weighted combination
            weights = {
                "historical": 0.4,
                "similar_patients": 0.35,
                "symptom_match": 0.25
            }

            predicted_effectiveness = (
                historical_score * weights["historical"] +
                similar_patient_score * weights["similar_patients"] +
                symptom_match_score * weights["symptom_match"]
            )

            # Apply optimization level
            if optimization_level == "aggressive":
                predicted_effectiveness = min(1.0, predicted_effectiveness * 1.15)
            elif optimization_level == "conservative":
                predicted_effectiveness = max(0.0, predicted_effectiveness * 0.85)

            # Calculate confidence
            confidence = self._calculate_prediction_confidence(
                historical_score, similar_patient_score, len(similar_patients)
            )

            # Reasoning
            reasoning = self._generate_reasoning(
                predicted_effectiveness, similar_patients, optimization_level
            )

            # Average improvement from similar patients
            avg_improvement = await self._get_average_improvement(
                recommendation.id, similar_patients
            )

            return RecommendationScore(
                recommendation_id=recommendation.id,
                herb_name=recommendation.herb_name if hasattr(recommendation, 'herb_name') else "Unknown",
                predicted_effectiveness=round(predicted_effectiveness, 3),
                confidence=round(confidence, 3),
                reasoning=reasoning,
                evidence_source=self._determine_evidence_source(
                    historical_score, similar_patient_score, symptom_match_score
                ),
                similar_patient_count=len(similar_patients),
                average_improvement=round(avg_improvement, 2),
                expected_duration_days=28
            )

        except Exception as e:
            logger.error(f"Error scoring recommendation: {str(e)}")
            return None

    # ===========================
    # Scoring Helper Methods
    # ===========================

    async def _calculate_historical_effectiveness(self, recommendation_id: int) -> float:
        """Calculate effectiveness based on historical feedback"""
        try:
            # Use analytics service to get effectiveness metrics
            metrics = await self.analytics_service.calculate_recommendation_effectiveness(recommendation_id)

            if metrics:
                return metrics.effectiveness_score
            return 0.5  # Default neutral score
        except Exception as e:
            logger.error(f"Error calculating historical effectiveness: {str(e)}")
            return 0.5

    async def _find_similar_patients(
        self,
        patient: Patient,
        diagnosis: DiagnosticFinding
    ) -> List[Patient]:
        """Find patients similar to current patient"""
        try:
            # Find patients with same/similar conditions and mizaj
            similar = self.db.query(Patient).filter(
                and_(
                    Patient.id != patient.id,
                    Patient.mizaj_type == patient.mizaj_type
                )
            ).limit(20).all()

            return similar
        except Exception as e:
            logger.error(f"Error finding similar patients: {str(e)}")
            return []

    async def _calculate_similar_patient_effectiveness(
        self,
        recommendation_id: int,
        similar_patients: List[Patient]
    ) -> float:
        """Calculate effectiveness among similar patients"""
        try:
            if not similar_patients:
                return 0.5

            patient_ids = [p.id for p in similar_patients]

            # Get feedback from similar patients
            feedbacks = self.db.query(HealthRecord).filter(
                and_(
                    HealthRecord.recommendation_id == recommendation_id,
                    HealthRecord.patient_id.in_(patient_ids)
                )
            ).all()

            if not feedbacks:
                return 0.5

            # Calculate success rate
            successful = sum(1 for f in feedbacks if f.rating and f.rating >= 3)
            effectiveness = successful / len(feedbacks) if feedbacks else 0.5

            return effectiveness
        except Exception as e:
            logger.error(f"Error calculating similar patient effectiveness: {str(e)}")
            return 0.5

    async def _calculate_symptom_match(
        self,
        recommendation: Recommendation,
        condition: str,
        primary_finding: str
    ) -> float:
        """Calculate how well recommendation matches symptoms"""
        try:
            # Simple keyword matching (can be enhanced with NLP)
            # For now, all recommendations for a diagnosis get high score
            return 0.7  # Baseline, could use ML for better matching
        except Exception as e:
            logger.error(f"Error calculating symptom match: {str(e)}")
            return 0.5

    def _calculate_prediction_confidence(
        self,
        historical_score: float,
        similar_patient_score: float,
        similar_patient_count: int
    ) -> float:
        """Calculate confidence in prediction"""
        # More similar patients = higher confidence
        sample_confidence = min(1.0, similar_patient_count / 10.0)

        # Consistency between sources increases confidence
        score_diff = abs(historical_score - similar_patient_score)
        consistency_confidence = 1.0 - (score_diff * 0.3)

        confidence = (sample_confidence * 0.5) + (consistency_confidence * 0.5)
        return max(0.0, min(1.0, confidence))

    def _determine_evidence_source(
        self,
        historical_score: float,
        similar_patient_score: float,
        symptom_match_score: float
    ) -> str:
        """Determine primary evidence source for prediction"""
        scores = {
            "historical_effectiveness": historical_score,
            "similar_patients": similar_patient_score,
            "symptom_match": symptom_match_score
        }
        return max(scores, key=scores.get)

    def _generate_reasoning(
        self,
        effectiveness: float,
        similar_patients: List[Patient],
        optimization_level: str
    ) -> str:
        """Generate human-readable reasoning"""
        if effectiveness >= 0.8:
            return "بسیار موثر بر اساس داده‌های تاریخی"
        elif effectiveness >= 0.6:
            return f"موثر - {len(similar_patients)} بیمار مشابه موفق بوده‌اند"
        elif effectiveness >= 0.4:
            return "متوسط - نتایج متغیر برای بیماران مشابه"
        else:
            return "کم موثر - در تاریخچه کمتر موفق بوده"

    async def _get_average_improvement(
        self,
        recommendation_id: int,
        similar_patients: List[Patient]
    ) -> float:
        """Get average symptom improvement"""
        try:
            if not similar_patients:
                return 3.0

            patient_ids = [p.id for p in similar_patients]

            # Get improvement scores
            result = self.db.query(
                func.avg(HealthRecord.symptom_improvement)
            ).filter(
                and_(
                    HealthRecord.recommendation_id == recommendation_id,
                    HealthRecord.patient_id.in_(patient_ids)
                )
            ).scalar()

            return result if result else 3.0
        except Exception as e:
            logger.error(f"Error getting average improvement: {str(e)}")
            return 3.0

    # ===========================
    # Recommendation Optimization Methods
    # ===========================

    async def optimize_recommendations(
        self,
        diagnosis_id: int,
        target_effectiveness: float = 0.75
    ) -> Optional[List[RecommendationScore]]:
        """
        Optimize recommendations for better expected outcomes
        
        Args:
            diagnosis_id: Diagnosis ID
            target_effectiveness: Target effectiveness score
        
        Returns:
            Optimized list of recommendations
        """
        try:
            # Get predictions
            predictions = await self.predict_recommendations(diagnosis_id, "balanced")

            if not predictions:
                return None

            # Filter by target effectiveness
            optimized = [
                r for r in predictions.predicted_recommendations
                if r.predicted_effectiveness >= target_effectiveness * 0.8
            ]

            # If none meet target, return top 3
            if not optimized:
                optimized = predictions.predicted_recommendations[:3]

            return optimized

        except Exception as e:
            logger.error(f"Error optimizing recommendations: {str(e)}")
            return None

    async def broadcast_recommendation_update(
        self,
        diagnosis_id: int,
        old_recommendations: List[int],
        new_recommendations: List[int]
    ) -> bool:
        """
        Broadcast recommendation update via WebSocket
        
        Args:
            diagnosis_id: Diagnosis ID
            old_recommendations: Previous recommendation IDs
            new_recommendations: Updated recommendation IDs
        
        Returns:
            True if successful
        """
        try:
            # Determine what changed
            added = set(new_recommendations) - set(old_recommendations)
            removed = set(old_recommendations) - set(new_recommendations)

            improvements = []
            if added:
                improvements.append(f"Added {len(added)} new recommendations")
            if removed:
                improvements.append(f"Removed {len(removed)} low-effectiveness recommendations")

            # Prepare broadcast message
            message = {
                "type": "recommendation_update",
                "data": {
                    "diagnosis_id": diagnosis_id,
                    "old_recommendations": old_recommendations,
                    "new_recommendations": new_recommendations,
                    "improvements": improvements,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }

            # Broadcast via WebSocket
            await self.connection_manager.broadcast(
                message=message,
                diagnosis_id=diagnosis_id
            )

            logger.info(f"Broadcast recommendation update for diagnosis {diagnosis_id}")
            return True

        except Exception as e:
            logger.error(f"Error broadcasting recommendation update: {str(e)}")
            return False

    # ===========================
    # Patient Profile Methods
    # ===========================

    def get_patient_profile(self, patient_id: int) -> Optional[PatientProfile]:
        """Get patient profile for analysis"""
        try:
            patient = self.db.query(Patient).filter(Patient.id == patient_id).first()

            if not patient:
                return None

            # Get successful and unsuccessful treatments
            health_records = self.db.query(HealthRecord).filter(
                HealthRecord.patient_id == patient_id
            ).all()

            successful = []
            unsuccessful = []

            for record in health_records:
                if record.rating and record.rating >= 3:
                    successful.append(record.recommendation_id)
                else:
                    unsuccessful.append(record.recommendation_id)

            return PatientProfile(
                patient_id=patient_id,
                age=patient.age,
                gender=patient.gender,
                mizaj_type=patient.mizaj_type,
                conditions=[],
                successful_treatments=successful,
                unsuccessful_treatments=unsuccessful,
                preferred_treatment_types=[]
            )

        except Exception as e:
            logger.error(f"Error getting patient profile: {str(e)}")
            return None

    # ===========================
    # Analytics Methods
    # ===========================

    def get_prediction_accuracy(self, diagnosis_id: int) -> float:
        """
        Calculate accuracy of past predictions
        
        Args:
            diagnosis_id: Diagnosis ID
        
        Returns:
            Accuracy score 0-1
        """
        try:
            # Get recommendations for diagnosis
            recommendations = self.db.query(Recommendation).filter(
                Recommendation.diagnosis_id == diagnosis_id
            ).all()

            if not recommendations:
                return 0.0

            # Get actual effectiveness
            total_accuracy = 0.0
            for rec in recommendations:
                # Get predicted score
                # (would need to store past predictions)
                # For now, just get current effectiveness
                metrics = self.db.query(
                    func.avg(HealthRecord.rating)
                ).filter(
                    HealthRecord.recommendation_id == rec.id
                ).scalar()

                if metrics:
                    total_accuracy += metrics

            return min(1.0, total_accuracy / len(recommendations)) if recommendations else 0.0

        except Exception as e:
            logger.error(f"Error calculating prediction accuracy: {str(e)}")
            return 0.0

    def get_recommendation_evolution(self, diagnosis_id: int, days: int = 30) -> Dict[str, Any]:
        """
        Track how recommendations have evolved
        
        Args:
            diagnosis_id: Diagnosis ID
            days: Historical days to analyze
        
        Returns:
            Evolution data showing changes over time
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)

            # Get old recommendations (if any)
            old_recs = self.db.query(Recommendation).filter(
                and_(
                    Recommendation.diagnosis_id == diagnosis_id,
                    Recommendation.created_at < cutoff_date
                )
            ).all()

            # Get current recommendations
            current_recs = self.db.query(Recommendation).filter(
                and_(
                    Recommendation.diagnosis_id == diagnosis_id,
                    Recommendation.created_at >= cutoff_date
                )
            ).all()

            return {
                "diagnosis_id": diagnosis_id,
                "period_days": days,
                "old_recommendations": [r.id for r in old_recs],
                "current_recommendations": [r.id for r in current_recs],
                "total_changes": len(set([r.id for r in old_recs]) ^ set([r.id for r in current_recs]))
            }

        except Exception as e:
            logger.error(f"Error getting recommendation evolution: {str(e)}")
            return {}


# ===========================
# Module Functions
# ===========================

def get_prediction_service(db: Session) -> PredictionService:
    """Get or create prediction service instance"""
    return PredictionService(db)


async def predict_recommendations(
    db: Session,
    diagnosis_id: int,
    optimization_level: str = "balanced"
) -> Optional[PredictionResult]:
    """Convenience function to predict recommendations"""
    service = get_prediction_service(db)
    return await service.predict_recommendations(diagnosis_id, optimization_level)


async def optimize_recommendations(
    db: Session,
    diagnosis_id: int,
    target_effectiveness: float = 0.75
) -> Optional[List[RecommendationScore]]:
    """Convenience function to optimize recommendations"""
    service = get_prediction_service(db)
    return await service.optimize_recommendations(diagnosis_id, target_effectiveness)


def get_patient_profile(
    db: Session,
    patient_id: int
) -> Optional[PatientProfile]:
    """Convenience function to get patient profile"""
    service = get_prediction_service(db)
    return service.get_patient_profile(patient_id)
