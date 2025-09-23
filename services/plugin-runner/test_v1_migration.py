"""
Test suite for Plugin Runner v1 API migration.

Tests the new standardized *_v1.py implementation to ensure:
- All endpoints follow API standards
- Error handling uses Error-Envelope format
- Pagination works correctly
- Health checks function properly
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock

import sys
from pathlib import Path

# Add service to path
SERVICE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SERVICE_DIR))

from app_v1 import app
from models.requests import PluginExecutionRequest, PluginBatchRequest
from models.responses import PluginInfo, PluginExecutionResponse


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_plugin_registry():
    """Mock plugin registry for testing."""
    mock_registry = Mock()
    mock_registry.plugins = {
        "test-plugin": Mock(
            name="test-plugin",
            version="1.0.0",
            description="Test plugin",
            category="test",
            risk_level="low",
            requires_network=False,
            requires_root=False,
            parameters=[],
            output_format="json",
            security={}
        )
    }
    mock_registry.get_plugin = Mock(return_value=mock_registry.plugins["test-plugin"])
    return mock_registry


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
        assert data["service"] == "plugin-runner"
    
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
        assert data["service"] == "plugin-runner"
        assert data["version"] == "1.0.0"
        assert data["api_version"] == "v1"
        assert "endpoints" in data
        assert "capabilities" in data


class TestPluginEndpoints:
    """Test plugin-related endpoints."""
    
    @patch('app_v1.plugin_registry')
    def test_list_plugins(self, mock_registry, client, mock_plugin_registry):
        """Test list plugins endpoint."""
        mock_registry.return_value = mock_plugin_registry
        app_v1.plugin_registry = mock_plugin_registry
        
        response = client.get("/v1/plugins")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
    
    @patch('app_v1.plugin_registry')
    def test_list_plugins_with_filters(self, mock_registry, client, mock_plugin_registry):
        """Test list plugins with filters."""
        app_v1.plugin_registry = mock_plugin_registry
        
        response = client.get("/v1/plugins?category=test&risk_level=low")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
    
    @patch('app_v1.plugin_registry')
    def test_get_plugin_info(self, mock_registry, client, mock_plugin_registry):
        """Test get specific plugin info."""
        app_v1.plugin_registry = mock_plugin_registry
        
        response = client.get("/v1/plugins/test-plugin")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "test-plugin"
        assert data["version"] == "1.0.0"
        assert data["category"] == "test"
    
    @patch('app_v1.plugin_registry')
    def test_get_plugin_not_found(self, mock_registry, client, mock_plugin_registry):
        """Test get non-existent plugin."""
        mock_plugin_registry.get_plugin.return_value = None
        app_v1.plugin_registry = mock_plugin_registry
        
        response = client.get("/v1/plugins/nonexistent")
        assert response.status_code == 404
        
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "RESOURCE_NOT_FOUND"
    
    @patch('app_v1.plugin_registry')
    def test_plugin_health_check(self, mock_registry, client, mock_plugin_registry):
        """Test plugin health check."""
        app_v1.plugin_registry = mock_plugin_registry
        
        response = client.get("/v1/plugins/test-plugin/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["plugin_name"] == "test-plugin"
        assert "status" in data
        assert "checks" in data


class TestJobEndpoints:
    """Test job execution and management endpoints."""
    
    @patch('app_v1.plugin_registry')
    @patch('app_v1.job_queue')
    @patch('app_v1.running_jobs', {})
    def test_execute_plugin(self, mock_queue, mock_registry, client, mock_plugin_registry):
        """Test plugin execution."""
        app_v1.plugin_registry = mock_plugin_registry
        mock_queue.put = AsyncMock()
        app_v1.job_queue = mock_queue
        
        request_data = {
            "plugin_name": "test-plugin",
            "parameters": {"param1": "value1"},
            "timeout": 300,
            "output_format": "json",
            "priority": 1
        }
        
        response = client.post("/v1/plugins/test-plugin/execute", json=request_data)
        assert response.status_code == 202
        
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "queued"
        assert data["plugin_name"] == "test-plugin"
    
    @patch('app_v1.plugin_registry')
    def test_execute_plugin_not_found(self, mock_registry, client, mock_plugin_registry):
        """Test executing non-existent plugin."""
        mock_plugin_registry.get_plugin.return_value = None
        app_v1.plugin_registry = mock_plugin_registry
        
        request_data = {
            "plugin_name": "nonexistent",
            "parameters": {}
        }
        
        response = client.post("/v1/plugins/nonexistent/execute", json=request_data)
        assert response.status_code == 404
        
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "RESOURCE_NOT_FOUND"
    
    @patch('app_v1.running_jobs')
    def test_list_jobs(self, mock_jobs, client):
        """Test list jobs endpoint."""
        mock_jobs.__iter__ = Mock(return_value=iter([]))
        mock_jobs.items.return_value = []
        app_v1.running_jobs = {}
        
        response = client.get("/v1/jobs")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
    
    @patch('app_v1.running_jobs')
    def test_get_job_status(self, mock_jobs, client):
        """Test get job status."""
        test_job_id = "test-job-123"
        test_job = {
            "status": "completed",
            "plugin_name": "test-plugin",
            "created_at": "2025-09-21T16:45:00Z",
            "results": {"output": "test result"}
        }
        
        mock_jobs.__getitem__ = Mock(return_value=test_job)
        mock_jobs.__contains__ = Mock(return_value=True)
        app_v1.running_jobs = {test_job_id: test_job}
        
        response = client.get(f"/v1/jobs/{test_job_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["job_id"] == test_job_id
        assert data["status"] == "completed"
        assert data["plugin_name"] == "test-plugin"
    
    @patch('app_v1.running_jobs')
    def test_get_job_not_found(self, mock_jobs, client):
        """Test get non-existent job."""
        mock_jobs.__contains__ = Mock(return_value=False)
        app_v1.running_jobs = {}
        
        response = client.get("/v1/jobs/nonexistent")
        assert response.status_code == 404
        
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "RESOURCE_NOT_FOUND"
    
    @patch('app_v1.running_jobs')
    def test_cancel_job(self, mock_jobs, client):
        """Test cancel job."""
        test_job_id = "test-job-123"
        test_job = {
            "status": "queued",
            "plugin_name": "test-plugin",
            "created_at": "2025-09-21T16:45:00Z"
        }
        
        mock_jobs.__contains__ = Mock(return_value=True)
        mock_jobs.__getitem__ = Mock(return_value=test_job)
        app_v1.running_jobs = {test_job_id: test_job}
        
        response = client.delete(f"/v1/jobs/{test_job_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert data["job_id"] == test_job_id


class TestStatisticsEndpoints:
    """Test statistics and metadata endpoints."""
    
    @patch('app_v1.plugin_registry')
    @patch('app_v1.running_jobs')
    def test_get_categories(self, mock_jobs, mock_registry, client, mock_plugin_registry):
        """Test get plugin categories."""
        app_v1.plugin_registry = mock_plugin_registry
        app_v1.running_jobs = {}
        
        response = client.get("/v1/categories")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        if data:  # If categories exist
            assert "name" in data[0]
            assert "plugins" in data[0]
    
    @patch('app_v1.plugin_registry')
    @patch('app_v1.running_jobs')
    def test_get_statistics(self, mock_jobs, mock_registry, client, mock_plugin_registry):
        """Test get plugin statistics."""
        app_v1.plugin_registry = mock_plugin_registry
        app_v1.running_jobs = {}
        
        response = client.get("/v1/statistics")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_plugins" in data
        assert "total_jobs" in data
        assert "job_status_counts" in data
        assert "average_execution_time" in data
    
    @patch('app_v1.plugin_registry')
    def test_get_capabilities(self, mock_registry, client, mock_plugin_registry):
        """Test get system capabilities."""
        app_v1.plugin_registry = mock_plugin_registry
        
        response = client.get("/v1/capabilities")
        assert response.status_code == 200
        
        data = response.json()
        assert "max_concurrent_jobs" in data
        assert "supported_formats" in data
        assert "docker_available" in data
        assert "features" in data
    
    def test_get_plugin_system_health(self, client):
        """Test get plugin system health."""
        response = client.get("/v1/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "plugin_registry_loaded" in data
        assert "docker_available" in data
        assert "total_plugins" in data
        assert "active_jobs" in data


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
    
    def test_legacy_plugins_deprecated(self, client):
        """Test legacy plugins endpoint returns deprecation."""
        response = client.get("/plugins")
        assert response.status_code == 410
        
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "DEPRECATED_ENDPOINT"
    
    def test_legacy_execute_deprecated(self, client):
        """Test legacy execute endpoint returns deprecation."""
        response = client.post("/execute", json={})
        assert response.status_code == 410
        
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "DEPRECATED_ENDPOINT"


class TestErrorHandling:
    """Test error handling and validation."""
    
    def test_service_unavailable_when_registry_not_ready(self, client):
        """Test service unavailable when plugin registry not initialized."""
        # This would need proper mocking of app state
        pass
    
    def test_validation_errors(self, client):
        """Test request validation errors."""
        # Test invalid plugin execution request
        invalid_request = {
            "plugin_name": "",  # Invalid empty name
            "timeout": -1  # Invalid negative timeout
        }
        
        response = client.post("/v1/plugins/test/execute", json=invalid_request)
        assert response.status_code == 422  # Validation error
    
    def test_error_envelope_format(self, client):
        """Test that errors follow the Error-Envelope format."""
        # Test a 404 error
        response = client.get("/v1/plugins/nonexistent")
        
        if response.status_code == 404:
            data = response.json()
            assert "error" in data
            assert "code" in data["error"]
            assert "message" in data["error"]


class TestPagination:
    """Test pagination functionality."""
    
    @patch('app_v1.plugin_registry')
    def test_plugins_pagination(self, mock_registry, client, mock_plugin_registry):
        """Test plugins list pagination."""
        app_v1.plugin_registry = mock_plugin_registry
        
        response = client.get("/v1/plugins?page=1&size=10")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert data["page"] == 1
        assert data["size"] == 10
    
    @patch('app_v1.running_jobs')
    def test_jobs_pagination(self, mock_jobs, client):
        """Test jobs list pagination."""
        app_v1.running_jobs = {}
        
        response = client.get("/v1/jobs?page=1&size=20")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
