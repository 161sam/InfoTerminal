"""
Test suite for feedback-aggregator service v1 migration.

Tests the v1 API endpoints and service integration to ensure
the migration from the legacy monolithic main.py is successful.
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, Mock

from fastapi.testclient import TestClient
from service import FeedbackService, FeedbackAnalyzer
from models.requests import FeedbackCreate, FeedbackType, Priority, Status


class MockRequest:
    """Mock request object for testing dependencies."""
    def __init__(self, feedback_service):
        self.app = Mock()
        self.app.state = Mock()
        self.app.state.feedback_service = feedback_service


class TestFeedbackAnalyzer:
    """Test the feedback analysis engine."""
    
    def setup_method(self):
        self.analyzer = FeedbackAnalyzer()
    
    def test_sentiment_analysis_positive(self):
        """Test positive sentiment detection."""
        text = "this is great and excellent work"
        sentiment = self.analyzer._analyze_sentiment(text)
        assert sentiment == "positive"
    
    def test_sentiment_analysis_negative(self):
        """Test negative sentiment detection."""
        text = "this is terrible and broken"
        sentiment = self.analyzer._analyze_sentiment(text)
        assert sentiment == "negative"
    
    def test_sentiment_analysis_neutral(self):
        """Test neutral sentiment when no keywords match."""
        text = "this is some regular text"
        sentiment = self.analyzer._analyze_sentiment(text)
        assert sentiment == "neutral"
    
    def test_urgency_analysis(self):
        """Test urgency level detection."""
        critical_text = "system crash error urgent"
        urgency = self.analyzer._analyze_urgency(critical_text)
        assert urgency == "critical"
        
        low_text = "minor cosmetic improvement"
        urgency = self.analyzer._analyze_urgency(low_text)
        assert urgency == "low"
    
    def test_tag_extraction(self):
        """Test automatic tag extraction."""
        text = "the search interface is slow and needs performance improvements"
        tags = self.analyzer._extract_tags(text)
        assert "search" in tags
        assert "performance" in tags
        assert "ui" in tags
    
    def test_priority_suggestion(self):
        """Test priority suggestion based on type and content."""
        bug_feedback = FeedbackCreate(
            session_id="test",
            feedback_type=FeedbackType.BUG_REPORT,
            title="Critical system crash",
            description="The system crashes when loading data",
            page_url="http://test.com",
            user_agent="test"
        )
        
        analysis = self.analyzer.analyze_feedback(bug_feedback)
        assert analysis["suggested_priority"] in [Priority.HIGH, Priority.CRITICAL]
        assert analysis["sentiment"] in ["positive", "negative", "neutral"]
        assert analysis["urgency"] in ["critical", "high", "medium", "low"]
        assert isinstance(analysis["extracted_tags"], list)
        assert isinstance(analysis["confidence_score"], float)
        assert 0 <= analysis["confidence_score"] <= 1


class TestFeedbackServiceIntegration:
    """Test the main feedback service integration."""
    
    @pytest.fixture
    def mock_service(self):
        """Create a mock feedback service for testing."""
        service = Mock(spec=FeedbackService)
        
        # Mock successful responses
        service.create_feedback = AsyncMock(return_value=Mock(
            id=1,
            title="Test feedback",
            description="Test description",
            feedback_type=FeedbackType.BUG_REPORT,
            priority=Priority.MEDIUM,
            status=Status.NEW,
            votes=0,
            created_at=datetime.utcnow()
        ))
        
        service.get_feedback_by_id = AsyncMock(return_value=Mock(
            id=1,
            title="Test feedback",
            feedback_type=FeedbackType.BUG_REPORT
        ))
        
        service.get_feedback_stats = AsyncMock(return_value=Mock(
            total_feedback=10,
            by_type={"bug_report": 5, "feature_request": 3},
            by_priority={"medium": 7, "high": 3},
            by_status={"new": 8, "resolved": 2},
            by_sentiment={"neutral": 6, "negative": 4},
            average_rating=3.5,
            top_tags=[{"tag": "ui", "count": 5}],
            recent_trends={"this_week": 3},
            resolution_metrics={"average_days": 2.5}
        ))
        
        service.get_health_status = AsyncMock(return_value=Mock(
            status="healthy",
            service="feedback-aggregator",
            database_healthy=True,
            redis_healthy=True,
            github_integration_healthy=True,
            total_feedback=10,
            pending_analysis=0,
            recent_activity=5,
            uptime_seconds=3600,
            memory_usage_mb=128
        ))
        
        return service
    
    def test_router_dependency_injection(self, mock_service):
        """Test that the router properly injects the service dependency."""
        from routers.feedback_aggregator_v1 import get_feedback_service
        
        mock_request = MockRequest(mock_service)
        injected_service = get_feedback_service(mock_request)
        
        assert injected_service == mock_service
    
    @pytest.mark.asyncio
    async def test_create_feedback_endpoint(self, mock_service):
        """Test the create feedback endpoint with mock service."""
        from routers.feedback_aggregator_v1 import create_feedback
        from models.requests import FeedbackCreate
        
        feedback_data = FeedbackCreate(
            session_id="test_session",
            feedback_type=FeedbackType.BUG_REPORT,
            title="Test bug report",
            description="This is a test bug report description",
            page_url="http://test.com/page",
            user_agent="Mozilla/5.0 Test Browser"
        )
        
        background_tasks = Mock()
        
        # Mock the service method
        mock_service.create_feedback.return_value = Mock(
            id=1,
            title="Test bug report",
            description="This is a test bug report description",
            feedback_type=FeedbackType.BUG_REPORT
        )
        
        result = await create_feedback(feedback_data, background_tasks, mock_service)
        
        # Verify service was called with correct parameters
        mock_service.create_feedback.assert_called_once_with(feedback_data, background_tasks)
        assert result.title == "Test bug report"
    
    @pytest.mark.asyncio
    async def test_get_feedback_stats_endpoint(self, mock_service):
        """Test the feedback stats endpoint."""
        from routers.feedback_aggregator_v1 import get_feedback_statistics
        
        result = await get_feedback_statistics(mock_service)
        
        mock_service.get_feedback_stats.assert_called_once()
        assert result.total_feedback == 10
        assert "bug_report" in result.by_type
    
    @pytest.mark.asyncio 
    async def test_health_endpoint(self, mock_service):
        """Test the health status endpoint."""
        from routers.feedback_aggregator_v1 import get_feedback_health
        
        result = await get_feedback_health(mock_service)
        
        mock_service.get_health_status.assert_called_once()
        assert result.status == "healthy"
        assert result.service == "feedback-aggregator"


class TestV1AppIntegration:
    """Test the v1 app integration and startup."""
    
    def test_app_creation(self):
        """Test that the v1 app creates successfully."""
        from app_v1 import app
        
        assert app.title == "Feedback Aggregator Service"
        assert app.version == "1.0.0"
        assert not app.deprecated  # Should not be deprecated
    
    def test_legacy_compatibility_endpoints(self):
        """Test that legacy endpoints return proper deprecation responses."""
        from main import app as legacy_app
        
        client = TestClient(legacy_app)
        
        # Test deprecated health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["deprecated"] == True
        assert "new_endpoint" in response.json()
        
        # Test moved endpoints return 410
        response = client.get("/feedback")
        assert response.status_code == 410
        assert response.json()["error_code"] == "ENDPOINT_MOVED"


def test_models_import():
    """Test that all models can be imported successfully."""
    from models import (
        FeedbackCreate, FeedbackResponse, FeedbackStats,
        FeedbackType, Priority, Status, Sentiment
    )
    
    # Verify enums work correctly
    assert FeedbackType.BUG_REPORT == "bug_report"
    assert Priority.HIGH == "high"
    assert Status.NEW == "new"
    assert Sentiment.POSITIVE == "positive"


def test_service_analyzer_integration():
    """Test that the service and analyzer integrate correctly."""
    analyzer = FeedbackAnalyzer()
    
    feedback = FeedbackCreate(
        session_id="test",
        feedback_type=FeedbackType.FEATURE_REQUEST,
        title="Add search functionality",
        description="We need better search with filters",
        page_url="http://test.com",
        user_agent="test"
    )
    
    analysis = analyzer.analyze_feedback(feedback)
    
    # Verify analysis structure
    required_keys = ["sentiment", "urgency", "suggested_priority", "extracted_tags", "estimated_effort", "confidence_score"]
    for key in required_keys:
        assert key in analysis
    
    # Verify types
    assert isinstance(analysis["extracted_tags"], list)
    assert isinstance(analysis["confidence_score"], float)
    assert analysis["suggested_priority"] in [p.value for p in Priority]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
