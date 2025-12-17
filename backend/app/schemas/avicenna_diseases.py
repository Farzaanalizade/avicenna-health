"""
Schemas برای بیماری‌ها و درمان‌های سنتی
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============ بیماری ============
class SymptomInfo(BaseModel):
    symptom_id: int
    name: str
    is_primary: bool = False


class DiseaseBase(BaseModel):
    name_fa: str
    name_ar: Optional[str] = None
    name_latin: Optional[str] = None
    category: str
    description: Optional[str] = None
    avicenna_description: Optional[str] = None


class DiseaseCreate(DiseaseBase):
    key_symptoms: Optional[List[str]] = None
    related_mizaj: Optional[List[str]] = None
    primary_affected_organs: Optional[List[str]] = None


class DiseaseResponse(DiseaseBase):
    id: int
    key_symptoms: Optional[List[str]]
    secondary_symptoms: Optional[List[str]]
    diagnostic_signs: Optional[Dict[str, Any]]
    potential_complications: Optional[List[str]]
    typical_duration: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============ علائم ============
class SymptomBase(BaseModel):
    name_fa: str
    name_ar: Optional[str] = None
    description: Optional[str] = None
    symptom_type: Optional[str] = None
    severity_range: Optional[str] = None


class SymptomCreate(SymptomBase):
    mizaj_related: Optional[List[str]] = None
    affected_areas: Optional[List[str]] = None


class SymptomResponse(SymptomBase):
    id: int
    mizaj_related: Optional[List[str]]
    affected_areas: Optional[List[str]]
    when_observed: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ============ درمان سنتی ============
class IngredientInfo(BaseModel):
    name: str
    quantity: str
    unit: str


class TraditionalRemedyBase(BaseModel):
    name_fa: str
    name_ar: Optional[str] = None
    remedy_type: str
    preparation_method: Optional[str] = None
    usage_method: Optional[str] = None
    dosage: Optional[str] = None
    duration: Optional[str] = None
    frequency: Optional[str] = None


class TraditionalRemedyCreate(TraditionalRemedyBase):
    ingredients: Optional[List[Dict[str, Any]]] = None
    used_for_diseases: Optional[List[int]] = None
    used_for_conditions: Optional[List[str]] = None
    effect_on_mizaj: Optional[List[str]] = None
    temperature_nature: Optional[str] = None
    moisture_nature: Optional[str] = None


class TraditionalRemedyResponse(TraditionalRemedyBase):
    id: int
    ingredients: Optional[List[Dict[str, Any]]]
    used_for_diseases: Optional[List[int]]
    effect_on_mizaj: Optional[List[str]]
    temperature_nature: Optional[str]
    moisture_nature: Optional[str]
    effectiveness_level: Optional[str]
    contraindications: Optional[List[str]]
    side_effects: Optional[List[str]]
    avicenna_reference: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============ معادله درمان و بیماری ============
class DiseaseRemedyRelationBase(BaseModel):
    disease_id: int
    remedy_id: int
    effectiveness_rate: Optional[float] = None
    stage_of_disease: Optional[str] = None
    is_primary_treatment: bool = False
    treatment_priority: Optional[int] = None


class DiseaseRemedyRelationCreate(DiseaseRemedyRelationBase):
    pass


class DiseaseRemedyRelationResponse(DiseaseRemedyRelationBase):
    id: int
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ============ درمان برای تعادل مزاج ============
class MizajBalanceTreatmentBase(BaseModel):
    current_mizaj: str
    target_mizaj: str


class MizajBalanceTreatmentCreate(MizajBalanceTreatmentBase):
    recommended_remedies: Optional[List[int]] = None
    dietary_recommendations: Optional[List[str]] = None
    lifestyle_changes: Optional[List[str]] = None


class MizajBalanceTreatmentUpdate(BaseModel):
    current_mizaj: Optional[str] = None
    target_mizaj: Optional[str] = None
    is_completed: Optional[bool] = None


class MizajBalanceTreatmentResponse(MizajBalanceTreatmentBase):
    id: int
    patient_id: int
    recommended_remedies: Optional[List[Dict[str, Any]]]
    dietary_recommendations: Optional[List[str]]
    lifestyle_changes: Optional[List[str]]
    treatment_plan: Optional[Dict[str, Any]]
    expected_duration: Optional[str]
    follow_up_date: Optional[datetime]
    is_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============ گیاهان دارویی ============
class MedicalPlantBase(BaseModel):
    name_fa: str
    name_ar: Optional[str] = None
    name_scientific: Optional[str] = None
    name_common: Optional[str] = None
    plant_part_used: Optional[str] = None


class MedicalPlantCreate(MedicalPlantBase):
    active_compounds: Optional[List[str]] = None
    medicinal_uses: Optional[List[str]] = None
    treats_diseases: Optional[List[int]] = None
    temperature_nature: Optional[str] = None
    moisture_nature: Optional[str] = None
    degree_of_strength: Optional[str] = None
    balances_mizaj: Optional[List[str]] = None


class MedicalPlantResponse(MedicalPlantBase):
    id: int
    active_compounds: Optional[List[str]]
    temperature_nature: Optional[str]
    moisture_nature: Optional[str]
    degree_of_strength: Optional[str]
    medicinal_uses: Optional[List[str]]
    treats_diseases: Optional[List[int]]
    balances_mizaj: Optional[List[str]]
    preparation_methods: Optional[List[str]]
    typical_dosage: Optional[str]
    safety_profile: Optional[str]
    contraindications: Optional[List[str]]
    avicenna_reference: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
