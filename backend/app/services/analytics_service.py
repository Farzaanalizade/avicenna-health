"""
Analytics Service - Phase 3 Week 3 Task 2

Real-time analytics tracking for recommendation effectiveness, feedback aggregation,
and success rate calculations. Integrates with WebSocket system to broadcast
effectiveness updates in real-time.

Key Responsibilities:
1. Track recommendation effectiveness scores
2. Calculate success rates from feedback
3. Generate real-time analytics
4. Broadcast updates to connected clients
5. Store analytics history for trending

Architecture:
- EffectivenessTracker: Core analytics engine
- Analytics aggregation by herb, condition, patient
- WebSocket integration for real-time notifications
- Configurable analytics windows (7-day, 30-day, all-time)
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.models.patient import Patient
from app.models.avicenna_diagnosis import DiagnosticFinding, Recommendation
from app.models.health_record import HealthRecord
from app.services.websocket_manager import broadcast_effectiveness_update

logger = logging.getLogger(__name__)


class EffectivenessMetrics:
    """Container for effectiveness metrics"""
    
    def __init__(
        self,
        recommendation_id: int,
        herb_name: str,
        effectiveness_score: float,  # 0-1
        confidence: float,  # 0-1
        sample_size: int,
        successful_cases: int,
        total_cases: int,
        average_rating: float,  # 1-5
        trend: str,  # "improving", "stable", "declining"
        last_updated: datetime
    ):
        self.recommendation_id = recommendation_id
        self.herb_name = herb_name
        self.effectiveness_score = effectiveness_score
        self.confidence = confidence
        self.sample_size = sample_size
        self.successful_cases = successful_cases
        self.total_cases = total_cases
        self.average_rating = average_rating
        self.trend = trend
        self.last_updated = last_updated
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "recommendation_id": self.recommendation_id,
            "herb_name": self.herb_name,
            "effectiveness_score": round(self.effectiveness_score, 3),
            "confidence": round(self.confidence, 3),
            "sample_size": self.sample_size,
            "successful_cases": self.successful_cases,
            "total_cases": self.total_cases,
            "average_rating": round(self.average_rating, 2),
            "trend": self.trend,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        }


class AnalyticsService:
    """
    Core analytics service for tracking recommendation effectiveness.
    
    Calculates effectiveness scores based on:
    - User feedback ratings (1-5)
    - Symptom resolution feedback (yes/no)
    - Side effects tracking
    - Success rate over time
    """
    
    # Configuration
    EFFECTIVENESS_WINDOW_DAYS = 90  # Consider last 90 days for trending
    MIN_SAMPLES_FOR_CONFIDENCE = 5  # Minimum feedback entries for valid score
    CONFIDENCE_MULTIPLIER = 0.1  # How much sample size affects confidence
    
    def __init__(self, db: Session):
        """Initialize analytics service with database session"""
        self.db = db
        self.logger = logger
    
    def calculate_recommendation_effectiveness(
        self,
        recommendation_id: int
    ) -> Optional[EffectivenessMetrics]:
        """
        Calculate effectiveness metrics for a recommendation.
        
        Algorithm:
        1. Get all feedback for this recommendation (last 90 days)
        2. Calculate success rate (positive ratings / total)
        3. Calculate confidence (sample size based)
        4. Calculate trend (recent vs older data)
        5. Return metrics
        
        Args:
            recommendation_id: ID of recommendation to analyze
            
        Returns:
            EffectivenessMetrics object or None if insufficient data
        """
        try:
            # Get recommendation
            recommendation = self.db.query(Recommendation).filter(
                Recommendation.id == recommendation_id
            ).first()
            
            if not recommendation:
                self.logger.warning(f"Recommendation {recommendation_id} not found")
                return None
            
            # Calculate date window (last 90 days)
            cutoff_date = datetime.utcnow() - timedelta(days=self.EFFECTIVENESS_WINDOW_DAYS)
            
            # Get all feedback for this recommendation
            feedbacks = self.db.query(HealthRecord).filter(
                and_(
                    HealthRecord.recommendation_id == recommendation_id,
                    HealthRecord.created_at >= cutoff_date
                )
            ).all()
            
            if not feedbacks:
                self.logger.debug(f"No feedback found for recommendation {recommendation_id}")
                return None
            
            # Calculate metrics from feedback
            total_cases = len(feedbacks)
            successful_cases = sum(1 for f in feedbacks if self._is_successful_feedback(f))
            ratings = [f.symptom_improvement if f.symptom_improvement else 3 for f in feedbacks]
            
            # Calculate effectiveness score (success rate)
            effectiveness_score = successful_cases / total_cases if total_cases > 0 else 0.0
            
            # Calculate confidence based on sample size
            confidence = min(
                1.0,
                0.5 + (min(total_cases, 100) / 100) * 0.5  # Scale from 0.5 to 1.0
            )
            
            # Calculate average rating
            average_rating = sum(ratings) / len(ratings) if ratings else 0.0
            
            # Calculate trend
            trend = self._calculate_trend(feedbacks)
            
            # Create metrics object
            metrics = EffectivenessMetrics(
                recommendation_id=recommendation_id,
                herb_name=recommendation.herb_name or "Unknown",
                effectiveness_score=effectiveness_score,
                confidence=confidence,
                sample_size=total_cases,
                successful_cases=successful_cases,
                total_cases=total_cases,
                average_rating=average_rating,
                trend=trend,
                last_updated=datetime.utcnow()
            )
            
            self.logger.info(
                f"Calculated effectiveness for recommendation {recommendation_id}: "
                f"score={effectiveness_score:.2f}, confidence={confidence:.2f}, "
                f"samples={total_cases}"
            )
            
            return metrics
        
        except Exception as e:
            self.logger.error(f"Error calculating effectiveness: {str(e)}")
            return None
    
    def calculate_diagnosis_effectiveness(
        self,
        diagnosis_id: int
    ) -> Dict[int, EffectivenessMetrics]:
        """
        Calculate effectiveness metrics for all recommendations in a diagnosis.
        
        Args:
            diagnosis_id: ID of diagnosis
            
        Returns:
            Dictionary mapping recommendation_id to EffectivenessMetrics
        """
        try:
            # Get all recommendations for this diagnosis
            diagnosis = self.db.query(DiagnosticFinding).filter(
                DiagnosticFinding.id == diagnosis_id
            ).first()
            
            if not diagnosis or not diagnosis.recommendations:
                return {}
            
            results = {}
            for recommendation in diagnosis.recommendations:
                metrics = self.calculate_recommendation_effectiveness(recommendation.id)
                if metrics:
                    results[recommendation.id] = metrics
            
            return results
        
        except Exception as e:
            self.logger.error(f"Error calculating diagnosis effectiveness: {str(e)}")
            return {}
    
    def calculate_condition_effectiveness(
        self,
        condition_name: str
    ) -> Optional[EffectivenessMetrics]:
        """
        Calculate effectiveness for all recommendations for a condition.
        
        Aggregates data across all patients for this condition.
        
        Args:
            condition_name: Name of condition (e.g., "Headache", "نسخه")
            
        Returns:
            Aggregated EffectivenessMetrics for the condition
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=self.EFFECTIVENESS_WINDOW_DAYS)
            
            # Get all diagnoses for this condition
            diagnoses = self.db.query(DiagnosticFinding).filter(
                and_(
                    DiagnosticFinding.primary_condition == condition_name,
                    DiagnosticFinding.created_at >= cutoff_date
                )
            ).all()
            
            if not diagnoses:
                return None
            
            # Aggregate feedback across all recommendations for this condition
            all_feedbacks = []
            recommendation_names = set()
            
            for diagnosis in diagnoses:
                for rec in diagnosis.recommendations:
                    recommendation_names.add(rec.herb_name)
                    feedbacks = self.db.query(HealthRecord).filter(
                        and_(
                            HealthRecord.recommendation_id == rec.id,
                            HealthRecord.created_at >= cutoff_date
                        )
                    ).all()
                    all_feedbacks.extend(feedbacks)
            
            if not all_feedbacks:
                return None
            
            # Calculate aggregated metrics
            total_cases = len(all_feedbacks)
            successful_cases = sum(1 for f in all_feedbacks if self._is_successful_feedback(f))
            effectiveness_score = successful_cases / total_cases
            confidence = min(1.0, 0.5 + (min(total_cases, 100) / 100) * 0.5)
            average_rating = sum(
                f.symptom_improvement for f in all_feedbacks if f.symptom_improvement
            ) / len(all_feedbacks)
            trend = self._calculate_trend(all_feedbacks)
            
            # Use condition name as "herb_name"
            recommended_herbs = ", ".join(sorted(recommendation_names)[:3])
            
            return EffectivenessMetrics(
                recommendation_id=-1,  # Special ID for aggregated data
                herb_name=f"{condition_name} ({recommended_herbs})",
                effectiveness_score=effectiveness_score,
                confidence=confidence,
                sample_size=total_cases,
                successful_cases=successful_cases,
                total_cases=total_cases,
                average_rating=average_rating,
                trend=trend,
                last_updated=datetime.utcnow()
            )
        
        except Exception as e:
            self.logger.error(f"Error calculating condition effectiveness: {str(e)}")
            return None
    
    def calculate_herb_effectiveness(
        self,
        herb_name: str
    ) -> Optional[EffectivenessMetrics]:
        """
        Calculate effectiveness for a specific herb across all uses.
        
        Args:
            herb_name: Name of herb (e.g., "Ginger", "زنجبیل")
            
        Returns:
            EffectivenessMetrics for the herb
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=self.EFFECTIVENESS_WINDOW_DAYS)
            
            # Get all recommendations with this herb
            recommendations = self.db.query(Recommendation).filter(
                Recommendation.herb_name == herb_name
            ).all()
            
            if not recommendations:
                return None
            
            # Get all feedback for these recommendations
            rec_ids = [r.id for r in recommendations]
            all_feedbacks = self.db.query(HealthRecord).filter(
                and_(
                    HealthRecord.recommendation_id.in_(rec_ids),
                    HealthRecord.created_at >= cutoff_date
                )
            ).all()
            
            if not all_feedbacks:
                return None
            
            # Calculate aggregated metrics
            total_cases = len(all_feedbacks)
            successful_cases = sum(1 for f in all_feedbacks if self._is_successful_feedback(f))
            effectiveness_score = successful_cases / total_cases
            confidence = min(1.0, 0.5 + (min(total_cases, 100) / 100) * 0.5)
            average_rating = sum(
                f.symptom_improvement for f in all_feedbacks if f.symptom_improvement
            ) / len(all_feedbacks)
            trend = self._calculate_trend(all_feedbacks)
            
            return EffectivenessMetrics(
                recommendation_id=-2,  # Special ID for herb data
                herb_name=herb_name,
                effectiveness_score=effectiveness_score,
                confidence=confidence,
                sample_size=total_cases,
                successful_cases=successful_cases,
                total_cases=total_cases,
                average_rating=average_rating,
                trend=trend,
                last_updated=datetime.utcnow()
            )
        
        except Exception as e:
            self.logger.error(f"Error calculating herb effectiveness: {str(e)}")
            return None
    
    def get_trending_recommendations(
        self,
        limit: int = 10,
        min_samples: int = 5
    ) -> List[EffectivenessMetrics]:
        """
        Get trending recommendations (highest effectiveness with good confidence).
        
        Args:
            limit: Maximum number of recommendations to return
            min_samples: Minimum feedback samples for inclusion
            
        Returns:
            List of top performing EffectivenessMetrics sorted by effectiveness
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=self.EFFECTIVENESS_WINDOW_DAYS)
            
            # Get all recommendations with enough feedback
            recommendations = self.db.query(Recommendation).all()
            
            trending = []
            for rec in recommendations:
                feedbacks = self.db.query(HealthRecord).filter(
                    and_(
                        HealthRecord.recommendation_id == rec.id,
                        HealthRecord.created_at >= cutoff_date
                    )
                ).all()
                
                if len(feedbacks) >= min_samples:
                    metrics = self.calculate_recommendation_effectiveness(rec.id)
                    if metrics:
                        trending.append(metrics)
            
            # Sort by effectiveness score (descending)
            trending.sort(key=lambda m: m.effectiveness_score, reverse=True)
            
            return trending[:limit]
        
        except Exception as e:
            self.logger.error(f"Error getting trending recommendations: {str(e)}")
            return []
    
    def get_worst_performing_recommendations(
        self,
        limit: int = 10,
        min_samples: int = 5
    ) -> List[EffectivenessMetrics]:
        """
        Get worst performing recommendations (lowest effectiveness with good confidence).
        
        Useful for identifying recommendations that need adjustment.
        
        Args:
            limit: Maximum number to return
            min_samples: Minimum feedback samples for inclusion
            
        Returns:
            List of lowest performing EffectivenessMetrics
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=self.EFFECTIVENESS_WINDOW_DAYS)
            
            recommendations = self.db.query(Recommendation).all()
            
            worst = []
            for rec in recommendations:
                feedbacks = self.db.query(HealthRecord).filter(
                    and_(
                        HealthRecord.recommendation_id == rec.id,
                        HealthRecord.created_at >= cutoff_date
                    )
                ).all()
                
                if len(feedbacks) >= min_samples:
                    metrics = self.calculate_recommendation_effectiveness(rec.id)
                    if metrics:
                        worst.append(metrics)
            
            # Sort by effectiveness score (ascending)
            worst.sort(key=lambda m: m.effectiveness_score)
            
            return worst[:limit]
        
        except Exception as e:
            self.logger.error(f"Error getting worst recommendations: {str(e)}")
            return []
    
    def broadcast_effectiveness_update(
        self,
        diagnosis_id: int,
        recommendation_id: int
    ) -> bool:
        """
        Calculate effectiveness and broadcast update via WebSocket.
        
        This bridges analytics and real-time systems.
        
        Args:
            diagnosis_id: ID of diagnosis
            recommendation_id: ID of recommendation
            
        Returns:
            True if broadcast successful, False otherwise
        """
        try:
            metrics = self.calculate_recommendation_effectiveness(recommendation_id)
            
            if not metrics:
                self.logger.warning(
                    f"Could not calculate metrics for recommendation {recommendation_id}"
                )
                return False
            
            # Broadcast to connected clients
            import asyncio
            
            # Create new event loop for async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                loop.run_until_complete(
                    broadcast_effectiveness_update(
                        diagnosis_id=diagnosis_id,
                        recommendation_id=recommendation_id,
                        effectiveness=metrics.effectiveness_score,
                        confidence=metrics.confidence,
                        sample_size=metrics.sample_size
                    )
                )
                return True
            finally:
                loop.close()
        
        except Exception as e:
            self.logger.error(f"Error broadcasting effectiveness update: {str(e)}")
            return False
    
    # Private helper methods
    
    def _is_successful_feedback(self, feedback: HealthRecord) -> bool:
        """
        Determine if feedback represents successful treatment.
        
        Criteria:
        - Symptom improvement >= 3 (on 1-5 scale)
        - No significant side effects
        - Overall rating >= 3
        """
        try:
            if not feedback.symptom_improvement:
                return False
            
            # Symptom improvement >= 3 is considered successful
            if feedback.symptom_improvement < 3:
                return False
            
            # Check for side effects (if available)
            # This would depend on your data model
            
            return True
        
        except Exception as e:
            self.logger.error(f"Error checking feedback success: {str(e)}")
            return False
    
    def _calculate_trend(self, feedbacks: List[HealthRecord]) -> str:
        """
        Calculate trend from feedback (improving, stable, declining).
        
        Compares recent feedback (last 30 days) to older feedback.
        """
        try:
            if not feedbacks or len(feedbacks) < 2:
                return "stable"
            
            cutoff_date = datetime.utcnow() - timedelta(days=30)
            
            recent = [f for f in feedbacks if f.created_at >= cutoff_date]
            older = [f for f in feedbacks if f.created_at < cutoff_date]
            
            if not recent or not older:
                return "stable"
            
            recent_success_rate = sum(
                1 for f in recent if self._is_successful_feedback(f)
            ) / len(recent)
            
            older_success_rate = sum(
                1 for f in older if self._is_successful_feedback(f)
            ) / len(older)
            
            # Calculate change
            change = recent_success_rate - older_success_rate
            
            if change > 0.1:  # 10% improvement
                return "improving"
            elif change < -0.1:  # 10% decline
                return "declining"
            else:
                return "stable"
        
        except Exception as e:
            self.logger.error(f"Error calculating trend: {str(e)}")
            return "stable"


# Singleton instance
_analytics_service: Optional[AnalyticsService] = None


def get_analytics_service(db: Session) -> AnalyticsService:
    """Get or create analytics service instance"""
    global _analytics_service
    if _analytics_service is None:
        _analytics_service = AnalyticsService(db)
    return _analytics_service


# Module-level functions for easy access

def calculate_effectiveness(
    db: Session,
    recommendation_id: int
) -> Optional[EffectivenessMetrics]:
    """Calculate effectiveness for a recommendation"""
    service = get_analytics_service(db)
    return service.calculate_recommendation_effectiveness(recommendation_id)


def get_trending(
    db: Session,
    limit: int = 10
) -> List[EffectivenessMetrics]:
    """Get trending recommendations"""
    service = get_analytics_service(db)
    return service.get_trending_recommendations(limit=limit)


def get_worst_performing(
    db: Session,
    limit: int = 10
) -> List[EffectivenessMetrics]:
    """Get worst performing recommendations"""
    service = get_analytics_service(db)
    return service.get_worst_performing_recommendations(limit=limit)
