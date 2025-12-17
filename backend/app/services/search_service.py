"""
Search Service for Advanced Search and Filtering
Provides full-text search, filtering, and recommendation discovery
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func, desc
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SearchService:
    """Advanced search and filtering service"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ===========================
    # Full-Text Search
    # ===========================
    
    def search_recommendations(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Full-text search for recommendations"""
        from app.models.patient_and_diagnosis_data import Recommendation
        
        # Search in herb name and description
        results = self.db.query(Recommendation).filter(
            or_(
                Recommendation.herb_name.ilike(f"%{query}%"),
                Recommendation.dosage.ilike(f"%{query}%"),
            )
        ).limit(limit).all()
        
        return [
            {
                "id": r.id,
                "herb_name": r.herb_name,
                "dosage": r.dosage,
                "effectiveness": r.effectiveness_rating,
            }
            for r in results
        ]
    
    def search_conditions(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search for health conditions"""
        from app.models.patient_and_diagnosis_data import DiagnosticFinding
        
        results = self.db.query(DiagnosticFinding).filter(
            DiagnosticFinding.condition.ilike(f"%{query}%")
        ).limit(limit).all()
        
        return [
            {
                "id": r.id,
                "condition": r.condition,
                "severity": r.severity,
            }
            for r in results
        ]
    
    # ===========================
    # Advanced Filtering
    # ===========================
    
    def filter_recommendations(
        self,
        effectiveness_min: float = 0.0,
        effectiveness_max: float = 1.0,
        mizaj_type: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Filter recommendations by criteria"""
        from app.models.patient_and_diagnosis_data import Recommendation
        
        query = self.db.query(Recommendation).filter(
            and_(
                Recommendation.effectiveness_rating >= effectiveness_min,
                Recommendation.effectiveness_rating <= effectiveness_max,
            )
        )
        
        results = query.limit(limit).all()
        
        return [
            {
                "id": r.id,
                "herb_name": r.herb_name,
                "dosage": r.dosage,
                "effectiveness": r.effectiveness_rating,
            }
            for r in results
        ]
    
    # ===========================
    # Similar Recommendations
    # ===========================
    
    def find_similar_recommendations(
        self,
        recommendation_id: int,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Find similar recommendations"""
        from app.models.patient_and_diagnosis_data import Recommendation, HealthRecord
        
        # Get the target recommendation
        target = self.db.query(Recommendation).filter(
            Recommendation.id == recommendation_id
        ).first()
        
        if not target:
            return []
        
        # Find recommendations with similar effectiveness
        similar = self.db.query(Recommendation).filter(
            and_(
                Recommendation.id != recommendation_id,
                Recommendation.effectiveness_rating >= (target.effectiveness_rating - 0.2),
                Recommendation.effectiveness_rating <= (target.effectiveness_rating + 0.2),
            )
        ).limit(limit).all()
        
        return [
            {
                "id": r.id,
                "herb_name": r.herb_name,
                "dosage": r.dosage,
                "effectiveness": r.effectiveness_rating,
                "similarity_score": 1.0 - abs(r.effectiveness_rating - target.effectiveness_rating),
            }
            for r in similar
        ]
    
    # ===========================
    # Saved Searches
    # ===========================
    
    def save_search(self, user_id: int, name: str, query: str, filters: Dict[str, Any]):
        """Save a search for later use"""
        from app.models.search_models import SavedSearch
        
        search = SavedSearch(
            user_id=user_id,
            name=name,
            query=query,
            filters=filters,
        )
        self.db.add(search)
        self.db.commit()
        return search.id
    
    def get_saved_searches(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user's saved searches"""
        from app.models.search_models import SavedSearch
        
        searches = self.db.query(SavedSearch).filter(
            SavedSearch.user_id == user_id
        ).all()
        
        return [
            {
                "id": s.id,
                "name": s.name,
                "query": s.query,
                "filters": s.filters,
                "created_at": s.created_at.isoformat(),
            }
            for s in searches
        ]
    
    def get_search_suggestions(self, partial_query: str, limit: int = 10) -> List[str]:
        """Get search suggestions based on partial query"""
        from app.models.patient_and_diagnosis_data import Recommendation
        
        suggestions = self.db.query(
            func.distinct(Recommendation.herb_name)
        ).filter(
            Recommendation.herb_name.ilike(f"{partial_query}%")
        ).limit(limit).all()
        
        return [s[0] for s in suggestions]


def get_search_service(db: Session) -> SearchService:
    """Get search service instance"""
    return SearchService(db)
