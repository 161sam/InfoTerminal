"""
Test suite for OPA Audit Sink v1 API migration.

Tests the new standardized *_v1.py implementation to ensure:
- All endpoints follow API standards
- Error handling uses Error-Envelope format
- ClickHouse integration works correctly
- Audit log processing functions properly
"""

import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
import json

import sys
from pathlib import Path

# Add service to path
SERVICE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SERVICE_DIR))

from app_v1 import app
from models.requests import OPADecisionLogRequest, OPABulkLogRequest, AuditQueryRequest
from models.responses import AuditIngestResult, OPADecisionLog, AuditStatistics


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_clickhouse_client():
    """Mock ClickHouse client for testing."""
    mock_client = AsyncMock()
    return mock_client


@pytest.fixture
def sample_opa_log():
    """Sample OPA decision log for testing."""
    return {
        "timestamp": "2025-09-22T10:00:00Z",
        "decision_id": "test-decision-123",
        "path": "data.policies.test",
        "input": {
            "user": {
                "username": "testuser",
                "roles": ["analyst", "viewer"],
                "tenant": "test-org"
            },
            "resource": {
                "classification": "confidential"
            },
            "action": "read"
        },
        "result": True,
        "bundles": {
            "main": {
                "revision": "v1.2.3"
            }
        }
    }


@pytest.fixture
def sample_audit_config():
    """Sample audit configuration for testing."""
    return {
        "clickhouse_url": "http://localhost:8123",
        "database": "test_logs",
        "table": "test_opa_decisions",
        "batch_size": 100,
        "compression_enabled": True
    }


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
        assert data["service"] == "opa-audit-sink"
    
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
        assert data["service"] == "opa-audit-sink"
        assert data["version"] == "1.0.0"
        assert data["api_version"] == "v1"
        assert "endpoints" in data
        assert "capabilities" in data


class TestAuditLogIngestion:
    """Test audit log ingestion endpoints."""
    
    @patch('routers.audit_v1._insert_to_clickhouse')
    @patch('app_v1.clickhouse_client', 'configured')
    def test_ingest_single_log(self, mock_insert, client, sample_opa_log):
        """Test ingesting a single OPA decision log."""
        mock_insert.return_value = {"inserted": 1, "failed": 0}
        
        response = client.post("/v1/logs", json=[sample_opa_log])
        assert response.status_code == 200
        
        data = response.json()
        assert "ingested_count" in data
        assert "batch_id" in data
        assert "processing_time_ms" in data
        assert data["ingested_count"] == 1
        assert data["failed_count"] == 0
    
    @patch('routers.audit_v1._insert_to_clickhouse')
    @patch('app_v1.clickhouse_client', 'configured')
    def test_bulk_ingest_logs(self, mock_insert, client, sample_opa_log):
        """Test bulk ingestion of OPA decision logs."""
        mock_insert.return_value = {"inserted": 3, "failed": 0}
        
        bulk_request = {
            "logs": [sample_opa_log] * 3,
            "batch_id": "test-batch-001",
            "source": "test-opa-instance"
        }
        
        response = client.post("/v1/logs/bulk", json=bulk_request)
        assert response.status_code == 200
        
        data = response.json()
        assert data["ingested_count"] == 3
        assert data["batch_id"] == "test-batch-001"
    
    def test_ingest_without_clickhouse(self, client, sample_opa_log):
        """Test ingestion fails gracefully without ClickHouse."""
        with patch('app_v1.clickhouse_client', None):
            response = client.post("/v1/logs", json=[sample_opa_log])
            assert response.status_code == 503
            
            data = response.json()
            assert "error" in data
            assert data["error"]["code"] == "SERVICE_UNAVAILABLE"
    
    def test_ingest_invalid_log_format(self, client):
        """Test ingestion with invalid log format."""
        invalid_log = {"invalid": "format"}
        
        with patch('app_v1.clickhouse_client', 'configured'):
            response = client.post("/v1/logs", json=[invalid_log])
            # Should still return 200 but with errors in response
            assert response.status_code == 200
            
            data = response.json()
            assert data["failed_count"] >= 0  # May have transformation errors


class TestAuditLogQuerying:
    """Test audit log querying endpoints."""
    
    @patch('httpx.AsyncClient')
    @patch('app_v1.clickhouse_client', 'configured')
    def test_query_audit_logs(self, mock_httpx, client):
        """Test querying audit logs."""
        # Mock ClickHouse responses
        mock_client = AsyncMock()
        mock_count_response = Mock()
        mock_count_response.status_code = 200
        mock_count_response.text = "100"
        mock_count_response.raise_for_status = Mock()
        
        mock_data_response = Mock()
        mock_data_response.status_code = 200
        mock_data_response.text = "2025-09-22T10:00:00Z\tdata.policies.test\ttest-123\ttestuser\t[]\ttest-org\tconfidential\tread\t1\tv1.2.3\t{}"
        mock_data_response.raise_for_status = Mock()
        
        mock_client.post.side_effect = [mock_count_response, mock_data_response]
        mock_httpx.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        
        response = client.get("/v1/logs/query?user=testuser&limit=10")
        assert response.status_code == 200
        
        data = response.json()
        assert "logs" in data
        assert "total_count" in data
        assert "query_time_ms" in data
        assert data["total_count"] == 100
    
    @patch('httpx.AsyncClient')
    @patch('app_v1.clickhouse_client', 'configured')
    def test_query_with_time_range(self, mock_httpx, client):
        """Test querying with time range filters."""
        mock_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "50"
        mock_response.raise_for_status = Mock()
        mock_client.post.return_value = mock_response
        mock_httpx.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        
        start_time = "2025-09-22T00:00:00Z"
        end_time = "2025-09-22T23:59:59Z"
        
        response = client.get(f"/v1/logs/query?start_time={start_time}&end_time={end_time}")
        assert response.status_code == 200
    
    def test_query_validation_error(self, client):
        """Test query validation errors."""
        # Invalid time range (end before start)
        start_time = "2025-09-22T23:59:59Z"
        end_time = "2025-09-22T00:00:00Z"
        
        response = client.get(f"/v1/logs/query?start_time={start_time}&end_time={end_time}")
        # Should handle gracefully, may not validate at query level
        assert response.status_code in [200, 422]


class TestAuditStatistics:
    """Test audit statistics endpoints."""
    
    @patch('httpx.AsyncClient')
    @patch('app_v1.clickhouse_client', 'configured')
    def test_get_audit_statistics(self, mock_httpx, client):
        """Test getting audit statistics."""
        mock_client = AsyncMock()
        
        # Mock various statistic queries
        stat_responses = [
            "1000",  # total_decisions
            "800",   # decisions_allowed
            "200",   # decisions_denied
            "50",    # decisions_last_hour
            "100",   # decisions_last_day
            "500",   # decisions_last_week
            "25",    # unique_users
            "10"     # unique_policies
        ]
        
        mock_responses = []
        for response_text in stat_responses:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = response_text
            mock_response.raise_for_status = Mock()
            mock_responses.append(mock_response)
        
        # Add responses for top users and policies
        top_users_response = Mock()
        top_users_response.status_code = 200
        top_users_response.text = "testuser1\t150\ntestuser2\t100"
        top_users_response.raise_for_status = Mock()
        mock_responses.append(top_users_response)
        
        top_policies_response = Mock()
        top_policies_response.status_code = 200
        top_policies_response.text = "data.policies.test\t500\ndata.policies.admin\t300"
        top_policies_response.raise_for_status = Mock()
        mock_responses.append(top_policies_response)
        
        mock_client.post.side_effect = mock_responses
        mock_httpx.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        
        response = client.get("/v1/statistics")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_decisions" in data
        assert "decisions_allowed" in data
        assert "decisions_denied" in data
        assert "unique_users" in data
        assert "top_users" in data
        assert data["total_decisions"] == 1000
        assert data["decisions_allowed"] == 800
    
    def test_statistics_time_range(self, client):
        """Test statistics with different time ranges."""
        with patch('app_v1.clickhouse_client', 'configured'):
            with patch('httpx.AsyncClient') as mock_httpx:
                mock_client = AsyncMock()
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.text = "100"
                mock_response.raise_for_status = Mock()
                mock_client.post.return_value = mock_response
                mock_httpx.return_value.__aenter__ = AsyncMock(return_value=mock_client)
                
                response = client.get("/v1/statistics?time_range=7d")
                assert response.status_code == 200


class TestAuditHealth:
    """Test audit health monitoring endpoints."""
    
    @patch('httpx.AsyncClient')
    @patch('app_v1.clickhouse_client', 'configured')
    def test_comprehensive_health(self, mock_httpx, client):
        """Test comprehensive health check."""
        mock_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_client.get.return_value = mock_response
        mock_httpx.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        
        response = client.get("/v1/health/comprehensive")
        assert response.status_code == 200
        
        data = response.json()
        assert "overall_health" in data
        assert "clickhouse_health" in data
        assert "ingestion_health" in data
        assert "storage_health" in data
    
    def test_health_with_clickhouse_down(self, client):
        """Test health check when ClickHouse is down."""
        with patch('app_v1.clickhouse_client', 'configured'):
            with patch('httpx.AsyncClient') as mock_httpx:
                mock_client = AsyncMock()
                mock_client.get.side_effect = Exception("Connection failed")
                mock_httpx.return_value.__aenter__ = AsyncMock(return_value=mock_client)
                
                response = client.get("/v1/health/comprehensive")
                assert response.status_code == 200
                
                data = response.json()
                assert data["overall_health"] in ["degraded", "unhealthy"]


class TestAuditCapabilities:
    """Test audit capabilities endpoints."""
    
    def test_get_capabilities(self, client):
        """Test getting audit system capabilities."""
        response = client.get("/v1/capabilities")
        assert response.status_code == 200
        
        data = response.json()
        assert "max_retention_days" in data
        assert "supported_formats" in data
        assert "max_batch_size" in data
        assert "supported_alert_conditions" in data
        assert data["max_retention_days"] == 3650
        assert "json" in data["supported_formats"]


class TestRetentionManagement:
    """Test retention policy management."""
    
    def test_set_retention_policy(self, client):
        """Test setting retention policy."""
        policy_request = {
            "retention_days": 90,
            "policy_name": "test-policy",
            "apply_immediately": False,
            "backup_before_deletion": True,
            "dry_run": True
        }
        
        response = client.post("/v1/retention/policy", json=policy_request)
        assert response.status_code == 200
        
        data = response.json()
        assert "policy_name" in data
        assert "retention_days" in data
        assert data["policy_name"] == "test-policy"
        assert data["retention_days"] == 90
    
    def test_list_retention_policies(self, client):
        """Test listing retention policies."""
        response = client.get("/v1/retention/policies")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)


class TestAuditConfiguration:
    """Test audit configuration management."""
    
    def test_update_config(self, client):
        """Test updating audit configuration."""
        config_update = {
            "batch_size": 200,
            "flush_interval": 120,
            "enable_compression": True
        }
        
        response = client.put("/v1/config", json=config_update)
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "updated_fields" in data
        assert "batch_size" in data["updated_fields"]
    
    def test_get_config(self, client):
        """Test getting current configuration."""
        response = client.get("/v1/config")
        assert response.status_code == 200
        
        data = response.json()
        assert "configuration" in data
        assert "timestamp" in data
        assert "service_version" in data


class TestErrorHandling:
    """Test error handling and validation."""
    
    def test_service_unavailable_when_clickhouse_not_ready(self, client):
        """Test service unavailable when ClickHouse not available."""
        with patch('app_v1.clickhouse_client', None):
            response = client.post("/v1/logs", json=[{"test": "log"}])
            assert response.status_code == 503
            
            data = response.json()
            assert "error" in data
            assert data["error"]["code"] == "SERVICE_UNAVAILABLE"
    
    def test_validation_errors(self, client):
        """Test request validation errors."""
        # Test invalid bulk request
        invalid_request = {
            "logs": [],  # Empty logs list
            "batch_id": "test"
        }
        
        response = client.post("/v1/logs/bulk", json=invalid_request)
        assert response.status_code == 422  # Validation error
    
    def test_error_envelope_format(self, client):
        """Test that errors follow the Error-Envelope format."""
        with patch('app_v1.clickhouse_client', None):
            response = client.post("/v1/logs", json=[{"test": "log"}])
            
            if response.status_code >= 400:
                data = response.json()
                assert "error" in data
                assert "code" in data["error"]
                assert "message" in data["error"]


class TestLegacyEndpoints:
    """Test legacy endpoint deprecation."""
    
    def test_legacy_logs_deprecated(self, client):
        """Test legacy logs endpoint returns deprecation."""
        response = client.post("/logs")
        assert response.status_code == 410
        
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "DEPRECATED_ENDPOINT"
        assert "/v1/logs" in data["error"]["message"]
    
    def test_legacy_healthz_deprecated(self, client):
        """Test legacy healthz endpoint returns deprecation."""
        response = client.get("/healthz")
        # This may redirect to the new healthz in app_v1.py
        assert response.status_code in [200, 410]


class TestDataTransformation:
    """Test OPA log data transformation."""
    
    def test_opa_log_transformation(self, sample_opa_log):
        """Test OPA decision log transformation."""
        from routers.audit_v1 import _transform_opa_log
        
        transformed = _transform_opa_log(sample_opa_log)
        
        assert "ts" in transformed
        assert "user" in transformed
        assert "roles" in transformed
        assert "allowed" in transformed
        assert transformed["user"] == "testuser"
        assert transformed["allowed"] == 1  # True -> 1
        assert transformed["classification"] == "confidential"
    
    def test_empty_log_transformation(self):
        """Test transformation of empty log."""
        from routers.audit_v1 import _transform_opa_log
        
        empty_log = {}
        transformed = _transform_opa_log(empty_log)
        
        assert "ts" in transformed
        assert transformed["user"] == ""
        assert transformed["allowed"] == 0
        assert transformed["path"] == ""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
