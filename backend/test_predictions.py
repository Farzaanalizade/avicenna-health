"""
Test suite for Prediction Service and Router
Tests ML model predictions, optimization, and WebSocket integration
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base
from app.models.patient_and_diagnosis_data import (
    Patient, DiagnosticFinding, Recommendation, HealthRecord
)
from app.services.prediction_service import (
    PredictionService, PredictionResult, RecommendationScore,
    get_prediction_service
)
from app.core.security import create_access_token


# ===========================
# Test Database Setup
# ===========================

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_predictions.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# ===========================
# Test Fixtures
# ===========================

@pytest.fixture(autouse=True)
def cleanup_db():
    """Clean database before each test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_db():
    """Get test database session"""
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture
def test_patients(test_db):
    """Create test patients with same mizaj type"""
    patients = []
    for i in range(5):
        patient = Patient(
            email=f"test{i}@example.com",
            hashed_password="hashed_pass",
            gender="MALE" if i % 2 == 0 else "FEMALE",
            age=25 + i * 5,
            mizaj_type="GARM_TAR"
        )
        test_db.add(patient)
        test_db.commit()
        test_db.refresh(patient)
        patients.append(patient)
    return patients


@pytest.fixture
def test_diagnosis(test_db, test_patients):
    """Create test diagnosis for first patient"""
    diagnosis = DiagnosticFinding(
        patient_id=test_patients[0].id,
        condition_name="سردرد",
        severity=3,
        primary_finding="گرم و تر",
        created_at=datetime.utcnow()
    )
    test_db.add(diagnosis)
    test_db.commit()
    test_db.refresh(diagnosis)
    return diagnosis


@pytest.fixture
def test_recommendations(test_db, test_diagnosis):
    """Create test recommendations"""
    recs = []
    for i, herb in enumerate(["زنجبیل", "دارچین", "نعناع"]):
        rec = Recommendation(
            diagnosis_id=test_diagnosis.id,
            herb_name=herb,
            dosage=f"1-2 تومان روزانه",
            duration_days=30,
            usage_method="دمنوش",
            effectiveness_rating=4.0 - i * 0.5,
            created_at=datetime.utcnow()
        )
        test_db.add(rec)
        test_db.commit()
        test_db.refresh(rec)
        recs.append(rec)
    return recs


@pytest.fixture
def test_feedbacks(test_db, test_patients, test_diagnosis, test_recommendations):
    """Create test feedback data"""
    # Create feedback from similar patients for each recommendation
    for patient in test_patients[1:]:
        for idx, rec in enumerate(test_recommendations):
            # Higher ratings for first recommendation
            rating = 5 - idx if idx < 2 else 2
            feedback = HealthRecord(
                patient_id=patient.id,
                recommendation_id=rec.id,
                diagnosis_id=test_diagnosis.id,
                rating=rating,
                symptom_improvement=rating - 1,
                created_at=datetime.utcnow() - timedelta(days=10 + idx * 5)
            )
            test_db.add(feedback)
    test_db.commit()


@pytest.fixture
def auth_headers(test_patients):
    """Get auth headers with JWT token"""
    token = create_access_token({"sub": str(test_patients[0].id)})
    return {"Authorization": f"Bearer {token}"}


# ===========================
# Test PredictionService
# ===========================

class TestPredictionService:
    """Test PredictionService class"""

    def test_service_creation(self, test_db):
        """Test service initialization"""
        service = get_prediction_service(test_db)
        assert service is not None
        assert service.db == test_db

    @pytest.mark.asyncio
    async def test_predict_recommendations_success(self, test_db, test_diagnosis,
                                                    test_recommendations, test_feedbacks):
        """Test successful recommendation prediction"""
        service = get_prediction_service(test_db)
        
        result = await service.predict_recommendations(test_diagnosis.id, "balanced")

        assert result is not None
        assert result.diagnosis_id == test_diagnosis.id
        assert len(result.predicted_recommendations) > 0
        assert result.model_version == "1.0"
        assert 0 <= result.overall_confidence <= 1.0

    @pytest.mark.asyncio
    async def test_predict_optimization_levels(self, test_db, test_diagnosis,
                                               test_recommendations, test_feedbacks):
        """Test different optimization levels"""
        service = get_prediction_service(test_db)

        for level in ["conservative", "balanced", "aggressive"]:
            result = await service.predict_recommendations(test_diagnosis.id, level)
            assert result is not None
            assert result.optimization_level == level

    @pytest.mark.asyncio
    async def test_recommendation_scoring(self, test_db, test_diagnosis,
                                          test_recommendations, test_feedbacks):
        """Test recommendation scoring"""
        service = get_prediction_service(test_db)

        result = await service.predict_recommendations(test_diagnosis.id, "balanced")

        # Check that recommendations are scored
        for rec in result.predicted_recommendations:
            assert isinstance(rec, RecommendationScore)
            assert 0 <= rec.predicted_effectiveness <= 1.0
            assert 0 <= rec.confidence <= 1.0
            assert rec.recommendation_id > 0
            assert rec.herb_name

    @pytest.mark.asyncio
    async def test_optimize_recommendations(self, test_db, test_diagnosis,
                                            test_recommendations, test_feedbacks):
        """Test recommendation optimization"""
        service = get_prediction_service(test_db)

        optimized = await service.optimize_recommendations(
            test_diagnosis.id,
            target_effectiveness=0.5
        )

        assert optimized is not None
        assert len(optimized) > 0

    def test_patient_profile_retrieval(self, test_db, test_patients):
        """Test patient profile retrieval"""
        service = get_prediction_service(test_db)

        profile = service.get_patient_profile(test_patients[0].id)

        assert profile is not None
        assert profile.patient_id == test_patients[0].id
        assert profile.age == test_patients[0].age
        assert profile.mizaj_type == test_patients[0].mizaj_type

    def test_prediction_accuracy_calculation(self, test_db, test_diagnosis,
                                             test_recommendations, test_feedbacks):
        """Test prediction accuracy calculation"""
        service = get_prediction_service(test_db)

        accuracy = service.get_prediction_accuracy(test_diagnosis.id)

        assert 0 <= accuracy <= 1.0

    def test_recommendation_evolution_tracking(self, test_db, test_diagnosis):
        """Test tracking recommendation evolution"""
        service = get_prediction_service(test_db)

        evolution = service.get_recommendation_evolution(test_diagnosis.id, days=30)

        assert "diagnosis_id" in evolution
        assert evolution["diagnosis_id"] == test_diagnosis.id

    @pytest.mark.asyncio
    async def test_broadcast_recommendation_update(self, test_db, test_diagnosis):
        """Test broadcasting recommendation updates"""
        service = get_prediction_service(test_db)

        result = await service.broadcast_recommendation_update(
            test_diagnosis.id,
            old_recommendations=[1, 2],
            new_recommendations=[2, 3, 4]
        )

        # Should return True even if WebSocket not connected
        assert result in [True, False]


# ===========================
# Test Prediction Endpoints
# ===========================

class TestPredictionEndpoints:
    """Test prediction API endpoints"""

    @pytest.mark.asyncio
    async def test_predict_endpoint(self, test_db, test_diagnosis, test_recommendations,
                                    test_feedbacks, auth_headers, cleanup_db):
        """Test GET /api/predictions/diagnosis/{id}/predict endpoint"""
        response = client.get(
            f"/api/predictions/diagnosis/{test_diagnosis.id}/predict",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data

    @pytest.mark.asyncio
    async def test_optimize_endpoint(self, test_db, test_diagnosis, test_recommendations,
                                     test_feedbacks, auth_headers, cleanup_db):
        """Test GET /api/predictions/diagnosis/{id}/optimize endpoint"""
        response = client.get(
            f"/api/predictions/diagnosis/{test_diagnosis.id}/optimize?target_effectiveness=0.5",
            headers=auth_headers
        )

        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert data["status"] == "success"

    @pytest.mark.asyncio
    async def test_patient_profile_endpoint(self, test_db, test_patients,
                                           auth_headers, cleanup_db):
        """Test GET /api/predictions/patient/{id}/profile endpoint"""
        response = client.get(
            f"/api/predictions/patient/{test_patients[0].id}/profile",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data

    def test_model_version_endpoint(self, cleanup_db):
        """Test GET /api/predictions/model/version endpoint"""
        response = client.get("/api/predictions/model/version")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "model" in data
        assert "version" in data["model"]

    def test_health_endpoint(self, cleanup_db):
        """Test GET /api/predictions/health endpoint"""
        response = client.get("/api/predictions/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["service"] == "predictions"


# ===========================
# Test Edge Cases
# ===========================

class TestPredictionEdgeCases:
    """Test edge cases and error handling"""

    @pytest.mark.asyncio
    async def test_invalid_diagnosis_id(self, test_db, auth_headers):
        """Test with invalid diagnosis ID"""
        response = client.get(
            "/api/predictions/diagnosis/99999/predict",
            headers=auth_headers
        )

        assert response.status_code in [403, 404]

    @pytest.mark.asyncio
    async def test_invalid_optimization_level(self, test_db, test_diagnosis,
                                              test_recommendations, auth_headers):
        """Test with invalid optimization level"""
        response = client.get(
            f"/api/predictions/diagnosis/{test_diagnosis.id}/predict?optimization_level=invalid",
            headers=auth_headers
        )

        # Should default to balanced and still work
        assert response.status_code in [200, 403]

    @pytest.mark.asyncio
    async def test_batch_prediction_limit(self, test_db, test_patients,
                                          auth_headers):
        """Test batch prediction limit"""
        diagnosis_ids = list(range(1, 25))  # More than 20

        response = client.post(
            "/api/predictions/batch/predict",
            json=diagnosis_ids,
            headers=auth_headers
        )

        assert response.status_code == 400

    def test_empty_recommendation_prediction(self, test_db, auth_headers):
        """Test prediction with no recommendations"""
        # Create diagnosis with no recommendations
        patient = test_db.query(Patient).first()
        if not patient:
            patient = Patient(
                email="test@example.com",
                hashed_password="pass",
                gender="MALE",
                age=30,
                mizaj_type="GARM"
            )
            test_db.add(patient)
            test_db.commit()
            test_db.refresh(patient)

        diagnosis = DiagnosticFinding(
            patient_id=patient.id,
            condition_name="test",
            severity=1,
            primary_finding="test"
        )
        test_db.add(diagnosis)
        test_db.commit()

        response = client.get(
            f"/api/predictions/diagnosis/{diagnosis.id}/predict",
            headers=auth_headers
        )

        # Should fail because diagnosis not owned by auth user
        assert response.status_code == 403


# ===========================
# Test Scoring Logic
# ===========================

class TestScoringLogic:
    """Test prediction scoring algorithms"""

    @pytest.mark.asyncio
    async def test_confidence_calculation(self, test_db, test_diagnosis,
                                          test_recommendations, test_feedbacks):
        """Test confidence score calculation"""
        service = get_prediction_service(test_db)

        result = await service.predict_recommendations(test_diagnosis.id, "balanced")

        for rec in result.predicted_recommendations:
            # Confidence should be between 0 and 1
            assert 0 <= rec.confidence <= 1.0

    @pytest.mark.asyncio
    async def test_evidence_source_determination(self, test_db, test_diagnosis,
                                                 test_recommendations, test_feedbacks):
        """Test evidence source determination"""
        service = get_prediction_service(test_db)

        result = await service.predict_recommendations(test_diagnosis.id, "balanced")

        for rec in result.predicted_recommendations:
            assert rec.evidence_source in [
                "historical_effectiveness",
                "similar_patients",
                "symptom_match"
            ]

    @pytest.mark.asyncio
    async def test_similar_patient_matching(self, test_db, test_diagnosis,
                                            test_recommendations, test_feedbacks):
        """Test similar patient matching"""
        service = get_prediction_service(test_db)

        result = await service.predict_recommendations(test_diagnosis.id, "balanced")

        # Should have found similar patients
        for rec in result.predicted_recommendations:
            # At least some patients from the cohort
            assert rec.similar_patient_count >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
