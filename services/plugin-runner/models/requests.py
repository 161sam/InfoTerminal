"""
Request models for Plugin Runner API.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field, validator


class PluginExecutionRequest(BaseModel):
    """Request model for executing a plugin."""
    
    plugin_name: str = Field(
        ...,
        description="Name of the plugin to execute",
        pattern=r"^[a-zA-Z0-9_-]+$",
        min_length=1,
        max_length=100
    )
    
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters to pass to the plugin"
    )
    
    timeout: Optional[int] = Field(
        default=300,
        description="Execution timeout in seconds",
        ge=1,
        le=3600
    )
    
    output_format: str = Field(
        default="json",
        description="Desired output format",
        pattern=r"^(json|yaml|xml|text)$"
    )
    
    priority: int = Field(
        default=1,
        description="Execution priority (1=highest, 5=lowest)",
        ge=1,
        le=5
    )
    
    save_output: bool = Field(
        default=True,
        description="Whether to save output files"
    )
    
    notification_webhook: Optional[str] = Field(
        default=None,
        description="Webhook URL for completion notification"
    )
    
    tags: List[str] = Field(
        default_factory=list,
        description="Tags for job categorization",
        max_items=10
    )
    
    @validator('plugin_name')
    def validate_plugin_name(cls, v):
        """Validate plugin name format."""
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Plugin name must be alphanumeric with hyphens/underscores only')
        return v
    
    @validator('parameters')
    def validate_parameters(cls, v):
        """Validate parameters don't contain sensitive data."""
        if isinstance(v, dict):
            # Check for potentially sensitive keys
            sensitive_keys = {'password', 'secret', 'key', 'token', 'api_key'}
            for key in v.keys():
                if any(sensitive in key.lower() for sensitive in sensitive_keys):
                    # Log warning but don't reject - just note it
                    pass
        return v


class PluginBatchRequest(BaseModel):
    """Request model for batch plugin execution."""
    
    executions: List[PluginExecutionRequest] = Field(
        ...,
        description="List of plugin executions to run",
        min_items=1,
        max_items=50
    )
    
    sequential: bool = Field(
        default=False,
        description="Whether to run executions sequentially or in parallel"
    )
    
    stop_on_error: bool = Field(
        default=False,
        description="Whether to stop the batch if any execution fails"
    )
    
    batch_name: Optional[str] = Field(
        default=None,
        description="Optional name for the batch job",
        max_length=200
    )
    
    callback_webhook: Optional[str] = Field(
        default=None,
        description="Webhook URL for batch completion notification"
    )


class PluginConfigRequest(BaseModel):
    """Request model for updating plugin configuration."""
    
    enabled: Optional[bool] = Field(
        default=None,
        description="Whether the plugin is enabled"
    )
    
    priority: Optional[int] = Field(
        default=None,
        description="Plugin priority",
        ge=1,
        le=10
    )
    
    timeout: Optional[int] = Field(
        default=None,
        description="Default timeout for this plugin",
        ge=1,
        le=3600
    )
    
    max_concurrent: Optional[int] = Field(
        default=None,
        description="Maximum concurrent executions for this plugin",
        ge=1,
        le=10
    )
    
    resource_limits: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Resource limits for plugin execution"
    )


class PluginSearchRequest(BaseModel):
    """Request model for searching plugins."""
    
    query: Optional[str] = Field(
        default=None,
        description="Search query",
        max_length=200
    )
    
    category: Optional[str] = Field(
        default=None,
        description="Filter by category",
        max_length=50
    )
    
    risk_level: Optional[str] = Field(
        default=None,
        description="Filter by risk level",
        pattern=r"^(low|medium|high|critical)$"
    )
    
    requires_network: Optional[bool] = Field(
        default=None,
        description="Filter by network requirement"
    )
    
    requires_root: Optional[bool] = Field(
        default=None,
        description="Filter by root requirement"
    )
    
    enabled_only: bool = Field(
        default=True,
        description="Only return enabled plugins"
    )
