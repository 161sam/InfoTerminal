"""
Response models for Egress Gateway API.
"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field

from .requests import ProxyType, AnonymityLevel


class ProxyResponse(BaseModel):
    """Response from a proxied HTTP request."""
    
    request_id: str = Field(..., description="Unique request identifier")
    status_code: int = Field(..., description="HTTP status code from target")
    
    headers: Dict[str, str] = Field(
        default_factory=dict,
        description="Response headers (sanitized)"
    )
    
    content: str = Field(..., description="Response content/body")
    content_type: Optional[str] = Field(None, description="Content type")
    content_length: Optional[int] = Field(None, description="Content length in bytes")
    
    proxy_used: str = Field(..., description="Proxy configuration used")
    proxy_type: ProxyType = Field(..., description="Type of proxy used")
    anonymity_level: AnonymityLevel = Field(..., description="Achieved anonymity level")
    
    execution_time: float = Field(..., description="Request execution time in seconds")
    
    target_url: str = Field(..., description="Target URL (may differ from request if redirected)")
    method: str = Field(..., description="HTTP method used")
    
    redirects: List[str] = Field(
        default_factory=list,
        description="Redirect chain if any"
    )
    
    retry_count: int = Field(default=0, description="Number of retries performed")
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional request metadata"
    )
    
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    tags: List[str] = Field(
        default_factory=list,
        description="Request tags"
    )


class ProxyStatus(BaseModel):
    """Current status of proxy infrastructure."""
    
    # Tor Status
    tor_available: bool = Field(..., description="Tor daemon availability")
    tor_circuit_established: bool = Field(..., description="Tor circuit status")
    tor_country_exit: Optional[str] = Field(None, description="Tor exit node country")
    
    # VPN Status
    vpn_available: bool = Field(..., description="VPN connection availability")
    vpn_pools: List[str] = Field(default_factory=list, description="Available VPN pools")
    active_vpn: Optional[str] = Field(None, description="Currently active VPN")
    
    # Proxy Status
    proxy_pools: List[str] = Field(default_factory=list, description="Available proxy pools")
    active_proxy: Optional[str] = Field(None, description="Currently active proxy")
    
    # Overall Status
    anonymity_level: AnonymityLevel = Field(..., description="Current anonymity level")
    active_proxy_type: ProxyType = Field(..., description="Currently active proxy type")
    
    # Performance Metrics
    request_count: int = Field(default=0, description="Total requests processed")
    success_rate: float = Field(default=0.0, description="Success rate percentage")
    average_response_time: float = Field(default=0.0, description="Average response time")
    
    # Rotation Status  
    last_rotation: Optional[datetime] = Field(None, description="Last identity rotation time")
    rotation_interval: int = Field(default=3600, description="Auto-rotation interval in seconds")
    auto_rotation_enabled: bool = Field(default=True, description="Auto-rotation status")
    
    # System Status
    uptime_seconds: int = Field(..., description="Service uptime in seconds")
    health_status: str = Field(..., description="Overall health status")
    
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Status timestamp")


class ProxyStatistics(BaseModel):
    """Comprehensive proxy usage statistics."""
    
    # Request Statistics
    total_requests: int = Field(default=0, description="Total requests processed")
    successful_requests: int = Field(default=0, description="Successful requests")
    failed_requests: int = Field(default=0, description="Failed requests")
    
    # Timing Statistics
    average_response_time: float = Field(default=0.0, description="Average response time")
    fastest_response_time: float = Field(default=0.0, description="Fastest response time")
    slowest_response_time: float = Field(default=0.0, description="Slowest response time")
    
    # Proxy Type Usage
    proxy_type_usage: Dict[str, int] = Field(
        default_factory=dict,
        description="Usage count by proxy type"
    )
    
    # Anonymity Level Usage
    anonymity_level_usage: Dict[str, int] = Field(
        default_factory=dict,
        description="Usage count by anonymity level"
    )
    
    # Status Code Distribution
    status_code_distribution: Dict[str, int] = Field(
        default_factory=dict,
        description="Distribution of HTTP status codes"
    )
    
    # Domain Statistics (top domains)
    top_domains: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Most frequently accessed domains"
    )
    
    # Error Statistics
    error_types: Dict[str, int] = Field(
        default_factory=dict,
        description="Distribution of error types"
    )
    
    # Rotation Statistics
    identity_rotations: int = Field(default=0, description="Total identity rotations")
    average_rotation_interval: float = Field(default=0.0, description="Average rotation interval")
    
    # Bandwidth Statistics
    total_bytes_sent: int = Field(default=0, description="Total bytes sent")
    total_bytes_received: int = Field(default=0, description="Total bytes received")
    
    # Time Range
    statistics_period: str = Field(..., description="Time period for these statistics")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last statistics update")


class ProxyHealthStatus(BaseModel):
    """Detailed health status of proxy system components."""
    
    overall_health: str = Field(..., description="Overall system health")
    
    # Component Health
    components: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Health status of individual components"
    )
    
    # Connectivity Tests
    connectivity_tests: Dict[str, bool] = Field(
        default_factory=dict,
        description="Results of connectivity tests"
    )
    
    # Performance Metrics
    performance_metrics: Dict[str, float] = Field(
        default_factory=dict,
        description="Current performance metrics"
    )
    
    # Resource Usage
    resource_usage: Dict[str, Any] = Field(
        default_factory=dict,
        description="System resource usage"
    )
    
    # Alerts
    active_alerts: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Active system alerts"
    )
    
    last_health_check: datetime = Field(default_factory=datetime.utcnow, description="Last health check time")


class RotationResult(BaseModel):
    """Result of proxy/identity rotation."""
    
    success: bool = Field(..., description="Whether rotation was successful")
    rotation_type: str = Field(..., description="Type of rotation performed")
    
    previous_proxy: Optional[str] = Field(None, description="Previous proxy configuration")
    new_proxy: Optional[str] = Field(None, description="New proxy configuration")
    
    previous_anonymity: Optional[AnonymityLevel] = Field(None, description="Previous anonymity level")
    new_anonymity: Optional[AnonymityLevel] = Field(None, description="New anonymity level")
    
    rotation_time: float = Field(..., description="Time taken for rotation in seconds")
    message: str = Field(..., description="Human-readable result message")
    
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Rotation timestamp")
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional rotation metadata"
    )


class ProxyConfigInfo(BaseModel):
    """Proxy configuration information."""
    
    proxy_type: ProxyType = Field(..., description="Proxy type")
    enabled: bool = Field(..., description="Whether this proxy type is enabled")
    
    priority: int = Field(..., description="Priority for auto-selection")
    timeout: int = Field(..., description="Default timeout")
    max_concurrent: int = Field(..., description="Maximum concurrent requests")
    
    anonymity_level: AnonymityLevel = Field(..., description="Anonymity level provided")
    
    rotation_interval: int = Field(..., description="Auto-rotation interval")
    last_rotation: Optional[datetime] = Field(None, description="Last rotation time")
    
    # Performance Stats
    success_rate: float = Field(..., description="Success rate for this proxy type")
    average_response_time: float = Field(..., description="Average response time")
    total_requests: int = Field(..., description="Total requests through this proxy")
    
    # Status
    status: str = Field(..., description="Current proxy status")
    health_check: bool = Field(..., description="Health check result")
    
    custom_settings: Dict[str, Any] = Field(
        default_factory=dict,
        description="Proxy-specific configuration"
    )
    
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last configuration update")


class BulkProxyResponse(BaseModel):
    """Response from bulk proxy requests."""
    
    batch_id: str = Field(..., description="Batch identifier")
    total_requests: int = Field(..., description="Total requests in batch")
    
    completed_requests: int = Field(default=0, description="Completed requests")
    successful_requests: int = Field(default=0, description="Successful requests")
    failed_requests: int = Field(default=0, description="Failed requests")
    
    responses: List[ProxyResponse] = Field(
        default_factory=list,
        description="Individual request responses"
    )
    
    execution_time: float = Field(..., description="Total batch execution time")
    
    batch_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Batch metadata"
    )
    
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Batch completion timestamp")


class ProxyCapabilities(BaseModel):
    """System proxy capabilities and limits."""
    
    supported_proxy_types: List[ProxyType] = Field(..., description="Supported proxy types")
    supported_anonymity_levels: List[AnonymityLevel] = Field(..., description="Supported anonymity levels")
    
    max_concurrent_requests: int = Field(..., description="Maximum concurrent requests")
    max_request_timeout: int = Field(..., description="Maximum request timeout")
    max_bulk_requests: int = Field(..., description="Maximum bulk request size")
    
    features: Dict[str, bool] = Field(
        default_factory=dict,
        description="Available features"
    )
    
    rate_limits: Dict[str, int] = Field(
        default_factory=dict,
        description="Rate limiting configuration"
    )
    
    supported_protocols: List[str] = Field(
        default_factory=list,
        description="Supported protocols"
    )
    
    geographical_coverage: List[str] = Field(
        default_factory=list,
        description="Available geographical regions"
    )
