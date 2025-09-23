"""
Pydantic models for Ops Controller Service v1.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


# Ops Management Models
class StackInfo(BaseModel):
    """Information about a service stack."""
    name: str = Field(..., description="Stack name")
    files: List[str] = Field(..., description="Docker compose file paths")


class StackListResponse(BaseModel):
    """Response for listing available stacks."""
    stacks: Dict[str, StackInfo] = Field(..., description="Available service stacks")


class ServiceStatus(BaseModel):
    """Status information for a service."""
    name: str = Field(..., description="Service name")
    status: str = Field(..., description="Service status (running, stopped, etc.)")
    state: str = Field(..., description="Service state")
    health: str = Field(..., description="Health status")


class StackStatusResponse(BaseModel):
    """Response for stack status check."""
    stack: str = Field(..., description="Stack name")
    services: List[ServiceStatus] = Field(..., description="Service status list")


class StackOperationResponse(BaseModel):
    """Response for stack operations (up/down/restart)."""
    ok: bool = Field(..., description="Operation success status")
    stack: str = Field(..., description="Stack name")
    message: str = Field(default="Operation completed successfully")


class ScaleRequest(BaseModel):
    """Request to scale a service."""
    service: str = Field(..., description="Service name to scale")
    replicas: int = Field(..., description="Number of replicas", ge=0, le=10)


class ScaleResponse(BaseModel):
    """Response for scaling operation."""
    ok: bool = Field(..., description="Scaling success status")
    stack: str = Field(..., description="Stack name")
    service: str = Field(..., description="Service name")
    replicas: int = Field(..., description="New replica count")


# Security Models
class StartIncognitoRequest(BaseModel):
    """Request to start incognito session."""
    sessionId: str = Field(..., description="Unique session identifier")
    autoWipeMinutes: Optional[int] = Field(None, description="Auto-wipe timeout in minutes")
    memoryOnlyMode: bool = Field(True, description="Use memory-only mode")
    isolatedContainers: bool = Field(True, description="Use isolated containers")


class IncognitoSessionResponse(BaseModel):
    """Response for incognito session operations."""
    sessionId: str = Field(..., description="Session identifier")
    containerCount: int = Field(..., description="Number of containers", ge=0)
    memoryOnlyMode: bool = Field(..., description="Memory-only mode active")


class IncognitoStatusResponse(BaseModel):
    """Status of incognito mode."""
    active: bool = Field(..., description="Whether incognito mode is active")
    sessionId: Optional[str] = Field(None, description="Current session ID")
    timeRemaining: Optional[float] = Field(None, description="Time remaining until auto-wipe (ms)")


class ContainerInfo(BaseModel):
    """Container information."""
    id: str = Field(..., description="Container ID")
    name: str = Field(..., description="Container name")
    status: str = Field(..., description="Container status")
    image: str = Field(..., description="Container image")
    created: str = Field(..., description="Creation timestamp")


class ContainersStatusResponse(BaseModel):
    """Container security status."""
    ephemeralContainers: List[ContainerInfo] = Field(default_factory=list, description="Ephemeral containers")
    memoryOnlyMode: bool = Field(..., description="Memory-only mode active")
    autoWipeEnabled: bool = Field(..., description="Auto-wipe enabled")


class WipeDataRequest(BaseModel):
    """Request to wipe session data."""
    sessionId: str = Field(..., description="Session ID to wipe")
    secure: bool = Field(True, description="Use secure wiping")
    overwritePasses: int = Field(3, description="Number of overwrite passes", ge=1, le=10)


class WipeResponse(BaseModel):
    """Response for data wiping operations."""
    success: bool = Field(..., description="Wipe operation success")
    sessionId: str = Field(..., description="Session ID")
    message: str = Field(default="Data wiping completed")


class DataCategory(BaseModel):
    """Data category for scanning."""
    id: str = Field(..., description="Category identifier")
    name: str = Field(..., description="Category name")
    size_bytes: int = Field(..., description="Data size in bytes", ge=0)
    file_count: int = Field(..., description="Number of files", ge=0)
    sensitive: bool = Field(..., description="Contains sensitive data")


class DataScanResponse(BaseModel):
    """Response for data scanning."""
    categories: List[DataCategory] = Field(..., description="Data categories found")


# Performance Monitoring Models
class SystemMetrics(BaseModel):
    """System performance metrics."""
    cpu_usage_percent: float = Field(..., description="CPU usage percentage", ge=0, le=100)
    memory_usage_percent: float = Field(..., description="Memory usage percentage", ge=0, le=100)
    disk_usage_percent: float = Field(..., description="Disk usage percentage", ge=0, le=100)
    uptime_seconds: float = Field(..., description="System uptime in seconds", ge=0)


class CpuMetrics(BaseModel):
    """CPU performance metrics."""
    usage_percent: float = Field(..., description="CPU usage percentage")
    load_avg: List[float] = Field(..., description="Load averages [1m, 5m, 15m]")
    core_count: int = Field(..., description="Number of CPU cores", ge=1)


class MemoryMetrics(BaseModel):
    """Memory performance metrics."""
    total_gb: float = Field(..., description="Total memory in GB")
    used_gb: float = Field(..., description="Used memory in GB")
    available_gb: float = Field(..., description="Available memory in GB")
    usage_percent: float = Field(..., description="Memory usage percentage")


class DiskMetrics(BaseModel):
    """Disk performance metrics."""
    total_gb: float = Field(..., description="Total disk space in GB")
    used_gb: float = Field(..., description="Used disk space in GB")
    free_gb: float = Field(..., description="Free disk space in GB")
    usage_percent: float = Field(..., description="Disk usage percentage")


class NetworkMetrics(BaseModel):
    """Network performance metrics."""
    bytes_sent: int = Field(..., description="Bytes sent", ge=0)
    bytes_recv: int = Field(..., description="Bytes received", ge=0)
    packets_sent: int = Field(..., description="Packets sent", ge=0)
    packets_recv: int = Field(..., description="Packets received", ge=0)


class RedisStatus(BaseModel):
    """Redis connection status."""
    available: bool = Field(..., description="Redis available")
    connected_clients: int = Field(0, description="Connected clients", ge=0)
    used_memory_human: str = Field("N/A", description="Used memory (human readable)")
    keyspace_hits: int = Field(0, description="Keyspace hits", ge=0)
    keyspace_misses: int = Field(0, description="Keyspace misses", ge=0)
    hit_rate: Optional[float] = Field(None, description="Cache hit rate", ge=0, le=1)


class ComprehensiveHealthResponse(BaseModel):
    """Comprehensive health check response."""
    status: str = Field(..., description="Overall health status")
    timestamp: float = Field(..., description="Check timestamp")
    response_time_ms: float = Field(..., description="Response time in milliseconds")
    system_metrics: SystemMetrics = Field(..., description="System performance metrics")
    service_status: Dict[str, Any] = Field(..., description="Service status information")
    redis_status: RedisStatus = Field(..., description="Redis status")
    security_manager_active: bool = Field(..., description="Security manager status")


class SystemPerformanceResponse(BaseModel):
    """System performance metrics response."""
    timestamp: float = Field(..., description="Metrics timestamp")
    cpu: CpuMetrics = Field(..., description="CPU metrics")
    memory: MemoryMetrics = Field(..., description="Memory metrics")
    disk: DiskMetrics = Field(..., description="Disk metrics")
    network: NetworkMetrics = Field(..., description="Network metrics")
    uptime_hours: float = Field(..., description="System uptime in hours")


# Container Operations Models
class ContainerOperationResponse(BaseModel):
    """Response for container operations."""
    success: bool = Field(..., description="Operation success")
    containerId: str = Field(..., description="Container ID")
    message: str = Field(default="Container operation completed")


class EmergencyShutdownResponse(BaseModel):
    """Response for emergency shutdown."""
    success: bool = Field(..., description="Shutdown success")
    message: str = Field(..., description="Shutdown status message")


# Log Streaming Models  
class LogRequest(BaseModel):
    """Request for log streaming."""
    service: Optional[str] = Field(None, description="Specific service to get logs for")
    tail: Optional[int] = Field(None, description="Number of lines to tail")
    follow: bool = Field(True, description="Follow log output")


# General Response Models
class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    code: str = Field(..., description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
