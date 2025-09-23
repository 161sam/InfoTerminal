"""
Pydantic models for Federation Proxy Service v1.

Comprehensive models for federation management, request proxying, 
health monitoring, and security policy enforcement.
"""

from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum
import uuid


class EndpointStatus(str, Enum):
    """Status of a federation endpoint."""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"
    MAINTENANCE = "maintenance"


class LoadBalancingStrategy(str, Enum):
    """Load balancing strategies for federation."""
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_CONNECTIONS = "least_connections"
    LEAST_RESPONSE_TIME = "least_response_time"
    HEALTH_BASED = "health_based"
    GEOGRAPHIC = "geographic"


class SecurityLevel(str, Enum):
    """Security levels for federation endpoints."""
    OPEN = "open"
    AUTHENTICATED = "authenticated"
    ENCRYPTED = "encrypted"
    MUTUAL_TLS = "mutual_tls"


class CircuitBreakerState(str, Enum):
    """Circuit breaker states."""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


# Core Federation Models

class RemoteEndpoint(BaseModel):
    """Configuration for a remote federation endpoint."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique endpoint identifier")
    name: str = Field(..., description="Human-readable endpoint name")
    url: str = Field(..., description="Base URL of the remote endpoint")
    region: Optional[str] = Field(None, description="Geographic region")
    datacenter: Optional[str] = Field(None, description="Datacenter location")
    service_types: List[str] = Field(default_factory=list, description="Available service types")
    
    # Status and health
    status: EndpointStatus = Field(default=EndpointStatus.UNKNOWN, description="Current endpoint status")
    last_health_check: Optional[datetime] = Field(None, description="Last health check timestamp")
    response_time_ms: Optional[float] = Field(None, description="Average response time in milliseconds")
    success_rate: Optional[float] = Field(None, description="Success rate percentage", ge=0, le=100)
    
    # Configuration
    weight: int = Field(default=100, description="Load balancing weight", ge=1, le=1000)
    max_connections: int = Field(default=100, description="Maximum concurrent connections", ge=1)
    timeout_seconds: int = Field(default=30, description="Request timeout in seconds", ge=1, le=300)
    retry_attempts: int = Field(default=3, description="Number of retry attempts", ge=0, le=10)
    
    # Security
    security_level: SecurityLevel = Field(default=SecurityLevel.AUTHENTICATED, description="Required security level")
    api_key: Optional[str] = Field(None, description="API key for authentication")
    client_cert_path: Optional[str] = Field(None, description="Path to client certificate")
    trusted_ca_path: Optional[str] = Field(None, description="Path to trusted CA certificate")
    
    # Capabilities
    capabilities: Dict[str, Any] = Field(default_factory=dict, description="Endpoint capabilities and features")
    version: Optional[str] = Field(None, description="Remote service version")
    
    # Metadata
    tags: List[str] = Field(default_factory=list, description="Endpoint tags for organization")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "InfoTerminal East Coast",
                "url": "https://infoterminal-east.example.com",
                "region": "us-east-1",
                "datacenter": "virginia-1",
                "service_types": ["search", "graph", "nlp"],
                "weight": 150,
                "max_connections": 200,
                "security_level": "mutual_tls",
                "capabilities": {
                    "search_api": "v1",
                    "graph_api": "v1",
                    "nlp_api": "v1"
                },
                "tags": ["production", "primary"]
            }
        }


class RoutingRule(BaseModel):
    """Request routing rule for federation."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Rule identifier")
    name: str = Field(..., description="Rule name")
    pattern: str = Field(..., description="URL pattern to match (regex)")
    target_endpoints: List[str] = Field(..., description="Target endpoint IDs")
    load_balancing_strategy: LoadBalancingStrategy = Field(default=LoadBalancingStrategy.ROUND_ROBIN)
    priority: int = Field(default=100, description="Rule priority (higher = more priority)", ge=1, le=1000)
    enabled: bool = Field(default=True, description="Whether rule is active")
    
    # Conditions
    methods: List[str] = Field(default_factory=lambda: ["GET", "POST", "PUT", "DELETE"], description="HTTP methods")
    headers: Dict[str, str] = Field(default_factory=dict, description="Required headers")
    query_params: Dict[str, str] = Field(default_factory=dict, description="Required query parameters")
    
    # Transformations
    request_transforms: List[Dict[str, Any]] = Field(default_factory=list, description="Request transformations")
    response_transforms: List[Dict[str, Any]] = Field(default_factory=list, description="Response transformations")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Search API Routing",
                "pattern": r"^/v1/search.*",
                "target_endpoints": ["endpoint-1", "endpoint-2"],
                "load_balancing_strategy": "least_response_time",
                "methods": ["GET", "POST"],
                "priority": 200
            }
        }


class SecurityPolicy(BaseModel):
    """Security policy for federation endpoints."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Policy identifier")
    name: str = Field(..., description="Policy name")
    description: str = Field(..., description="Policy description")
    
    # Access control
    allowed_ips: List[str] = Field(default_factory=list, description="Allowed IP addresses/CIDR blocks")
    blocked_ips: List[str] = Field(default_factory=list, description="Blocked IP addresses/CIDR blocks")
    required_headers: Dict[str, str] = Field(default_factory=dict, description="Required headers")
    
    # Rate limiting
    rate_limit_requests: Optional[int] = Field(None, description="Requests per minute limit")
    rate_limit_burst: Optional[int] = Field(None, description="Burst requests allowed")
    
    # Authentication
    require_authentication: bool = Field(default=True, description="Require authentication")
    allowed_auth_methods: List[str] = Field(default_factory=lambda: ["jwt", "api_key"], description="Allowed auth methods")
    token_validation_endpoint: Optional[str] = Field(None, description="Token validation endpoint")
    
    # Encryption
    require_tls: bool = Field(default=True, description="Require TLS encryption")
    min_tls_version: str = Field(default="1.2", description="Minimum TLS version")
    
    # Audit
    log_requests: bool = Field(default=True, description="Log all requests")
    log_responses: bool = Field(default=False, description="Log response bodies")
    
    # Assignment
    endpoint_ids: List[str] = Field(default_factory=list, description="Assigned endpoint IDs")
    
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Production Security Policy",
                "description": "Standard security policy for production endpoints",
                "allowed_ips": ["10.0.0.0/8", "192.168.0.0/16"],
                "rate_limit_requests": 1000,
                "require_authentication": True,
                "require_tls": True,
                "min_tls_version": "1.3"
            }
        }


class ConnectionPool(BaseModel):
    """Connection pool configuration and status."""
    endpoint_id: str = Field(..., description="Associated endpoint ID")
    max_connections: int = Field(default=100, description="Maximum pool size")
    current_connections: int = Field(default=0, description="Current active connections")
    idle_connections: int = Field(default=0, description="Idle connections in pool")
    connection_timeout: int = Field(default=30, description="Connection timeout in seconds")
    keep_alive_timeout: int = Field(default=300, description="Keep-alive timeout in seconds")
    
    # Statistics
    total_requests: int = Field(default=0, description="Total requests processed")
    successful_requests: int = Field(default=0, description="Successful requests")
    failed_requests: int = Field(default=0, description="Failed requests")
    average_response_time: float = Field(default=0.0, description="Average response time in ms")
    
    # Health
    healthy: bool = Field(default=True, description="Pool health status")
    last_activity: Optional[datetime] = Field(None, description="Last activity timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "endpoint_id": "endpoint-1",
                "max_connections": 200,
                "current_connections": 45,
                "idle_connections": 15,
                "total_requests": 10000,
                "successful_requests": 9850,
                "average_response_time": 125.5
            }
        }


class CircuitBreaker(BaseModel):
    """Circuit breaker configuration and status."""
    endpoint_id: str = Field(..., description="Associated endpoint ID")
    state: CircuitBreakerState = Field(default=CircuitBreakerState.CLOSED, description="Current state")
    
    # Configuration
    failure_threshold: int = Field(default=5, description="Failures before opening", ge=1, le=100)
    success_threshold: int = Field(default=3, description="Successes before closing", ge=1, le=100)
    timeout_seconds: int = Field(default=60, description="Open state timeout", ge=1, le=3600)
    
    # Statistics
    failure_count: int = Field(default=0, description="Current failure count")
    success_count: int = Field(default=0, description="Current success count")
    last_failure_time: Optional[datetime] = Field(None, description="Last failure timestamp")
    last_success_time: Optional[datetime] = Field(None, description="Last success timestamp")
    state_changed_at: datetime = Field(default_factory=datetime.utcnow, description="State change timestamp")
    
    # Metrics
    total_calls: int = Field(default=0, description="Total calls processed")
    successful_calls: int = Field(default=0, description="Successful calls")
    failed_calls: int = Field(default=0, description="Failed calls")
    rejected_calls: int = Field(default=0, description="Rejected calls (circuit open)")
    
    class Config:
        schema_extra = {
            "example": {
                "endpoint_id": "endpoint-1",
                "state": "closed",
                "failure_threshold": 5,
                "success_threshold": 3,
                "failure_count": 1,
                "total_calls": 1000,
                "successful_calls": 950,
                "failed_calls": 49
            }
        }


class LoadBalancer(BaseModel):
    """Load balancer configuration and status."""
    strategy: LoadBalancingStrategy = Field(default=LoadBalancingStrategy.ROUND_ROBIN, description="Balancing strategy")
    sticky_sessions: bool = Field(default=False, description="Enable sticky sessions")
    health_check_interval: int = Field(default=30, description="Health check interval in seconds", ge=1, le=3600)
    
    # Endpoint weights for weighted strategies
    endpoint_weights: Dict[str, int] = Field(default_factory=dict, description="Endpoint weights")
    
    # Geographic routing
    region_preferences: Dict[str, List[str]] = Field(default_factory=dict, description="Region routing preferences")
    
    # Current state
    active_endpoints: List[str] = Field(default_factory=list, description="Currently active endpoint IDs")
    total_requests: int = Field(default=0, description="Total requests balanced")
    request_distribution: Dict[str, int] = Field(default_factory=dict, description="Requests per endpoint")
    
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "strategy": "weighted_round_robin",
                "health_check_interval": 30,
                "endpoint_weights": {
                    "endpoint-1": 150,
                    "endpoint-2": 100,
                    "endpoint-3": 200
                },
                "active_endpoints": ["endpoint-1", "endpoint-2", "endpoint-3"],
                "total_requests": 50000
            }
        }


# Request/Response Models

class ProxyRequest(BaseModel):
    """Request to be proxied to a federation endpoint."""
    method: str = Field(..., description="HTTP method")
    path: str = Field(..., description="Request path")
    headers: Dict[str, str] = Field(default_factory=dict, description="Request headers")
    query_params: Dict[str, str] = Field(default_factory=dict, description="Query parameters")
    body: Optional[bytes] = Field(None, description="Request body")
    target_endpoint: Optional[str] = Field(None, description="Specific target endpoint ID")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    
    class Config:
        schema_extra = {
            "example": {
                "method": "POST",
                "path": "/v1/search",
                "headers": {"Content-Type": "application/json"},
                "query_params": {"limit": "100"},
                "timeout": 30
            }
        }


class ProxyResponse(BaseModel):
    """Response from a proxied request."""
    status_code: int = Field(..., description="HTTP status code")
    headers: Dict[str, str] = Field(default_factory=dict, description="Response headers")
    body: Any = Field(None, description="Response body")
    endpoint_id: str = Field(..., description="Endpoint that handled the request")
    response_time_ms: float = Field(..., description="Response time in milliseconds")
    attempt_count: int = Field(default=1, description="Number of attempts made")
    
    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "headers": {"Content-Type": "application/json"},
                "body": {"results": []},
                "endpoint_id": "endpoint-1",
                "response_time_ms": 125.5,
                "attempt_count": 1
            }
        }


# Health and Monitoring Models

class HealthStatus(BaseModel):
    """Health status of a federation endpoint."""
    endpoint_id: str = Field(..., description="Endpoint identifier")
    status: EndpointStatus = Field(..., description="Current status")
    last_check: datetime = Field(..., description="Last health check timestamp")
    response_time_ms: Optional[float] = Field(None, description="Response time in milliseconds")
    
    # Health details
    checks: Dict[str, Any] = Field(default_factory=dict, description="Individual health check results")
    error_message: Optional[str] = Field(None, description="Error message if unhealthy")
    
    # Performance metrics
    success_rate_1h: Optional[float] = Field(None, description="Success rate over last hour")
    success_rate_24h: Optional[float] = Field(None, description="Success rate over last 24 hours")
    avg_response_time_1h: Optional[float] = Field(None, description="Average response time over last hour")
    
    # Connection status
    active_connections: int = Field(default=0, description="Active connections")
    circuit_breaker_state: CircuitBreakerState = Field(default=CircuitBreakerState.CLOSED)
    
    class Config:
        schema_extra = {
            "example": {
                "endpoint_id": "endpoint-1",
                "status": "healthy",
                "last_check": "2025-09-21T16:30:00Z",
                "response_time_ms": 125.5,
                "success_rate_1h": 99.2,
                "success_rate_24h": 98.8,
                "active_connections": 45,
                "circuit_breaker_state": "closed"
            }
        }


class FederationMetrics(BaseModel):
    """Comprehensive federation performance metrics."""
    time_range: str = Field(..., description="Metrics time range")
    total_requests: int = Field(default=0, description="Total requests processed")
    successful_requests: int = Field(default=0, description="Successful requests")
    failed_requests: int = Field(default=0, description="Failed requests")
    
    # Performance metrics
    average_response_time: float = Field(default=0.0, description="Average response time in ms")
    p95_response_time: float = Field(default=0.0, description="95th percentile response time in ms")
    p99_response_time: float = Field(default=0.0, description="99th percentile response time in ms")
    
    # Endpoint metrics
    endpoint_metrics: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Per-endpoint metrics")
    
    # Load balancing metrics
    request_distribution: Dict[str, int] = Field(default_factory=dict, description="Request distribution by endpoint")
    load_balancing_efficiency: float = Field(default=0.0, description="Load balancing efficiency score")
    
    # Error metrics
    error_rate: float = Field(default=0.0, description="Overall error rate percentage")
    error_types: Dict[str, int] = Field(default_factory=dict, description="Error types and counts")
    
    # Security metrics
    authentication_failures: int = Field(default=0, description="Authentication failures")
    rate_limit_violations: int = Field(default=0, description="Rate limit violations")
    security_violations: int = Field(default=0, description="Security policy violations")
    
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Metrics generation timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "time_range": "24h",
                "total_requests": 100000,
                "successful_requests": 99200,
                "failed_requests": 800,
                "average_response_time": 145.2,
                "p95_response_time": 280.5,
                "error_rate": 0.8,
                "load_balancing_efficiency": 94.2
            }
        }


# Topology and Discovery Models

class ServiceDiscovery(BaseModel):
    """Service discovery information."""
    endpoint_id: str = Field(..., description="Endpoint identifier")
    discovered_services: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Discovered services")
    capabilities: List[str] = Field(default_factory=list, description="Service capabilities")
    api_versions: Dict[str, str] = Field(default_factory=dict, description="API versions")
    health_endpoints: Dict[str, str] = Field(default_factory=dict, description="Health check endpoints")
    
    last_discovery: datetime = Field(default_factory=datetime.utcnow, description="Last discovery timestamp")
    discovery_method: str = Field(default="api_introspection", description="Discovery method used")
    
    class Config:
        schema_extra = {
            "example": {
                "endpoint_id": "endpoint-1",
                "discovered_services": {
                    "search": {"version": "v1", "status": "available"},
                    "graph": {"version": "v1", "status": "available"}
                },
                "capabilities": ["full_text_search", "graph_analytics", "nlp_processing"],
                "api_versions": {"search": "v1", "graph": "v1", "nlp": "v1"}
            }
        }


class FederationTopology(BaseModel):
    """Federation network topology information."""
    total_endpoints: int = Field(default=0, description="Total configured endpoints")
    healthy_endpoints: int = Field(default=0, description="Healthy endpoints")
    
    # Geographic distribution
    regions: Dict[str, List[str]] = Field(default_factory=dict, description="Endpoints by region")
    datacenters: Dict[str, List[str]] = Field(default_factory=dict, description="Endpoints by datacenter")
    
    # Service distribution
    service_coverage: Dict[str, List[str]] = Field(default_factory=dict, description="Service coverage by endpoint")
    
    # Network topology
    connections: List[Dict[str, Any]] = Field(default_factory=list, description="Network connections")
    latency_matrix: Dict[str, Dict[str, float]] = Field(default_factory=dict, description="Inter-endpoint latencies")
    
    # Load distribution
    load_distribution: Dict[str, float] = Field(default_factory=dict, description="Load distribution by endpoint")
    
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "total_endpoints": 5,
                "healthy_endpoints": 4,
                "regions": {
                    "us-east": ["endpoint-1", "endpoint-2"],
                    "us-west": ["endpoint-3"],
                    "eu-central": ["endpoint-4", "endpoint-5"]
                },
                "service_coverage": {
                    "search": ["endpoint-1", "endpoint-2", "endpoint-3"],
                    "graph": ["endpoint-1", "endpoint-4", "endpoint-5"]
                }
            }
        }


class ConfigurationSync(BaseModel):
    """Configuration synchronization status."""
    endpoint_id: str = Field(..., description="Endpoint identifier")
    config_version: str = Field(..., description="Configuration version")
    last_sync: datetime = Field(..., description="Last synchronization timestamp")
    sync_status: str = Field(..., description="Synchronization status")
    
    # Sync details
    synced_items: List[str] = Field(default_factory=list, description="Successfully synced items")
    failed_items: List[str] = Field(default_factory=list, description="Failed sync items")
    conflicts: List[Dict[str, Any]] = Field(default_factory=list, description="Configuration conflicts")
    
    next_sync: Optional[datetime] = Field(None, description="Next scheduled sync")
    
    class Config:
        schema_extra = {
            "example": {
                "endpoint_id": "endpoint-1",
                "config_version": "1.2.3",
                "last_sync": "2025-09-21T16:30:00Z",
                "sync_status": "success",
                "synced_items": ["routing_rules", "security_policies"],
                "failed_items": [],
                "conflicts": []
            }
        }


# Main Configuration Model

class FederationConfig(BaseModel):
    """Complete federation configuration."""
    version: str = Field(default="1.0", description="Configuration version")
    
    # Core configuration
    endpoints: List[RemoteEndpoint] = Field(default_factory=list, description="Remote endpoints")
    routing_rules: List[RoutingRule] = Field(default_factory=list, description="Routing rules")
    security_policies: List[SecurityPolicy] = Field(default_factory=list, description="Security policies")
    
    # Load balancing
    load_balancer: LoadBalancer = Field(default_factory=LoadBalancer, description="Load balancer configuration")
    
    # Global settings
    default_timeout: int = Field(default=30, description="Default request timeout", ge=1, le=300)
    max_retries: int = Field(default=3, description="Default max retries", ge=0, le=10)
    health_check_interval: int = Field(default=30, description="Health check interval", ge=1, le=3600)
    
    # Feature flags
    enable_circuit_breaker: bool = Field(default=True, description="Enable circuit breaker")
    enable_request_logging: bool = Field(default=True, description="Enable request logging")
    enable_metrics_collection: bool = Field(default=True, description="Enable metrics collection")
    
    # Metadata
    name: str = Field(default="InfoTerminal Federation", description="Federation name")
    description: Optional[str] = Field(None, description="Federation description")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "version": "1.0",
                "name": "InfoTerminal Production Federation",
                "description": "Production federation for InfoTerminal services",
                "default_timeout": 30,
                "max_retries": 3,
                "enable_circuit_breaker": True,
                "endpoints": [],
                "routing_rules": [],
                "security_policies": []
            }
        }
