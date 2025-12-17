"""
CRUD operations برای بیماری‌ها و درمان‌های سنتی
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.avicenna_diseases import (
    Disease, Symptom, DiseaseSymptomRelation, TraditionalRemedy,
    DiseaseRemediRelation, MizajBalanceTreatment, MedicalPlant
)
from app.schemas.avicenna_diseases import (
    DiseaseCreate, SymptomCreate, TraditionalRemedyCreate,
    DiseaseRemedyRelationCreate, MizajBalanceTreatmentCreate
)


# ============ بیماری ============
class DiseaseOps:
    @staticmethod
    def create(db: Session, disease_data: DiseaseCreate) -> Disease:
        """ایجاد بیماری جدید"""
        db_disease = Disease(**disease_data.dict())
        db.add(db_disease)
        db.commit()
        db.refresh(db_disease)
        return db_disease

    @staticmethod
    def get_by_id(db: Session, disease_id: int) -> Optional[Disease]:
        """دریافت بیماری با ID"""
        return db.query(Disease).filter(Disease.id == disease_id).first()

    @staticmethod
    def get_all_active(db: Session, skip: int = 0, limit: int = 100) -> List[Disease]:
        """دریافت تمام بیماری‌های فعال"""
        return db.query(Disease).filter(Disease.is_active == True).offset(skip).limit(limit).all()

    @staticmethod
    def search_by_name(db: Session, name: str) -> List[Disease]:
        """جستجو بر اساس نام"""
        return db.query(Disease).filter(
            (Disease.name_fa.contains(name)) | 
            (Disease.name_ar.contains(name)) |
            (Disease.name_latin.contains(name))
        ).filter(Disease.is_active == True).all()

    @staticmethod
    def get_by_mizaj(db: Session, mizaj: str) -> List[Disease]:
        """دریافت بیماری‌های مرتبط با یک مزاج"""
        # JSON query برای PostgreSQL یا دیگر DB‌ها
        return db.query(Disease).filter(
            Disease.related_mizaj.contains([mizaj])
        ).filter(Disease.is_active == True).all()

    @staticmethod
    def get_by_category(db: Session, category: str) -> List[Disease]:
        """دریافت بیماری‌های یک دسته"""
        return db.query(Disease).filter(Disease.category == category).filter(
            Disease.is_active == True
        ).all()

    @staticmethod
    def update(db: Session, disease_id: int, disease_data: dict) -> Optional[Disease]:
        """به‌روزرسانی بیماری"""
        db_disease = DiseaseOps.get_by_id(db, disease_id)
        if db_disease:
            for key, value in disease_data.items():
                if value is not None:
                    setattr(db_disease, key, value)
            db.commit()
            db.refresh(db_disease)
        return db_disease

    @staticmethod
    def deactivate(db: Session, disease_id: int) -> bool:
        """غیرفعال کردن بیماری"""
        db_disease = DiseaseOps.get_by_id(db, disease_id)
        if db_disease:
            db_disease.is_active = False
            db.commit()
            return True
        return False


# ============ علائم ============
class SymptomOps:
    @staticmethod
    def create(db: Session, symptom_data: SymptomCreate) -> Symptom:
        """ایجاد علامت جدید"""
        db_symptom = Symptom(**symptom_data.dict())
        db.add(db_symptom)
        db.commit()
        db.refresh(db_symptom)
        return db_symptom

    @staticmethod
    def get_by_id(db: Session, symptom_id: int) -> Optional[Symptom]:
        """دریافت علامت با ID"""
        return db.query(Symptom).filter(Symptom.id == symptom_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Symptom]:
        """دریافت تمام علائم"""
        return db.query(Symptom).offset(skip).limit(limit).all()

    @staticmethod
    def search_by_name(db: Session, name: str) -> List[Symptom]:
        """جستجو بر اساس نام علامت"""
        return db.query(Symptom).filter(
            (Symptom.name_fa.contains(name)) | 
            (Symptom.name_ar.contains(name))
        ).all()

    @staticmethod
    def get_by_mizaj(db: Session, mizaj: str) -> List[Symptom]:
        """دریافت علائم مرتبط با یک مزاج"""
        return db.query(Symptom).filter(
            Symptom.mizaj_related.contains([mizaj])
        ).all()

    @staticmethod
    def get_for_disease(db: Session, disease_id: int) -> List[Symptom]:
        """دریافت علائم یک بیماری"""
        return db.query(Symptom).join(DiseaseSymptomRelation).filter(
            DiseaseSymptomRelation.disease_id == disease_id
        ).all()

    @staticmethod
    def update(db: Session, symptom_id: int, symptom_data: dict) -> Optional[Symptom]:
        """به‌روزرسانی علامت"""
        db_symptom = SymptomOps.get_by_id(db, symptom_id)
        if db_symptom:
            for key, value in symptom_data.items():
                if value is not None:
                    setattr(db_symptom, key, value)
            db.commit()
            db.refresh(db_symptom)
        return db_symptom


# ============ درمان سنتی ============
class TraditionalRemedyOps:
    @staticmethod
    def create(db: Session, remedy_data: TraditionalRemedyCreate) -> TraditionalRemedy:
        """ایجاد درمان سنتی جدید"""
        db_remedy = TraditionalRemedy(**remedy_data.dict())
        db.add(db_remedy)
        db.commit()
        db.refresh(db_remedy)
        return db_remedy

    @staticmethod
    def get_by_id(db: Session, remedy_id: int) -> Optional[TraditionalRemedy]:
        """دریافت درمان با ID"""
        return db.query(TraditionalRemedy).filter(TraditionalRemedy.id == remedy_id).first()

    @staticmethod
    def get_all_active(db: Session, skip: int = 0, limit: int = 100) -> List[TraditionalRemedy]:
        """دریافت تمام درمان‌های فعال"""
        return db.query(TraditionalRemedy).filter(TraditionalRemedy.is_active == True).offset(skip).limit(limit).all()

    @staticmethod
    def search_by_name(db: Session, name: str) -> List[TraditionalRemedy]:
        """جستجو بر اساس نام درمان"""
        return db.query(TraditionalRemedy).filter(
            (TraditionalRemedy.name_fa.contains(name)) | 
            (TraditionalRemedy.name_ar.contains(name))
        ).filter(TraditionalRemedy.is_active == True).all()

    @staticmethod
    def get_for_disease(db: Session, disease_id: int) -> List[TraditionalRemedy]:
        """دریافت درمان‌های توصیه‌شده برای یک بیماری"""
        return db.query(TraditionalRemedy).join(DiseaseRemediRelation).filter(
            DiseaseRemediRelation.disease_id == disease_id
        ).filter(TraditionalRemedy.is_active == True).all()

    @staticmethod
    def get_by_type(db: Session, remedy_type: str) -> List[TraditionalRemedy]:
        """دریافت درمان‌های نوع خاص"""
        return db.query(TraditionalRemedy).filter(TraditionalRemedy.remedy_type == remedy_type).filter(
            TraditionalRemedy.is_active == True
        ).all()

    @staticmethod
    def get_for_mizaj(db: Session, mizaj: str) -> List[TraditionalRemedy]:
        """دریافت درمان‌های برای تعادل مزاج"""
        return db.query(TraditionalRemedy).filter(
            TraditionalRemedy.effect_on_mizaj.contains([mizaj])
        ).filter(TraditionalRemedy.is_active == True).all()

    @staticmethod
    def update(db: Session, remedy_id: int, remedy_data: dict) -> Optional[TraditionalRemedy]:
        """به‌روزرسانی درمان"""
        db_remedy = TraditionalRemedyOps.get_by_id(db, remedy_id)
        if db_remedy:
            for key, value in remedy_data.items():
                if value is not None:
                    setattr(db_remedy, key, value)
            db.commit()
            db.refresh(db_remedy)
        return db_remedy


# ============ معادله درمان و بیماری ============
class DiseaseRemedyRelationOps:
    @staticmethod
    def create(db: Session, relation_data: DiseaseRemedyRelationCreate) -> DiseaseRemediRelation:
        """ایجاد رابطه بیماری-درمان"""
        db_relation = DiseaseRemediRelation(**relation_data.dict())
        db.add(db_relation)
        db.commit()
        db.refresh(db_relation)
        return db_relation

    @staticmethod
    def get_primary_remedies_for_disease(db: Session, disease_id: int) -> List[TraditionalRemedy]:
        """دریافت درمان‌های اولیه برای بیماری"""
        return db.query(TraditionalRemedy).join(DiseaseRemediRelation).filter(
            DiseaseRemediRelation.disease_id == disease_id,
            DiseaseRemediRelation.is_primary_treatment == True
        ).all()


# ============ درمان برای تعادل مزاج ============
class MizajBalanceTreatmentOps:
    @staticmethod
    def create(db: Session, treatment_data: MizajBalanceTreatmentCreate, patient_id: int) -> MizajBalanceTreatment:
        """ایجاد برنامه درمانی برای تعادل مزاج"""
        db_treatment = MizajBalanceTreatment(patient_id=patient_id, **treatment_data.dict())
        db.add(db_treatment)
        db.commit()
        db.refresh(db_treatment)
        return db_treatment

    @staticmethod
    def get_by_id(db: Session, treatment_id: int) -> Optional[MizajBalanceTreatment]:
        """دریافت برنامه درمانی با ID"""
        return db.query(MizajBalanceTreatment).filter(MizajBalanceTreatment.id == treatment_id).first()

    @staticmethod
    def get_by_patient(db: Session, patient_id: int) -> List[MizajBalanceTreatment]:
        """دریافت تمام برنامه‌های درمانی برای بیمار"""
        return db.query(MizajBalanceTreatment).filter(MizajBalanceTreatment.patient_id == patient_id).order_by(
            MizajBalanceTreatment.created_at.desc()
        ).all()

    @staticmethod
    def get_active_treatment(db: Session, patient_id: int) -> Optional[MizajBalanceTreatment]:
        """دریافت برنامه درمانی فعال (تکمیل‌نشده)"""
        return db.query(MizajBalanceTreatment).filter(
            MizajBalanceTreatment.patient_id == patient_id,
            MizajBalanceTreatment.is_completed == False
        ).order_by(MizajBalanceTreatment.created_at.desc()).first()

    @staticmethod
    def update(db: Session, treatment_id: int, treatment_data: dict) -> Optional[MizajBalanceTreatment]:
        """به‌روزرسانی برنامه درمانی"""
        db_treatment = MizajBalanceTreatmentOps.get_by_id(db, treatment_id)
        if db_treatment:
            for key, value in treatment_data.items():
                if value is not None:
                    setattr(db_treatment, key, value)
            db.commit()
            db.refresh(db_treatment)
        return db_treatment


# ============ گیاهان دارویی ============
class MedicalPlantOps:
    @staticmethod
    def create(db: Session, plant_data: dict) -> MedicalPlant:
        """ایجاد گیاه دارویی جدید"""
        db_plant = MedicalPlant(**plant_data)
        db.add(db_plant)
        db.commit()
        db.refresh(db_plant)
        return db_plant

    @staticmethod
    def get_by_id(db: Session, plant_id: int) -> Optional[MedicalPlant]:
        """دریافت گیاه با ID"""
        return db.query(MedicalPlant).filter(MedicalPlant.id == plant_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[MedicalPlant]:
        """دریافت تمام گیاهان دارویی"""
        return db.query(MedicalPlant).offset(skip).limit(limit).all()

    @staticmethod
    def search_by_name(db: Session, name: str) -> List[MedicalPlant]:
        """جستجو بر اساس نام"""
        return db.query(MedicalPlant).filter(
            (MedicalPlant.name_fa.contains(name)) | 
            (MedicalPlant.name_ar.contains(name)) |
            (MedicalPlant.name_scientific.contains(name))
        ).all()

    @staticmethod
    def get_for_disease(db: Session, disease_id: int) -> List[MedicalPlant]:
        """دریافت گیاهان برای درمان بیماری"""
        remedies = db.query(TraditionalRemedy).join(DiseaseRemediRelation).filter(
            DiseaseRemediRelation.disease_id == disease_id
        ).all()
        
        plants = []
        for remedy in remedies:
            if remedy.remedy_type == "herbal":
                plant = MedicalPlantOps.search_by_name(db, remedy.name_fa)
                plants.extend(plant)
        
        return list(set(plants))  # Remove duplicates

    @staticmethod
    def get_for_mizaj(db: Session, mizaj: str) -> List[MedicalPlant]:
        """دریافت گیاهان برای تعادل مزاج"""
        return db.query(MedicalPlant).filter(
            MedicalPlant.balances_mizaj.contains([mizaj])
        ).all()

    @staticmethod
    def update(db: Session, plant_id: int, plant_data: dict) -> Optional[MedicalPlant]:
        """به‌روزرسانی گیاه"""
        db_plant = MedicalPlantOps.get_by_id(db, plant_id)
        if db_plant:
            for key, value in plant_data.items():
                if value is not None:
                    setattr(db_plant, key, value)
            db.commit()
            db.refresh(db_plant)
        return db_plant
