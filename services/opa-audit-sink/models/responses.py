"""
Response models for OPA Audit Sink API.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class OPADecisionLog(BaseModel):
    """Processed OPA decision log entry."""
    
    timestamp: datetime = Field(..., description="Decision timestamp")
    decision_id: str = Field(..., description="Unique decision identifier")
    path: str = Field(..., description="OPA policy path")
    
    # User context
    user: str = Field(default="", description="Username")
    roles: List[str] = Field(default_factory=list, description="User roles")
    tenant: str = Field(default="", description="User tenant")
    
    # Resource context
    classification: str = Field(default="", description="Resource classification")
    action: str = Field(default="", description="Action being performed")
    
    # Decision result
    allowed: bool = Field(..., description="Whether action was allowed")
    
    # Metadata
    policy_version: str = Field(default="", description="Policy bundle version")
    execution_time_ms: Optional[float] = Field(None, description="Execution time in milliseconds")
    
    # Raw data (optional)
    raw_log: Optional[Dict[str, Any]] = Field(None, description="Raw OPA decision log")
    
    # Ingestion metadata
    ingested_at: datetime = Field(default_factory=datetime.utcnow, description="Log ingestion timestamp")
    source: Optional[str] = Field(None, description="Source OPA instance")


class AuditIngestResult(BaseModel):
    """Result of audit log ingestion operation."""
    
    ingested_count: int = Field(..., description="Number of logs successfully ingested")
    failed_count: int = Field(default=0, description="Number of logs that failed to ingest")
    
    batch_id: Optional[str] = Field(None, description="Batch identifier")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    
    # Error details
    errors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Ingestion errors"
    )
    
    # Statistics
    total_size_bytes: Optional[int] = Field(None, description="Total data size processed")
    compression_ratio: Optional[float] = Field(None, description="Compression ratio achieved")
    
    # Storage details
    stored_in_table: str = Field(..., description="ClickHouse table where logs were stored")
    storage_backend: str = Field(default="clickhouse", description="Storage backend used")
    
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Ingestion timestamp")


class AuditStatistics(BaseModel):
    """Comprehensive audit log statistics."""
    
    # Volume statistics
    total_decisions: int = Field(default=0, description="Total number of decisions")
    decisions_allowed: int = Field(default=0, description="Number of allowed decisions")
    decisions_denied: int = Field(default=0, description="Number of denied decisions")
    
    # Time-based statistics
    decisions_last_hour: int = Field(default=0, description="Decisions in last hour")
    decisions_last_day: int = Field(default=0, description="Decisions in last day")
    decisions_last_week: int = Field(default=0, description="Decisions in last week")
    
    # User statistics
    unique_users: int = Field(default=0, description="Number of unique users")
    top_users: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Most active users"
    )
    
    # Policy statistics
    unique_policies: int = Field(default=0, description="Number of unique policies used")
    top_policies: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Most frequently used policies"
    )
    
    # Resource statistics
    top_classifications: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Most accessed resource classifications"
    )
    
    top_actions: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Most common actions"
    )
    
    # Performance statistics
    average_decision_time_ms: Optional[float] = Field(None, description="Average decision time")
    slowest_policies: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Slowest performing policies"
    )
    
    # Data quality
    data_completeness_score: float = Field(default=100.0, description="Data completeness percentage")
    anomaly_count: int = Field(default=0, description="Number of detected anomalies")
    
    # Storage statistics
    total_storage_size_bytes: int = Field(default=0, description="Total storage size in bytes")
    oldest_log_date: Optional[datetime] = Field(None, description="Oldest log date")
    newest_log_date: Optional[datetime] = Field(None, description="Newest log date")
    
    # Computed at
    computed_at: datetime = Field(default_factory=datetime.utcnow, description="Statistics computation time")
    time_range: Dict[str, Any] = Field(
        default_factory=dict,
        description="Time range for statistics"
    )


class AuditQueryResult(BaseModel):
    """Result of audit log query."""
    
    logs: List[OPADecisionLog] = Field(
        default_factory=list,
        description="Query result logs"
    )
    
    total_count: int = Field(..., description="Total number of matching logs")
    returned_count: int = Field(..., description="Number of logs returned")
    
    # Query metadata
    query_time_ms: float = Field(..., description="Query execution time in milliseconds")
    query_filters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Applied query filters"
    )
    
    # Aggregations (if requested)
    aggregations: Dict[str, Any] = Field(
        default_factory=dict,
        description="Query aggregation results"
    )
    
    # Pagination info
    has_more: bool = Field(default=False, description="Whether more results are available")
    next_cursor: Optional[str] = Field(None, description="Cursor for next page")
    
    executed_at: datetime = Field(default_factory=datetime.utcnow, description="Query execution time")


class RetentionPolicyStatus(BaseModel):
    """Status of audit log retention policy."""
    
    policy_name: str = Field(..., description="Retention policy name")
    retention_days: int = Field(..., description="Retention period in days")
    
    # Status
    is_active: bool = Field(..., description="Whether policy is active")
    last_applied: Optional[datetime] = Field(None, description="Last time policy was applied")
    next_scheduled: Optional[datetime] = Field(None, description="Next scheduled application")
    
    # Statistics
    total_logs_before: int = Field(default=0, description="Total logs before last application")
    logs_deleted: int = Field(default=0, description="Logs deleted in last application")
    logs_backed_up: int = Field(default=0, description="Logs backed up before deletion")
    
    # Storage impact
    space_freed_bytes: int = Field(default=0, description="Storage space freed")
    backup_size_bytes: int = Field(default=0, description="Backup size created")
    
    # Execution details
    last_execution_time_ms: Optional[float] = Field(None, description="Last execution time")
    last_execution_status: str = Field(default="unknown", description="Last execution status")
    last_execution_errors: List[str] = Field(
        default_factory=list,
        description="Errors from last execution"
    )
    
    created_at: datetime = Field(..., description="Policy creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last policy update")


class AuditHealthStatus(BaseModel):
    """Health status of audit system components."""
    
    overall_health: str = Field(..., description="Overall system health")
    
    # Component health
    clickhouse_health: Dict[str, Any] = Field(
        default_factory=dict,
        description="ClickHouse database health"
    )
    
    ingestion_health: Dict[str, Any] = Field(
        default_factory=dict,
        description="Log ingestion pipeline health"
    )
    
    storage_health: Dict[str, Any] = Field(
        default_factory=dict,
        description="Storage system health"
    )
    
    # Performance metrics
    ingestion_rate: Dict[str, float] = Field(
        default_factory=dict,
        description="Current ingestion rates"
    )
    
    query_performance: Dict[str, float] = Field(
        default_factory=dict,
        description="Query performance metrics"
    )
    
    # Resource usage
    storage_usage: Dict[str, Any] = Field(
        default_factory=dict,
        description="Storage usage information"
    )
    
    memory_usage: Dict[str, Any] = Field(
        default_factory=dict,
        description="Memory usage information"
    )
    
    # Alerts and issues
    active_alerts: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Active system alerts"
    )
    
    recent_errors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Recent system errors"
    )
    
    # Uptime and availability
    uptime_seconds: int = Field(..., description="System uptime in seconds")
    availability_percentage: float = Field(default=100.0, description="System availability percentage")
    
    last_health_check: datetime = Field(default_factory=datetime.utcnow, description="Last health check time")


class AuditExportResult(BaseModel):
    """Result of audit log export operation."""
    
    export_id: str = Field(..., description="Unique export identifier")
    status: str = Field(..., description="Export status")
    
    # Export details
    file_path: Optional[str] = Field(None, description="Path to exported file")
    file_size_bytes: Optional[int] = Field(None, description="Export file size")
    file_format: str = Field(..., description="Export file format")
    
    # Data details
    records_exported: int = Field(..., description="Number of records exported")
    time_range: Dict[str, datetime] = Field(..., description="Time range of exported data")
    
    # Processing info
    started_at: datetime = Field(..., description="Export start time")
    completed_at: Optional[datetime] = Field(None, description="Export completion time")
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")
    
    # Compression and optimization
    compression_ratio: Optional[float] = Field(None, description="Compression ratio achieved")
    original_size_bytes: Optional[int] = Field(None, description="Original data size before compression")
    
    # Error handling
    errors: List[str] = Field(
        default_factory=list,
        description="Export errors"
    )
    
    # Download info
    download_url: Optional[str] = Field(None, description="Download URL for export file")
    expires_at: Optional[datetime] = Field(None, description="Download URL expiration time")


class AuditCapabilities(BaseModel):
    """Audit system capabilities and configuration."""
    
    # Storage capabilities
    max_retention_days: int = Field(default=3650, description="Maximum retention period")
    supported_formats: List[str] = Field(
        default_factory=lambda: ["json", "csv", "parquet"],
        description="Supported export formats"
    )
    
    # Query capabilities
    max_query_time_range_days: int = Field(default=365, description="Maximum query time range")
    max_query_results: int = Field(default=10000, description="Maximum query results")
    supported_aggregations: List[str] = Field(
        default_factory=lambda: ["count", "sum", "avg", "min", "max", "group_by"],
        description="Supported query aggregations"
    )
    
    # Ingestion capabilities
    max_batch_size: int = Field(default=1000, description="Maximum batch size for ingestion")
    max_ingestion_rate: int = Field(default=10000, description="Maximum ingestion rate per minute")
    
    # Alert capabilities
    supported_alert_conditions: List[str] = Field(
        default_factory=lambda: ["threshold", "anomaly", "pattern", "rate"],
        description="Supported alert condition types"
    )
    
    # Integration capabilities
    supported_data_sources: List[str] = Field(
        default_factory=lambda: ["opa", "custom"],
        description="Supported data sources"
    )
    
    supported_destinations: List[str] = Field(
        default_factory=lambda: ["clickhouse", "s3", "webhook"],
        description="Supported data destinations"
    )
    
    # Security features
    encryption_available: bool = Field(default=True, description="Encryption support available")
    access_control_enabled: bool = Field(default=True, description="Access control enabled")
    audit_trail_enabled: bool = Field(default=True, description="Audit trail for system changes")
    
    version: str = Field(default="1.0.0", description="System version")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Capabilities last updated")
