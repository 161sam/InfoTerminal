"""
Response Models for Agent Connector Service

Standardized response schemas for all plugin management endpoints.
All responses follow InfoTerminal API conventions.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class PluginManifest(BaseModel):
    """Plugin manifest information."""
    name: str = Field(..., description="Plugin name")
    version: str = Field(..., description="Plugin version")
    provider: Optional[str] = Field(None, description="Plugin provider/author")
    description: Optional[str] = Field(None, description="Plugin description")
    category: Optional[str] = Field(None, description="Plugin category")
    api_version: str = Field(..., description="Supported API version")
    capabilities: Optional[Dict[str, Any]] = Field(None, description="Plugin capabilities")
    endpoints: Optional[Dict[str, str]] = Field(None, description="Plugin endpoint configuration")
    requirements: Optional[List[str]] = Field(None, description="Plugin requirements")
    tags: Optional[List[str]] = Field(None, description="Plugin tags")


class PluginRegistryItem(BaseModel):
    """Item in the plugin registry."""
    manifest: PluginManifest = Field(..., description="Plugin manifest")
    status: str = Field(..., description="Plugin status: available, installed, error")
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")


class PluginRegistryResponse(BaseModel):
    """Response for plugin registry listing."""
    items: List[PluginRegistryItem] = Field(..., description="List of plugins in registry")
    total: int = Field(..., description="Total number of plugins")
    categories: List[str] = Field(..., description="Available plugin categories")
    providers: List[str] = Field(..., description="Available plugin providers")


class PluginStateItem(BaseModel):
    """Plugin state for a user/global scope."""
    name: str = Field(..., description="Plugin name")
    version: Optional[str] = Field(None, description="Plugin version")
    provider: Optional[str] = Field(None, description="Plugin provider")
    enabled: bool = Field(False, description="Whether plugin is enabled")
    config: Dict[str, Any] = Field(default_factory=dict, description="Plugin configuration")
    scope: str = Field(..., description="Configuration scope: user or global")
    last_modified: Optional[datetime] = Field(None, description="Last modification timestamp")


class PluginStateResponse(BaseModel):
    """Response for plugin state listing."""
    items: List[PluginStateItem] = Field(..., description="List of plugin states")
    user_id: Optional[str] = Field(None, description="User ID for user-scoped states")
    scope: str = Field(..., description="Response scope: user, global, or all")


class PluginToggleResponse(BaseModel):
    """Response for plugin enable/disable."""
    name: str = Field(..., description="Plugin name")
    enabled: bool = Field(..., description="New enabled status")
    scope: str = Field(..., description="Configuration scope")
    previous_enabled: Optional[bool] = Field(None, description="Previous enabled status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Operation timestamp")


class PluginConfigResponse(BaseModel):
    """Response for plugin configuration."""
    name: str = Field(..., description="Plugin name")
    config: Dict[str, Any] = Field(..., description="Current plugin configuration")
    scope: str = Field(..., description="Configuration scope")
    timestamp: datetime = Field(default_factory=datetime.now, description="Operation timestamp")


class PluginTool(BaseModel):
    """Plugin tool definition."""
    name: str = Field(..., description="Tool name")
    plugin: str = Field(..., description="Plugin that provides this tool")
    description: Optional[str] = Field(None, description="Tool description")
    category: Optional[str] = Field(None, description="Tool category")
    args_schema: Optional[Dict[str, Any]] = Field(None, description="JSON schema for tool arguments")
    capabilities: Optional[List[str]] = Field(None, description="Required capabilities")
    examples: Optional[List[Dict[str, Any]]] = Field(None, description="Usage examples")


class PluginToolsResponse(BaseModel):
    """Response for tool discovery."""
    api_version: str = Field(..., description="API version")
    tools: List[PluginTool] = Field(..., description="Available tools")
    total: int = Field(..., description="Total number of tools")
    plugins: List[str] = Field(..., description="Plugins that provide tools")
    categories: List[str] = Field(..., description="Available tool categories")


class PluginInvokeResponse(BaseModel):
    """Response for plugin tool invocation."""
    success: bool = Field(..., description="Whether tool execution was successful")
    result: Optional[Any] = Field(None, description="Tool execution result")
    plugin: str = Field(..., description="Plugin that executed the tool")
    tool: str = Field(..., description="Tool that was executed")
    execution_time_ms: Optional[int] = Field(None, description="Execution time in milliseconds")
    timestamp: datetime = Field(default_factory=datetime.now, description="Execution timestamp")
    request_id: Optional[str] = Field(None, description="Request ID for tracing")


class PluginHealthResponse(BaseModel):
    """Response for plugin health check."""
    name: str = Field(..., description="Plugin name")
    status: str = Field(..., description="Health status: up, down, degraded, unknown")
    latency_ms: Optional[int] = Field(None, description="Health check latency in milliseconds")
    checked_at: Optional[int] = Field(None, description="Timestamp of health check (Unix timestamp)")
    error: Optional[str] = Field(None, description="Error message if health check failed")
    endpoint: Optional[str] = Field(None, description="Health check endpoint URL")


class PluginErrorResponse(BaseModel):
    """Standardized error response for plugin operations."""
    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    plugin: Optional[str] = Field(None, description="Plugin name related to error")
    tool: Optional[str] = Field(None, description="Tool name related to error")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
