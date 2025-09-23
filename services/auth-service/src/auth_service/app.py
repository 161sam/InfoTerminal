"""Main FastAPI application for InfoTerminal Auth Service."""

import os
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, Response
from starlette.exceptions import HTTPException as StarletteHTTPException
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import REGISTRY, CollectorRegistry
from sqlalchemy import text

from .models.database import create_tables, init_database
from .api.auth import router as auth_router
from .api.users import router as users_router
from .api.roles import router as roles_router
from .api.schemas import HealthResponse, ErrorResponse

# Prometheus metrics
REQUEST_COUNT = Counter(
    'auth_service_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'auth_service_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

ERROR_COUNT = Counter(
    'auth_service_errors_total',
    'Total number of errors',
    ['error_type']
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    try:
        # Create database tables
        create_tables()
        print("✅ Database tables created successfully")
        
        # Initialize database with default data
        init_database()
        print("✅ Database initialized with default roles and permissions")
        
        print("🚀 Auth Service started successfully")
        
    except Exception as e:
        print(f"❌ Failed to initialize Auth Service: {e}")
        raise
    
    yield
    
    # Shutdown
    print("🛑 Auth Service shutting down")


# Create FastAPI application
app = FastAPI(
    title="InfoTerminal Auth Service",
    description="User Management and Authentication Service for InfoTerminal OSINT Platform",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
trusted_hosts = os.getenv("TRUSTED_HOSTS", "localhost,127.0.0.1").split(",")
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=trusted_hosts
)


# Metrics middleware
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware to collect Prometheus metrics."""
    start_time = datetime.now(timezone.utc)
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = (datetime.now(timezone.utc) - start_time).total_seconds()
    
    # Record metrics
    method = request.method
    endpoint = request.url.path
    status_code = response.status_code
    
    REQUEST_COUNT.labels(
        method=method,
        endpoint=endpoint,
        status=status_code
    ).inc()
    
    REQUEST_DURATION.labels(
        method=method,
        endpoint=endpoint
    ).observe(duration)
    
    # Count errors
    if status_code >= 400:
        if status_code < 500:
            ERROR_COUNT.labels(error_type="client_error").inc()
        else:
            ERROR_COUNT.labels(error_type="server_error").inc()
    
    return response


# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            details={"status_code": exc.status_code}
        ).dict()
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    ERROR_COUNT.labels(error_type="validation_error").inc()
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(
            error=str(exc),
            details={"error_type": "ValueError"}
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    ERROR_COUNT.labels(error_type="internal_error").inc()
    
    # Log the error (in production, use proper logging)
    print(f"Unhandled exception: {exc}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            details={"error_type": type(exc).__name__}
        ).dict()
    )


# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        from .models.database import SessionLocal
        
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        database_status = "healthy"
        
    except Exception as e:
        database_status = f"unhealthy: {str(e)}"
    
    return HealthResponse(
        status="healthy" if database_status == "healthy" else "degraded",
        timestamp=datetime.now(timezone.utc),
        version="1.0.0",
        database=database_status,
        services={
            "auth": "healthy",
            "user_management": "healthy",
            "role_management": "healthy"
        }
    )


# Metrics endpoint
@app.get("/metrics", tags=["metrics"])
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(
        content=generate_latest(REGISTRY),
        media_type=CONTENT_TYPE_LATEST
    )


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint with service information."""
    return {
        "service": "InfoTerminal Auth Service",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "docs": "/docs",
            "auth": "/auth",
            "users": "/users",
            "roles": "/roles"
        }
    }


# Include API routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)


# Security headers middleware
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    """Add security headers to responses."""
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    # Only add HSTS in production with HTTPS
    if os.getenv("ENVIRONMENT") == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response


# Request ID middleware
@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    """Add request ID to responses."""
    import uuid
    
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    
    return response


if __name__ == "__main__":
    import uvicorn
    
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    workers = int(os.getenv("WORKERS", "1"))
    log_level = os.getenv("LOG_LEVEL", "info")
    
    # Run the application
    uvicorn.run(
        "auth_service.app:app",
        host=host,
        port=port,
        workers=workers,
        log_level=log_level,
        reload=os.getenv("ENVIRONMENT") == "development"
    )
