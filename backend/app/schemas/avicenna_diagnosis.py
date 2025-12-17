"""
Schemas برای اصول تشخیصی سینا
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============ نبض ============
class PulseAnalysisBase(BaseModel):
    pulse_rate: int
    primary_type: Optional[str] = None
    secondary_types: Optional[Dict[str, Any]] = None
    strength: Optional[str] = None
    rhythm: Optional[str] = None
    temperature: Optional[float] = None
    mizaj_indicator: Optional[str] = None
    condition_assessment: Optional[str] = None
    location: Optional[str] = None
    depth: Optional[str] = None
    width: Optional[str] = None


class PulseAnalysisCreate(PulseAnalysisBase):
    patient_id: int


class PulseAnalysisUpdate(BaseModel):
    pulse_rate: Optional[int] = None
    strength: Optional[str] = None
    rhythm: Optional[str] = None
    temperature: Optional[float] = None
    mizaj_indicator: Optional[str] = None
    condition_assessment: Optional[str] = None


class PulseAnalysisResponse(PulseAnalysisBase):
    id: int
    patient_id: int
    ai_assessment: Optional[str]
    confidence_score: Optional[float]
    recorded_at: datetime

    class Config:
        from_attributes = True


# ============ ادرار ============
class UrineAnalysisBase(BaseModel):
    color: Optional[str] = None
    density: Optional[str] = None
    odor: Optional[str] = None
    clarity: Optional[str] = None
    foam: Optional[str] = None
    sediment_present: bool = False
    crystals_present: bool = False
    blood_present: bool = False
    protein_level: Optional[str] = None
    sugar_level: Optional[str] = None
    mizaj_indicator: Optional[str] = None
    temperature_indication: Optional[str] = None
    moisture_indication: Optional[str] = None
    collection_time: Optional[str] = None


class UrineAnalysisCreate(UrineAnalysisBase):
    patient_id: int


class UrineAnalysisUpdate(BaseModel):
    color: Optional[str] = None
    density: Optional[str] = None
    clarity: Optional[str] = None
    mizaj_indicator: Optional[str] = None


class UrineAnalysisResponse(UrineAnalysisBase):
    id: int
    patient_id: int
    health_status: Optional[str]
    potential_conditions: Optional[List[Dict[str, Any]]]
    ai_assessment: Optional[str]
    confidence_score: Optional[float]
    recorded_at: datetime

    class Config:
        from_attributes = True


# ============ زبان ============
class TongueCoatingBase(BaseModel):
    coating_color: Optional[str] = None
    coating_thickness: Optional[str] = None
    coating_distribution: Optional[str] = None
    body_color: Optional[str] = None
    body_shape: Optional[str] = None
    body_size: Optional[str] = None
    moisture_level: Optional[str] = None
    temperature_feeling: Optional[str] = None
    cracks_pattern: Optional[str] = None
    tooth_marks: bool = False
    bumps_or_papillae: Optional[str] = None


class TongueCoatingCreate(TongueCoatingBase):
    patient_id: int


class TongueCoatingUpdate(BaseModel):
    coating_color: Optional[str] = None
    moisture_level: Optional[str] = None
    mizaj_type: Optional[str] = None


class TongueCoatingResponse(TongueCoatingBase):
    id: int
    patient_id: int
    mizaj_type: Optional[str]
    organ_indicators: Optional[Dict[str, Any]]
    disease_indicators: Optional[List[Dict[str, Any]]]
    ai_assessment: Optional[str]
    confidence_score: Optional[float]
    recorded_at: datetime

    class Config:
        from_attributes = True


# ============ یافته‌های تشخیصی ============
class DiagnosticFindingBase(BaseModel):
    pulse_analysis_id: Optional[int] = None
    urine_analysis_id: Optional[int] = None
    tongue_coating_id: Optional[int] = None
    primary_mizaj: Optional[str] = None
    secondary_mizaj: Optional[str] = None
    overall_health_status: Optional[str] = None


class DiagnosticFindingCreate(DiagnosticFindingBase):
    patient_id: int


class DiagnosticFindingResponse(DiagnosticFindingBase):
    id: int
    patient_id: int
    affected_organs: Optional[List[str]]
    identified_imbalances: Optional[List[Dict[str, Any]]]
    recommended_treatments: Optional[List[Dict[str, Any]]]
    lifestyle_recommendations: Optional[List[str]]
    dietary_recommendations: Optional[List[str]]
    created_at: datetime

    class Config:
        from_attributes = True
