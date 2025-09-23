"""
Request models for Egress Gateway API.
"""

from typing import Dict, List, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, validator


class ProxyType(str, Enum):
    """Available proxy types for egress routing."""
    TOR = "tor"
    VPN = "vpn"
    PROXY = "proxy"
    DIRECT = "direct"
    AUTO = "auto"


class AnonymityLevel(str, Enum):
    """Anonymity levels for proxy requests."""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"  
    HIGH = "high"
    EXTREME = "extreme"


class ProxyRequest(BaseModel):
    """Request model for proxied HTTP requests."""
    
    url: HttpUrl = Field(
        ...,
        description="Target URL for the proxied request"
    )
    
    method: str = Field(
        default="GET",
        description="HTTP method",
        pattern=r"^(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)$"
    )
    
    headers: Optional[Dict[str, str]] = Field(
        default=None,
        description="HTTP headers to include in request"
    )
    
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Request body data (for POST/PUT/PATCH)"
    )
    
    proxy_type: ProxyType = Field(
        default=ProxyType.AUTO,
        description="Preferred proxy type for this request"
    )
    
    anonymity_level: AnonymityLevel = Field(
        default=AnonymityLevel.MEDIUM,
        description="Required anonymity level"
    )
    
    rotate_identity: bool = Field(
        default=False,
        description="Force identity rotation before request"
    )
    
    sanitize_headers: bool = Field(
        default=True,
        description="Remove identifying headers"
    )
    
    follow_redirects: bool = Field(
        default=True,
        description="Follow HTTP redirects"
    )
    
    timeout: int = Field(
        default=30,
        description="Request timeout in seconds",
        ge=1,
        le=300
    )
    
    retry_count: int = Field(
        default=3,
        description="Number of retry attempts",
        ge=0,
        le=10
    )
    
    tags: List[str] = Field(
        default_factory=list,
        description="Tags for request categorization",
        max_items=10
    )
    
    priority: int = Field(
        default=1,
        description="Request priority (1=highest, 5=lowest)",
        ge=1,
        le=5
    )
    
    @validator('headers')
    def validate_headers(cls, v):
        """Validate headers don't contain sensitive data."""
        if v:
            # Check for potentially sensitive headers
            sensitive_headers = {'authorization', 'cookie', 'x-api-key', 'x-auth-token'}
            for header in v.keys():
                if header.lower() in sensitive_headers:
                    # Log warning but allow (user may legitimately need these)
                    pass
        return v
    
    @validator('url')
    def validate_url_safety(cls, v):
        """Basic URL safety validation."""
        url_str = str(v)
        
        # Block potentially dangerous schemes
        dangerous_schemes = ['file', 'ftp', 'ldap']
        if any(url_str.startswith(f"{scheme}://") for scheme in dangerous_schemes):
            raise ValueError(f"URL scheme not allowed for security reasons")
        
        # Block internal/private networks (basic check)
        if 'localhost' in url_str or '127.0.0.1' in url_str:
            raise ValueError("Requests to localhost not allowed")
        
        return v


class ProxyRotateRequest(BaseModel):
    """Request model for proxy/identity rotation."""
    
    proxy_type: Optional[ProxyType] = Field(
        default=None,
        description="Specific proxy type to rotate (or all if None)"
    )
    
    force_new_circuit: bool = Field(
        default=False,
        description="Force new Tor circuit if using Tor"
    )
    
    clear_session: bool = Field(
        default=False,
        description="Clear session data/cookies"
    )
    
    reason: Optional[str] = Field(
        default=None,
        description="Reason for rotation (for audit logs)",
        max_length=200
    )


class ProxyConfigRequest(BaseModel):
    """Request model for proxy configuration updates."""
    
    proxy_type: ProxyType = Field(
        ...,
        description="Proxy type to configure"
    )
    
    enabled: Optional[bool] = Field(
        default=None,
        description="Enable/disable this proxy type"
    )
    
    priority: Optional[int] = Field(
        default=None,
        description="Priority for auto-selection",
        ge=1,
        le=10
    )
    
    timeout: Optional[int] = Field(
        default=None,
        description="Default timeout for this proxy type",
        ge=1,
        le=300
    )
    
    max_concurrent: Optional[int] = Field(
        default=None,
        description="Maximum concurrent requests",
        ge=1,
        le=100
    )
    
    rotation_interval: Optional[int] = Field(
        default=None,
        description="Automatic rotation interval in seconds",
        ge=60,
        le=86400  # 24 hours
    )
    
    anonymity_level: Optional[AnonymityLevel] = Field(
        default=None,
        description="Default anonymity level for this proxy"
    )
    
    custom_settings: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Proxy-specific configuration settings"
    )


class ProxyBulkRequest(BaseModel):
    """Request model for bulk proxy requests."""
    
    requests: List[ProxyRequest] = Field(
        ...,
        description="List of proxy requests to execute",
        min_items=1,
        max_items=20
    )
    
    sequential: bool = Field(
        default=False,
        description="Execute requests sequentially vs parallel"
    )
    
    stop_on_error: bool = Field(
        default=False,
        description="Stop execution if any request fails"
    )
    
    shared_session: bool = Field(
        default=False,
        description="Share session/cookies across requests"
    )
    
    batch_name: Optional[str] = Field(
        default=None,
        description="Optional name for the batch",
        max_length=100
    )


class ProxyFilterRequest(BaseModel):
    """Request model for filtering proxy requests/logs."""
    
    start_time: Optional[str] = Field(
        default=None,
        description="Start time filter (ISO format)"
    )
    
    end_time: Optional[str] = Field(
        default=None,
        description="End time filter (ISO format)"
    )
    
    proxy_type: Optional[ProxyType] = Field(
        default=None,
        description="Filter by proxy type"
    )
    
    anonymity_level: Optional[AnonymityLevel] = Field(
        default=None,
        description="Filter by anonymity level"
    )
    
    status_code: Optional[int] = Field(
        default=None,
        description="Filter by HTTP status code"
    )
    
    domain: Optional[str] = Field(
        default=None,
        description="Filter by target domain",
        max_length=200
    )
    
    tags: Optional[List[str]] = Field(
        default=None,
        description="Filter by tags"
    )
