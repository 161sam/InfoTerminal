"""
InfoTerminal API Standards Package

This package provides unified API standards for all InfoTerminal services:
- Standard error envelopes
- Pagination patterns  
- Health/Ready endpoints
- OpenAPI configuration
- Middleware and CORS setup
"""

from .error_schemas import APIError, ErrorCodes, StandardError, ValidationError
from .pagination import PaginatedResponse, PaginationParams
from .health import HealthResponse, ReadyResponse, health_check, ready_check
from .middleware import setup_standard_exception_handlers, setup_standard_middleware
from .openapi import (
    get_service_tags_metadata,
    get_standard_openapi_config,
    setup_standard_openapi,
)

__all__ = [
    "StandardError",
    "ValidationError",
    "APIError",
    "ErrorCodes",
    "PaginatedResponse",
    "PaginationParams",
    "HealthResponse",
    "ReadyResponse",
    "health_check",
    "ready_check",
    "setup_standard_middleware",
    "setup_standard_exception_handlers",
    "get_standard_openapi_config",
    "setup_standard_openapi",
    "get_service_tags_metadata",
]
