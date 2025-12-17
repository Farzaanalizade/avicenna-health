"""
Predictions Router - API endpoints for ML-based recommendation predictions
Endpoints for getting predictions, optimizing recommendations, and tracking changes
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.patient_and_diagnosis_data import Patient, DiagnosticFinding
from app.services.prediction_service import (
    PredictionService, PredictionResult, RecommendationScore,
    PatientProfile, get_prediction_service
)

router = APIRouter(prefix="/api/predictions", tags=["predictions"])


# ===========================
# Prediction Endpoints
# ===========================

@router.get("/diagnosis/{diagnosis_id}/predict", response_model=dict)
async def predict_recommendations(
    diagnosis_id: int,
    optimization_level: str = "balanced",
    current_user: Patient = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get ML predictions for recommendations
    
    Uses historical effectiveness data, similar patient outcomes, and symptom matching
    to predict which recommendations will work best for this diagnosis.
    
    Query Parameters:
        - optimization_level: conservative, balanced, or aggressive
    
    Returns:
        PredictionResult with scored recommendations
    """
    try:
        # Verify user owns diagnosis
        diagnosis = db.query(DiagnosticFinding).filter(
            DiagnosticFinding.id == diagnosis_id,
            DiagnosticFinding.patient_id == current_user.id
        ).first()

        if not diagnosis:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this diagnosis"
            )

        if optimization_level not in ["conservative", "balanced", "aggressive"]:
            optimization_level = "balanced"

        service = get_prediction_service(db)
        result = await service.predict_recommendations(diagnosis_id, optimization_level)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No recommendations found for this diagnosis"
            )

        return {
            "status": "success",
            "data": result.dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating predictions: {str(e)}"
        )


@router.get("/diagnosis/{diagnosis_id}/optimize", response_model=dict)
async def optimize_recommendations(
    diagnosis_id: int,
    target_effectiveness: float = 0.75,
    current_user: Patient = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get optimized recommendations
    
    Filters predictions to only show recommendations expected to achieve
    target effectiveness level.
    
    Query Parameters:
        - target_effectiveness: 0.0-1.0 (default 0.75 = 75%)
    
    Returns:
        List of optimized RecommendationScore objects
    """
    try:
        # Verify user owns diagnosis
        diagnosis = db.query(DiagnosticFinding).filter(
            DiagnosticFinding.id == diagnosis_id,
            DiagnosticFinding.patient_id == current_user.id
        ).first()

        if not diagnosis:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this diagnosis"
            )

        if target_effectiveness < 0.0 or target_effectiveness > 1.0:
            target_effectiveness = 0.75

        service = get_prediction_service(db)
        optimized = await service.optimize_recommendations(
            diagnosis_id,
            target_effectiveness
        )

        if not optimized:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No recommendations meet target effectiveness"
            )

        return {
            "status": "success",
            "count": len(optimized),
            "target_effectiveness": target_effectiveness,
            "data": [r.dict() for r in optimized]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error optimizing recommendations: {str(e)}"
        )


# ===========================
# Patient Profile Endpoints
# ===========================

@router.get("/patient/{patient_id}/profile", response_model=dict)
async def get_patient_profile(
    patient_id: int,
    current_user: Patient = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get patient profile for prediction analysis
    
    Shows patient's age, constitutional type (mizaj), and treatment history.
    User can only view own profile.
    
    Returns:
        PatientProfile with demographics and treatment history
    """
    try:
        if patient_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only view own profile"
            )

        service = get_prediction_service(db)
        profile = service.get_patient_profile(patient_id)

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )

        return {
            "status": "success",
            "data": profile.dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving profile: {str(e)}"
        )


# ===========================
# Prediction History Endpoints
# ===========================

@router.get("/diagnosis/{diagnosis_id}/evolution", response_model=dict)
async def get_recommendation_evolution(
    diagnosis_id: int,
    days: int = 30,
    current_user: Patient = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get how recommendations have evolved over time
    
    Tracks changes in recommendations as new feedback arrives
    and models are updated.
    
    Query Parameters:
        - days: Historical period to analyze (default 30)
    
    Returns:
        Evolution data showing what changed and when
    """
    try:
        # Verify user owns diagnosis
        diagnosis = db.query(DiagnosticFinding).filter(
            DiagnosticFinding.id == diagnosis_id,
            DiagnosticFinding.patient_id == current_user.id
        ).first()

        if not diagnosis:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this diagnosis"
            )

        if days < 1 or days > 365:
            days = 30

        service = get_prediction_service(db)
        evolution = service.get_recommendation_evolution(diagnosis_id, days)

        return {
            "status": "success",
            "data": evolution
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving evolution: {str(e)}"
        )


# ===========================
# Accuracy & Performance Endpoints
# ===========================

@router.get("/diagnosis/{diagnosis_id}/accuracy", response_model=dict)
async def get_prediction_accuracy(
    diagnosis_id: int,
    current_user: Patient = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get accuracy of predictions for a diagnosis
    
    Compares predicted effectiveness with actual feedback results.
    Higher accuracy indicates better predictions.
    
    Returns:
        Accuracy score (0.0-1.0)
    """
    try:
        # Verify user owns diagnosis
        diagnosis = db.query(DiagnosticFinding).filter(
            DiagnosticFinding.id == diagnosis_id,
            DiagnosticFinding.patient_id == current_user.id
        ).first()

        if not diagnosis:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this diagnosis"
            )

        service = get_prediction_service(db)
        accuracy = service.get_prediction_accuracy(diagnosis_id)

        return {
            "status": "success",
            "diagnosis_id": diagnosis_id,
            "accuracy_score": accuracy,
            "interpretation": self._interpret_accuracy(accuracy)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating accuracy: {str(e)}"
        )


# ===========================
# Public Prediction Endpoints
# ===========================

@router.get("/recommendation/{recommendation_id}/prediction-stats", response_model=dict)
async def get_recommendation_prediction_stats(
    recommendation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get prediction statistics for a recommendation
    
    Public endpoint showing how often this recommendation is predicted
    to be effective and actual outcomes.
    
    Returns:
        Statistics on prediction accuracy and frequency
    """
    try:
        from app.models.patient_and_diagnosis_data import Recommendation
        
        rec = db.query(Recommendation).filter(
            Recommendation.id == recommendation_id
        ).first()

        if not rec:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recommendation not found"
            )

        # Get all feedback for this recommendation
        from app.models.patient_and_diagnosis_data import HealthRecord
        feedbacks = db.query(HealthRecord).filter(
            HealthRecord.recommendation_id == recommendation_id
        ).all()

        if not feedbacks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No prediction data available"
            )

        # Calculate stats
        total = len(feedbacks)
        successful = sum(1 for f in feedbacks if f.rating and f.rating >= 3)
        success_rate = successful / total if total > 0 else 0.0

        return {
            "status": "success",
            "recommendation_id": recommendation_id,
            "total_predictions": total,
            "successful_outcomes": successful,
            "success_rate": round(success_rate, 3),
            "average_rating": round(
                sum(f.rating for f in feedbacks if f.rating) / total if total > 0 else 0.0,
                2
            ),
            "average_improvement": round(
                sum(f.symptom_improvement for f in feedbacks if f.symptom_improvement) / total if total > 0 else 0.0,
                2
            )
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving stats: {str(e)}"
        )


# ===========================
# Batch Prediction Endpoints
# ===========================

@router.post("/batch/predict", response_model=dict)
async def batch_predict(
    diagnosis_ids: List[int],
    current_user: Patient = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get predictions for multiple diagnoses
    
    Batch endpoint to predict recommendations for multiple diagnoses at once.
    Max 20 diagnoses per request.
    
    Returns:
        Dict mapping diagnosis_id to PredictionResult
    """
    try:
        if len(diagnosis_ids) > 20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum 20 diagnoses per batch"
            )

        service = get_prediction_service(db)
        results = {}

        for diagnosis_id in diagnosis_ids:
            # Verify ownership
            diagnosis = db.query(DiagnosticFinding).filter(
                DiagnosticFinding.id == diagnosis_id,
                DiagnosticFinding.patient_id == current_user.id
            ).first()

            if diagnosis:
                prediction = await service.predict_recommendations(diagnosis_id, "balanced")
                if prediction:
                    results[diagnosis_id] = prediction.dict()

        return {
            "status": "success",
            "count": len(results),
            "data": results
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in batch prediction: {str(e)}"
        )


# ===========================
# Model Information Endpoints
# ===========================

@router.get("/model/version", response_model=dict)
async def get_model_version(db: Session = Depends(get_db)):
    """
    Get prediction model version and information
    
    Public endpoint showing current ML model version and capabilities.
    
    Returns:
        Model metadata including version and training date
    """
    try:
        service = get_prediction_service(db)

        return {
            "status": "success",
            "model": {
                "version": service.MODEL_VERSION,
                "type": "ensemble",
                "components": [
                    "historical_effectiveness",
                    "similar_patient_matching",
                    "symptom_matching"
                ],
                "weights": {
                    "historical": 0.4,
                    "similar_patients": 0.35,
                    "symptom_match": 0.25
                },
                "min_confidence_threshold": service.CONFIDENCE_THRESHOLD,
                "min_similar_patients": service.MIN_SIMILAR_PATIENTS,
                "cache_hours": service.PREDICTION_CACHE_HOURS
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving model info: {str(e)}"
        )


@router.get("/health", response_model=dict)
async def prediction_health(db: Session = Depends(get_db)):
    """
    Health check for prediction service
    
    Returns service status and basic statistics
    """
    try:
        from app.models.patient_and_diagnosis_data import DiagnosticFinding

        total_diagnoses = db.query(DiagnosticFinding).count()

        return {
            "status": "success",
            "service": "predictions",
            "healthy": True,
            "statistics": {
                "total_diagnoses": total_diagnoses,
                "model_version": "1.0"
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction service error: {str(e)}"
        )


# ===========================
# Helper Methods
# ===========================

def _interpret_accuracy(accuracy: float) -> str:
    """Interpret accuracy score"""
    if accuracy >= 0.8:
        return "Excellent - predictions very reliable"
    elif accuracy >= 0.6:
        return "Good - predictions generally reliable"
    elif accuracy >= 0.4:
        return "Moderate - predictions somewhat reliable"
    else:
        return "Low - insufficient data for reliable predictions"
