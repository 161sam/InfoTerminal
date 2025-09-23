"""
Pydantic models for Performance Monitor Service v1.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class AlertLevel(str, Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class MetricType(str, Enum):
    """Types of performance metrics."""
    RESPONSE_TIME = "response_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    DATABASE_LATENCY = "database_latency"


class PerformanceMetric(BaseModel):
    """Individual performance metric."""
    id: str = Field(..., description="Unique metric identifier")
    timestamp: datetime = Field(..., description="When the metric was recorded")
    metric_type: MetricType = Field(..., description="Type of metric")
    value: float = Field(..., description="Metric value")
    service_name: str = Field(..., description="Service that generated the metric")
    endpoint: Optional[str] = Field(None, description="API endpoint (if applicable)")
    user_id: Optional[str] = Field(None, description="User identifier (if applicable)")
    request_id: Optional[str] = Field(None, description="Request identifier")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metric metadata")


class PerformanceAlert(BaseModel):
    """Performance alert."""
    id: str = Field(..., description="Unique alert identifier")
    timestamp: datetime = Field(..., description="When the alert was triggered")
    level: AlertLevel = Field(..., description="Alert severity level")
    metric_type: MetricType = Field(..., description="Type of metric that triggered alert")
    message: str = Field(..., description="Human-readable alert message")
    threshold_value: float = Field(..., description="Threshold that was exceeded")
    actual_value: float = Field(..., description="Actual metric value")
    service_name: str = Field(..., description="Service that triggered the alert")
    endpoint: Optional[str] = Field(None, description="Endpoint (if applicable)")
    resolved: bool = Field(False, description="Whether alert has been resolved")
    resolved_at: Optional[datetime] = Field(None, description="When alert was resolved")


class MetricRequest(BaseModel):
    """Request to record a custom performance metric."""
    metric_type: MetricType = Field(..., description="Type of metric to record")
    value: float = Field(..., description="Metric value")
    service_name: str = Field(..., description="Service name")
    endpoint: Optional[str] = Field(None, description="API endpoint")
    user_id: Optional[str] = Field(None, description="User identifier")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class MetricRecordResponse(BaseModel):
    """Response for recording a metric."""
    message: str = Field(..., description="Status message")
    metric_id: str = Field(..., description="ID of recorded metric")


class ResponseTimeAnalysis(BaseModel):
    """Response time trend analysis."""
    trend: str = Field(..., description="Trend direction (improving/degrading/stable/no_data/insufficient_data)")
    slope: Optional[float] = Field(None, description="Trend slope")
    average_ms: Optional[float] = Field(None, description="Average response time in milliseconds")
    p95_ms: Optional[float] = Field(None, description="95th percentile response time")
    min_ms: Optional[float] = Field(None, description="Minimum response time")
    max_ms: Optional[float] = Field(None, description="Maximum response time")
    recommendation: str = Field(..., description="Optimization recommendation")


class MemoryAnalysis(BaseModel):
    """Memory usage pattern analysis."""
    status: str = Field(..., description="Memory status (normal/high_usage/memory_leak_suspected/no_data)")
    trend: Optional[float] = Field(None, description="Memory usage trend")
    average_percent: Optional[float] = Field(None, description="Average memory usage percentage")
    peak_percent: Optional[float] = Field(None, description="Peak memory usage percentage")
    recommendation: str = Field(..., description="Memory optimization recommendation")


class ServiceSummaryResponse(BaseModel):
    """Performance summary for a service."""
    service_name: str = Field(..., description="Service name")
    time_range_hours: int = Field(..., description="Time range analyzed in hours")
    response_time: ResponseTimeAnalysis = Field(..., description="Response time analysis")
    memory: MemoryAnalysis = Field(..., description="Memory usage analysis")
    error_rate_percent: float = Field(..., description="Error rate percentage")
    total_requests: int = Field(..., description="Total number of requests", ge=0)
    recommendations: List[str] = Field(..., description="Optimization recommendations")


class AlertsResponse(BaseModel):
    """Response containing performance alerts."""
    alerts: List[PerformanceAlert] = Field(..., description="List of performance alerts")
    total: int = Field(..., description="Total number of alerts", ge=0)


class MetricsResponse(BaseModel):
    """Response containing performance metrics."""
    metrics: List[PerformanceMetric] = Field(..., description="List of performance metrics")
    total: int = Field(..., description="Total number of metrics", ge=0)
    service_name: str = Field(..., description="Service name")
    metric_type: MetricType = Field(..., description="Metric type")


class SystemMetrics(BaseModel):
    """Current system performance metrics."""
    cpu_usage_percent: float = Field(..., description="CPU usage percentage", ge=0, le=100)
    memory_usage_percent: float = Field(..., description="Memory usage percentage", ge=0, le=100)
    disk_usage_percent: float = Field(..., description="Disk usage percentage", ge=0, le=100)
    load_average: Optional[List[float]] = Field(None, description="System load averages [1m, 5m, 15m]")
    uptime_hours: float = Field(..., description="System uptime in hours", ge=0)


class PerformanceThresholds(BaseModel):
    """Performance monitoring thresholds."""
    response_time_warning_ms: float = Field(500, description="Response time warning threshold (ms)")
    response_time_critical_ms: float = Field(2000, description="Response time critical threshold (ms)")
    memory_usage_warning_percent: float = Field(80, description="Memory usage warning threshold (%)")
    memory_usage_critical_percent: float = Field(95, description="Memory usage critical threshold (%)")
    cpu_usage_warning_percent: float = Field(70, description="CPU usage warning threshold (%)")
    cpu_usage_critical_percent: float = Field(90, description="CPU usage critical threshold (%)")
    error_rate_warning_percent: float = Field(5, description="Error rate warning threshold (%)")
    error_rate_critical_percent: float = Field(15, description="Error rate critical threshold (%)")


class ThresholdsUpdateRequest(BaseModel):
    """Request to update performance thresholds."""
    service_name: Optional[str] = Field(None, description="Service to update thresholds for (null for global)")
    thresholds: PerformanceThresholds = Field(..., description="New threshold values")


class ServiceHealthStatus(BaseModel):
    """Health status for a service."""
    service_name: str = Field(..., description="Service name")
    status: str = Field(..., description="Overall health status (healthy/degraded/critical)")
    last_check: datetime = Field(..., description="Last health check timestamp")
    response_time_status: str = Field(..., description="Response time health status")
    memory_status: str = Field(..., description="Memory usage health status")
    error_rate_status: str = Field(..., description="Error rate health status")
    active_alerts: int = Field(..., description="Number of active alerts", ge=0)


class OverallSystemHealth(BaseModel):
    """Overall system health summary."""
    status: str = Field(..., description="Overall system status")
    total_services: int = Field(..., description="Total number of monitored services", ge=0)
    healthy_services: int = Field(..., description="Number of healthy services", ge=0)
    degraded_services: int = Field(..., description="Number of degraded services", ge=0)
    critical_services: int = Field(..., description="Number of critical services", ge=0)
    total_alerts: int = Field(..., description="Total number of active alerts", ge=0)
    system_metrics: SystemMetrics = Field(..., description="Current system metrics")
    services: List[ServiceHealthStatus] = Field(..., description="Individual service health status")


class PerformanceReport(BaseModel):
    """Comprehensive performance report."""
    report_id: str = Field(..., description="Unique report identifier")
    generated_at: datetime = Field(..., description="Report generation timestamp")
    time_range_hours: int = Field(..., description="Time range covered by report")
    overall_health: OverallSystemHealth = Field(..., description="Overall system health")
    top_issues: List[str] = Field(..., description="Top performance issues identified")
    recommendations: List[str] = Field(..., description="High-priority recommendations")
    metrics_summary: Dict[str, Any] = Field(..., description="Summary of key metrics")


class AlertRule(BaseModel):
    """Custom alert rule."""
    id: str = Field(..., description="Rule identifier")
    name: str = Field(..., description="Rule name")
    service_name: Optional[str] = Field(None, description="Service to monitor (null for all)")
    metric_type: MetricType = Field(..., description="Metric type to monitor")
    threshold: float = Field(..., description="Alert threshold")
    level: AlertLevel = Field(..., description="Alert level")
    enabled: bool = Field(True, description="Whether rule is enabled")
    cooldown_minutes: int = Field(5, description="Cooldown period between alerts", ge=1)


class CreateAlertRuleRequest(BaseModel):
    """Request to create a custom alert rule."""
    name: str = Field(..., description="Rule name", min_length=1)
    service_name: Optional[str] = Field(None, description="Service to monitor")
    metric_type: MetricType = Field(..., description="Metric type")
    threshold: float = Field(..., description="Alert threshold")
    level: AlertLevel = Field(..., description="Alert level")
    cooldown_minutes: int = Field(5, description="Cooldown period", ge=1, le=60)


class AlertRulesResponse(BaseModel):
    """Response containing alert rules."""
    rules: List[AlertRule] = Field(..., description="List of alert rules")
    total: int = Field(..., description="Total number of rules", ge=0)
