"""
API Routes برای بیماری‌ها و درمان‌های سنتی
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies import get_db
from app.schemas.avicenna_diseases import (
    DiseaseCreate, DiseaseResponse,
    SymptomCreate, SymptomResponse,
    TraditionalRemedyCreate, TraditionalRemedyResponse,
    DiseaseRemedyRelationCreate, DiseaseRemedyRelationResponse,
    MizajBalanceTreatmentCreate, MizajBalanceTreatmentResponse, MizajBalanceTreatmentUpdate,
    MedicalPlantCreate, MedicalPlantResponse
)
from app.crud.avicenna_diseases import (
    DiseaseOps, SymptomOps, TraditionalRemedyOps,
    DiseaseRemedyRelationOps, MizajBalanceTreatmentOps, MedicalPlantOps
)

router = APIRouter(prefix="/api/v1", tags=["بیماری و درمان"])


# ============ بیماری ============
@router.post("/diseases", response_model=DiseaseResponse)
def create_disease(disease_data: DiseaseCreate, db: Session = Depends(get_db)):
    """ایجاد بیماری جدید"""
    return DiseaseOps.create(db, disease_data)


@router.get("/diseases/{disease_id}", response_model=DiseaseResponse)
def get_disease(disease_id: int, db: Session = Depends(get_db)):
    """دریافت بیماری با ID"""
    disease = DiseaseOps.get_by_id(db, disease_id)
    if not disease:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="بیماری یافت نشد")
    return disease


@router.get("/diseases", response_model=List[DiseaseResponse])
def list_diseases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """دریافت لیست بیماری‌ها"""
    return DiseaseOps.get_all_active(db, skip, limit)


@router.get("/diseases/search/{name}")
def search_diseases(name: str, db: Session = Depends(get_db)):
    """جستجو برای بیماری‌ها بر اساس نام"""
    return DiseaseOps.search_by_name(db, name)


@router.get("/diseases/category/{category}", response_model=List[DiseaseResponse])
def get_diseases_by_category(category: str, db: Session = Depends(get_db)):
    """دریافت بیماری‌های یک دسته"""
    return DiseaseOps.get_by_category(db, category)


@router.get("/diseases/mizaj/{mizaj}", response_model=List[DiseaseResponse])
def get_diseases_by_mizaj(mizaj: str, db: Session = Depends(get_db)):
    """دریافت بیماری‌های مرتبط با مزاج"""
    return DiseaseOps.get_by_mizaj(db, mizaj)


@router.put("/diseases/{disease_id}", response_model=DiseaseResponse)
def update_disease(
    disease_id: int,
    disease_data: dict,
    db: Session = Depends(get_db)
):
    """به‌روزرسانی بیماری"""
    updated = DiseaseOps.update(db, disease_id, disease_data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="بیماری یافت نشد")
    return updated


@router.delete("/diseases/{disease_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_disease(disease_id: int, db: Session = Depends(get_db)):
    """حذف (غیرفعال) بیماری"""
    if not DiseaseOps.deactivate(db, disease_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="بیماری یافت نشد")


# ============ علائم ============
@router.post("/symptoms", response_model=SymptomResponse)
def create_symptom(symptom_data: SymptomCreate, db: Session = Depends(get_db)):
    """ایجاد علامت جدید"""
    return SymptomOps.create(db, symptom_data)


@router.get("/symptoms/{symptom_id}", response_model=SymptomResponse)
def get_symptom(symptom_id: int, db: Session = Depends(get_db)):
    """دریافت علامت با ID"""
    symptom = SymptomOps.get_by_id(db, symptom_id)
    if not symptom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="علامت یافت نشد")
    return symptom


@router.get("/symptoms", response_model=List[SymptomResponse])
def list_symptoms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """دریافت لیست علائم"""
    return SymptomOps.get_all(db, skip, limit)


@router.get("/symptoms/search/{name}")
def search_symptoms(name: str, db: Session = Depends(get_db)):
    """جستجو برای علائم بر اساس نام"""
    return SymptomOps.search_by_name(db, name)


@router.get("/symptoms/disease/{disease_id}", response_model=List[SymptomResponse])
def get_disease_symptoms(disease_id: int, db: Session = Depends(get_db)):
    """دریافت علائم یک بیماری"""
    return SymptomOps.get_for_disease(db, disease_id)


@router.put("/symptoms/{symptom_id}", response_model=SymptomResponse)
def update_symptom(
    symptom_id: int,
    symptom_data: dict,
    db: Session = Depends(get_db)
):
    """به‌روزرسانی علامت"""
    updated = SymptomOps.update(db, symptom_id, symptom_data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="علامت یافت نشد")
    return updated


# ============ درمان سنتی ============
@router.post("/remedies", response_model=TraditionalRemedyResponse)
def create_remedy(remedy_data: TraditionalRemedyCreate, db: Session = Depends(get_db)):
    """ایجاد درمان سنتی جدید"""
    return TraditionalRemedyOps.create(db, remedy_data)


@router.get("/remedies/{remedy_id}", response_model=TraditionalRemedyResponse)
def get_remedy(remedy_id: int, db: Session = Depends(get_db)):
    """دریافت درمان با ID"""
    remedy = TraditionalRemedyOps.get_by_id(db, remedy_id)
    if not remedy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="درمان یافت نشد")
    return remedy


@router.get("/remedies", response_model=List[TraditionalRemedyResponse])
def list_remedies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """دریافت لیست درمان‌ها"""
    return TraditionalRemedyOps.get_all_active(db, skip, limit)


@router.get("/remedies/search/{name}")
def search_remedies(name: str, db: Session = Depends(get_db)):
    """جستجو برای درمان‌ها بر اساس نام"""
    return TraditionalRemedyOps.search_by_name(db, name)


@router.get("/remedies/disease/{disease_id}", response_model=List[TraditionalRemedyResponse])
def get_disease_remedies(disease_id: int, db: Session = Depends(get_db)):
    """دریافت درمان‌های توصیه‌شده برای بیماری"""
    return TraditionalRemedyOps.get_for_disease(db, disease_id)


@router.get("/remedies/type/{remedy_type}", response_model=List[TraditionalRemedyResponse])
def get_remedies_by_type(remedy_type: str, db: Session = Depends(get_db)):
    """دریافت درمان‌های نوع خاص"""
    return TraditionalRemedyOps.get_by_type(db, remedy_type)


@router.get("/remedies/mizaj/{mizaj}", response_model=List[TraditionalRemedyResponse])
def get_remedies_for_mizaj(mizaj: str, db: Session = Depends(get_db)):
    """دریافت درمان‌های برای تعادل مزاج"""
    return TraditionalRemedyOps.get_for_mizaj(db, mizaj)


@router.put("/remedies/{remedy_id}", response_model=TraditionalRemedyResponse)
def update_remedy(
    remedy_id: int,
    remedy_data: dict,
    db: Session = Depends(get_db)
):
    """به‌روزرسانی درمان"""
    updated = TraditionalRemedyOps.update(db, remedy_id, remedy_data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="درمان یافت نشد")
    return updated


# ============ درمان مزاج ============
@router.post("/patients/{patient_id}/mizaj-treatments", response_model=MizajBalanceTreatmentResponse)
def create_mizaj_treatment(
    patient_id: int,
    treatment_data: MizajBalanceTreatmentCreate,
    db: Session = Depends(get_db)
):
    """ایجاد برنامه درمانی برای تعادل مزاج"""
    return MizajBalanceTreatmentOps.create(db, treatment_data, patient_id)


@router.get("/mizaj-treatments/{treatment_id}", response_model=MizajBalanceTreatmentResponse)
def get_mizaj_treatment(treatment_id: int, db: Session = Depends(get_db)):
    """دریافت برنامه درمانی"""
    treatment = MizajBalanceTreatmentOps.get_by_id(db, treatment_id)
    if not treatment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="برنامه درمانی یافت نشد")
    return treatment


@router.get("/patients/{patient_id}/mizaj-treatments", response_model=List[MizajBalanceTreatmentResponse])
def get_patient_mizaj_treatments(patient_id: int, db: Session = Depends(get_db)):
    """دریافت تمام برنامه‌های درمانی برای بیمار"""
    return MizajBalanceTreatmentOps.get_by_patient(db, patient_id)


@router.get("/patients/{patient_id}/mizaj-treatments/active", response_model=Optional[MizajBalanceTreatmentResponse])
def get_active_mizaj_treatment(patient_id: int, db: Session = Depends(get_db)):
    """دریافت برنامه درمانی فعال (تکمیل‌نشده)"""
    return MizajBalanceTreatmentOps.get_active_treatment(db, patient_id)


@router.put("/mizaj-treatments/{treatment_id}", response_model=MizajBalanceTreatmentResponse)
def update_mizaj_treatment(
    treatment_id: int,
    treatment_data: MizajBalanceTreatmentUpdate,
    db: Session = Depends(get_db)
):
    """به‌روزرسانی برنامه درمانی"""
    updated = MizajBalanceTreatmentOps.update(db, treatment_id, treatment_data.dict())
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="برنامه درمانی یافت نشد")
    return updated


# ============ گیاهان دارویی ============
@router.post("/medical-plants", response_model=MedicalPlantResponse)
def create_plant(plant_data: MedicalPlantCreate, db: Session = Depends(get_db)):
    """ایجاد گیاه دارویی جدید"""
    return MedicalPlantOps.create(db, plant_data.dict())


@router.get("/medical-plants/{plant_id}", response_model=MedicalPlantResponse)
def get_plant(plant_id: int, db: Session = Depends(get_db)):
    """دریافت گیاه با ID"""
    plant = MedicalPlantOps.get_by_id(db, plant_id)
    if not plant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="گیاه یافت نشد")
    return plant


@router.get("/medical-plants", response_model=List[MedicalPlantResponse])
def list_plants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """دریافت لیست گیاهان دارویی"""
    return MedicalPlantOps.get_all(db, skip, limit)


@router.get("/medical-plants/search/{name}")
def search_plants(name: str, db: Session = Depends(get_db)):
    """جستجو برای گیاهان بر اساس نام"""
    return MedicalPlantOps.search_by_name(db, name)


@router.get("/medical-plants/disease/{disease_id}", response_model=List[MedicalPlantResponse])
def get_plants_for_disease(disease_id: int, db: Session = Depends(get_db)):
    """دریافت گیاهان برای درمان بیماری"""
    return MedicalPlantOps.get_for_disease(db, disease_id)


@router.get("/medical-plants/mizaj/{mizaj}", response_model=List[MedicalPlantResponse])
def get_plants_for_mizaj(mizaj: str, db: Session = Depends(get_db)):
    """دریافت گیاهان برای تعادل مزاج"""
    return MedicalPlantOps.get_for_mizaj(db, mizaj)


@router.put("/medical-plants/{plant_id}", response_model=MedicalPlantResponse)
def update_plant(
    plant_id: int,
    plant_data: dict,
    db: Session = Depends(get_db)
):
    """به‌روزرسانی گیاه"""
    updated = MedicalPlantOps.update(db, plant_id, plant_data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="گیاه یافت نشد")
    return updated
