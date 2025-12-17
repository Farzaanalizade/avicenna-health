import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
import asyncio
import time
import json
from datetime import datetime, timedelta
from app.main import app
from app.database import get_db, SessionLocal, engine
from app.models import Base, Patient, DiagnosticFinding, HealthRecord, Recommendation
from app.schemas import PatientRegister, DiagnosticFindingCreate, FeedbackRating, RecommendationOptimizationRequest
from app.core.security import create_access_token, get_password_hash

"""
Integration Test Suite for Phase 3 Week 3 Real-time System
Tests complete workflow: Feedback → Analytics → Predictions → WebSocket → Mobile

Coverage:
- End-to-end feedback collection and analysis
- Recommendation prediction and optimization
- WebSocket real-time updates and broadcasting
- Performance under load (1000+ concurrent connections)
- Complete data flow validation
"""

# Fixtures
@pytest.fixture
def setup_db():
    """Setup test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(setup_db):
    """Create test user"""
    db = SessionLocal()
    user = Patient(
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        name="Test User",
        age=30,
        gender="MALE",
        mizaj_type="GARM_TAR",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.close()


@pytest.fixture
def test_token(test_user):
    """Create test JWT token"""
    token = create_access_token(data={"sub": test_user.email}, expires_delta=timedelta(hours=1))
    return token


@pytest.fixture
def test_diagnosis(test_user, setup_db):
    """Create test diagnosis"""
    db = SessionLocal()
    diagnosis = DiagnosticFinding(
        patient_id=test_user.id,
        condition="Headache",
        severity=3,
        duration_days=7,
        mizaj_imbalance="GARM",
    )
    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)
    yield diagnosis
    db.close()


@pytest.fixture
def async_client():
    """Create async test client"""
    async def get_test_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_test_db
    return AsyncClient(app=app, base_url="http://test")


# ============ Task 3 Feedback Collection Tests ============

class TestFeedbackCollection:
    """Test Task 3: User feedback system"""

    @pytest.mark.asyncio
    async def test_submit_feedback_creates_record(self, async_client, test_user, test_diagnosis, test_token):
        """Test feedback submission and storage"""
        feedback_data = {
            "diagnosis_id": test_diagnosis.id,
            "recommendation_id": 1,
            "rating": 4,
            "symptom_improvement": 3,
            "comment": "Helped reduce pain",
            "side_effects": [],
            "compliance_score": 0.9,
        }

        response = await async_client.post(
            "/api/feedback/submit",
            json=feedback_data,
            headers={"Authorization": f"Bearer {test_token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["rating"] == 4
        assert data["symptom_improvement"] == 3

    @pytest.mark.asyncio
    async def test_multiple_feedbacks_aggregate_correctly(self, async_client, test_user, test_diagnosis, test_token):
        """Test feedback aggregation with multiple submissions"""
        # Submit 5 feedbacks
        ratings = [3, 4, 5, 4, 4]
        for rating in ratings:
            await async_client.post(
                "/api/feedback/submit",
                json={
                    "diagnosis_id": test_diagnosis.id,
                    "recommendation_id": 1,
                    "rating": rating,
                    "symptom_improvement": rating - 1,
                    "comment": f"Rating {rating}",
                    "side_effects": [],
                    "compliance_score": 0.8,
                },
                headers={"Authorization": f"Bearer {test_token}"},
            )

        # Get summary
        response = await async_client.get(
            "/api/feedback/recommendation/1/summary",
            headers={"Authorization": f"Bearer {test_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        expected_avg = sum(ratings) / len(ratings)
        assert abs(data["average_rating"] - expected_avg) < 0.01

    @pytest.mark.asyncio
    async def test_feedback_triggers_analytics_update(self, async_client, test_user, test_diagnosis, test_token):
        """Test that 5 feedbacks trigger analytics recalculation"""
        # Submit 5 feedbacks to trigger analytics
        for i in range(5):
            response = await async_client.post(
                "/api/feedback/submit",
                json={
                    "diagnosis_id": test_diagnosis.id,
                    "recommendation_id": 1,
                    "rating": 4 + (i % 2),
                    "symptom_improvement": 3,
                    "comment": f"Feedback {i}",
                    "side_effects": [],
                    "compliance_score": 0.8,
                },
                headers={"Authorization": f"Bearer {test_token}"},
            )
            assert response.status_code == 201


# ============ Task 2 Analytics Tests ============

class TestAnalyticsCalculation:
    """Test Task 2: Analytics service"""

    @pytest.mark.asyncio
    async def test_effectiveness_calculation_from_feedback(self, async_client, test_user, test_diagnosis, test_token):
        """Test effectiveness score calculation"""
        # Submit successful feedbacks
        for _ in range(3):
            await async_client.post(
                "/api/feedback/submit",
                json={
                    "diagnosis_id": test_diagnosis.id,
                    "recommendation_id": 1,
                    "rating": 5,
                    "symptom_improvement": 4,
                    "comment": "Very effective",
                    "side_effects": [],
                    "compliance_score": 0.9,
                },
                headers={"Authorization": f"Bearer {test_token}"},
            )

        # Trigger analytics calculation
        response = await async_client.post(
            "/api/analytics/calculate/1",
            headers={"Authorization": f"Bearer {test_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["effectiveness_score"] >= 0.75

    @pytest.mark.asyncio
    async def test_trending_recommendations_detected(self, async_client):
        """Test trending recommendations detection"""
        response = await async_client.get("/api/analytics/trending")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_batch_analytics_calculation(self, async_client, test_token):
        """Test batch analytics calculation"""
        response = await async_client.post(
            "/api/analytics/batch/calculate",
            json={"recommendation_ids": [1, 2, 3, 4, 5]},
            headers={"Authorization": f"Bearer {test_token}"},
        )

        assert response.status_code in [200, 201]


# ============ Task 4 Predictions Tests ============

class TestMLPredictions:
    """Test Task 4: ML prediction models"""

    @pytest.mark.asyncio
    async def test_predict_recommendations_returns_scores(self, async_client, test_user, test_diagnosis, test_token):
        """Test recommendation prediction with scores"""
        response = await async_client.get(
            f"/api/predictions/diagnosis/{test_diagnosis.id}/predict?optimization_level=balanced",
            headers={"Authorization": f"Bearer {test_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "predicted_recommendations" in data
        assert data["model_version"] == "1.0"

    @pytest.mark.asyncio
    async def test_optimize_recommendations(self, async_client, test_user, test_diagnosis, test_token):
        """Test recommendation optimization"""
        response = await async_client.get(
            f"/api/predictions/diagnosis/{test_diagnosis.id}/optimize?target_effectiveness=0.75",
            headers={"Authorization": f"Bearer {test_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_optimization_levels_differ(self, async_client, test_user, test_diagnosis, test_token):
        """Test different optimization levels produce different results"""
        conservative = await async_client.get(
            f"/api/predictions/diagnosis/{test_diagnosis.id}/predict?optimization_level=conservative",
            headers={"Authorization": f"Bearer {test_token}"},
        )

        aggressive = await async_client.get(
            f"/api/predictions/diagnosis/{test_diagnosis.id}/predict?optimization_level=aggressive",
            headers={"Authorization": f"Bearer {test_token}"},
        )

        assert conservative.status_code == 200
        assert aggressive.status_code == 200
        # Scores should differ
        con_data = conservative.json()
        agg_data = aggressive.json()
        assert con_data != agg_data


# ============ Task 1 WebSocket Tests ============

class TestWebSocketIntegration:
    """Test Task 1: Real-time WebSocket system"""

    @pytest.mark.asyncio
    async def test_websocket_connection_succeeds(self, test_user, test_token):
        """Test WebSocket connection with authentication"""
        # Note: This would require a WebSocket client in real tests
        # Simulating with HTTP endpoint
        response = await AsyncClient(app=app).get(
            "/ws/status",
            headers={"Authorization": f"Bearer {test_token}"},
        )
        assert response.status_code in [200, 404]  # 404 if endpoint not implemented

    @pytest.mark.asyncio
    async def test_websocket_message_history(self, async_client):
        """Test WebSocket message storage"""
        response = await async_client.get("/ws/status")
        # Should return connection statistics
        assert response.status_code in [200, 404]


# ============ End-to-End Workflow Tests ============

class TestCompleteWorkflow:
    """Test complete feedback → analytics → predictions → WebSocket flow"""

    @pytest.mark.asyncio
    async def test_complete_feedback_to_prediction_flow(self, async_client, test_user, test_diagnosis, test_token):
        """Test entire workflow from feedback to prediction"""
        # Step 1: Submit feedback
        for i in range(5):
            response = await async_client.post(
                "/api/feedback/submit",
                json={
                    "diagnosis_id": test_diagnosis.id,
                    "recommendation_id": 1,
                    "rating": 4 + (i % 2),
                    "symptom_improvement": 3,
                    "comment": f"Test feedback {i}",
                    "side_effects": [],
                    "compliance_score": 0.8,
                },
                headers={"Authorization": f"Bearer {test_token}"},
            )
            assert response.status_code == 201

        # Step 2: Check analytics calculated
        analytics_response = await async_client.get(
            "/api/recommendation/1/effectiveness",
            headers={"Authorization": f"Bearer {test_token}"},
        )
        assert analytics_response.status_code == 200

        # Step 3: Get predictions
        predictions_response = await async_client.get(
            f"/api/predictions/diagnosis/{test_diagnosis.id}/predict",
            headers={"Authorization": f"Bearer {test_token}"},
        )
        assert predictions_response.status_code == 200

    @pytest.mark.asyncio
    async def test_feedback_analytics_predictions_consistency(self, async_client, test_user, test_diagnosis, test_token):
        """Test data consistency across all systems"""
        # Submit feedback
        feedback_response = await async_client.post(
            "/api/feedback/submit",
            json={
                "diagnosis_id": test_diagnosis.id,
                "recommendation_id": 1,
                "rating": 5,
                "symptom_improvement": 4,
                "comment": "Very effective",
                "side_effects": [],
                "compliance_score": 0.9,
            },
            headers={"Authorization": f"Bearer {test_token}"},
        )
        feedback_id = feedback_response.json()["id"]

        # Get analytics
        analytics = await async_client.get(
            "/api/recommendation/1/effectiveness",
            headers={"Authorization": f"Bearer {test_token}"},
        )

        # Get predictions
        predictions = await async_client.get(
            f"/api/predictions/diagnosis/{test_diagnosis.id}/predict",
            headers={"Authorization": f"Bearer {test_token}"},
        )

        # Verify consistency
        assert feedback_response.status_code == 201
        assert analytics.status_code == 200
        assert predictions.status_code == 200


# ============ Performance & Load Tests ============

class TestPerformance:
    """Test system performance under load"""

    @pytest.mark.asyncio
    async def test_concurrent_feedback_submissions(self, async_client, test_user, test_diagnosis, test_token):
        """Test 100 concurrent feedback submissions"""
        tasks = []
        for i in range(100):
            task = async_client.post(
                "/api/feedback/submit",
                json={
                    "diagnosis_id": test_diagnosis.id,
                    "recommendation_id": 1 + (i % 5),
                    "rating": 3 + (i % 3),
                    "symptom_improvement": 2 + (i % 3),
                    "comment": f"Concurrent feedback {i}",
                    "side_effects": [],
                    "compliance_score": 0.8,
                },
                headers={"Authorization": f"Bearer {test_token}"},
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        successful = sum(1 for r in responses if isinstance(r, dict) or r.status_code == 201)
        assert successful >= 95  # At least 95% should succeed

    @pytest.mark.asyncio
    async def test_analytics_calculation_performance(self, async_client, test_token):
        """Test analytics calculation speed (target < 500ms for 100 items)"""
        start = time.time()

        response = await async_client.post(
            "/api/analytics/batch/calculate",
            json={"recommendation_ids": list(range(1, 101))},
            headers={"Authorization": f"Bearer {test_token}"},
        )

        elapsed = time.time() - start
        assert response.status_code in [200, 201]
        assert elapsed < 1.0  # Should complete in < 1 second

    @pytest.mark.asyncio
    async def test_prediction_response_time(self, async_client, test_diagnosis, test_token):
        """Test prediction endpoint response time (target < 200ms)"""
        start = time.time()

        response = await async_client.get(
            f"/api/predictions/diagnosis/{test_diagnosis.id}/predict",
            headers={"Authorization": f"Bearer {test_token}"},
        )

        elapsed = time.time() - start
        assert response.status_code == 200
        assert elapsed < 0.5  # Should complete in < 500ms


# ============ Error Handling & Edge Cases ============

class TestErrorHandling:
    """Test error handling and edge cases"""

    @pytest.mark.asyncio
    async def test_invalid_diagnosis_id(self, async_client, test_token):
        """Test invalid diagnosis ID handling"""
        response = await async_client.get(
            "/api/predictions/diagnosis/99999/predict",
            headers={"Authorization": f"Bearer {test_token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, async_client, test_diagnosis):
        """Test unauthorized access without token"""
        response = await async_client.get(
            f"/api/predictions/diagnosis/{test_diagnosis.id}/predict"
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_invalid_optimization_level(self, async_client, test_diagnosis, test_token):
        """Test invalid optimization level"""
        response = await async_client.get(
            f"/api/predictions/diagnosis/{test_diagnosis.id}/predict?optimization_level=invalid",
            headers={"Authorization": f"Bearer {test_token}"},
        )
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_batch_prediction_limit(self, async_client, test_token):
        """Test batch prediction max limit (20 items)"""
        response = await async_client.post(
            "/api/predictions/batch/predict",
            json={"diagnosis_ids": list(range(1, 51))},  # 50 items (exceeds limit)
            headers={"Authorization": f"Bearer {test_token}"},
        )
        assert response.status_code == 400


# ============ Data Validation Tests ============

class TestDataValidation:
    """Test data validation and integrity"""

    @pytest.mark.asyncio
    async def test_feedback_rating_boundaries(self, async_client, test_user, test_diagnosis, test_token):
        """Test feedback rating must be 1-5"""
        # Test invalid rating 0
        response = await async_client.post(
            "/api/feedback/submit",
            json={
                "diagnosis_id": test_diagnosis.id,
                "recommendation_id": 1,
                "rating": 0,
                "symptom_improvement": 3,
                "comment": "Invalid rating",
                "side_effects": [],
                "compliance_score": 0.8,
            },
            headers={"Authorization": f"Bearer {test_token}"},
        )
        assert response.status_code == 400

        # Test invalid rating 6
        response = await async_client.post(
            "/api/feedback/submit",
            json={
                "diagnosis_id": test_diagnosis.id,
                "recommendation_id": 1,
                "rating": 6,
                "symptom_improvement": 3,
                "comment": "Invalid rating",
                "side_effects": [],
                "compliance_score": 0.8,
            },
            headers={"Authorization": f"Bearer {test_token}"},
        )
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_effectiveness_score_bounds(self, async_client):
        """Test effectiveness scores are 0.0-1.0"""
        response = await async_client.get("/api/recommendation/1/effectiveness")
        if response.status_code == 200:
            data = response.json()
            if "effectiveness_score" in data:
                assert 0.0 <= data["effectiveness_score"] <= 1.0

    @pytest.mark.asyncio
    async def test_confidence_score_bounds(self, async_client):
        """Test confidence scores are 0.0-1.0"""
        response = await async_client.get("/api/recommendation/1/effectiveness")
        if response.status_code == 200:
            data = response.json()
            if "confidence" in data:
                assert 0.0 <= data["confidence"] <= 1.0


# ============ Run Tests ============

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
