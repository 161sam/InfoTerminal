"""
Request Models for Agent Connector Service

Standardized request schemas for all plugin management endpoints.
All requests follow InfoTerminal API conventions.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, validator


class PluginToggleRequest(BaseModel):
    """Request to enable/disable a plugin."""
    enabled: bool = Field(..., description="Whether to enable or disable the plugin")
    scope: str = Field(
        default="user", 
        regex="^(user|global)$",
        description="Scope for the setting: 'user' (current user) or 'global' (all users)"
    )
    
    @validator('scope')
    def validate_scope(cls, v):
        if v not in ['user', 'global']:
            raise ValueError("scope must be 'user' or 'global'")
        return v


class PluginConfigRequest(BaseModel):
    """Request to set plugin configuration."""
    config: Dict[str, Any] = Field(..., description="Configuration key-value pairs")
    scope: str = Field(
        default="user",
        regex="^(user|global)$", 
        description="Scope for the configuration: 'user' (current user) or 'global' (all users)"
    )
    
    @validator('config')
    def validate_config(cls, v):
        # Check for secrets that shouldn't be stored in config
        secret_keys = {'secret', 'token', 'password', 'apikey', 'api_key', 'key'}
        for key in v.keys():
            if key.lower() in secret_keys:
                raise ValueError(f"Secret key '{key}' must be configured via ENV/Vault, not API")
        return v
    
    @validator('scope')
    def validate_scope(cls, v):
        if v not in ['user', 'global']:
            raise ValueError("scope must be 'user' or 'global'")
        return v


class PluginInvokeRequest(BaseModel):
    """Request to invoke a plugin tool."""
    args: Dict[str, Any] = Field(
        default_factory=dict,
        description="Arguments to pass to the plugin tool"
    )
    timeout: Optional[int] = Field(
        default=15,
        ge=1,
        le=300,
        description="Timeout in seconds for tool execution (1-300 seconds)"
    )
    context: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional context for tool execution"
    )


class PluginRegistryFilter(BaseModel):
    """Filter parameters for plugin registry listing."""
    category: Optional[str] = Field(None, description="Filter by plugin category")
    provider: Optional[str] = Field(None, description="Filter by plugin provider")
    enabled_only: Optional[bool] = Field(False, description="Show only enabled plugins")
    search: Optional[str] = Field(None, description="Search in plugin name or description")


class PluginToolFilter(BaseModel):
    """Filter parameters for tool discovery."""
    plugin: Optional[str] = Field(None, description="Filter by specific plugin name")
    category: Optional[str] = Field(None, description="Filter by tool category")
    capability: Optional[str] = Field(None, description="Filter by required capability")
    search: Optional[str] = Field(None, description="Search in tool name or description")


class PluginStateFilter(BaseModel):
    """Filter parameters for plugin state listing."""
    scope: Optional[str] = Field(
        None,
        regex="^(user|global|all)$",
        description="Filter by scope: 'user', 'global', or 'all'"
    )
    enabled_only: Optional[bool] = Field(False, description="Show only enabled plugins")
    search: Optional[str] = Field(None, description="Search in plugin name")
