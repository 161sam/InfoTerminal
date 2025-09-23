"""
Test suite for federation-proxy service v1 migration.

Tests the v1 API endpoints and federation service integration to ensure
the migration from the legacy main.py is successful.
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch
from typing import Dict, Any

from fastapi.testclient import TestClient
from service import FederationService, EndpointHealthMonitor, LoadBalancerManager, CircuitBreakerManager
from models.requests import (
    FederationConfig, RemoteEndpoint, ProxyRequest, ProxyResponse,
    HealthStatus, FederationMetrics, SecurityPolicy, LoadBalancer,
    EndpointStatus, LoadBalancingStrategy, SecurityLevel, CircuitBreakerState
)


class MockRequest:
    """Mock request object for testing dependencies."""
    def __init__(self, federation_service):
        self.app = Mock()
        self.app.state = Mock()
        self.app.state.federation_service = federation_service


class TestEndpointHealthMonitor:
    """Test the endpoint health monitoring system."""
    
    def setup_method(self):
        self.health_monitor = EndpointHealthMonitor()
    
    @pytest.mark.asyncio
    async def test_health_check_healthy_endpoint(self):
        """Test health check for a healthy endpoint."""
        endpoint = RemoteEndpoint(
            name="Test Endpoint",
            url="https://test.example.com",
            region="us-east-1"
        )
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            health_status = await self.health_monitor._check_endpoint_health(endpoint)
            
            assert health_status.endpoint_id == endpoint.id
            assert health_status.status == EndpointStatus.HEALTHY
            assert health_status.response_time_ms is not None
            assert health_status.checks["connectivity"] == True
            assert health_status.checks["api_response"] == True
    
    @pytest.mark.asyncio
    async def test_health_check_unhealthy_endpoint(self):
        """Test health check for an unhealthy endpoint."""
        endpoint = RemoteEndpoint(
            name="Unhealthy Endpoint",
            url="https://down.example.com",
            region="us-west-1"
        )
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            health_status = await self.health_monitor._check_endpoint_health(endpoint)
            
            assert health_status.endpoint_id == endpoint.id
            assert health_status.status == EndpointStatus.UNHEALTHY
            assert health_status.error_message == "HTTP 500"
            assert health_status.checks["connectivity"] == True
            assert health_status.checks["api_response"] == False
    
    @pytest.mark.asyncio
    async def test_health_check_timeout(self):
        """Test health check with timeout."""
        endpoint = RemoteEndpoint(
            name="Timeout Endpoint",
            url="https://timeout.example.com",
            region="eu-central-1"
        )
        
        with patch('httpx.AsyncClient') as mock_client:
            import httpx
            mock_client.return_value.__aenter__.return_value.get.side_effect = httpx.TimeoutException("Timeout")
            
            health_status = await self.health_monitor._check_endpoint_health(endpoint)
            
            assert health_status.endpoint_id == endpoint.id
            assert health_status.status == EndpointStatus.UNHEALTHY
            assert "timeout" in health_status.error_message.lower()
            assert health_status.checks["connectivity"] == False


class TestLoadBalancerManager:
    """Test the load balancing system."""
    
    def setup_method(self):
        self.load_balancer = LoadBalancerManager()
        self.health_monitor = Mock()
    
    def test_round_robin_selection(self):
        """Test round-robin endpoint selection."""
        endpoints = [
            RemoteEndpoint(name="Endpoint 1", url="https://ep1.example.com"),
            RemoteEndpoint(name="Endpoint 2", url="https://ep2.example.com"),
            RemoteEndpoint(name="Endpoint 3", url="https://ep3.example.com")
        ]
        
        # Mock all endpoints as healthy
        self.health_monitor.get_health_status.return_value = HealthStatus(
            endpoint_id="test",
            status=EndpointStatus.HEALTHY,
            last_check=datetime.utcnow()
        )
        
        self.load_balancer.strategy = LoadBalancingStrategy.ROUND_ROBIN
        
        # Test round-robin distribution
        selected_endpoints = []
        for _ in range(6):
            selected = self.load_balancer.select_endpoint(endpoints, self.health_monitor)
            selected_endpoints.append(selected.name if selected else None)
        
        # Should cycle through endpoints
        expected = ["Endpoint 1", "Endpoint 2", "Endpoint 3", "Endpoint 1", "Endpoint 2", "Endpoint 3"]
        assert selected_endpoints == expected
    
    def test_least_connections_selection(self):
        """Test least connections endpoint selection."""
        endpoints = [
            RemoteEndpoint(name="Endpoint 1", url="https://ep1.example.com"),
            RemoteEndpoint(name="Endpoint 2", url="https://ep2.example.com")
        ]
        
        # Mock all endpoints as healthy
        self.health_monitor.get_health_status.return_value = HealthStatus(
            endpoint_id="test",
            status=EndpointStatus.HEALTHY,
            last_check=datetime.utcnow()
        )
        
        self.load_balancer.strategy = LoadBalancingStrategy.LEAST_CONNECTIONS
        
        # Set different connection counts
        self.load_balancer.connection_counts[endpoints[0].id] = 5
        self.load_balancer.connection_counts[endpoints[1].id] = 2
        
        selected = self.load_balancer.select_endpoint(endpoints, self.health_monitor)
        assert selected.name == "Endpoint 2"  # Should select endpoint with fewer connections
    
    def test_no_healthy_endpoints(self):
        """Test selection when no endpoints are healthy."""
        endpoints = [
            RemoteEndpoint(name="Unhealthy Endpoint", url="https://down.example.com")
        ]
        
        # Mock endpoint as unhealthy
        self.health_monitor.get_health_status.return_value = HealthStatus(
            endpoint_id="test",
            status=EndpointStatus.UNHEALTHY,
            last_check=datetime.utcnow()
        )
        
        selected = self.load_balancer.select_endpoint(endpoints, self.health_monitor)
        assert selected is None


class TestCircuitBreakerManager:
    """Test the circuit breaker pattern implementation."""
    
    def setup_method(self):
        self.circuit_breaker_manager = CircuitBreakerManager()
    
    def test_circuit_breaker_closed_state(self):
        """Test circuit breaker in closed state."""
        endpoint_id = "test-endpoint"
        
        # Should allow requests in closed state
        assert self.circuit_breaker_manager.can_execute_request(endpoint_id) == True
        
        circuit_breaker = self.circuit_breaker_manager.get_circuit_breaker(endpoint_id)
        assert circuit_breaker.state == CircuitBreakerState.CLOSED
    
    def test_circuit_breaker_failure_threshold(self):
        """Test circuit breaker opening after failure threshold."""
        endpoint_id = "test-endpoint"
        circuit_breaker = self.circuit_breaker_manager.get_circuit_breaker(endpoint_id)
        circuit_breaker.failure_threshold = 3
        
        # Record failures up to threshold
        for i in range(3):
            self.circuit_breaker_manager.record_failure(endpoint_id)
            if i < 2:
                assert circuit_breaker.state == CircuitBreakerState.CLOSED
        
        # Should open after threshold
        assert circuit_breaker.state == CircuitBreakerState.OPEN
        assert self.circuit_breaker_manager.can_execute_request(endpoint_id) == False
    
    def test_circuit_breaker_success_recovery(self):
        """Test circuit breaker recovery after successes."""
        endpoint_id = "test-endpoint"
        circuit_breaker = self.circuit_breaker_manager.get_circuit_breaker(endpoint_id)
        circuit_breaker.failure_threshold = 2
        circuit_breaker.success_threshold = 2
        
        # Open circuit breaker
        for _ in range(2):
            self.circuit_breaker_manager.record_failure(endpoint_id)
        
        assert circuit_breaker.state == CircuitBreakerState.OPEN
        
        # Move to half-open after timeout (simulate timeout)
        circuit_breaker.state = CircuitBreakerState.HALF_OPEN
        circuit_breaker.state_changed_at = datetime.utcnow()
        
        # Record successes to close circuit
        for i in range(2):
            self.circuit_breaker_manager.record_success(endpoint_id)
            if i < 1:
                assert circuit_breaker.state == CircuitBreakerState.HALF_OPEN
        
        # Should close after success threshold
        assert circuit_breaker.state == CircuitBreakerState.CLOSED


class TestFederationServiceIntegration:
    """Test the main federation service integration."""
    
    @pytest.fixture
    def mock_service(self):
        """Create a mock federation service for testing."""
        service = Mock(spec=FederationService)
        
        # Mock federation config
        service.get_federation_config = AsyncMock(return_value=FederationConfig(
            name="Test Federation",
            endpoints=[
                RemoteEndpoint(name="Test Endpoint", url="https://test.example.com")
            ]
        ))
        
        # Mock endpoint listing
        service.list_remote_endpoints = AsyncMock(return_value=Mock(
            items=[RemoteEndpoint(name="Test Endpoint", url="https://test.example.com")],
            total=1,
            page=1,
            size=10,
            pages=1
        ))
        
        # Mock endpoint creation
        service.create_remote_endpoint = AsyncMock(return_value=RemoteEndpoint(
            name="New Endpoint",
            url="https://new.example.com"
        ))
        
        # Mock proxy request
        service.proxy_request = AsyncMock(return_value=ProxyResponse(
            status_code=200,
            headers={"Content-Type": "application/json"},
            body={"status": "success"},
            endpoint_id="test-endpoint",
            response_time_ms=125.0,
            attempt_count=1
        ))
        
        # Mock health status
        service.get_federation_health = AsyncMock(return_value=[
            HealthStatus(
                endpoint_id="test-endpoint",
                status=EndpointStatus.HEALTHY,
                last_check=datetime.utcnow(),
                response_time_ms=100.0
            )
        ])
        
        # Mock metrics
        service.get_federation_metrics = AsyncMock(return_value=FederationMetrics(
            time_range="1h",
            total_requests=1000,
            successful_requests=950,
            failed_requests=50,
            average_response_time=125.0,
            error_rate=5.0,
            load_balancing_efficiency=95.0
        ))
        
        return service
    
    def test_router_dependency_injection(self, mock_service):
        """Test that the router properly injects the service dependency."""
        from routers.federation_proxy_v1 import get_federation_service
        
        mock_request = MockRequest(mock_service)
        injected_service = get_federation_service(mock_request)
        
        assert injected_service == mock_service
    
    @pytest.mark.asyncio
    async def test_get_federation_config_endpoint(self, mock_service):
        """Test the federation config endpoint."""
        from routers.federation_proxy_v1 import get_federation_config
        
        result = await get_federation_config(mock_service)
        
        mock_service.get_federation_config.assert_called_once()
        assert result.name == "Test Federation"
        assert len(result.endpoints) == 1
    
    @pytest.mark.asyncio
    async def test_list_endpoints_endpoint(self, mock_service):
        """Test the list endpoints endpoint."""
        from routers.federation_proxy_v1 import list_remote_endpoints
        from _shared.api_standards.pagination import PaginationParams
        
        pagination = PaginationParams(page=1, size=10)
        
        result = await list_remote_endpoints(
            pagination=pagination,
            service=mock_service
        )
        
        mock_service.list_remote_endpoints.assert_called_once()
        assert result.total == 1
        assert len(result.items) == 1
    
    @pytest.mark.asyncio
    async def test_create_endpoint_endpoint(self, mock_service):
        """Test the create endpoint endpoint."""
        from routers.federation_proxy_v1 import create_remote_endpoint
        
        endpoint_data = RemoteEndpoint(
            name="New Endpoint",
            url="https://new.example.com",
            region="us-east-1"
        )
        
        result = await create_remote_endpoint(endpoint_data, mock_service, None)
        
        mock_service.create_remote_endpoint.assert_called_once_with(endpoint_data, None)
        assert result.name == "New Endpoint"
    
    @pytest.mark.asyncio
    async def test_proxy_request_endpoint(self, mock_service):
        """Test the proxy request endpoint."""
        from routers.federation_proxy_v1 import proxy_request
        from fastapi import Request
        
        # Mock FastAPI request
        mock_request = Mock(spec=Request)
        mock_request.method = "GET"
        mock_request.headers = {"Accept": "application/json"}
        mock_request.query_params = {"limit": "10"}
        mock_request.body = AsyncMock(return_value=b"")
        
        result = await proxy_request(
            request=mock_request,
            path="test/path",
            service=mock_service
        )
        
        mock_service.proxy_request.assert_called_once()
        assert result.status_code == 200
    
    @pytest.mark.asyncio
    async def test_federation_health_endpoint(self, mock_service):
        """Test the federation health endpoint."""
        from routers.federation_proxy_v1 import get_federation_health
        
        result = await get_federation_health(service=mock_service)
        
        mock_service.get_federation_health.assert_called_once_with(include_details=True)
        assert len(result) == 1
        assert result[0].endpoint_id == "test-endpoint"
        assert result[0].status == EndpointStatus.HEALTHY
    
    @pytest.mark.asyncio
    async def test_federation_metrics_endpoint(self, mock_service):
        """Test the federation metrics endpoint."""
        from routers.federation_proxy_v1 import get_federation_metrics
        
        result = await get_federation_metrics(
            time_range="1h",
            service=mock_service
        )
        
        mock_service.get_federation_metrics.assert_called_once_with(
            time_range="1h",
            endpoint_id=None
        )
        assert result.total_requests == 1000
        assert result.successful_requests == 950
        assert result.error_rate == 5.0


class TestV1AppIntegration:
    """Test the v1 app integration and startup."""
    
    def test_app_creation(self):
        """Test that the v1 app creates successfully."""
        from app_v1 import app
        
        assert app.title == "Federation Proxy Service"
        assert app.version == "1.0.0"
        assert not app.deprecated  # Should not be deprecated
    
    def test_legacy_compatibility_endpoints(self):
        """Test that legacy endpoints return proper deprecation responses."""
        from app.main import app as legacy_app
        
        client = TestClient(legacy_app)
        
        # Test deprecated health endpoint
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json()["deprecated"] == True
        assert "new_endpoint" in response.json()
        
        # Test deprecated remotes endpoint
        response = client.get("/remotes")
        assert response.status_code == 200
        assert response.json()["deprecated"] == True
        assert response.json()["new_endpoint"] == "/v1/federation/endpoints"
        
        # Test moved endpoints return 410
        response = client.post("/remotes")
        assert response.status_code == 410
        assert response.json()["error_code"] == "ENDPOINT_MOVED"


def test_models_import():
    """Test that all models can be imported successfully."""
    from models import (
        FederationConfig, RemoteEndpoint, ProxyRequest, ProxyResponse,
        HealthStatus, FederationMetrics, SecurityPolicy, LoadBalancer,
        EndpointStatus, LoadBalancingStrategy, SecurityLevel
    )
    
    # Verify enums work correctly
    assert EndpointStatus.HEALTHY == "healthy"
    assert LoadBalancingStrategy.ROUND_ROBIN == "round_robin"
    assert SecurityLevel.AUTHENTICATED == "authenticated"


def test_federation_config_validation():
    """Test federation configuration validation."""
    # Valid configuration
    config = FederationConfig(
        name="Test Federation",
        endpoints=[
            RemoteEndpoint(
                name="Valid Endpoint",
                url="https://valid.example.com",
                region="us-east-1"
            )
        ]
    )
    
    assert config.name == "Test Federation"
    assert len(config.endpoints) == 1
    assert config.endpoints[0].url == "https://valid.example.com"


def test_endpoint_model_validation():
    """Test remote endpoint model validation."""
    endpoint = RemoteEndpoint(
        name="Test Endpoint",
        url="https://test.example.com",
        region="us-west-2",
        service_types=["search", "graph"],
        weight=150,
        security_level=SecurityLevel.MUTUAL_TLS
    )
    
    assert endpoint.name == "Test Endpoint"
    assert endpoint.weight == 150
    assert endpoint.security_level == SecurityLevel.MUTUAL_TLS
    assert "search" in endpoint.service_types
    assert "graph" in endpoint.service_types


def test_proxy_request_model():
    """Test proxy request model validation."""
    proxy_req = ProxyRequest(
        method="POST",
        path="/v1/search",
        headers={"Content-Type": "application/json"},
        query_params={"limit": "100"},
        timeout=30
    )
    
    assert proxy_req.method == "POST"
    assert proxy_req.path == "/v1/search"
    assert proxy_req.timeout == 30
    assert proxy_req.headers["Content-Type"] == "application/json"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
