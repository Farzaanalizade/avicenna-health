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
from app.schemas.avicenna_diagnosis import (
    PulseAnalysisCreate, PulseAnalysisResponse,
    UrineAnalysisCreate, UrineAnalysisResponse,
    TongueCoatingCreate, TongueCoatingResponse,
    DiagnosticFindingCreate, DiagnosticFindingResponse
)
from app.schemas.avicenna_diseases import (
    DiseaseCreate, DiseaseResponse,
    SymptomCreate, SymptomResponse,
    TraditionalRemedyCreate, TraditionalRemedyResponse,
    DiseaseRemedyRelationCreate, DiseaseRemedyRelationResponse,
    MizajBalanceTreatmentCreate, MizajBalanceTreatmentResponse,
    MedicalPlantCreate, MedicalPlantResponse
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
