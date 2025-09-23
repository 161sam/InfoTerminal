"""
Response models for Plugin Runner API.
"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field


class PluginInfo(BaseModel):
    """Information about a plugin."""
    
    name: str = Field(..., description="Plugin name")
    version: str = Field(..., description="Plugin version")
    description: str = Field(..., description="Plugin description")
    category: str = Field(..., description="Plugin category")
    author: Optional[str] = Field(None, description="Plugin author")
    risk_level: str = Field(..., description="Risk level: low, medium, high, critical")
    requires_network: bool = Field(..., description="Whether plugin requires network access")
    requires_root: bool = Field(..., description="Whether plugin requires root privileges")
    enabled: bool = Field(default=True, description="Whether plugin is enabled")
    
    parameters: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Plugin parameter specifications"
    )
    
    output_formats: List[str] = Field(
        default_factory=list,
        description="Supported output formats"
    )
    
    security: Dict[str, Any] = Field(
        default_factory=dict,
        description="Security configuration"
    )
    
    capabilities: List[str] = Field(
        default_factory=list,
        description="Plugin capabilities"
    )
    
    last_updated: Optional[datetime] = Field(
        None,
        description="Last update timestamp"
    )


class PluginExecutionResponse(BaseModel):
    """Response from plugin execution."""
    
    job_id: str = Field(..., description="Unique job identifier")
    status: str = Field(..., description="Job status: queued, running, completed, failed, cancelled")
    plugin_name: str = Field(..., description="Name of executed plugin")
    
    started_at: Optional[datetime] = Field(None, description="Job start time")
    completed_at: Optional[datetime] = Field(None, description="Job completion time")
    execution_time: Optional[float] = Field(None, description="Execution time in seconds")
    
    results: Optional[Dict[str, Any]] = Field(None, description="Plugin execution results")
    error: Optional[str] = Field(None, description="Error message if failed")
    
    output_files: List[str] = Field(
        default_factory=list,
        description="Generated output files"
    )
    
    graph_entities: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Graph entities discovered"
    )
    
    search_documents: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Search documents created"
    )
    
    tags: List[str] = Field(
        default_factory=list,
        description="Job tags"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional job metadata"
    )


class JobStatus(BaseModel):
    """Status information for a job."""
    
    job_id: str = Field(..., description="Job identifier")
    status: str = Field(..., description="Current status")
    plugin_name: str = Field(..., description="Plugin name")
    
    created_at: datetime = Field(..., description="Job creation time")
    started_at: Optional[datetime] = Field(None, description="Job start time")
    completed_at: Optional[datetime] = Field(None, description="Job completion time")
    
    progress: Optional[str] = Field(None, description="Progress information")
    error: Optional[str] = Field(None, description="Error message")
    
    priority: int = Field(default=1, description="Job priority")
    timeout: int = Field(default=300, description="Job timeout")
    
    resource_usage: Optional[Dict[str, Any]] = Field(
        None,
        description="Resource usage statistics"
    )


class PluginCategory(BaseModel):
    """Plugin category information."""
    
    name: str = Field(..., description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    
    plugins: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Plugins in this category"
    )
    
    risk_levels: List[str] = Field(
        default_factory=list,
        description="Risk levels present in this category"
    )
    
    total_plugins: int = Field(default=0, description="Total plugins in category")
    enabled_plugins: int = Field(default=0, description="Enabled plugins in category")


class PluginStatistics(BaseModel):
    """Plugin execution statistics."""
    
    total_plugins: int = Field(default=0, description="Total number of plugins")
    enabled_plugins: int = Field(default=0, description="Number of enabled plugins")
    
    total_jobs: int = Field(default=0, description="Total number of jobs")
    
    job_status_counts: Dict[str, int] = Field(
        default_factory=dict,
        description="Job counts by status"
    )
    
    plugin_usage_counts: Dict[str, int] = Field(
        default_factory=dict,
        description="Usage counts by plugin"
    )
    
    average_execution_time: float = Field(
        default=0.0,
        description="Average execution time in seconds"
    )
    
    success_rate: float = Field(
        default=0.0,
        description="Overall success rate as percentage"
    )
    
    docker_enabled: bool = Field(
        default=False,
        description="Whether Docker execution is enabled"
    )
    
    system_resources: Dict[str, Any] = Field(
        default_factory=dict,
        description="Current system resource usage"
    )


class PluginCapabilities(BaseModel):
    """System plugin capabilities."""
    
    max_concurrent_jobs: int = Field(..., description="Maximum concurrent jobs")
    max_execution_time: int = Field(..., description="Maximum execution time")
    supported_formats: List[str] = Field(..., description="Supported output formats")
    
    docker_available: bool = Field(..., description="Docker availability")
    security_sandbox: bool = Field(..., description="Security sandbox enabled")
    
    categories: List[str] = Field(
        default_factory=list,
        description="Available plugin categories"
    )
    
    risk_levels: List[str] = Field(
        default_factory=list,
        description="Available risk levels"
    )
    
    features: Dict[str, bool] = Field(
        default_factory=dict,
        description="Feature availability flags"
    )


class BatchExecutionResponse(BaseModel):
    """Response from batch plugin execution."""
    
    batch_id: str = Field(..., description="Unique batch identifier")
    status: str = Field(..., description="Batch status")
    
    total_jobs: int = Field(..., description="Total number of jobs in batch")
    completed_jobs: int = Field(default=0, description="Number of completed jobs")
    failed_jobs: int = Field(default=0, description="Number of failed jobs")
    
    job_ids: List[str] = Field(
        default_factory=list,
        description="List of job IDs in this batch"
    )
    
    started_at: Optional[datetime] = Field(None, description="Batch start time")
    completed_at: Optional[datetime] = Field(None, description="Batch completion time")
    
    results: List[PluginExecutionResponse] = Field(
        default_factory=list,
        description="Results from individual jobs"
    )


class PluginHealthStatus(BaseModel):
    """Health status for plugin system."""
    
    plugin_registry_loaded: bool = Field(..., description="Plugin registry status")
    docker_available: bool = Field(..., description="Docker availability")
    
    total_plugins: int = Field(..., description="Total plugins loaded")
    active_jobs: int = Field(..., description="Currently active jobs")
    queue_length: int = Field(..., description="Jobs in queue")
    
    resource_usage: Dict[str, Any] = Field(
        default_factory=dict,
        description="Current resource usage"
    )
    
    last_plugin_execution: Optional[datetime] = Field(
        None,
        description="Timestamp of last plugin execution"
    )
