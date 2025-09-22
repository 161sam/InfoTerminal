"""
Standard Health Check Schemas for InfoTerminal APIs

Provides consistent health and readiness check patterns across all services.
All services MUST implement both /healthz and /readyz endpoints using these standards.
"""

import time
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Callable, Awaitable
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """
    Standard health check response format.
    
    /healthz endpoint - Basic liveness check
    """
    status: str = Field(..., description="Service health status: 'healthy' or 'unhealthy'")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(..., description="Current timestamp")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")


class DependencyCheck(BaseModel):
    """Individual dependency health check result."""
    status: str = Field(..., description="Dependency status: 'healthy', 'unhealthy', or 'skipped'")
    latency_ms: Optional[float] = Field(None, description="Response latency in milliseconds")
    error: Optional[str] = Field(None, description="Error message if unhealthy")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional check details")


class ReadyResponse(BaseModel):
    """
    Standard readiness check response format.
    
    /readyz endpoint - Ready to serve traffic check
    """
    status: str = Field(..., description="Service readiness status: 'ready' or 'not_ready'")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(..., description="Current timestamp")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")
    dependencies: Dict[str, DependencyCheck] = Field(
        default_factory=dict,
        description="Dependency health check results"
    )


class HealthChecker:
    """
    Standard health checker implementation for InfoTerminal services.
    
    Usage:
        health_checker = HealthChecker("search-api", "1.0.0")
        health_checker.add_dependency("opensearch", check_opensearch)
        
        @app.get("/healthz")
        def healthz():
            return health_checker.health_check()
            
        @app.get("/readyz")  
        def readyz():
            return health_checker.ready_check()
    """
    
    def __init__(self, service_name: str, version: str):
        self.service_name = service_name
        self.version = version
        self.start_time = time.monotonic()
        self.dependencies: Dict[str, Callable[[], DependencyCheck]] = {}
    
    def add_dependency(
        self, 
        name: str, 
        check_func: Callable[[], DependencyCheck]
    ) -> None:
        """
        Add a dependency health check.
        
        Args:
            name: Dependency name (e.g., "database", "opensearch")
            check_func: Function that returns DependencyCheck result
        """
        self.dependencies[name] = check_func
    
    def health_check(self) -> HealthResponse:
        """
        Perform basic health check (liveness).
        
        Returns:
            HealthResponse indicating if service is alive
        """
        uptime = time.monotonic() - self.start_time
        
        return HealthResponse(
            status="healthy",
            service=self.service_name,
            version=self.version,
            timestamp=datetime.now(timezone.utc),
            uptime_seconds=uptime
        )
    
    def ready_check(self) -> ReadyResponse:
        """
        Perform readiness check (ready to serve traffic).
        
        Returns:
            ReadyResponse indicating if service and dependencies are ready
        """
        uptime = time.monotonic() - self.start_time
        
        # Skip dependency checks if forced ready
        if os.getenv("IT_FORCE_READY") == "1":
            return ReadyResponse(
                status="ready",
                service=self.service_name,
                version=self.version,
                timestamp=datetime.now(timezone.utc),
                uptime_seconds=uptime,
                dependencies={}
            )
        
        # Check all dependencies
        dependency_results = {}
        all_ready = True
        
        for name, check_func in self.dependencies.items():
            try:
                result = check_func()
                dependency_results[name] = result
                
                if result.status != "healthy":
                    all_ready = False
                    
            except Exception as e:
                dependency_results[name] = DependencyCheck(
                    status="unhealthy",
                    error=str(e)
                )
                all_ready = False
        
        overall_status = "ready" if all_ready else "not_ready"
        
        return ReadyResponse(
            status=overall_status,
            service=self.service_name,
            version=self.version,
            timestamp=datetime.now(timezone.utc),
            uptime_seconds=uptime,
            dependencies=dependency_results
        )


# Common dependency check implementations
def check_database_connection(db_func: Callable[[], None]) -> DependencyCheck:
    """
    Check database connectivity.
    
    Args:
        db_func: Function that performs a simple database operation
        
    Returns:
        DependencyCheck result
    """
    start_time = time.time()
    
    try:
        db_func()
        latency_ms = (time.time() - start_time) * 1000
        
        return DependencyCheck(
            status="healthy",
            latency_ms=latency_ms
        )
        
    except Exception as e:
        return DependencyCheck(
            status="unhealthy",
            error=str(e)
        )


def check_http_endpoint(url: str, timeout: int = 5) -> DependencyCheck:
    """
    Check HTTP endpoint availability.
    
    Args:
        url: HTTP endpoint URL to check
        timeout: Request timeout in seconds
        
    Returns:
        DependencyCheck result
    """
    import requests
    
    start_time = time.time()
    
    try:
        response = requests.get(url, timeout=timeout)
        latency_ms = (time.time() - start_time) * 1000
        
        if response.status_code < 400:
            return DependencyCheck(
                status="healthy",
                latency_ms=latency_ms,
                details={"status_code": response.status_code}
            )
        else:
            return DependencyCheck(
                status="unhealthy",
                error=f"HTTP {response.status_code}",
                details={"status_code": response.status_code}
            )
            
    except Exception as e:
        return DependencyCheck(
            status="unhealthy",
            error=str(e)
        )


# Convenience functions for FastAPI integration
def health_check(service_name: str, version: str) -> HealthResponse:
    """Simple health check function for FastAPI endpoints."""
    checker = HealthChecker(service_name, version)
    return checker.health_check()


def ready_check(
    service_name: str, 
    version: str,
    dependencies: Optional[Dict[str, Callable[[], DependencyCheck]]] = None
) -> ReadyResponse:
    """Simple readiness check function for FastAPI endpoints."""
    checker = HealthChecker(service_name, version)
    
    if dependencies:
        for name, check_func in dependencies.items():
            checker.add_dependency(name, check_func)
    
    return checker.ready_check()
