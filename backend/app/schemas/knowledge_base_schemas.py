"""
Knowledge Base Schemas
Pydantic models for knowledge base data access
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List


# ==================== AVICENNA KNOWLEDGE ====================

class AvicennaDiseaseResponse(BaseModel):
    id: int
    persian_name: str
    arabic_name: Optional[str]
    latin_name: Optional[str]
    modern_equivalent: Optional[str]
    category: str
    severity: Optional[str]
    related_mizaj: str
    involved_humors: Optional[List[Dict[str, Any]]]
    symptoms: Optional[List[Dict[str, Any]]]
    tongue_signs: Optional[List[Dict[str, Any]]]
    pulse_signs: Optional[List[Dict[str, Any]]]
    treatments: Optional[List[Dict[str, Any]]]
    prognosis: Optional[str]

    class Config:
        from_attributes = True


class AvicennaTongueDiagnosisResponse(BaseModel):
    id: int
    color_category: str
    coating_type: str
    coating_color: str
    texture: str
    moisture: str
    related_mizaj: str
    confidence: float

    class Config:
        from_attributes = True


class AvicennaPulseDiagnosisResponse(BaseModel):
    id: int
    pulse_rate_range: str
    pulse_rate_min: Optional[int]
    pulse_rate_max: Optional[int]
    pulse_rhythm: str
    pulse_strength: str
    pulse_depth: str
    related_mizaj: str
    confidence: float

    class Config:
        from_attributes = True


class AvicennaHerbalRemedyResponse(BaseModel):
    id: int
    persian_name: str
    english_name: str
    latin_botanical_name: Optional[str]
    potency: str
    moisture_property: str
    effects: Optional[List[Dict[str, Any]]]
    treats_diseases: Optional[List[Dict[str, Any]]]
    recommended_dosage: Optional[str]
    contraindications: Optional[List[Dict[str, Any]]]

    class Config:
        from_attributes = True


class AvicennaMizajBalanceGuideResponse(BaseModel):
    id: int
    mizaj: str
    persian_name: Optional[str]
    dominant_humor: Optional[str]
    recommended_foods: Optional[List[Dict[str, Any]]]
    recommended_activities: Optional[List[Dict[str, Any]]]
    potential_diseases: Optional[List[Dict[str, Any]]]

    class Config:
        from_attributes = True


# ==================== TCM KNOWLEDGE ====================

class TCMPatternDisharmonyResponse(BaseModel):
    id: int
    chinese_name: str
    pinyin_name: str
    english_name: str
    pattern_category: str
    involved_organs: List[Dict[str, Any]]
    main_symptoms: List[Dict[str, Any]]
    tongue_findings: Optional[List[Dict[str, Any]]]
    pulse_findings: Optional[List[Dict[str, Any]]]
    treatment_principles: Optional[List[Dict[str, Any]]]

    class Config:
        from_attributes = True


class TCMMeridianResponse(BaseModel):
    id: int
    chinese_name: str
    pinyin_name: str
    english_name: str
    meridian_type: str
    associated_organ: str
    acupuncture_points: Optional[List[Dict[str, Any]]]
    organ_clock_time: Optional[str]

    class Config:
        from_attributes = True


class TCMAcupuncturePointResponse(BaseModel):
    id: int
    point_code: str
    chinese_name: str
    pinyin_name: str
    english_name: str
    location: str
    functions: List[Dict[str, Any]]
    indications: Optional[List[Dict[str, Any]]]
    needle_depth: Optional[str]

    class Config:
        from_attributes = True


class TCMHerbalFormulaResponse(BaseModel):
    id: int
    chinese_name: str
    pinyin_name: str
    english_name: str
    formula_category: str
    treatment_principles: List[Dict[str, Any]]
    herbs: List[Dict[str, Any]]
    indications: List[Dict[str, Any]]
    dosage: Optional[str]
    dosage_frequency: Optional[str]

    class Config:
        from_attributes = True


class TCMHerbDictionaryResponse(BaseModel):
    id: int
    chinese_name: str
    pinyin_name: str
    english_name: str
    temperature_nature: str
    flavor: List[str]
    meridian_entries: List[str]
    primary_functions: List[Dict[str, Any]]
    treats_conditions: Optional[List[Dict[str, Any]]]
    typical_dosage: Optional[str]

    class Config:
        from_attributes = True


class TCMTongueDiagnosisResponse(BaseModel):
    id: int
    tongue_color: str
    coating_color: Optional[str]
    coating_thickness: Optional[str]
    moisture_level: Optional[str]
    cracks: bool
    related_patterns: Optional[List[Dict[str, Any]]]
    confidence_level: float

    class Config:
        from_attributes = True


class TCMPulseDiagnosisResponse(BaseModel):
    id: int
    pulse_position: str
    pulse_speed: str
    pulse_strength: str
    pulse_rhythm: str
    pulse_quality: Optional[str]
    related_patterns: Optional[List[Dict[str, Any]]]
    confidence_level: float

    class Config:
        from_attributes = True


# ==================== AYURVEDA KNOWLEDGE ====================

class AyurvedicConstitutionResponse(BaseModel):
    id: int
    dosha_type: str
    dosha_combination: str
    constitution_name: str
    physical_characteristics: Optional[List[Dict[str, Any]]]
    mental_characteristics: Optional[List[Dict[str, Any]]]
    recommended_foods: Optional[List[Dict[str, Any]]]
    lifestyle_recommendations: Optional[List[Dict[str, Any]]]
    predisposition_to_diseases: Optional[List[Dict[str, Any]]]

    class Config:
        from_attributes = True


class AyurvedicDiseaseResponse(BaseModel):
    id: int
    sanskrit_name: str
    english_name: str
    modern_equivalent: Optional[str]
    disease_category: str
    involved_doshas: List[Dict[str, Any]]
    main_symptoms: List[Dict[str, Any]]
    causes: Optional[List[Dict[str, Any]]]
    treatment_approaches: Optional[List[Dict[str, Any]]]
    herbal_recommendations: Optional[List[Dict[str, Any]]]

    class Config:
        from_attributes = True


class AyurvedicHerbResponse(BaseModel):
    id: int
    sanskrit_name: str
    english_name: str
    latin_botanical_name: Optional[str]
    tastes: List[str]
    potency: str
    post_digestive_effect: str
    dosha_effects: List[Dict[str, Any]]
    treats_conditions: Optional[List[Dict[str, Any]]]
    typical_dosage: Optional[str]

    class Config:
        from_attributes = True


class AyurvedicTherapyResponse(BaseModel):
    id: int
    sanskrit_name: str
    english_name: str
    therapy_type: str
    therapeutic_goals: List[Dict[str, Any]]
    dosha_effects: Optional[List[Dict[str, Any]]]
    treats_conditions: Optional[List[Dict[str, Any]]]
    session_duration: Optional[str]
    frequency: Optional[str]

    class Config:
        from_attributes = True


class AyurvedicDietaryGuidelineResponse(BaseModel):
    id: int
    guideline_name: str
    dosha_type: str
    beneficial_foods: Optional[List[Dict[str, Any]]]
    foods_to_avoid: Optional[List[Dict[str, Any]]]
    recommended_oils: Optional[List[Dict[str, Any]]]
    recommended_spices: Optional[List[Dict[str, Any]]]
    meal_timing: Optional[List[Dict[str, Any]]]

    class Config:
        from_attributes = True


class AyurvedicPulseDiagnosisResponse(BaseModel):
    id: int
    pulse_movement: str
    vata_pattern: Optional[str]
    pitta_pattern: Optional[str]
    kapha_pattern: Optional[str]
    pulse_position: Optional[str]
    dosha_indicators: Optional[List[Dict[str, Any]]]

    class Config:
        from_attributes = True


class AyurvedicTongueDiagnosisResponse(BaseModel):
    id: int
    tongue_color: str
    coating_color: Optional[str]
    coating_thickness: Optional[str]
    cracks_present: bool
    predominant_dosha: Optional[str]
    ama_level: Optional[str]

    class Config:
        from_attributes = True


class AyurvedicDhatuResponse(BaseModel):
    id: int
    sanskrit_name: str
    english_name: str
    order_number: Optional[int]
    functions: Optional[List[Dict[str, Any]]]
    health_signs: Optional[List[Dict[str, Any]]]
    disease_signs: Optional[List[Dict[str, Any]]]

    class Config:
        from_attributes = True


class AyurvedicSrotasResponse(BaseModel):
    id: int
    sanskrit_name: str
    english_name: str
    functions: Optional[List[Dict[str, Any]]]
    health_signs: Optional[List[Dict[str, Any]]]
    disease_signs: Optional[List[Dict[str, Any]]]

    class Config:
        from_attributes = True
