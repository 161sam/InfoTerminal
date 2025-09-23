"""
Egress Gateway API Models

This module contains all Pydantic models for the Egress Gateway service API.
"""

from .requests import (
    ProxyRequest,
    ProxyRotateRequest,
    ProxyConfigRequest
)

from .responses import (
    ProxyResponse,
    ProxyStatus,
    ProxyStatistics,
    ProxyHealthStatus,
    RotationResult,
    ProxyConfigInfo
)

__all__ = [
    # Requests
    "ProxyRequest",
    "ProxyRotateRequest", 
    "ProxyConfigRequest",
    
    # Responses
    "ProxyResponse",
    "ProxyStatus",
    "ProxyStatistics", 
    "ProxyHealthStatus",
    "RotationResult",
    "ProxyConfigInfo"
]
