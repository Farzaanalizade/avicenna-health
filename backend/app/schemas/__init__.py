from app.schemas.patient import (
    Gender, 
    MizajType, 
    PatientBase, 
    PatientRegister, 
    PatientLogin, 
    PatientUpdate,
    PatientResponse
)
from app.schemas.health import (
    TongueAnalysisInput, TongueAnalysisResult,
    EyeAnalysisInput, EyeAnalysisResult,
    VoiceAnalysisInput, VoiceAnalysisResult,
    AudioAnalysisInput, AudioAnalysisResult,
    PulseAnalysisInput, PulseAnalysisResult,
    VitalSignsInput, VitalSigns,
    QuickCheckRequest, QuickCheckResponse,
    FoodRecommendation, HerbalRecommendation,
    HealthRecordReport
)
# بقیه importهای patient, auth و سایر بخش‌ها هم طبق نیاز پروژه اضافه شوند



__all__ = [
    "Gender",
    "MizajType",
    "PatientBase",
    "PatientRegister",
    "PatientLogin",
    "PatientUpdate",
    "PatientResponse",
    "TongueAnalysisInput",
    "EyeAnalysisInput",
    "VoiceAnalysisInput",
    "QuickCheckRequest",
    "QuickCheckResponse",
    "FoodRecommendation",
    "HerbalRecommendation"
]
