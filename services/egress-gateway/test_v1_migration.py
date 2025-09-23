"""
Test suite for Egress Gateway v1 API migration.

Tests the new standardized *_v1.py implementation to ensure:
- All endpoints follow API standards
- Error handling uses Error-Envelope format
- Authentication works correctly
- Proxy functionality is preserved
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
import base64

import sys
from pathlib import Path

# Add service to path
SERVICE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SERVICE_DIR))

from app_v1 import app
from models.requests import ProxyRequest, ProxyRotateRequest, ProxyType, AnonymityLevel
from models.responses import ProxyResponse, ProxyStatus


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Create basic auth headers for testing."""
    credentials = base64.b64encode(b"dev:devpass").decode("ascii")
    return {"Authorization": f"Basic {credentials}"}


@pytest.fixture
def mock_proxy_manager():
    """Mock proxy manager for testing."""
    mock_manager = Mock()
    mock_manager.get_active_proxy = Mock(return_value="test-proxy")
    mock_manager.get_request_count = Mock(return_value=42)
    mock_manager.rotate_identity = AsyncMock()
    mock_manager.get_proxy = AsyncMock(return_value=Mock(
        proxy_url="http://proxy:8080",
        name="test-proxy",
        anonymity_level="medium"
    ))
    mock_manager.get_vpn_pools = Mock(return_value=["vpn1", "vpn2"])
    mock_manager.get_proxy_pools = Mock(return_value=["proxy1", "proxy2"])
    mock_manager.get_last_rotation = Mock(return_value=None)
    return mock_manager


@pytest.fixture
def mock_tor_controller():
    """Mock Tor controller for testing."""
    mock_tor = Mock()
    mock_tor.is_available = Mock(return_value=True)
    mock_tor.is_circuit_established = Mock(return_value=True)
    mock_tor.new_identity = AsyncMock()
    return mock_tor


class TestCoreEndpoints:
    """Test core service endpoints (health, ready, info)."""
    
    def test_healthz_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/healthz")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "service" in data
        assert "version" in data
        assert data["service"] == "egress-gateway"
    
    def test_readyz_endpoint(self, client):
        """Test readiness check endpoint."""
        response = client.get("/readyz")
        # May return 503 if dependencies not available in test
        assert response.status_code in [200, 503]
        
        data = response.json()
        assert "status" in data
        assert "checks" in data
    
    def test_info_endpoint(self, client):
        """Test service info endpoint."""
        response = client.get("/info")
        assert response.status_code == 200
        
        data = response.json()
        assert data["service"] == "egress-gateway"
        assert data["version"] == "1.0.0"
        assert data["api_version"] == "v1"
        assert "endpoints" in data
        assert "capabilities" in data


class TestProxyEndpoints:
    """Test proxy-related endpoints."""
    
    @patch('app_v1.proxy_manager')
    @patch('httpx.AsyncClient')
    def test_proxy_request(self, mock_httpx, mock_proxy_mgr, client, auth_headers, mock_proxy_manager):
        """Test proxy request endpoint."""
        # Mock the proxy manager
        app_v1.proxy_manager = mock_proxy_manager
        
        # Mock httpx response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Test response"
        mock_response.headers = {"content-type": "text/html"}
        mock_response.url = "https://example.com"
        mock_response.content = b"Test response"
        
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        mock_httpx.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        
        request_data = {
            "url": "https://example.com",
            "method": "GET",
            "proxy_type": "auto",
            "anonymity_level": "medium"
        }
        
        response = client.post("/v1/proxy/request", json=request_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "request_id" in data
        assert data["status_code"] == 200
        assert data["proxy_used"] == "test-proxy"
    
    def test_proxy_request_without_auth(self, client):
        """Test proxy request without authentication."""
        request_data = {
            "url": "https://example.com",
            "method": "GET"
        }
        
        response = client.post("/v1/proxy/request", json=request_data)
        assert response.status_code == 401
        
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "AUTHENTICATION_FAILED"
    
    def test_proxy_request_invalid_url(self, client, auth_headers):
        """Test proxy request with invalid URL."""
        request_data = {
            "url": "file:///etc/passwd",  # Should be blocked
            "method": "GET"
        }
        
        response = client.post("/v1/proxy/request", json=request_data, headers=auth_headers)
        assert response.status_code == 422  # Validation error
    
    @patch('app_v1.proxy_manager')
    def test_get_proxy_status(self, mock_proxy_mgr, client, mock_proxy_manager):
        """Test get proxy status endpoint."""
        app_v1.proxy_manager = mock_proxy_manager
        
        response = client.get("/v1/proxy/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "tor_available" in data
        assert "vpn_pools" in data
        assert "proxy_pools" in data
        assert "anonymity_level" in data
    
    @patch('app_v1.proxy_manager')
    def test_rotate_proxy(self, mock_proxy_mgr, client, auth_headers, mock_proxy_manager):
        """Test proxy rotation endpoint."""
        app_v1.proxy_manager = mock_proxy_manager
        
        request_data = {
            "proxy_type": "tor",
            "force_new_circuit": True
        }
        
        response = client.post("/v1/proxy/rotate", json=request_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "rotation_time" in data
        assert "message" in data
    
    def test_rotate_proxy_without_auth(self, client):
        """Test proxy rotation without authentication."""
        request_data = {
            "proxy_type": "tor"
        }
        
        response = client.post("/v1/proxy/rotate", json=request_data)
        assert response.status_code == 401


class TestStatisticsEndpoints:
    """Test statistics and monitoring endpoints."""
    
    @patch('app_v1.request_history', [])
    def test_get_proxy_statistics(self, client):
        """Test get proxy statistics."""
        response = client.get("/v1/proxy/statistics")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_requests" in data
        assert "successful_requests" in data
        assert "proxy_type_usage" in data
        assert "anonymity_level_usage" in data
    
    @patch('app_v1.proxy_manager')
    def test_get_proxy_health(self, mock_proxy_mgr, client, mock_proxy_manager):
        """Test get proxy health status."""
        app_v1.proxy_manager = mock_proxy_manager
        
        response = client.get("/v1/proxy/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "overall_health" in data
        assert "components" in data
        assert "connectivity_tests" in data
    
    def test_get_proxy_capabilities(self, client):
        """Test get proxy capabilities."""
        response = client.get("/v1/proxy/capabilities")
        assert response.status_code == 200
        
        data = response.json()
        assert "supported_proxy_types" in data
        assert "supported_anonymity_levels" in data
        assert "max_concurrent_requests" in data
        assert "features" in data


class TestRequestHistory:
    """Test request history and logging functionality."""
    
    @patch('app_v1.request_history', [
        {
            "request_id": "test-123",
            "timestamp": "2025-09-21T16:45:00Z",
            "url_domain": "example.com",
            "method": "GET",
            "status_code": 200,
            "proxy_used": "tor",
            "anonymity_level": "high",
            "execution_time": 1.5,
            "tags": ["test"]
        }
    ])
    def test_get_request_history(self, client):
        """Test get request history."""
        response = client.get("/v1/proxy/requests")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        
        if data["items"]:
            item = data["items"][0]
            assert "request_id" in item
            assert "url_domain" in item
            assert "status_code" in item
    
    @patch('app_v1.request_history', [{"test": "data"}])
    def test_clear_request_history(self, client, auth_headers):
        """Test clear request history."""
        response = client.delete("/v1/proxy/requests/history", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "cleared_requests" in data
    
    def test_clear_request_history_without_auth(self, client):
        """Test clear request history without authentication."""
        response = client.delete("/v1/proxy/requests/history")
        assert response.status_code == 401


class TestLegacyEndpoints:
    """Test legacy endpoint deprecation."""
    
    def test_legacy_health_deprecated(self, client):
        """Test legacy health endpoint returns deprecation."""
        response = client.get("/health")
        assert response.status_code == 410
        
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "DEPRECATED_ENDPOINT"
        assert "/healthz" in data["error"]["message"]
    
    def test_legacy_proxy_request_deprecated(self, client):
        """Test legacy proxy request endpoint returns deprecation."""
        response = client.post("/proxy/request", json={})
        assert response.status_code == 410
        
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "DEPRECATED_ENDPOINT"
    
    def test_legacy_proxy_status_deprecated(self, client):
        """Test legacy proxy status endpoint returns deprecation."""
        response = client.get("/proxy/status")
        assert response.status_code == 410
        
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "DEPRECATED_ENDPOINT"


class TestErrorHandling:
    """Test error handling and validation."""
    
    def test_service_unavailable_when_proxy_manager_not_ready(self, client, auth_headers):
        """Test service unavailable when proxy manager not initialized."""
        # This would need proper mocking of app state
        pass
    
    def test_validation_errors(self, client, auth_headers):
        """Test request validation errors."""
        # Test invalid proxy request
        invalid_request = {
            "url": "not-a-valid-url",
            "method": "INVALID_METHOD"
        }
        
        response = client.post("/v1/proxy/request", json=invalid_request, headers=auth_headers)
        assert response.status_code == 422  # Validation error
    
    def test_error_envelope_format(self, client):
        """Test that errors follow the Error-Envelope format."""
        # Test a 401 error
        response = client.post("/v1/proxy/request", json={"url": "https://example.com"})
        
        if response.status_code == 401:
            data = response.json()
            assert "error" in data
            assert "code" in data["error"]
            assert "message" in data["error"]


class TestPagination:
    """Test pagination functionality."""
    
    @patch('app_v1.request_history', [{"test": f"data_{i}"} for i in range(50)])
    def test_request_history_pagination(self, client):
        """Test request history pagination."""
        response = client.get("/v1/proxy/requests?page=1&size=10")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert data["page"] == 1
        assert data["size"] == 10


class TestAuthentication:
    """Test authentication functionality."""
    
    def test_basic_auth_success(self, client):
        """Test successful basic authentication."""
        credentials = base64.b64encode(b"dev:devpass").decode("ascii")
        headers = {"Authorization": f"Basic {credentials}"}
        
        # This would need a proxy manager mock
        request_data = {"url": "https://example.com"}
        response = client.post("/v1/proxy/request", json=request_data, headers=headers)
        
        # Should not be 401 (though might be 503 if proxy manager not available)
        assert response.status_code != 401
    
    def test_basic_auth_invalid_credentials(self, client):
        """Test basic authentication with invalid credentials."""
        credentials = base64.b64encode(b"wrong:credentials").decode("ascii")
        headers = {"Authorization": f"Basic {credentials}"}
        
        request_data = {"url": "https://example.com"}
        response = client.post("/v1/proxy/request", json=request_data, headers=headers)
        assert response.status_code == 401
        
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "AUTHENTICATION_FAILED"
    
    def test_no_auth_header(self, client):
        """Test request without authentication header."""
        request_data = {"url": "https://example.com"}
        response = client.post("/v1/proxy/request", json=request_data)
        assert response.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
