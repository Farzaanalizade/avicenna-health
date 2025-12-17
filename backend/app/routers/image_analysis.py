"""
🔌 Image Analysis Endpoints - Phase 3

تحلیل تصاویر توسط Gemini Vision API
شناسایی ویژگی‌های سلامت (زبان، چشم، صورت، پوست)
"""

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.patient import Patient
from app.models.sensor_and_diagnostic_data import DiagnosticFinding
from app.schemas.sensor_diagnostic_schemas import DiagnosticFindingResponse
from app.services.gemini_service import GeminiService
from app.services.image_processing_service import ImageProcessingService
import io
import logging

router = APIRouter(prefix="/api/v1/analysis", tags=["analysis"])
logger = logging.getLogger(__name__)

# Initialize services
gemini_service = GeminiService()
image_service = ImageProcessingService()


@router.post("/tongue")
async def analyze_tongue(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user),
):
    """
    🔴 تحلیل تصویر زبان
    
    Features detected:
    - Color: pale, red, crimson, purple, dark
    - Coating: white, yellow, greasy, etc.
    - Moisture: dry, normal, wet
    - Shape & cracks
    - Mizaj indication
    """
    try:
        logger.info(f"👅 Analyzing tongue image for patient {current_user.id}")
        
        # Read image file
        image_data = await image.read()
        
        # Validate image
        is_valid, error_msg = image_service.validate_image(image_data)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Analyze with Gemini Vision
        analysis_result = await gemini_service.analyze_tongue_image(image_data)
        
        # Save diagnostic finding to database
        diagnostic = DiagnosticFinding(
            patient_id=current_user.id,
            analysis_type="tongue",
            findings=analysis_result.get("findings", {}),
            confidence_score=analysis_result.get("confidence", 0),
            source="gemini_vision_api",
        )
        db.add(diagnostic)
        db.commit()
        db.refresh(diagnostic)
        
        logger.info(f"✅ Tongue analysis completed with {analysis_result.get('confidence', 0):.1%} confidence")
        
        return {
            "success": True,
            "analysis_type": "tongue",
            "diagnostic_id": diagnostic.id,
            "findings": analysis_result.get("findings"),
            "confidence": analysis_result.get("confidence"),
            "mizaj": analysis_result.get("mizaj"),
            "recommendations": analysis_result.get("recommendations", []),
            "timestamp": diagnostic.created_at,
        }
        
    except Exception as e:
        logger.error(f"❌ Tongue analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/eye")
async def analyze_eye(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user),
):
    """
    👁️ تحلیل تصویر چشم
    
    Features detected:
    - Sclera color: clear, yellow, red
    - Pupil size & brightness
    - Dark circles
    - General eye health
    """
    try:
        logger.info(f"👀 Analyzing eye image for patient {current_user.id}")
        
        image_data = await image.read()
        
        # Validate
        is_valid, error_msg = image_service.validate_image(image_data)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Analyze
        analysis_result = await gemini_service.analyze_eye_image(image_data)
        
        # Save to database
        diagnostic = DiagnosticFinding(
            patient_id=current_user.id,
            analysis_type="eye",
            findings=analysis_result.get("findings", {}),
            confidence_score=analysis_result.get("confidence", 0),
            source="gemini_vision_api",
        )
        db.add(diagnostic)
        db.commit()
        db.refresh(diagnostic)
        
        logger.info(f"✅ Eye analysis completed")
        
        return {
            "success": True,
            "analysis_type": "eye",
            "diagnostic_id": diagnostic.id,
            "findings": analysis_result.get("findings"),
            "confidence": analysis_result.get("confidence"),
            "health_status": analysis_result.get("health_status"),
            "recommendations": analysis_result.get("recommendations", []),
            "timestamp": diagnostic.created_at,
        }
        
    except Exception as e:
        logger.error(f"❌ Eye analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/face")
async def analyze_face(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user),
):
    """
    😊 تحلیل تصویر صورت
    
    Features detected:
    - Skin complexion: pale, red, yellow, balanced
    - Skin condition: healthy, dry, oily, inflamed
    - Color distribution
    - General appearance
    """
    try:
        logger.info(f"😊 Analyzing face image for patient {current_user.id}")
        
        image_data = await image.read()
        
        # Validate
        is_valid, error_msg = image_service.validate_image(image_data)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Analyze
        analysis_result = await gemini_service.analyze_face_image(image_data)
        
        # Save
        diagnostic = DiagnosticFinding(
            patient_id=current_user.id,
            analysis_type="face",
            findings=analysis_result.get("findings", {}),
            confidence_score=analysis_result.get("confidence", 0),
            source="gemini_vision_api",
        )
        db.add(diagnostic)
        db.commit()
        db.refresh(diagnostic)
        
        logger.info(f"✅ Face analysis completed")
        
        return {
            "success": True,
            "analysis_type": "face",
            "diagnostic_id": diagnostic.id,
            "findings": analysis_result.get("findings"),
            "confidence": analysis_result.get("confidence"),
            "complexion": analysis_result.get("complexion"),
            "recommendations": analysis_result.get("recommendations", []),
            "timestamp": diagnostic.created_at,
        }
        
    except Exception as e:
        logger.error(f"❌ Face analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/skin")
async def analyze_skin(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user),
):
    """
    🖐️ تحلیل تصویر پوست
    
    Features detected:
    - Skin condition: normal, dry, oily, sensitive
    - Texture quality
    - Any visible conditions (rash, inflammation, etc.)
    - Moisture level
    """
    try:
        logger.info(f"🖐️ Analyzing skin image for patient {current_user.id}")
        
        image_data = await image.read()
        
        # Validate
        is_valid, error_msg = image_service.validate_image(image_data)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Analyze
        analysis_result = await gemini_service.analyze_skin_image(image_data)
        
        # Save
        diagnostic = DiagnosticFinding(
            patient_id=current_user.id,
            analysis_type="skin",
            findings=analysis_result.get("findings", {}),
            confidence_score=analysis_result.get("confidence", 0),
            source="gemini_vision_api",
        )
        db.add(diagnostic)
        db.commit()
        db.refresh(diagnostic)
        
        logger.info(f"✅ Skin analysis completed")
        
        return {
            "success": True,
            "analysis_type": "skin",
            "diagnostic_id": diagnostic.id,
            "findings": analysis_result.get("findings"),
            "confidence": analysis_result.get("confidence"),
            "condition": analysis_result.get("condition"),
            "recommendations": analysis_result.get("recommendations", []),
            "timestamp": diagnostic.created_at,
        }
        
    except Exception as e:
        logger.error(f"❌ Skin analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/history/{patient_id}")
async def get_analysis_history(
    patient_id: int,
    analysis_type: str = None,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user),
):
    """
    📊 دریافت تاریخچۀ تحلیل‌ها
    
    Query params:
    - analysis_type: filter by type (tongue, eye, face, skin)
    - limit: max results (default 20)
    """
    try:
        # Check access rights
        if current_user.id != patient_id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Access denied")
        
        query = db.query(DiagnosticFinding).filter(
            DiagnosticFinding.patient_id == patient_id
        )
        
        if analysis_type:
            query = query.filter(DiagnosticFinding.analysis_type == analysis_type)
        
        diagnostics = query.order_by(DiagnosticFinding.created_at.desc()).limit(limit).all()
        
        return {
            "success": True,
            "total": len(diagnostics),
            "analyses": [
                {
                    "id": d.id,
                    "type": d.analysis_type,
                    "findings": d.findings,
                    "confidence": d.confidence_score,
                    "created_at": d.created_at,
                }
                for d in diagnostics
            ],
        }
        
    except Exception as e:
        logger.error(f"❌ History error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{diagnosis_id}/match")
async def get_knowledge_matches(
    diagnosis_id: int,
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user),
):
    """
    🔍 دریافت تطابق‌های دانایی پزشکی
    
    تطابق نتایج تحلیل با بیماری‌های سنت‌های مختلف (Avicenna, TCM, Ayurveda)
    
    Returns:
    {
        avicenna_matches: [{disease_name, confidence, supporting_findings}, ...],
        tcm_matches: [{pattern_name, confidence, organs}, ...],
        ayurveda_matches: [{disease_name, dosha, confidence}, ...]
    }
    """
    try:
        from app.services.knowledge_matching_service import get_matching_service
        
        logger.info(f"🔍 Matching knowledge for diagnosis {diagnosis_id}")
        
        # Check if diagnosis belongs to current user
        diagnosis = db.query(DiagnosticFinding).filter(
            DiagnosticFinding.id == diagnosis_id
        ).first()
        
        if not diagnosis:
            raise HTTPException(status_code=404, detail="Diagnosis not found")
        
        if diagnosis.patient_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get matches
        matching_service = get_matching_service()
        matches = await matching_service.get_all_matches(diagnosis_id, db)
        
        return {
            "success": True,
            "diagnosis_id": diagnosis_id,
            "matches": matches,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Matching error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{diagnosis_id}/recommendations")
async def get_recommendations(
    diagnosis_id: int,
    tradition: str = None,  # "avicenna", "tcm", "ayurveda"
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user),
):
    """
    💊 دریافت توصیه‌های درمانی
    
    بر اساس نتایج تطابق دانایی
    
    Returns:
    {
        avicenna_recommendations: {herbs: [...], diet: [...], lifestyle: [...]},
        tcm_recommendations: {...},
        ayurveda_recommendations: {...}
    }
    """
    try:
        from app.services.knowledge_matching_service import get_matching_service
        from app.services.recommendation_engine import get_recommendation_engine
        
        logger.info(f"💊 Getting recommendations for diagnosis {diagnosis_id}")
        
        # Check diagnosis ownership
        diagnosis = db.query(DiagnosticFinding).filter(
            DiagnosticFinding.id == diagnosis_id
        ).first()
        
        if not diagnosis:
            raise HTTPException(status_code=404, detail="Diagnosis not found")
        
        if diagnosis.patient_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get matches first
        matching_service = get_matching_service()
        matches = await matching_service.get_all_matches(diagnosis_id, db)
        
        # Get recommendations based on matches
        rec_engine = get_recommendation_engine()
        recommendations = {}
        
        # Avicenna recommendations
        if matches.get("avicenna_matches") and len(matches["avicenna_matches"]) > 0:
            disease_id = matches["avicenna_matches"][0]["disease_id"]
            recommendations["avicenna"] = await rec_engine.get_avicenna_recommendations(
                disease_id, db
            )
        
        # TCM recommendations
        if matches.get("tcm_matches") and len(matches["tcm_matches"]) > 0:
            pattern_id = matches["tcm_matches"][0]["pattern_id"]
            recommendations["tcm"] = await rec_engine.get_tcm_recommendations(
                pattern_id, db
            )
        
        # Ayurveda recommendations
        if matches.get("ayurveda_matches") and len(matches["ayurveda_matches"]) > 0:
            disease_id = matches["ayurveda_matches"][0]["disease_id"]
            recommendations["ayurveda"] = await rec_engine.get_ayurveda_recommendations(
                disease_id, db
            )
        
        return {
            "success": True,
            "diagnosis_id": diagnosis_id,
            "recommendations": recommendations,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Recommendation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{diagnosis_id}/compare")
async def compare_traditions(
    diagnosis_id: int,
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user),
):
    """
    ⚖️ مقایسه دیدگاه سنت‌های مختلف
    
    مقایسه Avicenna vs TCM vs Ayurveda برای یک تشخیص
    """
    try:
        from app.services.knowledge_matching_service import get_matching_service
        
        logger.info(f"⚖️ Comparing traditions for diagnosis {diagnosis_id}")
        
        # Check diagnosis ownership
        diagnosis = db.query(DiagnosticFinding).filter(
            DiagnosticFinding.id == diagnosis_id
        ).first()
        
        if not diagnosis:
            raise HTTPException(status_code=404, detail="Diagnosis not found")
        
        if diagnosis.patient_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get all matches (comparison)
        matching_service = get_matching_service()
        matches = await matching_service.get_all_matches(diagnosis_id, db)
        
        # Prepare comparison
        comparison = {
            "diagnosis_id": diagnosis_id,
            "analysis_type": diagnosis.analysis_type,
            "original_findings": diagnosis.findings,
            "traditions": {
                "avicenna": {
                    "total_matches": len(matches.get("avicenna_matches", [])),
                    "top_match": matches.get("avicenna_matches", [None])[0],
                    "all_matches": matches.get("avicenna_matches", []),
                },
                "tcm": {
                    "total_matches": len(matches.get("tcm_matches", [])),
                    "top_match": matches.get("tcm_matches", [None])[0],
                    "all_matches": matches.get("tcm_matches", []),
                },
                "ayurveda": {
                    "total_matches": len(matches.get("ayurveda_matches", [])),
                    "top_match": matches.get("ayurveda_matches", [None])[0],
                    "all_matches": matches.get("ayurveda_matches", []),
                },
            },
            "consensus_areas": await _find_consensus_areas(matches),
        }
        
        return {
            "success": True,
            "comparison": comparison,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Comparison error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def _find_consensus_areas(matches: dict) -> List[str]:
    """
    یافتن نقاط توافق در میان سنت‌ها
    """
    consensus = []
    
    # اگر همه سنت‌ها میزان اعتماد بالا داشتند
    avicenna_conf = matches.get("avicenna_matches", [{}])[0].get("confidence", 0)
    tcm_conf = matches.get("tcm_matches", [{}])[0].get("confidence", 0)
    ayurveda_conf = matches.get("ayurveda_matches", [{}])[0].get("confidence", 0)
    
    avg_confidence = (avicenna_conf + tcm_conf + ayurveda_conf) / 3
    
    if avg_confidence > 0.75:
        consensus.append("Strong agreement across all traditions")
    elif avg_confidence > 0.6:
        consensus.append("Moderate agreement among traditions")
    
    return consensus


@router.get("/")
async def health_check():
    """
    ✅ Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "Analysis API",
        "version": "1.0.0",
    }
