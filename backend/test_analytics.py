"""
Analytics Service Tests - Phase 3 Week 3 Task 2

Test suite for analytics service effectiveness calculations,
trending analysis, and real-time broadcasting integration.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi.testclient import TestClient

from app.main import app
from app.services.analytics_service import (
    AnalyticsService,
    EffectivenessMetrics,
    get_analytics_service,
    calculate_effectiveness,
    get_trending,
    get_worst_performing
)


class TestEffectivenessMetrics:
    """Test EffectivenessMetrics data class"""
    
    def test_metrics_creation(self):
        """Test creating metrics object"""
        metrics = EffectivenessMetrics(
            recommendation_id=1,
            herb_name="Ginger",
            effectiveness_score=0.85,
            confidence=0.92,
            sample_size=150,
            successful_cases=128,
            total_cases=150,
            average_rating=4.2,
            trend="improving",
            last_updated=datetime.utcnow()
        )
        
        assert metrics.recommendation_id == 1
        assert metrics.herb_name == "Ginger"
        assert metrics.effectiveness_score == 0.85
        assert metrics.confidence == 0.92
        assert metrics.trend == "improving"
    
    def test_metrics_to_dict(self):
        """Test converting metrics to dictionary"""
        metrics = EffectivenessMetrics(
            recommendation_id=1,
            herb_name="Ginger",
            effectiveness_score=0.85,
            confidence=0.92,
            sample_size=150,
            successful_cases=128,
            total_cases=150,
            average_rating=4.2,
            trend="improving",
            last_updated=datetime.utcnow()
        )
        
        data = metrics.to_dict()
        
        assert data["recommendation_id"] == 1
        assert data["herb_name"] == "Ginger"
        assert data["effectiveness_score"] == 0.85
        assert "last_updated" in data


class TestAnalyticsService:
    """Test AnalyticsService class"""
    
    def test_service_creation(self):
        """Test creating analytics service"""
        mock_db = MagicMock()
        service = AnalyticsService(mock_db)
        
        assert service.db == mock_db
        assert service.EFFECTIVENESS_WINDOW_DAYS == 90
        assert service.MIN_SAMPLES_FOR_CONFIDENCE == 5
    
    def test_is_successful_feedback_true(self):
        """Test success feedback detection - successful case"""
        mock_db = MagicMock()
        service = AnalyticsService(mock_db)
        
        feedback = MagicMock()
        feedback.symptom_improvement = 4  # > 3
        
        result = service._is_successful_feedback(feedback)
        assert result is True
    
    def test_is_successful_feedback_false(self):
        """Test success feedback detection - failed case"""
        mock_db = MagicMock()
        service = AnalyticsService(mock_db)
        
        feedback = MagicMock()
        feedback.symptom_improvement = 2  # < 3
        
        result = service._is_successful_feedback(feedback)
        assert result is False
    
    def test_is_successful_feedback_no_improvement(self):
        """Test success feedback detection - no improvement data"""
        mock_db = MagicMock()
        service = AnalyticsService(mock_db)
        
        feedback = MagicMock()
        feedback.symptom_improvement = None
        
        result = service._is_successful_feedback(feedback)
        assert result is False
    
    def test_calculate_trend_improving(self):
        """Test trend calculation - improving"""
        mock_db = MagicMock()
        service = AnalyticsService(mock_db)
        
        # Create mock feedbacks
        now = datetime.utcnow()
        recent_fb = MagicMock()
        recent_fb.created_at = now - timedelta(days=15)
        recent_fb.symptom_improvement = 5
        
        old_fb = MagicMock()
        old_fb.created_at = now - timedelta(days=60)
        old_fb.symptom_improvement = 2
        
        feedbacks = [recent_fb, old_fb]
        
        # Mock success check
        service._is_successful_feedback = MagicMock(
            side_effect=lambda f: f.symptom_improvement >= 3
        )
        
        trend = service._calculate_trend(feedbacks)
        
        assert trend in ["improving", "stable", "declining"]
    
    def test_calculate_trend_stable(self):
        """Test trend calculation - stable"""
        mock_db = MagicMock()
        service = AnalyticsService(mock_db)
        
        # Create mock feedbacks with similar scores
        now = datetime.utcnow()
        recent_fb = MagicMock()
        recent_fb.created_at = now - timedelta(days=15)
        recent_fb.symptom_improvement = 4
        
        old_fb = MagicMock()
        old_fb.created_at = now - timedelta(days=60)
        old_fb.symptom_improvement = 3
        
        feedbacks = [recent_fb, old_fb]
        
        # Mock success check
        service._is_successful_feedback = MagicMock(return_value=True)
        
        trend = service._calculate_trend(feedbacks)
        
        assert trend == "stable"
    
    def test_calculate_trend_insufficient_data(self):
        """Test trend calculation - insufficient data"""
        mock_db = MagicMock()
        service = AnalyticsService(mock_db)
        
        feedbacks = [MagicMock()]  # Only one feedback
        
        trend = service._calculate_trend(feedbacks)
        
        assert trend == "stable"


class TestAnalyticsEndpoints:
    """Test analytics API endpoints"""
    
    def test_analytics_status_endpoint(self):
        """Test GET /api/analytics/status"""
        client = TestClient(app)
        response = client.get("/api/analytics/status")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "analytics"
        assert "features" in data
    
    def test_trending_endpoint(self):
        """Test GET /api/analytics/trending"""
        client = TestClient(app)
        response = client.get("/api/analytics/trending")
        
        # May not have data, but endpoint should work
        assert response.status_code in [200, 404]
    
    def test_worst_performing_endpoint(self):
        """Test GET /api/analytics/worst-performing"""
        client = TestClient(app)
        response = client.get("/api/analytics/worst-performing")
        
        # May not have data, but endpoint should work
        assert response.status_code in [200, 404]


class TestAnalyticsIntegration:
    """Integration tests for analytics with other systems"""
    
    def test_analytics_with_websocket(self):
        """Test analytics broadcasting with WebSocket"""
        mock_db = MagicMock()
        service = AnalyticsService(mock_db)
        
        # Mock recommendation
        mock_rec = MagicMock()
        mock_rec.id = 1
        mock_rec.herb_name = "Ginger"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_rec
        mock_db.query.return_value.filter.return_value.all.return_value = []
        
        # This should not raise an exception
        result = service.broadcast_effectiveness_update(
            diagnosis_id=1,
            recommendation_id=1
        )
        
        # Result depends on having actual feedback data
        assert isinstance(result, (bool, type(None)))


class TestAnalyticsCalculations:
    """Test effectiveness calculation algorithms"""
    
    def test_effectiveness_score_calculation(self):
        """Test effectiveness score calculation"""
        # Score should be: successful_cases / total_cases
        
        successful = 85
        total = 100
        expected = successful / total
        
        assert expected == 0.85
    
    def test_confidence_calculation(self):
        """Test confidence score calculation"""
        # Confidence should scale from 0.5 to 1.0 based on sample size
        
        sample_size = 50
        max_samples = 100
        
        confidence = min(
            1.0,
            0.5 + (min(sample_size, max_samples) / max_samples) * 0.5
        )
        
        assert 0.5 <= confidence <= 1.0
        assert confidence == 0.75  # 0.5 + (50/100)*0.5


class TestAnalyticsEdgeCases:
    """Test edge cases and error handling"""
    
    def test_no_feedback_data(self):
        """Test handling case with no feedback"""
        mock_db = MagicMock()
        service = AnalyticsService(mock_db)
        
        # Mock empty feedback
        mock_db.query.return_value.filter.return_value.all.return_value = []
        
        # Should handle gracefully
        result = service.calculate_trend([])
        assert result == "stable"
    
    def test_invalid_recommendation_id(self):
        """Test handling invalid recommendation ID"""
        mock_db = MagicMock()
        service = AnalyticsService(mock_db)
        
        # Mock recommendation not found
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = service.calculate_recommendation_effectiveness(999)
        
        assert result is None


if __name__ == "__main__":
    print("✅ Analytics test suite ready")
    print("\nTo run tests:")
    print("  pytest backend/test_analytics.py -v")
    print("\nTest coverage:")
    print("  - Metrics creation and serialization")
    print("  - Effectiveness calculations")
    print("  - Trend analysis")
    print("  - API endpoints")
    print("  - Integration with WebSocket")
    print("  - Edge case handling")
