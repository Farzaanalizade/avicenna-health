"""
Cache service for advanced caching strategies
Handles cache warming, invalidation, and multi-level caching
"""

import logging
from typing import Any, Optional, List, Dict, Callable
from datetime import datetime, timedelta
from app.core.cache import get_cache, cache_invalidate, cached
from app.database import SessionLocal
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class CacheService:
    """Advanced caching service with warming and invalidation strategies"""
    
    def __init__(self):
        self.cache = get_cache()
        self.db = SessionLocal()
    
    # ===========================
    # Recommendations Cache
    # ===========================
    
    @cached(ttl_seconds=3600, prefix="recommendations")
    def get_recommendation_cache(self, recommendation_id: int) -> Optional[Dict[str, Any]]:
        """
        Get recommendation from cache
        
        TTL: 1 hour
        Pattern: recommendations:*
        """
        from app.models.patient_and_diagnosis_data import Recommendation
        
        rec = self.db.query(Recommendation).filter(
            Recommendation.id == recommendation_id
        ).first()
        
        if rec:
            return {
                "id": rec.id,
                "herb_name": rec.herb_name,
                "dosage": rec.dosage,
                "duration_days": rec.duration_days,
                "effectiveness_rating": rec.effectiveness_rating,
            }
        return None
    
    @cache_invalidate(pattern="recommendations:*")
    def invalidate_recommendations_cache(self):
        """Clear all recommendation caches"""
        logger.info("Invalidated recommendations cache")
    
    def warm_recommendations_cache(self, recommendation_ids: List[int]):
        """Warm cache with popular recommendations"""
        for rec_id in recommendation_ids:
            try:
                self.get_recommendation_cache(rec_id)
            except Exception as e:
                logger.error(f"Error warming recommendation cache {rec_id}: {e}")
    
    # ===========================
    # Analytics Cache
    # ===========================
    
    @cached(ttl_seconds=1800, prefix="analytics")  # 30 minutes
    def get_effectiveness_cache(self, recommendation_id: int) -> Optional[Dict[str, Any]]:
        """
        Get effectiveness metrics from cache
        
        TTL: 30 minutes (shorter because it changes frequently)
        Pattern: analytics:*
        """
        from app.models.patient_and_diagnosis_data import HealthRecord
        from sqlalchemy import func
        
        result = self.db.query(
            func.avg(HealthRecord.rating),
            func.count(HealthRecord.id),
            func.sum(HealthRecord.rating >= 3)
        ).filter(
            HealthRecord.recommendation_id == recommendation_id
        ).first()
        
        if result and result[1] > 0:
            avg_rating, total, successful = result
            return {
                "recommendation_id": recommendation_id,
                "average_rating": float(avg_rating) if avg_rating else 0.0,
                "total_feedbacks": total,
                "successful_count": successful or 0,
                "effectiveness_score": (successful or 0) / total if total > 0 else 0.0,
            }
        return None
    
    @cache_invalidate(pattern="analytics:*")
    def invalidate_analytics_cache(self):
        """Clear all analytics caches"""
        logger.info("Invalidated analytics cache")
    
    # ===========================
    # Predictions Cache
    # ===========================
    
    @cached(ttl_seconds=86400, prefix="predictions")  # 24 hours
    def get_predictions_cache(self, diagnosis_id: int, optimization_level: str) -> Optional[Dict[str, Any]]:
        """
        Get predictions from cache
        
        TTL: 24 hours (predictions don't change frequently)
        Pattern: predictions:*
        """
        # Predictions are expensive to compute, so cache for 24 hours
        return None  # Would be populated by prediction service
    
    @cache_invalidate(pattern="predictions:*")
    def invalidate_predictions_cache(self):
        """Clear all prediction caches"""
        logger.info("Invalidated predictions cache")
    
    # ===========================
    # Patient Profile Cache
    # ===========================
    
    @cached(ttl_seconds=7200, prefix="profile")  # 2 hours
    def get_patient_profile_cache(self, patient_id: int) -> Optional[Dict[str, Any]]:
        """
        Get patient profile from cache
        
        TTL: 2 hours
        Pattern: profile:*
        """
        from app.models.patient_and_diagnosis_data import Patient
        
        patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
        
        if patient:
            return {
                "patient_id": patient.id,
                "age": patient.age,
                "gender": patient.gender,
                "mizaj_type": patient.mizaj_type,
            }
        return None
    
    @cache_invalidate(pattern="profile:*")
    def invalidate_patient_cache(self, patient_id: int):
        """Clear specific patient cache"""
        logger.info(f"Invalidated patient cache {patient_id}")
    
    # ===========================
    # Trending & Popular Cache
    # ===========================
    
    @cached(ttl_seconds=3600, prefix="trending")
    def get_trending_recommendations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get trending recommendations
        
        TTL: 1 hour
        Pattern: trending:*
        """
        from app.models.patient_and_diagnosis_data import HealthRecord, Recommendation
        from sqlalchemy import func, desc
        
        trending = self.db.query(
            Recommendation.id,
            Recommendation.herb_name,
            func.count(HealthRecord.id).label("usage_count"),
            func.avg(HealthRecord.rating).label("avg_rating")
        ).join(HealthRecord).group_by(
            Recommendation.id, Recommendation.herb_name
        ).order_by(desc("usage_count")).limit(limit).all()
        
        return [
            {
                "id": t.id,
                "herb_name": t.herb_name,
                "usage_count": t.usage_count,
                "average_rating": float(t.avg_rating) if t.avg_rating else 0.0,
            }
            for t in trending
        ]
    
    @cache_invalidate(pattern="trending:*")
    def invalidate_trending_cache(self):
        """Clear trending cache"""
        logger.info("Invalidated trending cache")
    
    # ===========================
    # Cache Management
    # ===========================
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return self.cache.get_stats()
    
    def warm_critical_caches(self):
        """
        Warm up critical caches at startup
        Called from application startup event
        """
        logger.info("Warming critical caches...")
        
        try:
            # Warm recommendations
            from app.models.patient_and_diagnosis_data import Recommendation
            popular_recs = self.db.query(Recommendation).limit(20).all()
            self.warm_recommendations_cache([r.id for r in popular_recs])
            
            # Warm trending
            self.get_trending_recommendations()
            
            logger.info("✓ Critical caches warmed successfully")
        except Exception as e:
            logger.error(f"Error warming caches: {e}")
    
    def cache_health_check(self) -> Dict[str, Any]:
        """
        Check cache health and statistics
        
        Returns:
            Health status and metrics
        """
        stats = self.cache.get_stats()
        healthy = stats.get("connected", False)
        
        if not healthy:
            logger.warning("Cache (Redis) is not healthy!")
        
        return {
            "healthy": healthy,
            "cache_type": "Redis",
            "stats": stats,
        }
    
    def clear_old_caches(self, older_than_hours: int = 24):
        """
        Clear caches older than specified duration
        Note: Redis TTL handles this automatically
        """
        logger.info(f"Redis TTL will automatically clear caches older than {older_than_hours} hours")
    
    def __del__(self):
        """Cleanup database session"""
        try:
            self.db.close()
        except:
            pass


# Singleton instance
_cache_service: Optional[CacheService] = None

def get_cache_service() -> CacheService:
    """Get or create cache service instance"""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service


__all__ = [
    "CacheService",
    "get_cache_service",
]
