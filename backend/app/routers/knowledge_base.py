"""
Knowledge Base API Router
Routes for accessing Avicenna, TCM, and Ayurveda knowledge bases
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, func
from typing import List

from app.database import get_db
from app.models.avicenna_knowledge_base import (
    AvicennaDisease, AvicennaTongueDiagnosis, AvicennaPulseDiagnosis,
    AvicennaEyeDiagnosis, AvicennaTreatment, AvicennaHerbalRemedyDictionary,
    AvicennaMizajBalanceGuide
)
from app.models.tcm_knowledge_base import (
    TCMPatternDisharmony, TCMMeridian, TCMAcupuncturePoint,
    TCMHerbalFormula, TCMHerbDictionary, TCMTongueDiagnosis,
    TCMPulseDiagnosis
)
from app.models.ayurveda_knowledge_base import (
    AyurvedicConstitution, AyurvedicDisease, AyurvedicPulseDiagnosis,
    AyurvedicTongueDiagnosis, AyurvedicHerbDictionary, AyurvedicTherapy,
    AyurvedicDietaryGuideline, AyurvedicDhatu, AyurvedicSrotas
)
from app.schemas.knowledge_base_schemas import (
    AvicennaDiseaseResponse, AvicennaTongueDiagnosisResponse,
    AvicennaPulseDiagnosisResponse, AvicennaHerbalRemedyResponse,
    AvicennaMizajBalanceGuideResponse,
    TCMPatternDisharmonyResponse, TCMMeridianResponse,
    TCMAcupuncturePointResponse, TCMHerbalFormulaResponse,
    TCMHerbDictionaryResponse, TCMTongueDiagnosisResponse,
    TCMPulseDiagnosisResponse,
    AyurvedicConstitutionResponse, AyurvedicDiseaseResponse,
    AyurvedicHerbResponse, AyurvedicTherapyResponse,
    AyurvedicDietaryGuidelineResponse, AyurvedicPulseDiagnosisResponse,
    AyurvedicTongueDiagnosisResponse, AyurvedicDhatuResponse,
    AyurvedicSrotasResponse
)

router = APIRouter(
    prefix="/api/v1/knowledge",
    tags=["knowledge_base"]
)


# ==================== AVICENNA KNOWLEDGE ====================

@router.get("/avicenna/diseases", response_model=List[AvicennaDiseaseResponse])
def search_avicenna_diseases(
    query: str = Query(None, min_length=2),
    mizaj: str = Query(None),
    category: str = Query(None),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """جستجو در بیماری‌های شناخت‌شده در طب سینایی"""
    q = db.query(AvicennaDisease)
    
    if query:
        q = q.filter(
            or_(
                AvicennaDisease.persian_name.ilike(f"%{query}%"),
                AvicennaDisease.arabic_name.ilike(f"%{query}%"),
                AvicennaDisease.modern_equivalent.ilike(f"%{query}%")
            )
        )
    
    if mizaj:
        q = q.filter(AvicennaDisease.related_mizaj == mizaj)
    
    if category:
        q = q.filter(AvicennaDisease.category == category)
    
    return q.limit(limit).all()


@router.get("/avicenna/diseases/{disease_id}", response_model=AvicennaDiseaseResponse)
def get_avicenna_disease(
    disease_id: int,
    db: Session = Depends(get_db)
):
    """دریافت جزئیات بیماری سینایی"""
    disease = db.query(AvicennaDisease).filter(AvicennaDisease.id == disease_id).first()
    if not disease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    return disease


@router.get("/avicenna/tongue-diagnosis", response_model=List[AvicennaTongueDiagnosisResponse])
def search_avicenna_tongue_diagnosis(
    color: str = Query(None),
    mizaj: str = Query(None),
    db: Session = Depends(get_db)
):
    """جستجو در معیارهای تشخیصی زبان سینایی"""
    q = db.query(AvicennaTongueDiagnosis)
    
    if color:
        q = q.filter(AvicennaTongueDiagnosis.color_category == color)
    
    if mizaj:
        q = q.filter(AvicennaTongueDiagnosis.color_mizaj == mizaj)
    
    return q.all()


@router.get("/avicenna/pulse-diagnosis", response_model=List[AvicennaPulseDiagnosisResponse])
def search_avicenna_pulse_diagnosis(
    rhythm: str = Query(None),
    strength: str = Query(None),
    db: Session = Depends(get_db)
):
    """جستجو در معیارهای تشخیصی نبض سینایی"""
    q = db.query(AvicennaPulseDiagnosis)
    
    if rhythm:
        q = q.filter(AvicennaPulseDiagnosis.pulse_rhythm == rhythm)
    
    if strength:
        q = q.filter(AvicennaPulseDiagnosis.pulse_strength == strength)
    
    return q.all()


@router.get("/avicenna/herbal-remedies", response_model=List[AvicennaHerbalRemedyResponse])
def search_avicenna_herbal_remedies(
    query: str = Query(None, min_length=2),
    potency: str = Query(None),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """جستجو در فرهنگ دارو‌های گیاهی سینایی"""
    q = db.query(AvicennaHerbalRemedyDictionary)
    
    if query:
        q = q.filter(
            or_(
                AvicennaHerbalRemedyDictionary.persian_name.ilike(f"%{query}%"),
                AvicennaHerbalRemedyDictionary.english_name.ilike(f"%{query}%"),
                AvicennaHerbalRemedyDictionary.latin_botanical_name.ilike(f"%{query}%")
            )
        )
    
    if potency:
        q = q.filter(AvicennaHerbalRemedyDictionary.potency == potency)
    
    return q.limit(limit).all()


@router.get("/avicenna/mizaj-balance/{mizaj}", response_model=AvicennaMizajBalanceGuideResponse)
def get_avicenna_mizaj_guide(
    mizaj: str,
    db: Session = Depends(get_db)
):
    """دریافت راهنمای تعادل مزاج"""
    guide = db.query(AvicennaMizajBalanceGuide).filter(
        AvicennaMizajBalanceGuide.mizaj == mizaj
    ).first()
    
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="راهنمای مزاج یافت نشد"
        )
    return guide


# ==================== TCM KNOWLEDGE ====================

@router.get("/tcm/patterns", response_model=List[TCMPatternDisharmonyResponse])
def search_tcm_patterns(
    query: str = Query(None, min_length=2),
    category: str = Query(None),
    organ: str = Query(None),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """جستجو در نمط‌های بی‌هماهنگی طب چینی"""
    q = db.query(TCMPatternDisharmony)
    
    if query:
        q = q.filter(
            or_(
                TCMPatternDisharmony.chinese_name.ilike(f"%{query}%"),
                TCMPatternDisharmony.english_name.ilike(f"%{query}%")
            )
        )
    
    if category:
        q = q.filter(TCMPatternDisharmony.pattern_category == category)
    
    if organ:
        q = q.filter(TCMPatternDisharmony.involved_organs.cast(str).contains(organ))
    
    return q.limit(limit).all()


@router.get("/tcm/patterns/{pattern_id}", response_model=TCMPatternDisharmonyResponse)
def get_tcm_pattern(
    pattern_id: int,
    db: Session = Depends(get_db)
):
    """دریافت جزئیات نمط طب چینی"""
    pattern = db.query(TCMPatternDisharmony).filter(
        TCMPatternDisharmony.id == pattern_id
    ).first()
    
    if not pattern:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="نمط یافت نشد"
        )
    return pattern


@router.get("/tcm/meridians", response_model=List[TCMMeridianResponse])
def list_tcm_meridians(
    organ: str = Query(None),
    db: Session = Depends(get_db)
):
    """لیست مسیرهای انرژی"""
    q = db.query(TCMMeridian)
    
    if organ:
        q = q.filter(TCMMeridian.associated_organ.ilike(f"%{organ}%"))
    
    return q.all()


@router.get("/tcm/meridians/{meridian_id}", response_model=TCMMeridianResponse)
def get_tcm_meridian(
    meridian_id: int,
    db: Session = Depends(get_db)
):
    """دریافت جزئیات مسیر انرژی"""
    meridian = db.query(TCMMeridian).filter(TCMMeridian.id == meridian_id).first()
    
    if not meridian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="مسیر یافت نشد"
        )
    return meridian


@router.get("/tcm/acupuncture-points", response_model=List[TCMAcupuncturePointResponse])
def search_tcm_acupuncture_points(
    point_code: str = Query(None),
    function: str = Query(None),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """جستجو در نقاط آکوپنکچر"""
    q = db.query(TCMAcupuncturePoint)
    
    if point_code:
        q = q.filter(TCMAcupuncturePoint.point_code.ilike(f"%{point_code}%"))
    
    if function:
        q = q.filter(TCMAcupuncturePoint.functions.cast(str).contains(function))
    
    return q.limit(limit).all()


@router.get("/tcm/formulas", response_model=List[TCMHerbalFormulaResponse])
def search_tcm_formulas(
    query: str = Query(None, min_length=2),
    category: str = Query(None),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """جستجو در فرمول‌های داروی چینی"""
    q = db.query(TCMHerbalFormula)
    
    if query:
        q = q.filter(
            or_(
                TCMHerbalFormula.chinese_name.ilike(f"%{query}%"),
                TCMHerbalFormula.english_name.ilike(f"%{query}%")
            )
        )
    
    if category:
        q = q.filter(TCMHerbalFormula.formula_category == category)
    
    return q.limit(limit).all()


@router.get("/tcm/herbs", response_model=List[TCMHerbDictionaryResponse])
def search_tcm_herbs(
    query: str = Query(None, min_length=2),
    temperature: str = Query(None),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """جستجو در فرهنگ گیاهان چینی"""
    q = db.query(TCMHerbDictionary)
    
    if query:
        q = q.filter(
            or_(
                TCMHerbDictionary.chinese_name.ilike(f"%{query}%"),
                TCMHerbDictionary.english_name.ilike(f"%{query}%")
            )
        )
    
    if temperature:
        q = q.filter(TCMHerbDictionary.temperature_nature == temperature)
    
    return q.limit(limit).all()


# ==================== AYURVEDA KNOWLEDGE ====================

@router.get("/ayurveda/constitutions", response_model=List[AyurvedicConstitutionResponse])
def list_ayurveda_constitutions(
    dosha: str = Query(None),
    db: Session = Depends(get_db)
):
    """لیست ساختار‌های تشکیل‌کننده"""
    q = db.query(AyurvedicConstitution)
    
    if dosha:
        q = q.filter(
            or_(
                AyurvedicConstitution.dosha_type == dosha,
                AyurvedicConstitution.dosha_combination.contains(dosha)
            )
        )
    
    return q.all()


@router.get("/ayurveda/constitutions/{constitution_id}", response_model=AyurvedicConstitutionResponse)
def get_ayurveda_constitution(
    constitution_id: int,
    db: Session = Depends(get_db)
):
    """دریافت جزئیات ساختار تشکیل‌کننده"""
    constitution = db.query(AyurvedicConstitution).filter(
        AyurvedicConstitution.id == constitution_id
    ).first()
    
    if not constitution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ساختار یافت نشد"
        )
    return constitution


@router.get("/ayurveda/diseases", response_model=List[AyurvedicDiseaseResponse])
def search_ayurveda_diseases(
    query: str = Query(None, min_length=2),
    dosha: str = Query(None),
    category: str = Query(None),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """جستجو در بیماری‌های آیورودا"""
    q = db.query(AyurvedicDisease)
    
    if query:
        q = q.filter(
            or_(
                AyurvedicDisease.sanskrit_name.ilike(f"%{query}%"),
                AyurvedicDisease.english_name.ilike(f"%{query}%"),
                AyurvedicDisease.modern_equivalent.ilike(f"%{query}%")
            )
        )
    
    if dosha:
        q = q.filter(AyurvedicDisease.involved_doshas.cast(str).contains(dosha))
    
    if category:
        q = q.filter(AyurvedicDisease.disease_category == category)
    
    return q.limit(limit).all()


@router.get("/ayurveda/diseases/{disease_id}", response_model=AyurvedicDiseaseResponse)
def get_ayurveda_disease(
    disease_id: int,
    db: Session = Depends(get_db)
):
    """دریافت جزئیات بیماری آیورودا"""
    disease = db.query(AyurvedicDisease).filter(
        AyurvedicDisease.id == disease_id
    ).first()
    
    if not disease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="بیماری یافت نشد"
        )
    return disease


@router.get("/ayurveda/herbs", response_model=List[AyurvedicHerbResponse])
def search_ayurveda_herbs(
    query: str = Query(None, min_length=2),
    potency: str = Query(None),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """جستجو در فرهنگ گیاهان آیورودا"""
    q = db.query(AyurvedicHerbDictionary)
    
    if query:
        q = q.filter(
            or_(
                AyurvedicHerbDictionary.sanskrit_name.ilike(f"%{query}%"),
                AyurvedicHerbDictionary.english_name.ilike(f"%{query}%")
            )
        )
    
    if potency:
        q = q.filter(AyurvedicHerbDictionary.potency == potency)
    
    return q.limit(limit).all()


@router.get("/ayurveda/therapies", response_model=List[AyurvedicTherapyResponse])
def search_ayurveda_therapies(
    therapy_type: str = Query(None),
    dosha: str = Query(None),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """جستجو در درمان‌های آیورودا"""
    q = db.query(AyurvedicTherapy)
    
    if therapy_type:
        q = q.filter(AyurvedicTherapy.therapy_type.ilike(f"%{therapy_type}%"))
    
    if dosha:
        q = q.filter(AyurvedicTherapy.dosha_effects.cast(str).contains(dosha))
    
    return q.limit(limit).all()


@router.get("/ayurveda/dietary-guidelines", response_model=List[AyurvedicDietaryGuidelineResponse])
def get_ayurveda_dietary_guidelines(
    dosha: str = Query(None),
    db: Session = Depends(get_db)
):
    """دریافت دستورالعمل‌های تغذیه‌ای"""
    q = db.query(AyurvedicDietaryGuideline)
    
    if dosha:
        q = q.filter(AyurvedicDietaryGuideline.dosha_type == dosha)
    
    return q.all()


@router.get("/ayurveda/dhatus", response_model=List[AyurvedicDhatuResponse])
def list_ayurveda_dhatus(
    order: bool = Query(True),
    db: Session = Depends(get_db)
):
    """لیست بافت‌های بدن"""
    q = db.query(AyurvedicDhatu)
    
    if order:
        q = q.order_by(AyurvedicDhatu.order_number)
    
    return q.all()


@router.get("/ayurveda/srotas", response_model=List[AyurvedicSrotasResponse])
def list_ayurveda_srotas(
    db: Session = Depends(get_db)
):
    """لیست قنوات بدن"""
    return db.query(AyurvedicSrotas).all()


# ==================== COMPARATIVE KNOWLEDGE ====================

@router.get("/compare/disease")
def compare_disease_across_traditions(
    disease_name: str = Query(None, min_length=2),
    db: Session = Depends(get_db)
):
    """مقایسۀ تفسیر بیماری در سه سنت"""
    if not disease_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="نام بیماری الزامی است"
        )
    
    avicenna_matches = db.query(AvicennaDisease).filter(
        or_(
            AvicennaDisease.persian_name.ilike(f"%{disease_name}%"),
            AvicennaDisease.modern_equivalent.ilike(f"%{disease_name}%")
        )
    ).all()
    
    ayurveda_matches = db.query(AyurvedicDisease).filter(
        or_(
            AyurvedicDisease.english_name.ilike(f"%{disease_name}%"),
            AyurvedicDisease.modern_equivalent.ilike(f"%{disease_name}%")
        )
    ).all()
    
    return {
        "query": disease_name,
        "avicenna": [
            {
                "id": d.id,
                "name": d.persian_name,
                "modern": d.modern_equivalent,
                "mizaj": d.related_mizaj
            }
            for d in avicenna_matches
        ],
        "ayurveda": [
            {
                "id": d.id,
                "name": d.english_name,
                "modern": d.modern_equivalent,
                "doshas": d.involved_doshas
            }
            for d in ayurveda_matches
        ]
    }


@router.get("/statistics/knowledge-base")
def get_knowledge_base_statistics(db: Session = Depends(get_db)):
    """آمار پایگاه دانش"""
    return {
        "avicenna": {
            "diseases": db.query(func.count(AvicennaDisease.id)).scalar(),
            "herbal_remedies": db.query(func.count(AvicennaHerbalRemedyDictionary.id)).scalar(),
            "tongue_diagnosis_patterns": db.query(func.count(AvicennaTongueDiagnosis.id)).scalar(),
            "pulse_diagnosis_patterns": db.query(func.count(AvicennaPulseDiagnosis.id)).scalar(),
        },
        "tcm": {
            "patterns": db.query(func.count(TCMPatternDisharmony.id)).scalar(),
            "meridians": db.query(func.count(TCMMeridian.id)).scalar(),
            "acupuncture_points": db.query(func.count(TCMAcupuncturePoint.id)).scalar(),
            "formulas": db.query(func.count(TCMHerbalFormula.id)).scalar(),
            "herbs": db.query(func.count(TCMHerbDictionary.id)).scalar(),
        },
        "ayurveda": {
            "constitutions": db.query(func.count(AyurvedicConstitution.id)).scalar(),
            "diseases": db.query(func.count(AyurvedicDisease.id)).scalar(),
            "herbs": db.query(func.count(AyurvedicHerbDictionary.id)).scalar(),
            "therapies": db.query(func.count(AyurvedicTherapy.id)).scalar(),
            "dhatus": db.query(func.count(AyurvedicDhatu.id)).scalar(),
            "srotas": db.query(func.count(AyurvedicSrotas.id)).scalar(),
        }
    }
