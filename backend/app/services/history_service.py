"""
Recommendation History Service
Tracks recommendation changes over time and shows evolution
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class HistoryService:
    """Recommendation history and evolution tracking"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ===========================
    # History Tracking
    # ===========================
    
    def log_recommendation_change(
        self,
        diagnosis_id: int,
        previous_recs: List[int],
        new_recs: List[int],
        reason: str = ""
    ):
        """Log recommendation changes"""
        from app.models.history_models import RecommendationChange
        
        # Find what changed
        added = [r for r in new_recs if r not in previous_recs]
        removed = [r for r in previous_recs if r not in new_recs]
        
        for rec_id in added:
            change = RecommendationChange(
                diagnosis_id=diagnosis_id,
                recommendation_id=rec_id,
                change_type="added",
                reason=reason,
                timestamp=datetime.utcnow(),
            )
            self.db.add(change)
        
        for rec_id in removed:
            change = RecommendationChange(
                diagnosis_id=diagnosis_id,
                recommendation_id=rec_id,
                change_type="removed",
                reason=reason,
                timestamp=datetime.utcnow(),
            )
            self.db.add(change)
        
        self.db.commit()
        logger.info(f"Logged {len(added)} additions, {len(removed)} removals for diagnosis {diagnosis_id}")
    
    # ===========================
    # History Retrieval
    # ===========================
    
    def get_recommendation_history(self, diagnosis_id: int) -> List[Dict[str, Any]]:
        """Get complete recommendation history for a diagnosis"""
        from app.models.history_models import RecommendationChange
        from app.models.patient_and_diagnosis_data import Recommendation
        
        changes = self.db.query(RecommendationChange).filter(
            RecommendationChange.diagnosis_id == diagnosis_id
        ).order_by(desc(RecommendationChange.timestamp)).all()
        
        history = []
        for change in changes:
            rec = self.db.query(Recommendation).filter(
                Recommendation.id == change.recommendation_id
            ).first()
            
            history.append({
                "id": change.id,
                "recommendation_id": change.recommendation_id,
                "herb_name": rec.herb_name if rec else "Unknown",
                "change_type": change.change_type,  # added, removed, updated
                "reason": change.reason,
                "timestamp": change.timestamp.isoformat(),
                "days_ago": (datetime.utcnow() - change.timestamp).days,
            })
        
        return history
    
    # ===========================
    # Comparison
    # ===========================
    
    def compare_recommendations(
        self,
        diagnosis_id: int,
        version_a_date: datetime,
        version_b_date: datetime
    ) -> Dict[str, Any]:
        """Compare recommendations between two time periods"""
        from app.models.history_models import RecommendationChange
        
        # Get recommendations at version_a
        changes_a = self.db.query(RecommendationChange).filter(
            RecommendationChange.diagnosis_id == diagnosis_id,
            RecommendationChange.timestamp <= version_a_date,
        ).order_by(desc(RecommendationChange.timestamp)).all()
        
        # Get recommendations at version_b
        changes_b = self.db.query(RecommendationChange).filter(
            RecommendationChange.diagnosis_id == diagnosis_id,
            RecommendationChange.timestamp <= version_b_date,
        ).order_by(desc(RecommendationChange.timestamp)).all()
        
        recs_a = set(c.recommendation_id for c in changes_a if c.change_type == "added")
        recs_b = set(c.recommendation_id for c in changes_b if c.change_type == "added")
        
        added = recs_b - recs_a
        removed = recs_a - recs_b
        same = recs_a & recs_b
        
        return {
            "version_a_date": version_a_date.isoformat(),
            "version_b_date": version_b_date.isoformat(),
            "added_recommendations": list(added),
            "removed_recommendations": list(removed),
            "unchanged_recommendations": list(same),
            "total_change_percentage": ((len(added) + len(removed)) / (len(recs_a) + 1)) * 100,
        }
    
    # ===========================
    # Evolution Tracking
    # ===========================
    
    def get_recommendation_evolution(self, recommendation_id: int) -> List[Dict[str, Any]]:
        """Track how many times a recommendation was added/removed"""
        from app.models.history_models import RecommendationChange
        from app.models.patient_and_diagnosis_data import Recommendation
        
        rec = self.db.query(Recommendation).filter(
            Recommendation.id == recommendation_id
        ).first()
        
        changes = self.db.query(RecommendationChange).filter(
            RecommendationChange.recommendation_id == recommendation_id
        ).order_by(RecommendationChange.timestamp).all()
        
        evolution = {
            "recommendation_id": recommendation_id,
            "herb_name": rec.herb_name if rec else "Unknown",
            "total_changes": len(changes),
            "times_added": sum(1 for c in changes if c.change_type == "added"),
            "times_removed": sum(1 for c in changes if c.change_type == "removed"),
            "last_change": changes[-1].timestamp.isoformat() if changes else None,
            "change_history": [
                {
                    "type": c.change_type,
                    "reason": c.reason,
                    "timestamp": c.timestamp.isoformat(),
                }
                for c in changes[-10:]  # Last 10 changes
            ],
        }
        
        return evolution
    
    # ===========================
    # Decision Analysis
    # ===========================
    
    def analyze_change_reasons(self, diagnosis_id: int) -> Dict[str, Any]:
        """Analyze why recommendations changed"""
        from app.models.history_models import RecommendationChange
        from sqlalchemy import func
        
        # Group by reason
        reasons = self.db.query(
            RecommendationChange.reason,
            func.count(RecommendationChange.id).label("count")
        ).filter(
            RecommendationChange.diagnosis_id == diagnosis_id
        ).group_by(RecommendationChange.reason).all()
        
        # Group by change type
        types = self.db.query(
            RecommendationChange.change_type,
            func.count(RecommendationChange.id).label("count")
        ).filter(
            RecommendationChange.diagnosis_id == diagnosis_id
        ).group_by(RecommendationChange.change_type).all()
        
        return {
            "diagnosis_id": diagnosis_id,
            "change_reasons": {r.reason: r.count for r in reasons if r.reason},
            "change_types": {t.change_type: t.count for t in types},
            "total_changes": sum(t.count for t in types),
        }


def get_history_service(db: Session) -> HistoryService:
    """Get history service instance"""
    return HistoryService(db)
