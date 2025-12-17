"""
Test suite for Feedback Service and Router
Tests feedback submission, retrieval, analytics, and WebSocket integration
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
from app.services.feedback_service import (
    FeedbackService, FeedbackRating, FeedbackSummary, get_feedback_service
)
from app.core.security import create_access_token


# ===========================
# Test Database Setup
# ===========================

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_feedback.db"
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
def test_patient(test_db):
    """Create test patient"""
    patient = Patient(
        email="test@example.com",
        hashed_password="hashed_pass",
        gender="MALE",
        age=35,
        mizaj_type="GARM_TAR"
    )
    test_db.add(patient)
    test_db.commit()
    test_db.refresh(patient)
    return patient


@pytest.fixture
def test_diagnosis(test_db, test_patient):
    """Create test diagnosis"""
    diagnosis = DiagnosticFinding(
        patient_id=test_patient.id,
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
            effectiveness_rating=4.0,
            created_at=datetime.utcnow()
        )
        test_db.add(rec)
        test_db.commit()
        test_db.refresh(rec)
        recs.append(rec)
    return recs


@pytest.fixture
def auth_headers(test_patient):
    """Get auth headers with JWT token"""
    token = create_access_token({"sub": str(test_patient.id)})
    return {"Authorization": f"Bearer {token}"}


# ===========================
# Test FeedbackService
# ===========================

class TestFeedbackService:
    """Test FeedbackService class"""

    def test_service_creation(self, test_db):
        """Test service initialization"""
        service = get_feedback_service(test_db)
        assert service is not None
        assert service.db == test_db

    @pytest.mark.asyncio
    async def test_submit_feedback_success(self, test_db, test_patient, test_diagnosis, test_recommendations):
        """Test successful feedback submission"""
        service = get_feedback_service(test_db)
        
        feedback_data = FeedbackRating(
            recommendation_id=test_recommendations[0].id,
            diagnosis_id=test_diagnosis.id,
            rating=5,
            symptom_improvement=4,
            comment="بسیار موثر بود",
            compliance_score=5
        )

        result = await service.submit_feedback(test_patient.id, feedback_data)

        assert result is not None
        assert result.rating == 5
        assert result.symptom_improvement == 4
        assert result.comment == "بسیار موثر بود"

    @pytest.mark.asyncio
    async def test_submit_feedback_unauthorized_diagnosis(self, test_db, test_patient, test_recommendations):
        """Test feedback submission to unauthorized diagnosis"""
        service = get_feedback_service(test_db)
        
        # Create another patient and diagnosis
        other_patient = Patient(
            email="other@example.com",
            hashed_password="pass",
            gender="FEMALE",
            age=28,
            mizaj_type="SARD_TAR"
        )
        test_db.add(other_patient)
        test_db.commit()

        other_diagnosis = DiagnosticFinding(
            patient_id=other_patient.id,
            condition_name="حمی",
            severity=2,
            primary_finding="سرد و تر"
        )
        test_db.add(other_diagnosis)
        test_db.commit()

        feedback_data = FeedbackRating(
            recommendation_id=test_recommendations[0].id,
            diagnosis_id=other_diagnosis.id,
            rating=3,
            symptom_improvement=3
        )

        # Current patient tries to submit feedback to other patient's diagnosis
        result = await service.submit_feedback(test_patient.id, feedback_data)
        assert result is None

    @pytest.mark.asyncio
    async def test_update_feedback(self, test_db, test_patient, test_diagnosis, test_recommendations):
        """Test feedback update"""
        service = get_feedback_service(test_db)
        
        # First submit
        feedback_data = FeedbackRating(
            recommendation_id=test_recommendations[0].id,
            diagnosis_id=test_diagnosis.id,
            rating=3,
            symptom_improvement=2
        )
        
        result1 = await service.submit_feedback(test_patient.id, feedback_data)
        health_record_id = result1.id

        # Update feedback
        updated_data = FeedbackRating(
            recommendation_id=test_recommendations[0].id,
            diagnosis_id=test_diagnosis.id,
            rating=5,
            symptom_improvement=5,
            comment="بعد از تغییر نظر"
        )

        result2 = await service.update_feedback(test_patient.id, health_record_id, updated_data)

        assert result2.rating == 5
        assert result2.symptom_improvement == 5
        assert result2.comment == "بعد از تغییر نظر"

    def test_get_feedback_history(self, test_db, test_patient, test_diagnosis, test_recommendations):
        """Test retrieving feedback history"""
        service = get_feedback_service(test_db)

        # Submit multiple feedbacks
        for i, rec in enumerate(test_recommendations):
            health_record = HealthRecord(
                patient_id=test_patient.id,
                recommendation_id=rec.id,
                diagnosis_id=test_diagnosis.id,
                rating=3 + i,
                symptom_improvement=2 + i,
                comment=f"تست {i}",
                created_at=datetime.utcnow()
            )
            test_db.add(health_record)
        test_db.commit()

        history = service.get_feedback_history(test_patient.id)

        assert len(history) == 3
        assert history[0].rating >= 3

    def test_get_feedback_history_filtered(self, test_db, test_patient, test_diagnosis, test_recommendations):
        """Test filtering feedback history"""
        service = get_feedback_service(test_db)

        # Submit feedbacks
        for rec in test_recommendations:
            health_record = HealthRecord(
                patient_id=test_patient.id,
                recommendation_id=rec.id,
                diagnosis_id=test_diagnosis.id,
                rating=4,
                symptom_improvement=3
            )
            test_db.add(health_record)
        test_db.commit()

        # Filter by recommendation
        history = service.get_feedback_history(
            test_patient.id,
            recommendation_id=test_recommendations[0].id
        )

        assert len(history) == 1

    def test_recommendation_feedback_summary(self, test_db, test_diagnosis, test_recommendations):
        """Test feedback summary calculation"""
        service = get_feedback_service(test_db)

        # Add multiple feedbacks
        for rating in [3, 4, 5, 5, 4]:
            health_record = HealthRecord(
                patient_id=1,
                recommendation_id=test_recommendations[0].id,
                diagnosis_id=test_diagnosis.id,
                rating=rating,
                symptom_improvement=rating - 1,
                compliance_score=5
            )
            test_db.add(health_record)
        test_db.commit()

        summary = service.get_recommendation_feedback_summary(test_recommendations[0].id)

        assert summary is not None
        assert summary.total_feedbacks == 5
        assert summary.average_rating == 4.2
        assert summary.positive_feedback_percentage == 100.0

    def test_feedback_summary_with_side_effects(self, test_db, test_diagnosis, test_recommendations):
        """Test side effects aggregation in summary"""
        service = get_feedback_service(test_db)

        # Add feedbacks with side effects
        side_effects_list = ["سردرد", "تهوع", "سردرد", "ضعف"]
        for effects in side_effects_list:
            health_record = HealthRecord(
                patient_id=1,
                recommendation_id=test_recommendations[0].id,
                diagnosis_id=test_diagnosis.id,
                rating=3,
                symptom_improvement=2,
                side_effects=effects
            )
            test_db.add(health_record)
        test_db.commit()

        summary = service.get_recommendation_feedback_summary(test_recommendations[0].id)

        assert len(summary.side_effects_reported) == 3
        assert "سردرد" in summary.side_effects_reported

    def test_feedback_trend_improving(self, test_db, test_diagnosis, test_recommendations):
        """Test trend analysis - improving"""
        service = get_feedback_service(test_db)

        # Old feedbacks (lower rating)
        for _ in range(3):
            health_record = HealthRecord(
                patient_id=1,
                recommendation_id=test_recommendations[0].id,
                diagnosis_id=test_diagnosis.id,
                rating=2,
                symptom_improvement=2,
                created_at=datetime.utcnow() - timedelta(days=60)
            )
            test_db.add(health_record)

        # Recent feedbacks (higher rating)
        for _ in range(3):
            health_record = HealthRecord(
                patient_id=1,
                recommendation_id=test_recommendations[0].id,
                diagnosis_id=test_diagnosis.id,
                rating=4,
                symptom_improvement=4,
                created_at=datetime.utcnow() - timedelta(days=5)
            )
            test_db.add(health_record)

        test_db.commit()

        trend = service.get_feedback_trend(test_recommendations[0].id)

        assert trend is not None
        assert trend.trend_direction == "improving"
        assert trend.recent_average > trend.older_average

    def test_feedback_trend_declining(self, test_db, test_diagnosis, test_recommendations):
        """Test trend analysis - declining"""
        service = get_feedback_service(test_db)

        # Old feedbacks (higher rating)
        for _ in range(3):
            health_record = HealthRecord(
                patient_id=1,
                recommendation_id=test_recommendations[0].id,
                diagnosis_id=test_diagnosis.id,
                rating=5,
                symptom_improvement=4,
                created_at=datetime.utcnow() - timedelta(days=60)
            )
            test_db.add(health_record)

        # Recent feedbacks (lower rating)
        for _ in range(3):
            health_record = HealthRecord(
                patient_id=1,
                recommendation_id=test_recommendations[0].id,
                diagnosis_id=test_diagnosis.id,
                rating=2,
                symptom_improvement=2,
                created_at=datetime.utcnow() - timedelta(days=5)
            )
            test_db.add(health_record)

        test_db.commit()

        trend = service.get_feedback_trend(test_recommendations[0].id)

        assert trend is not None
        assert trend.trend_direction == "declining"
        assert trend.recent_average < trend.older_average

    def test_diagnosis_feedback_overview(self, test_db, test_diagnosis, test_recommendations):
        """Test diagnosis-level feedback overview"""
        service = get_feedback_service(test_db)

        # Add feedbacks for all recommendations
        for rec in test_recommendations:
            for _ in range(2):
                health_record = HealthRecord(
                    patient_id=1,
                    recommendation_id=rec.id,
                    diagnosis_id=test_diagnosis.id,
                    rating=4,
                    symptom_improvement=3
                )
                test_db.add(health_record)
        test_db.commit()

        overview = service.get_diagnosis_feedback_overview(test_diagnosis.id)

        assert overview["diagnosis_id"] == test_diagnosis.id
        assert overview["total_recommendations"] == 3
        assert len(overview["recommendations"]) == 3


# ===========================
# Test Feedback Endpoints
# ===========================

class TestFeedbackEndpoints:
    """Test feedback API endpoints"""

    def test_submit_feedback_endpoint(self, test_db, test_patient, test_diagnosis, 
                                       test_recommendations, auth_headers, cleanup_db):
        """Test POST /api/feedback/submit endpoint"""
        feedback_data = {
            "recommendation_id": test_recommendations[0].id,
            "diagnosis_id": test_diagnosis.id,
            "rating": 5,
            "symptom_improvement": 4,
            "comment": "بسیار موثر",
            "compliance_score": 5
        }

        response = client.post(
            "/api/feedback/submit",
            json=feedback_data,
            headers=auth_headers
        )

        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert "data" in response.json()

    def test_feedback_history_endpoint(self, test_db, test_patient, test_diagnosis,
                                       test_recommendations, auth_headers, cleanup_db):
        """Test GET /api/feedback/history endpoint"""
        # Add feedback
        health_record = HealthRecord(
            patient_id=test_patient.id,
            recommendation_id=test_recommendations[0].id,
            diagnosis_id=test_diagnosis.id,
            rating=4,
            symptom_improvement=3,
            comment="test"
        )
        test_db.add(health_record)
        test_db.commit()

        response = client.get(
            "/api/feedback/history",
            headers=auth_headers
        )

        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["count"] >= 0

    def test_recommendation_summary_endpoint(self, test_db, test_diagnosis,
                                            test_recommendations, cleanup_db):
        """Test GET /api/feedback/recommendation/{id}/summary endpoint"""
        # Add feedbacks
        for _ in range(3):
            health_record = HealthRecord(
                patient_id=1,
                recommendation_id=test_recommendations[0].id,
                diagnosis_id=test_diagnosis.id,
                rating=4,
                symptom_improvement=3
            )
            test_db.add(health_record)
        test_db.commit()

        response = client.get(
            f"/api/feedback/recommendation/{test_recommendations[0].id}/summary"
        )

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["total_feedbacks"] == 3
        assert data["average_rating"] == 4.0

    def test_health_endpoint(self, cleanup_db):
        """Test GET /api/feedback/health endpoint"""
        response = client.get("/api/feedback/health")

        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["service"] == "feedback"


# ===========================
# Test Edge Cases
# ===========================

class TestFeedbackEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_feedback_summary(self, test_db, test_recommendations):
        """Test summary with no feedback"""
        service = get_feedback_service(test_db)
        summary = service.get_recommendation_feedback_summary(test_recommendations[0].id)

        assert summary is None

    def test_insufficient_feedback_for_trend(self, test_db, test_diagnosis, test_recommendations):
        """Test trend with insufficient feedback"""
        service = get_feedback_service(test_db)

        # Add only 1 feedback
        health_record = HealthRecord(
            patient_id=1,
            recommendation_id=test_recommendations[0].id,
            diagnosis_id=test_diagnosis.id,
            rating=3,
            symptom_improvement=2
        )
        test_db.add(health_record)
        test_db.commit()

        trend = service.get_feedback_trend(test_recommendations[0].id)

        assert trend is None

    def test_invalid_recommendation_id(self, test_db):
        """Test with invalid recommendation ID"""
        service = get_feedback_service(test_db)
        summary = service.get_recommendation_feedback_summary(99999)

        assert summary is None

    @pytest.mark.asyncio
    async def test_batch_feedback_submission(self, test_db, test_patient, test_diagnosis,
                                             test_recommendations, auth_headers, cleanup_db):
        """Test batch feedback submission"""
        feedbacks = [
            {
                "recommendation_id": test_recommendations[0].id,
                "diagnosis_id": test_diagnosis.id,
                "rating": 4,
                "symptom_improvement": 3
            },
            {
                "recommendation_id": test_recommendations[1].id,
                "diagnosis_id": test_diagnosis.id,
                "rating": 5,
                "symptom_improvement": 4
            }
        ]

        response = client.post(
            "/api/feedback/batch/submit",
            json=feedbacks,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["total"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
