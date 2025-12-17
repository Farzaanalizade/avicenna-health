"""
Analytics API Endpoints - Phase 3 Week 3 Task 2

REST endpoints for accessing recommendation effectiveness analytics and statistics.

Endpoints:
  GET    /api/analytics/status                              - Service health check
  GET    /api/analysis/{id}/effectiveness                  - Get effectiveness for all recs
  GET    /api/recommendations/{id}/effectiveness            - Get single recommendation
  GET    /api/analytics/trending                            - Get trending recommendations
  GET    /api/analytics/worst-performing                    - Get worst recommendations
  GET    /api/analytics/condition/{condition_name}          - Get condition effectiveness
  GET    /api/analytics/herb/{herb_name}                    - Get herb effectiveness
  POST   /api/analytics/calculate/{recommendation_id}       - Force recalculation + broadcast
"""

import logging
from typing import List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.models.user import User
from app.models.avicenna_diagnosis import DiagnosticFinding
from app.services.analytics_service import (
    get_analytics_service,
    EffectivenessMetrics,
    calculate_effectiveness,
    get_trending,
    get_worst_performing
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

# ─────────────────────────────────────────────────────────────────
# Health & Status Endpoints
# ─────────────────────────────────────────────────────────────────


@router.get("/status")
async def analytics_status():
    """
    Check analytics service health and status.
    
    Returns:
        Health status and service information
    """
    return {
        "status": "healthy",
        "service": "analytics",
        "version": "1.0.0",
        "features": [
            "effectiveness_tracking",
            "real_time_updates",
            "trending_analysis",
            "condition_analytics",
            "herb_analytics"
        ]
    }


# ─────────────────────────────────────────────────────────────────
# Diagnosis Analytics
# ─────────────────────────────────────────────────────────────────


@router.get("/diagnosis/{diagnosis_id}/effectiveness")
async def get_diagnosis_effectiveness(
    diagnosis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get effectiveness metrics for all recommendations in a diagnosis.
    
    Args:
        diagnosis_id: ID of diagnosis
        
    Returns:
        Dictionary mapping recommendation_id to effectiveness metrics
    """
    try:
        # Verify diagnosis exists and user owns it
        diagnosis = db.query(DiagnosticFinding).filter(
            DiagnosticFinding.id == diagnosis_id
        ).first()
        
        if not diagnosis:
            raise HTTPException(status_code=404, detail="Diagnosis not found")
        
        if diagnosis.patient_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get analytics service
        analytics = get_analytics_service(db)
        
        # Calculate effectiveness for all recommendations
        results = analytics.calculate_diagnosis_effectiveness(diagnosis_id)
        
        if not results:
            return {
                "diagnosis_id": diagnosis_id,
                "recommendations": [],
                "total_recommendations": 0,
                "message": "No effectiveness data available yet"
            }
        
        # Format response
        recommendations = [
            {
                "recommendation_id": rec_id,
                **metrics.to_dict()
            }
            for rec_id, metrics in results.items()
        ]
        
        # Calculate summary statistics
        effectiveness_scores = [m.effectiveness_score for m in results.values()]
        avg_effectiveness = sum(effectiveness_scores) / len(effectiveness_scores) if effectiveness_scores else 0
        
        return {
            "diagnosis_id": diagnosis_id,
            "recommendations": recommendations,
            "total_recommendations": len(recommendations),
            "average_effectiveness": round(avg_effectiveness, 3),
            "summary": {
                "high_performers": [r for r in recommendations if r["effectiveness_score"] >= 0.7],
                "moderate_performers": [r for r in recommendations if 0.4 <= r["effectiveness_score"] < 0.7],
                "low_performers": [r for r in recommendations if r["effectiveness_score"] < 0.4]
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting diagnosis effectiveness: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating effectiveness")


# ─────────────────────────────────────────────────────────────────
# Single Recommendation Analytics
# ─────────────────────────────────────────────────────────────────


@router.get("/recommendation/{recommendation_id}/effectiveness")
async def get_recommendation_effectiveness(
    recommendation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get effectiveness metrics for a single recommendation.
    
    Public endpoint - no auth required.
    
    Args:
        recommendation_id: ID of recommendation
        
    Returns:
        EffectivenessMetrics for the recommendation
    """
    try:
        metrics = calculate_effectiveness(db, recommendation_id)
        
        if not metrics:
            raise HTTPException(
                status_code=404,
                detail="Recommendation not found or insufficient feedback data"
            )
        
        return {
            "status": "success",
            **metrics.to_dict()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting recommendation effectiveness: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating effectiveness")


# ─────────────────────────────────────────────────────────────────
# Trending & Performance Analytics
# ─────────────────────────────────────────────────────────────────


@router.get("/trending")
async def get_trending_recommendations(
    limit: int = Query(10, ge=1, le=50),
    min_samples: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get trending (highest performing) recommendations.
    
    Returns recommendations with highest effectiveness scores
    that have sufficient feedback data.
    
    Args:
        limit: Maximum number to return (1-50, default 10)
        min_samples: Minimum feedback samples (1-100, default 5)
        
    Returns:
        List of trending EffectivenessMetrics
    """
    try:
        analytics = get_analytics_service(db)
        trending = analytics.get_trending_recommendations(
            limit=limit,
            min_samples=min_samples
        )
        
        return {
            "status": "success",
            "count": len(trending),
            "recommendations": [m.to_dict() for m in trending],
            "parameters": {
                "limit": limit,
                "min_samples": min_samples
            }
        }
    
    except Exception as e:
        logger.error(f"Error getting trending recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching trending data")


@router.get("/worst-performing")
async def get_worst_performing(
    limit: int = Query(10, ge=1, le=50),
    min_samples: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get worst performing recommendations.
    
    Returns recommendations with lowest effectiveness scores
    (for adjustment or further investigation).
    
    Args:
        limit: Maximum number to return (1-50, default 10)
        min_samples: Minimum feedback samples (1-100, default 5)
        
    Returns:
        List of worst performing EffectivenessMetrics
    """
    try:
        analytics = get_analytics_service(db)
        worst = analytics.get_worst_performing_recommendations(
            limit=limit,
            min_samples=min_samples
        )
        
        return {
            "status": "success",
            "count": len(worst),
            "recommendations": [m.to_dict() for m in worst],
            "alert": "These recommendations may need adjustment or further investigation",
            "parameters": {
                "limit": limit,
                "min_samples": min_samples
            }
        }
    
    except Exception as e:
        logger.error(f"Error getting worst performing: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching performance data")


# ─────────────────────────────────────────────────────────────────
# Condition & Herb Analytics
# ─────────────────────────────────────────────────────────────────


@router.get("/condition/{condition_name}")
async def get_condition_effectiveness(
    condition_name: str,
    db: Session = Depends(get_db)
):
    """
    Get aggregated effectiveness for all recommendations for a condition.
    
    Example:
        GET /api/analytics/condition/Headache
        
    Args:
        condition_name: Name of condition (e.g., "Headache", "نسخه")
        
    Returns:
        Aggregated EffectivenessMetrics for the condition
    """
    try:
        analytics = get_analytics_service(db)
        metrics = analytics.calculate_condition_effectiveness(condition_name)
        
        if not metrics:
            raise HTTPException(
                status_code=404,
                detail=f"No effectiveness data for condition: {condition_name}"
            )
        
        return {
            "status": "success",
            "condition": condition_name,
            **metrics.to_dict()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting condition effectiveness: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating effectiveness")


@router.get("/herb/{herb_name}")
async def get_herb_effectiveness(
    herb_name: str,
    db: Session = Depends(get_db)
):
    """
    Get aggregated effectiveness for a specific herb across all uses.
    
    Example:
        GET /api/analytics/herb/Ginger
        GET /api/analytics/herb/زنجبیل
        
    Args:
        herb_name: Name of herb (e.g., "Ginger", "زنجبیل")
        
    Returns:
        Aggregated EffectivenessMetrics for the herb
    """
    try:
        analytics = get_analytics_service(db)
        metrics = analytics.calculate_herb_effectiveness(herb_name)
        
        if not metrics:
            raise HTTPException(
                status_code=404,
                detail=f"No effectiveness data for herb: {herb_name}"
            )
        
        return {
            "status": "success",
            "herb": herb_name,
            **metrics.to_dict()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting herb effectiveness: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating effectiveness")


# ─────────────────────────────────────────────────────────────────
# Calculation & Broadcasting Endpoints
# ─────────────────────────────────────────────────────────────────


@router.post("/calculate/{recommendation_id}")
async def calculate_and_broadcast(
    recommendation_id: int,
    diagnosis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Force recalculation of effectiveness and broadcast update.
    
    This endpoint recalculates metrics and sends WebSocket
    notification to all connected clients.
    
    Args:
        recommendation_id: ID of recommendation to calculate
        diagnosis_id: ID of diagnosis for WebSocket broadcast
        
    Returns:
        Recalculated EffectivenessMetrics
    """
    try:
        # Verify diagnosis exists and user owns it
        diagnosis = db.query(DiagnosticFinding).filter(
            DiagnosticFinding.id == diagnosis_id
        ).first()
        
        if not diagnosis:
            raise HTTPException(status_code=404, detail="Diagnosis not found")
        
        if diagnosis.patient_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get analytics service
        analytics = get_analytics_service(db)
        
        # Calculate effectiveness
        metrics = analytics.calculate_recommendation_effectiveness(recommendation_id)
        
        if not metrics:
            raise HTTPException(
                status_code=404,
                detail="Could not calculate effectiveness"
            )
        
        # Broadcast update via WebSocket
        broadcast_success = analytics.broadcast_effectiveness_update(
            diagnosis_id=diagnosis_id,
            recommendation_id=recommendation_id
        )
        
        return {
            "status": "success",
            "calculation": metrics.to_dict(),
            "broadcast": {
                "status": "sent" if broadcast_success else "failed",
                "message": "Update broadcast to connected clients" if broadcast_success else "Broadcast failed (no connected clients)"
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in calculate and broadcast: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating effectiveness")


# ─────────────────────────────────────────────────────────────────
# Batch Analytics
# ─────────────────────────────────────────────────────────────────


@router.post("/batch/calculate")
async def batch_calculate(
    recommendation_ids: List[int],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Calculate effectiveness for multiple recommendations at once.
    
    Args:
        recommendation_ids: List of recommendation IDs
        
    Returns:
        Dictionary mapping recommendation_id to EffectivenessMetrics
    """
    try:
        if not recommendation_ids:
            raise HTTPException(status_code=400, detail="No recommendation IDs provided")
        
        if len(recommendation_ids) > 100:
            raise HTTPException(status_code=400, detail="Maximum 100 recommendations per request")
        
        analytics = get_analytics_service(db)
        results = {}
        
        for rec_id in recommendation_ids:
            metrics = analytics.calculate_recommendation_effectiveness(rec_id)
            if metrics:
                results[rec_id] = metrics.to_dict()
        
        return {
            "status": "success",
            "total_requested": len(recommendation_ids),
            "total_calculated": len(results),
            "results": results
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in batch calculate: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating effectiveness")
