from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

# =====================================================
#  SCHEMAS FOR COMPREHENSIVE HEALTH RECORD
# =====================================================

class HealthRecordCreate(BaseModel):
    """Schema for creating a new health record session."""
    patient_id: int
    notes: Optional[str] = None

class HealthRecordResponse(BaseModel):
    """Response schema after successfully recording health data."""
    report_id: int
    message: str
    tongue_analysis_id: Optional[int] = None
    eye_analysis_id: Optional[int] = None
    skin_analysis_id: Optional[int] = None
    audio_analysis_id: Optional[int] = None
    vital_signs_ids: Optional[List[int]] = None
    created_at: datetime

    class Config:
        orm_mode = True

# =====================================================
#  EXISTING SCHEMAS (with minor adjustments if needed)
# =====================================================


# -----------------------------------------------------
# 👅 تحلیل زبان
# -----------------------------------------------------
class TongueAnalysisInput(BaseModel):
    image_base64: str
    metadata: Optional[Dict[str, Any]] = None

class TongueAnalysisResult(BaseModel):
    color: Optional[str] = None
    coating: Optional[str] = None
    cracks: Optional[str] = None
    humidity: Optional[str] = None
    avicenna_diagnosis: Optional[str] = None
    recommendations: Optional[Dict[str, Any]] = None


# -----------------------------------------------------
# 👁 تحلیل چشم
# -----------------------------------------------------
class EyeAnalysisInput(BaseModel):
    image_base64: str
    metadata: Optional[Dict[str, Any]] = None

class EyeAnalysisResult(BaseModel):
    iris_color: Optional[str] = None
    sclera_condition: Optional[str] = None
    avicenna_diagnosis: Optional[str] = None
    recommendations: Optional[Dict[str, Any]] = None


# -----------------------------------------------------
# 🗣 تحلیل صدا (گفتاری)
# -----------------------------------------------------
class VoiceAnalysisInput(BaseModel):
    audio_data_base64: str
    sample_rate_hz: Optional[int] = None
    duration_seconds: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class VoiceAnalysisResult(BaseModel):
    pitch: Optional[float] = None
    tone_quality: Optional[str] = None
    speech_rate: Optional[float] = None
    avicenna_diagnosis: Optional[str] = None
    recommendations: Optional[Dict[str, Any]] = None


# -----------------------------------------------------
# 🔊 تحلیل صوت عمومی (غیرکلامی)
# -----------------------------------------------------
class AudioAnalysisInput(BaseModel):
    audio_data_base64: str
    sample_rate_hz: Optional[int] = None
    duration_seconds: Optional[float] = None
    audio_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class AudioAnalysisResult(BaseModel):
    detected_features: Optional[Dict[str, Any]] = None
    health_status: Optional[str] = None
    risks_identified: Optional[List[str]] = None
    recommendations: Optional[Dict[str, Any]] = None


# -----------------------------------------------------
# 💓 تحلیل نبض
# -----------------------------------------------------
class PulseAnalysisInput(BaseModel):
    waveform_data_base64: Optional[str] = None
    sampling_rate_hz: Optional[int] = None
    duration_seconds: Optional[float] = None
    device_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class PulseAnalysisResult(BaseModel):
    heart_rate: Optional[float] = None
    rhythm_type: Optional[str] = None
    mizaj_assessment: Optional[str] = None
    amplitude_profile: Optional[str] = None
    health_status: Optional[str] = None
    recommendations: Optional[Dict[str, Any]] = None


# -----------------------------------------------------
# 🩺 علائم حیاتی
# -----------------------------------------------------
class VitalSignsInput(BaseModel):
    temperature_celsius: Optional[float] = None
    heart_rate_bpm: Optional[int] = None
    respiratory_rate_bpm: Optional[int] = None
    blood_pressure_mmHg: Optional[str] = None
    oxygen_saturation_pct: Optional[float] = None

class VitalSigns(BaseModel):
    temperature_celsius: Optional[float] = None
    heart_rate_bpm: Optional[int] = None
    respiratory_rate_bpm: Optional[int] = None
    blood_pressure_mmHg: Optional[str] = None
    oxygen_saturation_pct: Optional[float] = None


# -----------------------------------------------------
# ⚡ Quick Check
# -----------------------------------------------------
class QuickCheckRequest(BaseModel):
    symptoms: List[str]
    vital_signs: Optional[VitalSigns] = None

class QuickCheckResponse(BaseModel):
    probable_conditions: List[str]
    recommendations: Optional[Dict[str, Any]] = None


# -----------------------------------------------------
# 🥗 توصیه‌های غذایی و گیاهی
# -----------------------------------------------------
class FoodRecommendation(BaseModel):
    food_name: str
    description: Optional[str] = None
    reason: Optional[str] = None

class HerbalRecommendation(BaseModel):
    herb_name: str
    description: Optional[str] = None
    reason: Optional[str] = None


# -----------------------------------------------------
# 📄 گزارش سلامت
# -----------------------------------------------------
class HealthRecordReport(BaseModel):
    patient_name: str # Changed from patient_id for better reporting
    mizaj_type: Optional[str] = None
    diagnoses: Dict[str, Any] # More structured than List[str]
    recommendations: Optional[Dict[str, Any]] = None
    generated_at: str # Changed from created_at for clarity

    class Config:
        orm_mode = True

