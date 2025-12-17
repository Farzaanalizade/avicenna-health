from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum


# ==================== SENSOR DATA ====================

class SensorDataCreate(BaseModel):
    sensor_type: str
    raw_value: Dict[str, Any]
    unit: Optional[str] = None
    device_info: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = 0.0


class SensorDataUpdate(BaseModel):
    processed_value: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None
    is_valid: Optional[bool] = None
    validation_notes: Optional[str] = None


class SensorDataResponse(BaseModel):
    id: int
    patient_id: int
    sensor_type: str
    raw_value: Dict[str, Any]
    processed_value: Optional[Dict[str, Any]]
    unit: Optional[str]
    device_info: Optional[Dict[str, Any]]
    confidence_score: float
    is_valid: bool
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== WEARABLE DEVICE ====================

class WearableDeviceCreate(BaseModel):
    device_type: str
    device_model: Optional[str] = None
    device_id: str
    device_name: Optional[str] = None
    api_token: Optional[str] = None
    api_url: Optional[str] = None
    sync_frequency: Optional[int] = 300


class WearableDeviceUpdate(BaseModel):
    connection_status: Optional[str] = None
    battery_level: Optional[int] = None
    is_active: Optional[bool] = None
    sync_frequency: Optional[int] = None


class WearableDeviceResponse(BaseModel):
    id: int
    patient_id: int
    device_type: str
    device_model: Optional[str]
    device_id: str
    device_name: Optional[str]
    connection_status: str
    battery_level: Optional[int]
    last_sync: Optional[datetime]
    is_active: bool
    paired_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== PULSE ANALYSIS ====================

class PulseAnalysisCreate(BaseModel):
    pulse_rate: int
    pulse_rhythm: str
    pulse_strength: str
    pulse_depth: str
    measurement_location: Optional[str] = None
    mizaj_indication: Optional[str] = None
    organ_involved: Optional[str] = None
    disease_indication: Optional[str] = None
    audio_recording_path: Optional[str] = None
    clinical_notes: Optional[str] = None


class PulseAnalysisResponse(BaseModel):
    id: int
    patient_id: int
    pulse_rate: int
    pulse_rhythm: str
    pulse_strength: str
    pulse_depth: str
    measurement_location: Optional[str]
    mizaj_indication: Optional[str]
    organ_involved: Optional[str]
    disease_indication: Optional[str]
    clinical_notes: Optional[str]
    confidence_score: float
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== URINE ANALYSIS ====================

class UrineAnalysisCreate(BaseModel):
    color: str
    transparency: str
    smell: Optional[str] = None
    consistency: str
    temperature: Optional[float] = None
    volume: Optional[float] = None
    ph_level: Optional[float] = None
    specific_gravity: Optional[float] = None
    protein_level: Optional[str] = None
    glucose_level: Optional[str] = None
    ketones: Optional[str] = None
    blood_present: Optional[bool] = False
    bacteria_present: Optional[bool] = False
    mizaj_indication: Optional[str] = None
    organ_involved: Optional[str] = None
    disease_indication: Optional[str] = None
    image_path: Optional[str] = None
    clinical_notes: Optional[str] = None


class UrineAnalysisResponse(BaseModel):
    id: int
    patient_id: int
    color: str
    transparency: str
    smell: Optional[str]
    consistency: str
    ph_level: Optional[float]
    specific_gravity: Optional[float]
    protein_level: Optional[str]
    glucose_level: Optional[str]
    mizaj_indication: Optional[str]
    organ_involved: Optional[str]
    disease_indication: Optional[str]
    blood_present: bool
    bacteria_present: bool
    confidence_score: float
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== TONGUE COATING ====================

class TongueCoatingCreate(BaseModel):
    body_color: str
    coating_type: str
    coating_color: str
    coating_distribution: Optional[str] = None
    texture: str
    moisture: str
    thickness: str
    cracks_present: Optional[bool] = False
    cracks_pattern: Optional[str] = None
    teeth_marks: Optional[bool] = False
    tremor: Optional[bool] = False
    nodules_present: Optional[bool] = False
    pimples_present: Optional[bool] = False
    swollen_papillae: Optional[bool] = False
    mizaj_indication: Optional[str] = None
    heat_cold_index: Optional[int] = None
    dryness_wetness_index: Optional[int] = None
    chinese_medicine_signs: Optional[Dict[str, Any]] = None
    ayurvedic_signs: Optional[Dict[str, Any]] = None
    potential_diseases: Optional[List[Dict[str, Any]]] = None
    image_path: Optional[str] = None
    clinical_notes: Optional[str] = None


class TongueCoatingResponse(BaseModel):
    id: int
    patient_id: int
    body_color: str
    coating_type: str
    coating_color: str
    texture: str
    moisture: str
    thickness: str
    cracks_present: bool
    teeth_marks: bool
    mizaj_indication: Optional[str]
    chinese_medicine_signs: Optional[Dict[str, Any]]
    ayurvedic_signs: Optional[Dict[str, Any]]
    potential_diseases: Optional[List[Dict[str, Any]]]
    confidence_score: float
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== DIAGNOSTIC FINDING ====================

class DiagnosticFindingCreate(BaseModel):
    finding_type: str
    avicenna_diagnosis: Optional[str] = None
    affected_organs: Optional[List[str]] = None
    affected_humors: Optional[List[Dict[str, Any]]] = None
    severity_level: Optional[str] = None
    prognosis: Optional[str] = None
    expected_duration: Optional[str] = None
    root_cause: Optional[str] = None
    contributing_factors: Optional[List[str]] = None
    recommended_treatment: Optional[List[Dict[str, Any]]] = None
    dietary_recommendations: Optional[List[Dict[str, Any]]] = None
    lifestyle_recommendations: Optional[List[Dict[str, Any]]] = None
    traditional_medicines: Optional[List[Dict[str, Any]]] = None
    prevention_measures: Optional[List[Dict[str, Any]]] = None
    complications_if_untreated: Optional[List[Dict[str, Any]]] = None
    requires_doctor_consultation: Optional[bool] = False
    urgency_level: Optional[str] = None
    specialist_type: Optional[str] = None
    physician_notes: Optional[str] = None


class DiagnosticFindingResponse(BaseModel):
    id: int
    patient_id: int
    finding_type: str
    avicenna_diagnosis: Optional[str]
    affected_organs: Optional[List[str]]
    affected_humors: Optional[List[Dict[str, Any]]]
    severity_level: Optional[str]
    prognosis: Optional[str]
    root_cause: Optional[str]
    recommended_treatment: Optional[List[Dict[str, Any]]]
    dietary_recommendations: Optional[List[Dict[str, Any]]]
    requires_doctor_consultation: bool
    urgency_level: str
    confidence_score: float
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== MIZAJ BALANCE TREATMENT ====================

class MizajBalanceTreatmentCreate(BaseModel):
    current_mizaj: str
    target_mizaj: str
    duration_days: Optional[int] = None
    dietary_treatments: Optional[List[Dict[str, Any]]] = None
    herbal_treatments: Optional[List[Dict[str, Any]]] = None
    lifestyle_treatments: Optional[List[Dict[str, Any]]] = None
    natural_treatments: Optional[List[Dict[str, Any]]] = None
    physical_treatments: Optional[List[Dict[str, Any]]] = None
    spiritual_treatments: Optional[List[Dict[str, Any]]] = None
    forbidden_items: Optional[List[str]] = None
    physician_notes: Optional[str] = None


class MizajBalanceTreatmentUpdate(BaseModel):
    status: Optional[str] = None
    progress_tracking: Optional[List[Dict[str, Any]]] = None
    physician_notes: Optional[str] = None
    confidence_score: Optional[float] = None


class MizajBalanceTreatmentResponse(BaseModel):
    id: int
    patient_id: int
    current_mizaj: str
    target_mizaj: str
    duration_days: Optional[int]
    dietary_treatments: Optional[List[Dict[str, Any]]]
    herbal_treatments: Optional[List[Dict[str, Any]]]
    lifestyle_treatments: Optional[List[Dict[str, Any]]]
    forbidden_items: Optional[List[str]]
    status: str
    confidence_score: float
    start_date: datetime
    end_date: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
