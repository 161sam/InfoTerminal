"""
Standard Error Schemas for InfoTerminal APIs

Provides consistent error response formats across all services.
All services MUST use these error schemas for API responses.
"""

from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Standard error detail structure."""
    code: str = Field(..., description="Error code for programmatic handling")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error context")


class StandardError(BaseModel):
    """
    Standard API error envelope used by all InfoTerminal services.
    
    Example:
    {
        "error": {
            "code": "VALIDATION_ERROR", 
            "message": "Invalid input parameters",
            "details": {"field": "email", "reason": "invalid format"}
        }
    }
    """
    error: ErrorDetail


class ValidationError(BaseModel):
    """Validation error with field-specific details."""
    error: ErrorDetail
    validation_errors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of field validation errors"
    )


class APIError(Exception):
    """
    Standard API exception that automatically converts to StandardError response.
    
    Usage:
        raise APIError("RESOURCE_NOT_FOUND", "Document not found", 404, {"doc_id": "123"})
    """
    
    def __init__(
        self, 
        code: str, 
        message: str, 
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)
    
    def to_response(self) -> StandardError:
        """Convert exception to StandardError response model."""
        return StandardError(
            error=ErrorDetail(
                code=self.code,
                message=self.message,
                details=self.details
            )
        )


# Standard error codes used across InfoTerminal services
class ErrorCodes:
    """Standard error codes for consistent error handling."""
    
    # Client errors (4xx)
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"
    RATE_LIMITED = "RATE_LIMITED"
    INVALID_REQUEST = "INVALID_REQUEST"
    
    # Server errors (5xx)
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    DATABASE_ERROR = "DATABASE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    TIMEOUT_ERROR = "TIMEOUT_ERROR"
    
    # InfoTerminal-specific errors
    SEARCH_ERROR = "SEARCH_ERROR"
    GRAPH_ERROR = "GRAPH_ERROR"
    NLP_ERROR = "NLP_ERROR"
    AUTH_ERROR = "AUTH_ERROR"
    VERIFICATION_ERROR = "VERIFICATION_ERROR"


def create_error_response(
    code: str, 
    message: str, 
    details: Optional[Dict[str, Any]] = None
) -> StandardError:
    """Helper function to create standardized error responses."""
    return StandardError(
        error=ErrorDetail(
            code=code,
            message=message,
            details=details
        )
    )


def create_validation_error_response(
    message: str,
    validation_errors: List[Dict[str, Any]],
    details: Optional[Dict[str, Any]] = None
) -> ValidationError:
    """Helper function to create validation error responses."""
    return ValidationError(
        error=ErrorDetail(
            code=ErrorCodes.VALIDATION_ERROR,
            message=message,
            details=details
        ),
        validation_errors=validation_errors
    )
