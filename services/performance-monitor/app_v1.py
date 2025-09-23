"""
Performance Monitor Service v1 - Real-time Performance Monitoring

Standardized FastAPI application with:
- /v1 API namespace
- Standard error handling  
- Health/ready checks
- OpenAPI documentation
- Comprehensive performance monitoring
- Automated alert system
- Trend analysis and recommendations
"""

import logging
import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics

# Add service and repo to path
SERVICE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_DIR.parent.parent
for p in (SERVICE_DIR, REPO_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# Import routers
from routers.core_v1 import router as core_router
from routers.performance_monitor_v1 import router as performance_router, initialize_monitor

# Import shared standards
try:
    from _shared.api_standards.middleware import setup_standard_middleware
    from _shared.api_standards.error_schemas import StandardError
    HAS_SHARED_STANDARDS = True
except ImportError:
    HAS_SHARED_STANDARDS = False
    logging.warning("Shared API standards not available, using fallback")

# Import legacy CORS if available
try:
    from _shared.cors import apply_cors, get_cors_settings_from_env
    HAS_LEGACY_CORS = True
except ImportError:
    HAS_LEGACY_CORS = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Performance Monitor Service",
    description="Real-time performance monitoring with metrics collection, analysis, alerting, and optimization recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Setup middleware
if HAS_SHARED_STANDARDS:
    setup_standard_middleware(app)
else:
    # Fallback middleware setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add Prometheus metrics
app.add_middleware(PrometheusMiddleware, app_name="performance_monitor")
app.add_route("/metrics", handle_metrics)

# Apply legacy CORS if available
if HAS_LEGACY_CORS:
    try:
        apply_cors(app)
    except Exception as e:
        logger.warning(f"Failed to apply legacy CORS: {e}")

# Include routers
app.include_router(core_router, prefix="")  # Core endpoints at root
app.include_router(performance_router, prefix="")  # Performance endpoints with /v1 prefix

# Legacy compatibility - preserve old endpoints with deprecation warnings
@app.get("/healthz", tags=["Legacy"], deprecated=True)
def legacy_healthz():
    """Legacy health endpoint. Use /healthz instead."""
    logger.warning("Legacy /healthz endpoint used. Consider upgrading to standardized endpoints.")
    return {"status": "ok", "warning": "Legacy endpoint deprecated"}

@app.post("/metrics", tags=["Legacy"], deprecated=True)
async def legacy_metrics():
    """Legacy metrics endpoint. Use /v1/metrics instead."""
    logger.warning("Legacy /metrics endpoint used. Use /v1/metrics")
    return {"error": "Legacy endpoint deprecated. Use /v1/metrics"}

@app.get("/metrics/{service_name}/summary", tags=["Legacy"], deprecated=True)
async def legacy_service_summary(service_name: str):
    """Legacy service summary endpoint. Use /v1/services/{service_name}/summary instead."""
    logger.warning(f"Legacy /metrics/{service_name}/summary endpoint used. Use /v1/services/{service_name}/summary")
    return {"error": "Legacy endpoint deprecated. Use /v1/services/{service_name}/summary"}

@app.get("/alerts", tags=["Legacy"], deprecated=True)
async def legacy_alerts():
    """Legacy alerts endpoint. Use /v1/alerts instead."""
    logger.warning("Legacy /alerts endpoint used. Use /v1/alerts")
    return {"error": "Legacy endpoint deprecated. Use /v1/alerts"}

@app.get("/metrics/{service_name}/{metric_type}", tags=["Legacy"], deprecated=True)
async def legacy_service_metrics(service_name: str, metric_type: str):
    """Legacy service metrics endpoint. Use /v1/services/{service_name}/metrics/{metric_type} instead."""
    logger.warning(f"Legacy /metrics/{service_name}/{metric_type} endpoint used. Use /v1/services/{service_name}/metrics/{metric_type}")
    return {"error": "Legacy endpoint deprecated. Use /v1/services/{service_name}/metrics/{metric_type}"}

@app.get("/health", tags=["Legacy"], deprecated=True)
async def legacy_health():
    """Legacy health endpoint. Use /v1/health/status instead."""
    logger.warning("Legacy /health endpoint used. Use /v1/health/status")
    return {"error": "Legacy endpoint deprecated. Use /v1/health/status"}

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """Service root information."""
    return {
        "service": "performance-monitor",
        "version": "v1",
        "status": "operational",
        "description": "Real-time performance monitoring with intelligent analysis and alerting",
        "capabilities": [
            "API response time monitoring",
            "System resource monitoring (CPU/Memory/Disk)",
            "Performance alert system with configurable thresholds",
            "Trend analysis and memory leak detection",
            "Error rate tracking and analysis",
            "Service-specific performance summaries",
            "Automated optimization recommendations",
            "Real-time metrics collection via middleware",
            "Redis-based persistence (optional)",
            "Comprehensive system health monitoring"
        ],
        "metric_types": [
            "response_time",
            "memory_usage",
            "cpu_usage", 
            "error_rate",
            "throughput",
            "database_latency"
        ],
        "endpoints": {
            "health": "/healthz",
            "ready": "/readyz", 
            "info": "/info",
            "api_docs": "/docs",
            "metrics": "/metrics",
            "v1_api": "/v1/*"
        }
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Service startup initialization."""
    logger.info("Performance Monitor service v1 starting up...")
    
    # Check dependencies
    try:
        import numpy
        import psutil
        logger.info("Required dependencies verified: numpy, psutil")
    except ImportError as e:
        logger.error(f"Missing required dependency: {e}")
        raise
    
    # Check optional dependencies
    try:
        import aioredis
        logger.info("Redis support available")
    except ImportError:
        logger.warning("Redis not available - using in-memory storage only")
    
    # Initialize performance monitor
    try:
        await initialize_monitor()
        logger.info("Performance monitor initialized")
    except Exception as e:
        logger.warning(f"Performance monitor initialization failed: {e}")
    
    # Start system metrics collection
    try:
        import asyncio
        from routers.performance_monitor_v1 import monitor
        
        # Create system metrics collector task
        async def collect_system_metrics():
            """Collect system metrics periodically."""
            import time
            import uuid
            from datetime import datetime
            from models import PerformanceMetric, MetricType
            
            while True:
                try:
                    timestamp = datetime.now()
                    service_name = "system"
                    
                    # Memory usage
                    memory = psutil.virtual_memory()
                    await monitor.record_metric(PerformanceMetric(
                        id=str(uuid.uuid4()),
                        timestamp=timestamp,
                        metric_type=MetricType.MEMORY_USAGE,
                        value=memory.percent,
                        service_name=service_name,
                        metadata={
                            "total_gb": round(memory.total / (1024**3), 2),
                            "available_gb": round(memory.available / (1024**3), 2),
                            "used_gb": round(memory.used / (1024**3), 2)
                        }
                    ))
                    
                    # CPU usage
                    cpu_percent = psutil.cpu_percent(interval=1)
                    await monitor.record_metric(PerformanceMetric(
                        id=str(uuid.uuid4()),
                        timestamp=timestamp,
                        metric_type=MetricType.CPU_USAGE,
                        value=cpu_percent,
                        service_name=service_name,
                        metadata={
                            "cpu_count": psutil.cpu_count(),
                            "load_average": list(os.getloadavg()) if hasattr(os, 'getloadavg') else None
                        }
                    ))
                    
                    await asyncio.sleep(30)  # Collect every 30 seconds
                    
                except Exception as e:
                    logger.error(f"Error collecting system metrics: {e}")
                    await asyncio.sleep(30)
        
        # Start system metrics collection task
        asyncio.create_task(collect_system_metrics())
        logger.info("System metrics collection started")
        
    except Exception as e:
        logger.warning(f"Failed to start system metrics collection: {e}")
    
    logger.info("Performance Monitor service v1 startup complete")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Service shutdown cleanup."""
    logger.info("Performance Monitor service v1 shutting down...")
    
    # Cleanup Redis connection
    from routers.performance_monitor_v1 import monitor
    if monitor.redis:
        try:
            await monitor.redis.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.warning(f"Redis cleanup failed: {e}")
    
    logger.info("Performance Monitor service v1 shutdown complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
