"""
Standard Middleware Setup for InfoTerminal APIs

Provides consistent middleware configuration across all services.
All services MUST use these middleware patterns for consistency.
"""

import os
import time
import uuid
from typing import List, Optional
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

try:
    from starlette_exporter import PrometheusMiddleware, handle_metrics
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

from .error_schemas import StandardError, APIError, ErrorCodes, create_error_response


def setup_standard_middleware(
    app: FastAPI,
    service_name: str,
    enable_metrics: bool = True,
    cors_origins: Optional[List[str]] = None,
    trusted_hosts: Optional[List[str]] = None
) -> None:
    """
    Set up standard middleware for InfoTerminal services.
    
    Args:
        app: FastAPI application instance
        service_name: Name of the service for metrics/logging
        enable_metrics: Whether to enable Prometheus metrics
        cors_origins: List of allowed CORS origins
        trusted_hosts: List of trusted host names
    """
    
    # CORS Middleware
    if cors_origins is None:
        cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Trusted Host Middleware
    if trusted_hosts is None:
        trusted_hosts = os.getenv("TRUSTED_HOSTS", "localhost,127.0.0.1").split(",")
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=trusted_hosts + ["*"]  # Allow all in development
    )
    
    # Prometheus Metrics Middleware
    if enable_metrics and PROMETHEUS_AVAILABLE and os.getenv("IT_ENABLE_METRICS") == "1":
        app.add_middleware(PrometheusMiddleware)
        app.add_route("/metrics", handle_metrics)
    
    # Request ID Middleware
    @app.middleware("http")
    async def request_id_middleware(request: Request, call_next):
        """Add unique request ID to all requests."""
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        
        # Store request ID for logging
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        return response
    
    # Security Headers Middleware
    @app.middleware("http")
    async def security_headers_middleware(request: Request, call_next):
        """Add security headers to all responses."""
        response = await call_next(request)
        
        # Standard security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # HSTS only in production with HTTPS
        if os.getenv("ENVIRONMENT") == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response
    
    # Performance Monitoring Middleware
    @app.middleware("http")
    async def performance_middleware(request: Request, call_next):
        """Monitor request performance."""
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        return response


def setup_standard_exception_handlers(app: FastAPI) -> None:
    """
    Set up standard exception handlers for InfoTerminal services.
    
    Args:
        app: FastAPI application instance
    """
    
    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError):
        """Handle custom APIError exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_response().dict()
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle HTTP exceptions with standard error format."""
        
        # Map HTTP status codes to error codes
        error_code_map = {
            400: ErrorCodes.INVALID_REQUEST,
            401: ErrorCodes.UNAUTHORIZED,
            403: ErrorCodes.FORBIDDEN,
            404: ErrorCodes.RESOURCE_NOT_FOUND,
            409: ErrorCodes.CONFLICT,
            429: ErrorCodes.RATE_LIMITED,
            500: ErrorCodes.INTERNAL_ERROR,
            503: ErrorCodes.SERVICE_UNAVAILABLE,
        }
        
        error_code = error_code_map.get(exc.status_code, ErrorCodes.INTERNAL_ERROR)
        
        error_response = create_error_response(
            code=error_code,
            message=exc.detail,
            details={"status_code": exc.status_code}
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.dict()
        )
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Handle ValueError as validation errors."""
        error_response = create_error_response(
            code=ErrorCodes.VALIDATION_ERROR,
            message=str(exc),
            details={"error_type": "ValueError"}
        )
        
        return JSONResponse(
            status_code=400,
            content=error_response.dict()
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all other exceptions."""
        
        # Log the error (in production, use proper logging)
        print(f"Unhandled exception in {request.url.path}: {exc}")
        
        error_response = create_error_response(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Internal server error",
            details={
                "error_type": type(exc).__name__,
                "request_id": getattr(request.state, "request_id", "unknown")
            }
        )
        
        return JSONResponse(
            status_code=500,
            content=error_response.dict()
        )


def setup_request_logging_middleware(app: FastAPI, service_name: str) -> None:
    """
    Set up request logging middleware.
    
    Args:
        app: FastAPI application instance
        service_name: Name of the service for log context
    """
    
    @app.middleware("http")
    async def logging_middleware(request: Request, call_next):
        """Log all requests with timing information."""
        start_time = time.time()
        
        # Get request info
        method = request.method
        url = str(request.url)
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        request_id = getattr(request.state, "request_id", "unknown")
        
        try:
            response = await call_next(request)
            
            # Calculate timing
            process_time = time.time() - start_time
            
            # Log successful request
            print(f"[{service_name}] {request_id} {method} {url} "
                  f"{response.status_code} {process_time:.3f}s "
                  f"ip={client_ip}")
            
            return response
            
        except Exception as e:
            # Log failed request
            process_time = time.time() - start_time
            print(f"[{service_name}] {request_id} {method} {url} "
                  f"ERROR {process_time:.3f}s "
                  f"ip={client_ip} error={str(e)}")
            raise


class RateLimitMiddleware:
    """
    Simple rate limiting middleware for InfoTerminal services.
    """
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = {}
    
    async def __call__(self, request: Request, call_next):
        """Apply rate limiting based on client IP."""
        if self.requests_per_minute <= 0:
            return await call_next(request)
        
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Clean old entries
        cutoff_time = current_time - 60
        self.requests = {
            ip: timestamps for ip, timestamps in self.requests.items()
            if any(t > cutoff_time for t in timestamps)
        }
        
        # Get recent requests for this IP
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        recent_requests = [
            t for t in self.requests[client_ip]
            if t > cutoff_time
        ]
        
        # Check rate limit
        if len(recent_requests) >= self.requests_per_minute:
            error_response = create_error_response(
                code=ErrorCodes.RATE_LIMITED,
                message="Rate limit exceeded",
                details={"requests_per_minute": self.requests_per_minute}
            )
            
            response = JSONResponse(
                status_code=429,
                content=error_response.dict()
            )
            response.headers["Retry-After"] = "60"
            return response
        
        # Record this request
        recent_requests.append(current_time)
        self.requests[client_ip] = recent_requests
        
        return await call_next(request)


def add_rate_limiting(app: FastAPI, requests_per_minute: int = 60) -> None:
    """
    Add rate limiting middleware to FastAPI app.
    
    Args:
        app: FastAPI application instance
        requests_per_minute: Maximum requests per minute per IP
    """
    rate_limit_middleware = RateLimitMiddleware(requests_per_minute)
    app.middleware("http")(rate_limit_middleware)
