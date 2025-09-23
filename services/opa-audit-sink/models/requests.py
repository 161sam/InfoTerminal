"""
Request models for OPA Audit Sink API.
"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field, validator


class OPADecisionLogRequest(BaseModel):
    """Request model for OPA decision log entry."""
    
    timestamp: Optional[str] = Field(
        default=None,
        description="Decision timestamp (ISO format, defaults to current time)"
    )
    
    decision_id: Optional[str] = Field(
        default=None,
        description="Unique decision identifier"
    )
    
    path: Optional[str] = Field(
        default="",
        description="OPA policy path that was evaluated"
    )
    
    input: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Input data provided to OPA for decision"
    )
    
    result: Optional[Union[bool, Dict[str, Any]]] = Field(
        default=False,
        description="OPA decision result"
    )
    
    bundles: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="OPA bundle information"
    )
    
    metrics: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Performance metrics for the decision"
    )
    
    erased: Optional[List[str]] = Field(
        default_factory=list,
        description="List of erased/redacted fields"
    )
    
    nd_builtin_cache: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Non-deterministic builtin cache data"
    )
    
    @validator('timestamp')
    def validate_timestamp(cls, v):
        """Validate timestamp format."""
        if v is not None:
            try:
                datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("Timestamp must be in ISO format")
        return v


class OPABulkLogRequest(BaseModel):
    """Request model for bulk OPA decision log entries."""
    
    logs: List[OPADecisionLogRequest] = Field(
        ...,
        description="List of OPA decision log entries",
        min_items=1,
        max_items=1000
    )
    
    batch_id: Optional[str] = Field(
        default=None,
        description="Optional batch identifier"
    )
    
    source: Optional[str] = Field(
        default=None,
        description="Source system or OPA instance identifier"
    )


class AuditQueryRequest(BaseModel):
    """Request model for querying audit logs."""
    
    start_time: Optional[datetime] = Field(
        default=None,
        description="Start time for query range"
    )
    
    end_time: Optional[datetime] = Field(
        default=None,
        description="End time for query range"
    )
    
    user: Optional[str] = Field(
        default=None,
        description="Filter by username"
    )
    
    tenant: Optional[str] = Field(
        default=None,
        description="Filter by tenant"
    )
    
    action: Optional[str] = Field(
        default=None,
        description="Filter by action"
    )
    
    classification: Optional[str] = Field(
        default=None,
        description="Filter by resource classification"
    )
    
    allowed: Optional[bool] = Field(
        default=None,
        description="Filter by decision result (allowed/denied)"
    )
    
    path: Optional[str] = Field(
        default=None,
        description="Filter by OPA policy path"
    )
    
    decision_id: Optional[str] = Field(
        default=None,
        description="Filter by specific decision ID"
    )
    
    limit: int = Field(
        default=100,
        description="Maximum number of results",
        ge=1,
        le=10000
    )
    
    @validator('end_time')
    def validate_time_range(cls, v, values):
        """Validate that end_time is after start_time."""
        if v and 'start_time' in values and values['start_time']:
            if v <= values['start_time']:
                raise ValueError("End time must be after start time")
        return v


class AuditRetentionRequest(BaseModel):
    """Request model for audit log retention policy."""
    
    retention_days: int = Field(
        ...,
        description="Number of days to retain audit logs",
        ge=1,
        le=3650  # Max 10 years
    )
    
    policy_name: str = Field(
        default="default",
        description="Retention policy name",
        max_length=100
    )
    
    apply_immediately: bool = Field(
        default=False,
        description="Apply retention policy immediately"
    )
    
    backup_before_deletion: bool = Field(
        default=True,
        description="Create backup before deleting old logs"
    )
    
    dry_run: bool = Field(
        default=True,
        description="Perform dry run without actual deletion"
    )


class AuditExportRequest(BaseModel):
    """Request model for exporting audit logs."""
    
    start_time: datetime = Field(
        ...,
        description="Export start time"
    )
    
    end_time: datetime = Field(
        ...,
        description="Export end time"
    )
    
    format: str = Field(
        default="json",
        description="Export format",
        regex=r"^(json|csv|parquet)$"
    )
    
    include_raw_logs: bool = Field(
        default=False,
        description="Include raw OPA decision logs"
    )
    
    compress: bool = Field(
        default=True,
        description="Compress export file"
    )
    
    filters: Optional[AuditQueryRequest] = Field(
        default=None,
        description="Optional filters for export"
    )


class AuditConfigRequest(BaseModel):
    """Request model for audit configuration updates."""
    
    clickhouse_url: Optional[str] = Field(
        default=None,
        description="ClickHouse connection URL"
    )
    
    database: Optional[str] = Field(
        default=None,
        description="ClickHouse database name"
    )
    
    table: Optional[str] = Field(
        default=None,
        description="ClickHouse table name"
    )
    
    batch_size: Optional[int] = Field(
        default=None,
        description="Batch size for log ingestion",
        ge=1,
        le=10000
    )
    
    flush_interval: Optional[int] = Field(
        default=None,
        description="Flush interval in seconds",
        ge=1,
        le=3600
    )
    
    enable_compression: Optional[bool] = Field(
        default=None,
        description="Enable compression for storage"
    )
    
    enable_encryption: Optional[bool] = Field(
        default=None,
        description="Enable encryption for sensitive data"
    )


class AuditAlertRequest(BaseModel):
    """Request model for setting up audit alerts."""
    
    alert_name: str = Field(
        ...,
        description="Alert name",
        max_length=100
    )
    
    condition: str = Field(
        ...,
        description="Alert condition (SQL-like expression)",
        max_length=1000
    )
    
    threshold: Optional[float] = Field(
        default=None,
        description="Threshold value for numeric conditions"
    )
    
    time_window: int = Field(
        default=300,
        description="Time window in seconds for alert evaluation",
        ge=60,
        le=86400
    )
    
    severity: str = Field(
        default="medium",
        description="Alert severity level",
        regex=r"^(low|medium|high|critical)$"
    )
    
    notification_channels: List[str] = Field(
        default_factory=list,
        description="Notification channels for alerts"
    )
    
    enabled: bool = Field(
        default=True,
        description="Whether alert is enabled"
    )
