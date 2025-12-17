"""
Feedback Router - API endpoints for user feedback collection and management
Endpoints for submitting ratings, viewing history, and analyzing effectiveness
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.patient_and_diagnosis_data import Patient
from app.services.feedback_service import (
    FeedbackService, FeedbackRating, FeedbackResponse, FeedbackSummary,
    FeedbackTrend, get_feedback_service
)

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


# ===========================
# Feedback Submission Endpoints
# ===========================

@router.post("/submit", response_model=dict)
async def submit_feedback(
    feedback_data: FeedbackRating,
    current_user: Patient = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit feedback for a recommendation
    
    Accepts rating (1-5), symptom improvement score, optional comment and side effects.
    Automatically triggers analytics recalculation and WebSocket broadcasts.
    
    Returns:
        Created FeedbackResponse with feedback ID and metadata
    """
    try:
        service = get_feedback_service(db)
        result = await service.submit_feedback(current_user.id, feedback_data)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Diagnosis not found or unauthorized access"
            )

        return {
            "status": "success",
            "message": "Feedback submitted successfully",
            "data": result.dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error submitting feedback: {str(e)}"
        )


@router.put("/update/{health_record_id}", response_model=dict)
async def update_feedback(
    health_record_id: int,
    feedback_data: FeedbackRating,
    current_user: Patient = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update existing feedback submission
    
    Allows users to modify their feedback, ratings, and comments.
    Automatically triggers analytics recalculation.
    
    Returns:
        Updated FeedbackResponse with new data
    """
    try:
        service = get_feedback_service(db)
        result = await service.update_feedback(current_user.id, health_record_id, feedback_data)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback record not found or unauthorized access"
            )

        return {
            "status": "success",
            "message": "Feedback updated successfully",
            "data": result.dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating feedback: {str(e)}"
        )


# ===========================
# Feedback History Endpoints
# ===========================

@router.get("/history", response_model=dict)
async def get_feedback_history(
    diagnosis_id: Optional[int] = None,
    recommendation_id: Optional[int] = None,
    limit: int = 50,
    current_user: Patient = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's feedback history
    
    Returns all feedback submissions, optionally filtered by diagnosis or recommendation.
    
    Query Parameters:
        - diagnosis_id: Filter by specific diagnosis
        - recommendation_id: Filter by specific recommendation
        - limit: Maximum results (default 50, max 200)
    
    Returns:
        List of FeedbackResponse objects
    """
    try:
        if limit > 200:
            limit = 200

        service = get_feedback_service(db)
        history = service.get_feedback_history(
            current_user.id,
            diagnosis_id=diagnosis_id,
            recommendation_id=recommendation_id,
            limit=limit
        )

        return {
            "status": "success",
            "count": len(history),
            "data": [f.dict() for f in history]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving feedback history: {str(e)}"
        )


# ===========================
# Analytics Endpoints (Public)
# ===========================

@router.get("/recommendation/{recommendation_id}/summary", response_model=dict)
async def get_recommendation_summary(
    recommendation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get feedback summary for a recommendation
    
    Public endpoint showing aggregated feedback statistics.
    Shows average rating, improvement scores, side effects, and trend.
    
    Returns:
        FeedbackSummary with aggregated feedback data
    """
    try:
        service = get_feedback_service(db)
        summary = service.get_recommendation_feedback_summary(recommendation_id)

        if not summary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No feedback data available for this recommendation"
            )

        return {
            "status": "success",
            "data": summary.dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving summary: {str(e)}"
        )


@router.get("/recommendation/{recommendation_id}/trend", response_model=dict)
async def get_recommendation_trend(
    recommendation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get feedback trend for a recommendation
    
    Analyzes recent vs older feedback to determine if effectiveness is improving, stable, or declining.
    
    Returns:
        FeedbackTrend with trend direction and confidence score
    """
    try:
        service = get_feedback_service(db)
        trend = service.get_feedback_trend(recommendation_id)

        if not trend:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insufficient feedback data to determine trend"
            )

        return {
            "status": "success",
            "data": trend.dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving trend: {str(e)}"
        )


# ===========================
# Diagnosis-Level Endpoints (Private)
# ===========================

@router.get("/diagnosis/{diagnosis_id}/overview", response_model=dict)
async def get_diagnosis_feedback_overview(
    diagnosis_id: int,
    current_user: Patient = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get complete feedback overview for a diagnosis
    
    Private endpoint showing feedback data for all recommendations in a diagnosis.
    User must own the diagnosis.
    
    Returns:
        Dict with summary and trend for each recommendation
    """
    try:
        # Verify user owns diagnosis
        from app.models.patient_and_diagnosis_data import DiagnosticFinding
        diagnosis = db.query(DiagnosticFinding).filter(
            DiagnosticFinding.id == diagnosis_id,
            DiagnosticFinding.patient_id == current_user.id
        ).first()

        if not diagnosis:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this diagnosis"
            )

        service = get_feedback_service(db)
        overview = service.get_diagnosis_feedback_overview(diagnosis_id)

        return {
            "status": "success",
            "data": overview
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving overview: {str(e)}"
        )


# ===========================
# Statistics Endpoints (Public)
# ===========================

@router.get("/stats/most-effective", response_model=dict)
async def get_most_effective_recommendations(
    limit: int = 10,
    min_feedbacks: int = 5,
    db: Session = Depends(get_db)
):
    """
    Get most effective recommendations based on feedback
    
    Public endpoint showing top-rated recommendations by user rating and symptom improvement.
    
    Query Parameters:
        - limit: Number of results (default 10, max 50)
        - min_feedbacks: Minimum feedback count required (default 5)
    
    Returns:
        List of recommendations sorted by effectiveness
    """
    try:
        if limit > 50:
            limit = 50

        service = get_feedback_service(db)
        
        # Get all recommendations with their summaries
        from app.models.patient_and_diagnosis_data import Recommendation
        recommendations = db.query(Recommendation).all()

        effective_recs = []
        for rec in recommendations:
            summary = service.get_recommendation_feedback_summary(rec.id)
            if summary and summary.total_feedbacks >= min_feedbacks:
                effective_recs.append({
                    "recommendation_id": rec.id,
                    "herb_name": rec.herb_name if hasattr(rec, 'herb_name') else "Unknown",
                    "average_rating": summary.average_rating,
                    "average_improvement": summary.average_improvement,
                    "total_feedbacks": summary.total_feedbacks,
                    "positive_percentage": summary.positive_feedback_percentage
                })

        # Sort by average rating
        effective_recs.sort(key=lambda x: x["average_rating"], reverse=True)

        return {
            "status": "success",
            "count": len(effective_recs[:limit]),
            "data": effective_recs[:limit]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving statistics: {str(e)}"
        )


@router.get("/stats/side-effects", response_model=dict)
async def get_reported_side_effects(
    recommendation_id: Optional[int] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get commonly reported side effects
    
    Public endpoint showing side effects from user feedback.
    
    Query Parameters:
        - recommendation_id: Optional filter by recommendation
        - limit: Number of results
    
    Returns:
        List of reported side effects with frequency
    """
    try:
        from app.models.patient_and_diagnosis_data import HealthRecord
        
        query = db.query(HealthRecord).filter(HealthRecord.side_effects != None)
        
        if recommendation_id:
            query = query.filter(HealthRecord.recommendation_id == recommendation_id)

        records = query.all()
        
        # Aggregate side effects
        side_effects_count = {}
        for record in records:
            if record.side_effects:
                effects = [e.strip() for e in record.side_effects.split(',')]
                for effect in effects:
                    side_effects_count[effect] = side_effects_count.get(effect, 0) + 1

        # Sort by frequency
        sorted_effects = sorted(
            side_effects_count.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]

        return {
            "status": "success",
            "count": len(sorted_effects),
            "data": [
                {"side_effect": effect, "reported_count": count}
                for effect, count in sorted_effects
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving side effects: {str(e)}"
        )


# ===========================
# Batch Operations Endpoints
# ===========================

@router.post("/batch/submit", response_model=dict)
async def batch_submit_feedback(
    feedbacks: List[FeedbackRating],
    current_user: Patient = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit multiple feedback entries at once
    
    Private endpoint for batch feedback submission (max 50 entries).
    Useful for mobile app to sync multiple ratings at once.
    
    Returns:
        Dict with success/failure count and details
    """
    try:
        if len(feedbacks) > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum 50 feedback entries per batch"
            )

        service = get_feedback_service(db)
        results = {
            "total": len(feedbacks),
            "successful": 0,
            "failed": 0,
            "details": []
        }

        for idx, feedback in enumerate(feedbacks):
            result = await service.submit_feedback(current_user.id, feedback)
            if result:
                results["successful"] += 1
                results["details"].append({
                    "index": idx,
                    "status": "success",
                    "feedback_id": result.id
                })
            else:
                results["failed"] += 1
                results["details"].append({
                    "index": idx,
                    "status": "failed",
                    "reason": "Unauthorized diagnosis or recommendation not found"
                })

        return {
            "status": "success",
            "data": results
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in batch submission: {str(e)}"
        )


@router.get("/health", response_model=dict)
async def feedback_health(db: Session = Depends(get_db)):
    """
    Health check endpoint for feedback service
    
    Returns service status and basic statistics
    """
    try:
        from app.models.patient_and_diagnosis_data import HealthRecord
        
        total_feedbacks = db.query(HealthRecord).count()
        
        return {
            "status": "success",
            "service": "feedback",
            "healthy": True,
            "statistics": {
                "total_feedbacks": total_feedbacks
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Feedback service error: {str(e)}"
        )
