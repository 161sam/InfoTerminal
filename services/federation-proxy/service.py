"""
Federation Service Implementation for v1 API.

Provides business logic for federation management, request proxying,
health monitoring, and security policy enforcement.
"""

import asyncio
import hashlib
import json
import logging
import os
import time
import uuid
import yaml
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse

import httpx
from fastapi import BackgroundTasks

from _shared.api_standards.error_schemas import StandardError, ErrorCodes
from _shared.api_standards.pagination import PaginatedResponse, PaginationParams
from models.requests import (
    FederationConfig, RemoteEndpoint, ProxyRequest, ProxyResponse,
    HealthStatus, FederationMetrics, RoutingRule, SecurityPolicy,
    ConnectionPool, CircuitBreaker, LoadBalancer,
    FederationTopology, ServiceDiscovery, ConfigurationSync,
    EndpointStatus, LoadBalancingStrategy, SecurityLevel, CircuitBreakerState
)

logger = logging.getLogger(__name__)


class EndpointHealthMonitor:
    """Health monitoring for federation endpoints."""
    
    def __init__(self):
        self.health_cache = {}
        self.health_check_interval = 30
        self.monitoring_tasks = {}
    
    async def start_monitoring(self, endpoint: RemoteEndpoint):
        """Start health monitoring for an endpoint."""
        if endpoint.id not in self.monitoring_tasks:
            task = asyncio.create_task(self._monitor_endpoint(endpoint))
            self.monitoring_tasks[endpoint.id] = task
    
    async def stop_monitoring(self, endpoint_id: str):
        """Stop health monitoring for an endpoint."""
        if endpoint_id in self.monitoring_tasks:
            self.monitoring_tasks[endpoint_id].cancel()
            del self.monitoring_tasks[endpoint_id]
    
    async def _monitor_endpoint(self, endpoint: RemoteEndpoint):
        """Continuous health monitoring loop."""
        while True:
            try:
                health_status = await self._check_endpoint_health(endpoint)
                self.health_cache[endpoint.id] = health_status
                
                # Log health changes
                if health_status.status != EndpointStatus.HEALTHY:
                    logger.warning(f"Endpoint {endpoint.id} health check failed: {health_status.error_message}")
                
                await asyncio.sleep(self.health_check_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health monitoring error for {endpoint.id}: {e}")
                await asyncio.sleep(self.health_check_interval)
    
    async def _check_endpoint_health(self, endpoint: RemoteEndpoint) -> HealthStatus:
        """Perform health check for a single endpoint."""
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                health_url = urljoin(endpoint.url, "/v1/healthz")
                response = await client.get(health_url)
                
                response_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    return HealthStatus(
                        endpoint_id=endpoint.id,
                        status=EndpointStatus.HEALTHY,
                        last_check=datetime.utcnow(),
                        response_time_ms=response_time,
                        checks={"connectivity": True, "api_response": True}
                    )
                else:
                    return HealthStatus(
                        endpoint_id=endpoint.id,
                        status=EndpointStatus.UNHEALTHY,
                        last_check=datetime.utcnow(),
                        response_time_ms=response_time,
                        error_message=f"HTTP {response.status_code}",
                        checks={"connectivity": True, "api_response": False}
                    )
                    
        except httpx.TimeoutException:
            return HealthStatus(
                endpoint_id=endpoint.id,
                status=EndpointStatus.UNHEALTHY,
                last_check=datetime.utcnow(),
                error_message="Health check timeout",
                checks={"connectivity": False, "api_response": False}
            )
        except Exception as e:
            return HealthStatus(
                endpoint_id=endpoint.id,
                status=EndpointStatus.UNHEALTHY,
                last_check=datetime.utcnow(),
                error_message=str(e),
                checks={"connectivity": False, "api_response": False}
            )
    
    def get_health_status(self, endpoint_id: str) -> Optional[HealthStatus]:
        """Get cached health status for an endpoint."""
        return self.health_cache.get(endpoint_id)


class LoadBalancerManager:
    """Load balancing management for federation endpoints."""
    
    def __init__(self):
        self.strategy = LoadBalancingStrategy.ROUND_ROBIN
        self.endpoint_weights = {}
        self.current_index = 0
        self.request_counts = {}
        self.connection_counts = {}
    
    def select_endpoint(self, endpoints: List[RemoteEndpoint], health_monitor: EndpointHealthMonitor) -> Optional[RemoteEndpoint]:
        """Select the best endpoint based on load balancing strategy."""
        # Filter healthy endpoints
        healthy_endpoints = []
        for endpoint in endpoints:
            health_status = health_monitor.get_health_status(endpoint.id)
            if health_status and health_status.status == EndpointStatus.HEALTHY:
                healthy_endpoints.append(endpoint)
        
        if not healthy_endpoints:
            return None
        
        if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            return self._round_robin_select(healthy_endpoints)
        elif self.strategy == LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN:
            return self._weighted_round_robin_select(healthy_endpoints)
        elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return self._least_connections_select(healthy_endpoints)
        elif self.strategy == LoadBalancingStrategy.LEAST_RESPONSE_TIME:
            return self._least_response_time_select(healthy_endpoints, health_monitor)
        else:
            return healthy_endpoints[0] if healthy_endpoints else None
    
    def _round_robin_select(self, endpoints: List[RemoteEndpoint]) -> RemoteEndpoint:
        """Simple round-robin selection."""
        if not endpoints:
            return None
        
        endpoint = endpoints[self.current_index % len(endpoints)]
        self.current_index += 1
        return endpoint
    
    def _weighted_round_robin_select(self, endpoints: List[RemoteEndpoint]) -> RemoteEndpoint:
        """Weighted round-robin selection based on endpoint weights."""
        if not endpoints:
            return None
        
        # Simple implementation - can be enhanced with proper weighted algorithm
        weighted_endpoints = []
        for endpoint in endpoints:
            weight = self.endpoint_weights.get(endpoint.id, endpoint.weight)
            weighted_endpoints.extend([endpoint] * max(1, weight // 10))
        
        if weighted_endpoints:
            selected = weighted_endpoints[self.current_index % len(weighted_endpoints)]
            self.current_index += 1
            return selected
        
        return endpoints[0]
    
    def _least_connections_select(self, endpoints: List[RemoteEndpoint]) -> RemoteEndpoint:
        """Select endpoint with least active connections."""
        if not endpoints:
            return None
        
        min_connections = float('inf')
        selected_endpoint = None
        
        for endpoint in endpoints:
            connections = self.connection_counts.get(endpoint.id, 0)
            if connections < min_connections:
                min_connections = connections
                selected_endpoint = endpoint
        
        return selected_endpoint or endpoints[0]
    
    def _least_response_time_select(self, endpoints: List[RemoteEndpoint], health_monitor: EndpointHealthMonitor) -> RemoteEndpoint:
        """Select endpoint with lowest response time."""
        if not endpoints:
            return None
        
        min_response_time = float('inf')
        selected_endpoint = None
        
        for endpoint in endpoints:
            health_status = health_monitor.get_health_status(endpoint.id)
            if health_status and health_status.response_time_ms:
                if health_status.response_time_ms < min_response_time:
                    min_response_time = health_status.response_time_ms
                    selected_endpoint = endpoint
        
        return selected_endpoint or endpoints[0]
    
    def record_request(self, endpoint_id: str):
        """Record a request for metrics."""
        self.request_counts[endpoint_id] = self.request_counts.get(endpoint_id, 0) + 1
    
    def add_connection(self, endpoint_id: str):
        """Add active connection count."""
        self.connection_counts[endpoint_id] = self.connection_counts.get(endpoint_id, 0) + 1
    
    def remove_connection(self, endpoint_id: str):
        """Remove active connection count."""
        if endpoint_id in self.connection_counts:
            self.connection_counts[endpoint_id] = max(0, self.connection_counts[endpoint_id] - 1)


class CircuitBreakerManager:
    """Circuit breaker pattern implementation for endpoints."""
    
    def __init__(self):
        self.circuit_breakers = {}
    
    def get_circuit_breaker(self, endpoint_id: str) -> CircuitBreaker:
        """Get or create circuit breaker for endpoint."""
        if endpoint_id not in self.circuit_breakers:
            self.circuit_breakers[endpoint_id] = CircuitBreaker(
                endpoint_id=endpoint_id,
                state=CircuitBreakerState.CLOSED
            )
        return self.circuit_breakers[endpoint_id]
    
    def can_execute_request(self, endpoint_id: str) -> bool:
        """Check if request can be executed based on circuit breaker state."""
        circuit_breaker = self.get_circuit_breaker(endpoint_id)
        
        if circuit_breaker.state == CircuitBreakerState.OPEN:
            # Check if timeout has passed to move to half-open
            if datetime.utcnow() - circuit_breaker.state_changed_at > timedelta(seconds=circuit_breaker.timeout_seconds):
                circuit_breaker.state = CircuitBreakerState.HALF_OPEN
                circuit_breaker.state_changed_at = datetime.utcnow()
                circuit_breaker.success_count = 0
                return True
            return False
        
        return True
    
    def record_success(self, endpoint_id: str):
        """Record successful request."""
        circuit_breaker = self.get_circuit_breaker(endpoint_id)
        circuit_breaker.successful_calls += 1
        circuit_breaker.total_calls += 1
        circuit_breaker.last_success_time = datetime.utcnow()
        
        if circuit_breaker.state == CircuitBreakerState.HALF_OPEN:
            circuit_breaker.success_count += 1
            if circuit_breaker.success_count >= circuit_breaker.success_threshold:
                circuit_breaker.state = CircuitBreakerState.CLOSED
                circuit_breaker.state_changed_at = datetime.utcnow()
                circuit_breaker.failure_count = 0
        elif circuit_breaker.state == CircuitBreakerState.CLOSED:
            circuit_breaker.failure_count = 0
    
    def record_failure(self, endpoint_id: str):
        """Record failed request."""
        circuit_breaker = self.get_circuit_breaker(endpoint_id)
        circuit_breaker.failed_calls += 1
        circuit_breaker.total_calls += 1
        circuit_breaker.last_failure_time = datetime.utcnow()
        
        if circuit_breaker.state in [CircuitBreakerState.CLOSED, CircuitBreakerState.HALF_OPEN]:
            circuit_breaker.failure_count += 1
            if circuit_breaker.failure_count >= circuit_breaker.failure_threshold:
                circuit_breaker.state = CircuitBreakerState.OPEN
                circuit_breaker.state_changed_at = datetime.utcnow()


class FederationService:
    """Main service class for federation operations."""
    
    def __init__(self):
        self.config_path = os.getenv("FEDERATION_CONFIG", "/app/remotes.yaml")
        self.federation_config = FederationConfig()
        self.endpoints = {}
        self.health_monitor = EndpointHealthMonitor()
        self.load_balancer = LoadBalancerManager()
        self.circuit_breaker_manager = CircuitBreakerManager()
        self.startup_time = time.time()
        self.request_metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "response_times": []
        }
    
    async def initialize(self):
        """Initialize federation service."""
        try:
            # Load configuration
            await self.load_federation_config()
            
            # Start health monitoring for all endpoints
            for endpoint in self.federation_config.endpoints:
                self.endpoints[endpoint.id] = endpoint
                await self.health_monitor.start_monitoring(endpoint)
            
            logger.info(f"Federation service initialized with {len(self.endpoints)} endpoints")
            
        except Exception as e:
            logger.error(f"Failed to initialize federation service: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup federation service resources."""
        # Stop health monitoring
        for endpoint_id in list(self.health_monitor.monitoring_tasks.keys()):
            await self.health_monitor.stop_monitoring(endpoint_id)
    
    async def load_federation_config(self):
        """Load federation configuration from file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config_data = yaml.safe_load(f) or {}
                
                # Convert legacy format if needed
                if "remotes" in config_data:
                    endpoints = []
                    for remote in config_data["remotes"]:
                        endpoint = RemoteEndpoint(
                            name=remote.get("name", "Unknown"),
                            url=remote.get("url"),
                            region=remote.get("region"),
                            service_types=remote.get("services", [])
                        )
                        endpoints.append(endpoint)
                    
                    self.federation_config = FederationConfig(endpoints=endpoints)
                else:
                    # Load full federation config
                    self.federation_config = FederationConfig(**config_data)
            else:
                # Create default config
                self.federation_config = FederationConfig()
                await self.save_federation_config()
                
        except Exception as e:
            logger.error(f"Failed to load federation config: {e}")
            self.federation_config = FederationConfig()
    
    async def save_federation_config(self):
        """Save federation configuration to file."""
        try:
            config_data = self.federation_config.dict(exclude_unset=True)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False)
                
        except Exception as e:
            logger.error(f"Failed to save federation config: {e}")
            raise
    
    async def get_federation_config(self) -> FederationConfig:
        """Get current federation configuration."""
        return self.federation_config
    
    async def update_federation_config(self, config: FederationConfig, background_tasks: BackgroundTasks = None) -> Dict[str, Any]:
        """Update federation configuration."""
        try:
            # Validate configuration
            validation_result = await self.validate_federation_config(config)
            if not validation_result["valid"]:
                raise ValueError(f"Configuration validation failed: {validation_result['details']}")
            
            # Update configuration
            old_endpoints = set(self.endpoints.keys())
            self.federation_config = config
            
            # Update endpoints
            new_endpoints = set()
            for endpoint in config.endpoints:
                self.endpoints[endpoint.id] = endpoint
                new_endpoints.add(endpoint.id)
                
                # Start monitoring for new endpoints
                if endpoint.id not in old_endpoints:
                    await self.health_monitor.start_monitoring(endpoint)
            
            # Stop monitoring for removed endpoints
            removed_endpoints = old_endpoints - new_endpoints
            for endpoint_id in removed_endpoints:
                await self.health_monitor.stop_monitoring(endpoint_id)
                if endpoint_id in self.endpoints:
                    del self.endpoints[endpoint_id]
            
            # Save configuration
            await self.save_federation_config()
            
            # Schedule background tasks
            if background_tasks:
                background_tasks.add_task(self._refresh_service_discovery_background)
            
            return {
                "config_id": str(uuid.uuid4()),
                "endpoints_updated": len(config.endpoints)
            }
            
        except Exception as e:
            logger.error(f"Failed to update federation config: {e}")
            raise
    
    async def validate_federation_config(self, config: FederationConfig) -> Dict[str, Any]:
        """Validate federation configuration."""
        try:
            validation_details = []
            warnings = []
            
            # Check endpoint URLs
            for endpoint in config.endpoints:
                try:
                    parsed_url = urlparse(endpoint.url)
                    if not parsed_url.scheme or not parsed_url.netloc:
                        validation_details.append(f"Invalid URL for endpoint {endpoint.name}: {endpoint.url}")
                except Exception:
                    validation_details.append(f"Invalid URL format for endpoint {endpoint.name}: {endpoint.url}")
            
            # Check for duplicate endpoint IDs
            endpoint_ids = [ep.id for ep in config.endpoints]
            if len(endpoint_ids) != len(set(endpoint_ids)):
                validation_details.append("Duplicate endpoint IDs found")
            
            # Check routing rules
            for rule in config.routing_rules:
                try:
                    import re
                    re.compile(rule.pattern)
                except re.error:
                    validation_details.append(f"Invalid regex pattern in rule {rule.name}: {rule.pattern}")
            
            # Performance warnings
            if len(config.endpoints) > 50:
                warnings.append("Large number of endpoints may impact performance")
            
            is_valid = len(validation_details) == 0
            
            return {
                "valid": is_valid,
                "details": validation_details,
                "warnings": warnings,
                "recommendations": [
                    "Consider using health-based load balancing for better reliability",
                    "Enable circuit breakers for automatic failure handling"
                ]
            }
            
        except Exception as e:
            logger.error(f"Configuration validation error: {e}")
            return {
                "valid": False,
                "details": [f"Validation error: {e}"],
                "warnings": [],
                "recommendations": []
            }
    
    async def list_remote_endpoints(self, pagination: PaginationParams, filters: Dict[str, Any]) -> PaginatedResponse[RemoteEndpoint]:
        """List remote endpoints with filtering."""
        try:
            endpoints = list(self.endpoints.values())
            
            # Apply filters
            if filters.get("status"):
                filtered_endpoints = []
                for endpoint in endpoints:
                    health_status = self.health_monitor.get_health_status(endpoint.id)
                    if health_status and health_status.status.value == filters["status"]:
                        filtered_endpoints.append(endpoint)
                endpoints = filtered_endpoints
            
            if filters.get("region"):
                endpoints = [ep for ep in endpoints if ep.region == filters["region"]]
            
            if filters.get("service_type"):
                endpoints = [ep for ep in endpoints if filters["service_type"] in ep.service_types]
            
            # Apply pagination
            total = len(endpoints)
            start_idx = pagination.skip
            end_idx = start_idx + pagination.limit
            paginated_endpoints = endpoints[start_idx:end_idx]
            
            return PaginatedResponse(
                items=paginated_endpoints,
                total=total,
                page=pagination.page,
                size=pagination.size,
                pages=(total + pagination.size - 1) // pagination.size
            )
            
        except Exception as e:
            logger.error(f"Failed to list endpoints: {e}")
            raise
    
    async def get_remote_endpoint(self, endpoint_id: str) -> Optional[RemoteEndpoint]:
        """Get remote endpoint by ID."""
        return self.endpoints.get(endpoint_id)
    
    async def create_remote_endpoint(self, endpoint: RemoteEndpoint, background_tasks: BackgroundTasks = None) -> RemoteEndpoint:
        """Create new remote endpoint."""
        try:
            # Validate endpoint
            if endpoint.id in self.endpoints:
                raise ValueError(f"Endpoint with ID {endpoint.id} already exists")
            
            # Test connectivity
            health_status = await self.health_monitor._check_endpoint_health(endpoint)
            if health_status.status != EndpointStatus.HEALTHY:
                logger.warning(f"Endpoint {endpoint.id} failed initial health check: {health_status.error_message}")
            
            # Add endpoint
            self.endpoints[endpoint.id] = endpoint
            self.federation_config.endpoints.append(endpoint)
            
            # Start monitoring
            await self.health_monitor.start_monitoring(endpoint)
            
            # Save configuration
            await self.save_federation_config()
            
            # Schedule background tasks
            if background_tasks:
                background_tasks.add_task(self._discover_endpoint_services, endpoint.id)
            
            return endpoint
            
        except Exception as e:
            logger.error(f"Failed to create endpoint: {e}")
            raise
    
    async def proxy_request(self, proxy_req: ProxyRequest) -> ProxyResponse:
        """Proxy HTTP request to federation endpoint."""
        start_time = time.time()
        
        try:
            # Select target endpoint
            if proxy_req.target_endpoint:
                endpoint = self.endpoints.get(proxy_req.target_endpoint)
                if not endpoint:
                    raise ValueError(f"Target endpoint not found: {proxy_req.target_endpoint}")
            else:
                # Use load balancer to select endpoint
                endpoints = list(self.endpoints.values())
                endpoint = self.load_balancer.select_endpoint(endpoints, self.health_monitor)
                if not endpoint:
                    raise ValueError("No healthy endpoints available")
            
            # Check circuit breaker
            if not self.circuit_breaker_manager.can_execute_request(endpoint.id):
                raise ValueError(f"Circuit breaker open for endpoint {endpoint.id}")
            
            # Record connection
            self.load_balancer.add_connection(endpoint.id)
            
            try:
                # Execute request
                async with httpx.AsyncClient(timeout=proxy_req.timeout) as client:
                    target_url = urljoin(endpoint.url, proxy_req.path)
                    
                    # Prepare request
                    request_kwargs = {
                        "method": proxy_req.method,
                        "url": target_url,
                        "headers": proxy_req.headers,
                        "params": proxy_req.query_params
                    }
                    
                    if proxy_req.body and proxy_req.method in ["POST", "PUT", "PATCH"]:
                        request_kwargs["content"] = proxy_req.body
                    
                    # Make request
                    response = await client.request(**request_kwargs)
                    
                    response_time = (time.time() - start_time) * 1000
                    
                    # Record success
                    self.circuit_breaker_manager.record_success(endpoint.id)
                    self.load_balancer.record_request(endpoint.id)
                    self._record_request_metrics(True, response_time)
                    
                    return ProxyResponse(
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        body=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                        endpoint_id=endpoint.id,
                        response_time_ms=response_time,
                        attempt_count=1
                    )
                    
            finally:
                # Remove connection
                self.load_balancer.remove_connection(endpoint.id)
                
        except Exception as e:
            # Record failure
            if 'endpoint' in locals():
                self.circuit_breaker_manager.record_failure(endpoint.id)
            
            response_time = (time.time() - start_time) * 1000
            self._record_request_metrics(False, response_time)
            
            logger.error(f"Proxy request failed: {e}")
            raise
    
    async def get_federation_health(self, include_details: bool = True) -> List[HealthStatus]:
        """Get health status of all endpoints."""
        health_statuses = []
        
        for endpoint_id in self.endpoints.keys():
            health_status = self.health_monitor.get_health_status(endpoint_id)
            if health_status:
                if include_details:
                    # Add additional details
                    circuit_breaker = self.circuit_breaker_manager.get_circuit_breaker(endpoint_id)
                    health_status.circuit_breaker_state = circuit_breaker.state
                    health_status.active_connections = self.load_balancer.connection_counts.get(endpoint_id, 0)
                
                health_statuses.append(health_status)
        
        return health_statuses
    
    async def get_federation_metrics(self, time_range: str, endpoint_id: Optional[str] = None) -> FederationMetrics:
        """Get federation performance metrics."""
        try:
            # Calculate metrics based on stored data
            total_requests = self.request_metrics["total_requests"]
            successful_requests = self.request_metrics["successful_requests"]
            failed_requests = self.request_metrics["failed_requests"]
            
            # Calculate response time metrics
            response_times = self.request_metrics["response_times"]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            # Sort for percentiles
            sorted_times = sorted(response_times)
            p95_index = int(0.95 * len(sorted_times)) if sorted_times else 0
            p99_index = int(0.99 * len(sorted_times)) if sorted_times else 0
            
            p95_response_time = sorted_times[p95_index] if sorted_times else 0
            p99_response_time = sorted_times[p99_index] if sorted_times else 0
            
            # Calculate error rate
            error_rate = (failed_requests / total_requests * 100) if total_requests > 0 else 0
            
            # Get request distribution
            request_distribution = dict(self.load_balancer.request_counts)
            
            # Calculate load balancing efficiency
            if request_distribution:
                max_requests = max(request_distribution.values())
                min_requests = min(request_distribution.values())
                efficiency = (min_requests / max_requests * 100) if max_requests > 0 else 100
            else:
                efficiency = 100
            
            return FederationMetrics(
                time_range=time_range,
                total_requests=total_requests,
                successful_requests=successful_requests,
                failed_requests=failed_requests,
                average_response_time=avg_response_time,
                p95_response_time=p95_response_time,
                p99_response_time=p99_response_time,
                error_rate=error_rate,
                request_distribution=request_distribution,
                load_balancing_efficiency=efficiency,
                endpoint_metrics={},  # TODO: Implement per-endpoint metrics
                error_types={},  # TODO: Implement error type tracking
                authentication_failures=0,  # TODO: Implement auth failure tracking
                rate_limit_violations=0,  # TODO: Implement rate limit tracking
                security_violations=0  # TODO: Implement security violation tracking
            )
            
        except Exception as e:
            logger.error(f"Failed to get federation metrics: {e}")
            raise
    
    def _record_request_metrics(self, success: bool, response_time: float):
        """Record request metrics."""
        self.request_metrics["total_requests"] += 1
        
        if success:
            self.request_metrics["successful_requests"] += 1
        else:
            self.request_metrics["failed_requests"] += 1
        
        # Keep last 1000 response times for percentile calculations
        self.request_metrics["response_times"].append(response_time)
        if len(self.request_metrics["response_times"]) > 1000:
            self.request_metrics["response_times"] = self.request_metrics["response_times"][-1000:]
    
    async def _discover_endpoint_services(self, endpoint_id: str):
        """Background task to discover services on an endpoint."""
        try:
            endpoint = self.endpoints.get(endpoint_id)
            if not endpoint:
                return
            
            # Try to discover services via API introspection
            async with httpx.AsyncClient(timeout=30.0) as client:
                info_url = urljoin(endpoint.url, "/v1/info")
                response = await client.get(info_url)
                
                if response.status_code == 200:
                    info_data = response.json()
                    
                    # Update endpoint capabilities
                    if "capabilities" in info_data:
                        endpoint.capabilities.update(info_data["capabilities"])
                    
                    if "service" in info_data:
                        service_name = info_data["service"]
                        if service_name not in endpoint.service_types:
                            endpoint.service_types.append(service_name)
                    
                    # Save updated configuration
                    await self.save_federation_config()
                    
                    logger.info(f"Service discovery completed for endpoint {endpoint_id}")
                
        except Exception as e:
            logger.warning(f"Service discovery failed for endpoint {endpoint_id}: {e}")
    
    async def _refresh_service_discovery_background(self):
        """Background task to refresh service discovery for all endpoints."""
        for endpoint_id in self.endpoints.keys():
            await self._discover_endpoint_services(endpoint_id)


# Placeholder implementations for methods referenced in router but not yet implemented

    async def update_remote_endpoint(self, endpoint_id: str, endpoint_update: RemoteEndpoint) -> Optional[RemoteEndpoint]:
        """Update remote endpoint - placeholder implementation."""
        # TODO: Implement endpoint update logic
        return None
    
    async def delete_remote_endpoint(self, endpoint_id: str, force: bool = False) -> bool:
        """Delete remote endpoint - placeholder implementation."""
        # TODO: Implement endpoint deletion logic
        return False
    
    async def trigger_health_check(self, endpoint_id: str, force: bool = False) -> Optional[HealthStatus]:
        """Trigger health check - placeholder implementation."""
        # TODO: Implement manual health check trigger
        return None
    
    async def get_federation_topology(self, include_inactive: bool = False) -> FederationTopology:
        """Get federation topology - placeholder implementation."""
        # TODO: Implement topology discovery
        return FederationTopology()
    
    async def refresh_service_discovery(self, background_tasks: BackgroundTasks = None) -> Dict[str, Any]:
        """Refresh service discovery - placeholder implementation."""
        # TODO: Implement service discovery refresh
        return {"discovery_id": str(uuid.uuid4())}
    
    async def list_security_policies(self) -> List[SecurityPolicy]:
        """List security policies - placeholder implementation."""
        # TODO: Implement security policy listing
        return []
    
    async def create_security_policy(self, policy: SecurityPolicy) -> SecurityPolicy:
        """Create security policy - placeholder implementation."""
        # TODO: Implement security policy creation
        return policy
    
    async def get_load_balancer_config(self) -> LoadBalancer:
        """Get load balancer config - placeholder implementation."""
        # TODO: Implement load balancer config retrieval
        return LoadBalancer()
    
    async def update_load_balancer_config(self, lb_config: LoadBalancer) -> Dict[str, Any]:
        """Update load balancer config - placeholder implementation."""
        # TODO: Implement load balancer config update
        return {"endpoints_affected": 0}
