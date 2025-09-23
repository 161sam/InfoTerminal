"""
InfoTerminal API Standards Package

This package provides unified API standards for all InfoTerminal services:
- Standard error envelopes
- Pagination patterns  
- Health/Ready endpoints
- OpenAPI configuration
- Middleware and CORS setup
"""

from .error_schemas import StandardError, ValidationError, APIError
from .pagination import PaginatedResponse, PaginationParams
from .health import HealthResponse, ReadyResponse, health_check, ready_check
from .middleware import setup_standard_middleware
from .openapi import get_standard_openapi_config

__all__ = [
    "StandardError",
    "ValidationError", 
    "APIError",
    "PaginatedResponse",
    "PaginationParams",
    "HealthResponse",
    "ReadyResponse",
    "health_check",
    "ready_check",
    "setup_standard_middleware",
    "get_standard_openapi_config",
]
