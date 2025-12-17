"""
Feedback Service - User feedback collection and management
Handles rating collection, comment processing, effectiveness scoring
Integrates with analytics service for real-time metric updates
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
import logging

from app.models.patient_and_diagnosis_data import (
    Patient, DiagnosticFinding, Recommendation, HealthRecord
)
from app.models.enums import Gender, MizajType
from app.services.analytics_service import get_analytics_service, AnalyticsService

logger = logging.getLogger(__name__)

# ===========================
# Feedback Data Models
# ===========================

class FeedbackRating(BaseModel):
    """User feedback rating submission"""
    recommendation_id: int
    diagnosis_id: int
    rating: int = Field(..., ge=1, le=5, description="1-5 effectiveness rating")
    symptom_improvement: int = Field(..., ge=1, le=5, description="1-5 symptom improvement score")
    comment: Optional[str] = Field(None, max_length=500, description="Optional feedback comment")
    side_effects: Optional[str] = Field(None, max_length=500, description="Any side effects reported")
    compliance_score: Optional[int] = Field(None, ge=1, le=5, description="How well user followed recommendation")

    class Config:
        schema_extra = {
            "example": {
                "recommendation_id": 1,
                "diagnosis_id": 5,
                "rating": 4,
                "symptom_improvement": 4,
                "comment": "بهتری قابل توجهی در علائم احساس کردم",
                "side_effects": None,
                "compliance_score": 5
            }
        }


class FeedbackResponse(BaseModel):
    """Feedback response data"""
    id: int
    recommendation_id: int
    diagnosis_id: int
    patient_id: int
    rating: int
    symptom_improvement: int
    comment: Optional[str]
    side_effects: Optional[str]
    compliance_score: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class FeedbackSummary(BaseModel):
    """Summary of feedback for a recommendation"""
    recommendation_id: int
    total_feedbacks: int
    average_rating: float
    average_improvement: float
    average_compliance: float
    latest_comment: Optional[str]
    positive_feedback_percentage: float
    side_effects_reported: List[str]
    last_updated: datetime


class FeedbackTrend(BaseModel):
    """Feedback trend analysis"""
    recommendation_id: int
    recent_average: float  # Last 30 days
    older_average: float   # 30-90 days
    trend_direction: str   # improving, stable, declining
    confidence: float      # 0.0-1.0


# ===========================
# Feedback Service
# ===========================

class FeedbackService:
    """Service for managing user feedback on recommendations"""

    # Configuration
    RECENT_WINDOW_DAYS = 30
    OLDER_WINDOW_DAYS = 90
    MIN_FEEDBACK_FOR_TREND = 3
    POSITIVE_THRESHOLD = 3  # Rating >= 3 is positive
    ANALYTICS_UPDATE_INTERVAL = 5  # Update analytics every 5 feedbacks

    def __init__(self, db: Session):
        self.db = db
        self.analytics_service = get_analytics_service(db)
        self.feedback_counter = 0

    # ===========================
    # Feedback Collection Methods
    # ===========================

    async def submit_feedback(
        self,
        patient_id: int,
        feedback_data: FeedbackRating
    ) -> Optional[FeedbackResponse]:
        """
        Submit user feedback for a recommendation
        
        Args:
            patient_id: Patient ID submitting feedback
            feedback_data: FeedbackRating with rating, comments, etc.
        
        Returns:
            FeedbackResponse with created feedback data, or None on error
        """
        try:
            # Verify patient owns this diagnosis
            diagnosis = self.db.query(DiagnosticFinding).filter(
                and_(
                    DiagnosticFinding.id == feedback_data.diagnosis_id,
                    DiagnosticFinding.patient_id == patient_id
                )
            ).first()

            if not diagnosis:
                logger.warning(f"Patient {patient_id} attempted to submit feedback for unauthorized diagnosis")
                return None

            # Verify recommendation exists in diagnosis
            recommendation = self.db.query(Recommendation).filter(
                Recommendation.id == feedback_data.recommendation_id
            ).first()

            if not recommendation:
                logger.warning(f"Recommendation {feedback_data.recommendation_id} not found")
                return None

            # Create or update HealthRecord with feedback
            health_record = self.db.query(HealthRecord).filter(
                and_(
                    HealthRecord.patient_id == patient_id,
                    HealthRecord.recommendation_id == feedback_data.recommendation_id
                )
            ).first()

            if health_record:
                # Update existing record
                health_record.symptom_improvement = feedback_data.symptom_improvement
                health_record.rating = feedback_data.rating
                health_record.comment = feedback_data.comment
                health_record.side_effects = feedback_data.side_effects
                health_record.compliance_score = feedback_data.compliance_score
                health_record.updated_at = datetime.utcnow()
            else:
                # Create new record
                health_record = HealthRecord(
                    patient_id=patient_id,
                    recommendation_id=feedback_data.recommendation_id,
                    diagnosis_id=feedback_data.diagnosis_id,
                    symptom_improvement=feedback_data.symptom_improvement,
                    rating=feedback_data.rating,
                    comment=feedback_data.comment,
                    side_effects=feedback_data.side_effects,
                    compliance_score=feedback_data.compliance_score,
                    created_at=datetime.utcnow()
                )
                self.db.add(health_record)

            self.db.commit()

            logger.info(
                f"Feedback submitted - Patient: {patient_id}, "
                f"Recommendation: {feedback_data.recommendation_id}, "
                f"Rating: {feedback_data.rating}/5"
            )

            # Trigger analytics update
            self.feedback_counter += 1
            if self.feedback_counter % self.ANALYTICS_UPDATE_INTERVAL == 0:
                await self._trigger_analytics_update(
                    feedback_data.diagnosis_id,
                    feedback_data.recommendation_id
                )

            return FeedbackResponse.from_orm(health_record)

        except Exception as e:
            logger.error(f"Error submitting feedback: {str(e)}")
            self.db.rollback()
            return None

    async def update_feedback(
        self,
        patient_id: int,
        health_record_id: int,
        feedback_data: FeedbackRating
    ) -> Optional[FeedbackResponse]:
        """
        Update existing feedback submission
        
        Args:
            patient_id: Patient ID making the update
            health_record_id: ID of HealthRecord to update
            feedback_data: Updated feedback data
        
        Returns:
            Updated FeedbackResponse or None on error
        """
        try:
            health_record = self.db.query(HealthRecord).filter(
                and_(
                    HealthRecord.id == health_record_id,
                    HealthRecord.patient_id == patient_id
                )
            ).first()

            if not health_record:
                return None

            # Update fields
            health_record.rating = feedback_data.rating
            health_record.symptom_improvement = feedback_data.symptom_improvement
            health_record.comment = feedback_data.comment
            health_record.side_effects = feedback_data.side_effects
            health_record.compliance_score = feedback_data.compliance_score
            health_record.updated_at = datetime.utcnow()

            self.db.commit()

            logger.info(f"Feedback updated - Patient: {patient_id}, HealthRecord: {health_record_id}")

            # Trigger analytics update
            await self._trigger_analytics_update(
                health_record.diagnosis_id,
                health_record.recommendation_id
            )

            return FeedbackResponse.from_orm(health_record)

        except Exception as e:
            logger.error(f"Error updating feedback: {str(e)}")
            self.db.rollback()
            return None

    # ===========================
    # Feedback Retrieval Methods
    # ===========================

    def get_feedback_history(
        self,
        patient_id: int,
        diagnosis_id: Optional[int] = None,
        recommendation_id: Optional[int] = None,
        limit: int = 50
    ) -> List[FeedbackResponse]:
        """
        Get feedback history for patient
        
        Args:
            patient_id: Patient ID
            diagnosis_id: Optional filter by diagnosis
            recommendation_id: Optional filter by recommendation
            limit: Maximum results
        
        Returns:
            List of FeedbackResponse objects
        """
        try:
            query = self.db.query(HealthRecord).filter(
                HealthRecord.patient_id == patient_id
            )

            if diagnosis_id:
                query = query.filter(HealthRecord.diagnosis_id == diagnosis_id)

            if recommendation_id:
                query = query.filter(HealthRecord.recommendation_id == recommendation_id)

            feedbacks = query.order_by(desc(HealthRecord.created_at)).limit(limit).all()

            return [FeedbackResponse.from_orm(f) for f in feedbacks]

        except Exception as e:
            logger.error(f"Error retrieving feedback history: {str(e)}")
            return []

    def get_recommendation_feedback_summary(
        self,
        recommendation_id: int
    ) -> Optional[FeedbackSummary]:
        """
        Get summary statistics for a recommendation
        
        Args:
            recommendation_id: Recommendation ID
        
        Returns:
            FeedbackSummary with aggregated statistics or None
        """
        try:
            feedbacks = self.db.query(HealthRecord).filter(
                HealthRecord.recommendation_id == recommendation_id
            ).all()

            if not feedbacks:
                return None

            total = len(feedbacks)
            avg_rating = sum(f.rating for f in feedbacks if f.rating) / total if total > 0 else 0.0
            avg_improvement = sum(f.symptom_improvement for f in feedbacks if f.symptom_improvement) / total if total > 0 else 0.0
            
            compliance_scores = [f.compliance_score for f in feedbacks if f.compliance_score]
            avg_compliance = sum(compliance_scores) / len(compliance_scores) if compliance_scores else 0.0

            positive_count = sum(1 for f in feedbacks if f.rating and f.rating >= self.POSITIVE_THRESHOLD)
            positive_percentage = (positive_count / total * 100) if total > 0 else 0.0

            # Extract unique side effects
            side_effects = []
            for f in feedbacks:
                if f.side_effects:
                    effects = [e.strip() for e in f.side_effects.split(',')]
                    side_effects.extend(effects)
            side_effects = list(set(side_effects))

            latest_comment = None
            for f in sorted(feedbacks, key=lambda x: x.created_at, reverse=True):
                if f.comment:
                    latest_comment = f.comment
                    break

            return FeedbackSummary(
                recommendation_id=recommendation_id,
                total_feedbacks=total,
                average_rating=round(avg_rating, 2),
                average_improvement=round(avg_improvement, 2),
                average_compliance=round(avg_compliance, 2),
                latest_comment=latest_comment,
                positive_feedback_percentage=round(positive_percentage, 1),
                side_effects_reported=side_effects,
                last_updated=max(f.updated_at or f.created_at for f in feedbacks)
            )

        except Exception as e:
            logger.error(f"Error generating feedback summary: {str(e)}")
            return None

    def get_feedback_trend(
        self,
        recommendation_id: int
    ) -> Optional[FeedbackTrend]:
        """
        Analyze feedback trend for a recommendation
        
        Args:
            recommendation_id: Recommendation ID
        
        Returns:
            FeedbackTrend with trend analysis or None
        """
        try:
            now = datetime.utcnow()
            recent_cutoff = now - timedelta(days=self.RECENT_WINDOW_DAYS)
            older_cutoff = now - timedelta(days=self.OLDER_WINDOW_DAYS)

            # Recent feedback (last 30 days)
            recent_feedbacks = self.db.query(HealthRecord).filter(
                and_(
                    HealthRecord.recommendation_id == recommendation_id,
                    HealthRecord.created_at >= recent_cutoff
                )
            ).all()

            # Older feedback (30-90 days)
            older_feedbacks = self.db.query(HealthRecord).filter(
                and_(
                    HealthRecord.recommendation_id == recommendation_id,
                    HealthRecord.created_at >= older_cutoff,
                    HealthRecord.created_at < recent_cutoff
                )
            ).all()

            if len(recent_feedbacks) < self.MIN_FEEDBACK_FOR_TREND:
                return None

            recent_avg = sum(f.rating for f in recent_feedbacks if f.rating) / len(recent_feedbacks) if recent_feedbacks else 0.0
            older_avg = sum(f.rating for f in older_feedbacks if f.rating) / len(older_feedbacks) if older_feedbacks else 0.0

            # Determine trend
            if not older_feedbacks or older_avg == 0:
                trend_direction = "new"
                confidence = 0.5
            else:
                diff = recent_avg - older_avg
                if diff > 0.5:
                    trend_direction = "improving"
                    confidence = min(1.0, abs(diff) / 5.0)
                elif diff < -0.5:
                    trend_direction = "declining"
                    confidence = min(1.0, abs(diff) / 5.0)
                else:
                    trend_direction = "stable"
                    confidence = 0.7

            return FeedbackTrend(
                recommendation_id=recommendation_id,
                recent_average=round(recent_avg, 2),
                older_average=round(older_avg, 2),
                trend_direction=trend_direction,
                confidence=round(confidence, 2)
            )

        except Exception as e:
            logger.error(f"Error analyzing feedback trend: {str(e)}")
            return None

    def get_diagnosis_feedback_overview(
        self,
        diagnosis_id: int
    ) -> Dict[str, any]:
        """
        Get complete feedback overview for a diagnosis
        
        Args:
            diagnosis_id: Diagnosis ID
        
        Returns:
            Dict with summaries for all recommendations in diagnosis
        """
        try:
            diagnosis = self.db.query(DiagnosticFinding).filter(
                DiagnosticFinding.id == diagnosis_id
            ).first()

            if not diagnosis:
                return {}

            # Get all recommendations
            recommendations = self.db.query(Recommendation).filter(
                Recommendation.diagnosis_id == diagnosis_id
            ).all()

            overview = {
                "diagnosis_id": diagnosis_id,
                "total_recommendations": len(recommendations),
                "recommendations": []
            }

            for rec in recommendations:
                summary = self.get_recommendation_feedback_summary(rec.id)
                trend = self.get_feedback_trend(rec.id)

                overview["recommendations"].append({
                    "id": rec.id,
                    "herb_name": rec.herb_name if hasattr(rec, 'herb_name') else "Unknown",
                    "summary": summary.dict() if summary else None,
                    "trend": trend.dict() if trend else None
                })

            return overview

        except Exception as e:
            logger.error(f"Error generating diagnosis feedback overview: {str(e)}")
            return {}

    # ===========================
    # Internal Methods
    # ===========================

    async def _trigger_analytics_update(
        self,
        diagnosis_id: int,
        recommendation_id: int
    ) -> bool:
        """
        Trigger analytics recalculation and WebSocket broadcast
        
        Args:
            diagnosis_id: Diagnosis ID for broadcast context
            recommendation_id: Recommendation ID to calculate
        
        Returns:
            True if successful, False on error
        """
        try:
            # Trigger analytics calculation
            await self.analytics_service.broadcast_effectiveness_update(
                diagnosis_id,
                recommendation_id
            )
            return True
        except Exception as e:
            logger.error(f"Error triggering analytics update: {str(e)}")
            return False

    def _get_side_effects_list(self, feedback_records: List[HealthRecord]) -> List[str]:
        """Extract and deduplicate side effects from feedback"""
        side_effects = []
        for record in feedback_records:
            if record.side_effects:
                effects = [e.strip() for e in record.side_effects.split(',')]
                side_effects.extend(effects)
        return list(set(side_effects))


# ===========================
# Module Functions
# ===========================

def get_feedback_service(db: Session) -> FeedbackService:
    """Get or create feedback service instance"""
    return FeedbackService(db)


async def submit_recommendation_feedback(
    db: Session,
    patient_id: int,
    feedback: FeedbackRating
) -> Optional[FeedbackResponse]:
    """Convenience function to submit feedback"""
    service = get_feedback_service(db)
    return await service.submit_feedback(patient_id, feedback)


def get_recommendation_summary(
    db: Session,
    recommendation_id: int
) -> Optional[FeedbackSummary]:
    """Convenience function to get recommendation summary"""
    service = get_feedback_service(db)
    return service.get_recommendation_feedback_summary(recommendation_id)


def get_diagnosis_overview(
    db: Session,
    diagnosis_id: int
) -> Dict[str, any]:
    """Convenience function to get diagnosis overview"""
    service = get_feedback_service(db)
    return service.get_diagnosis_feedback_overview(diagnosis_id)
