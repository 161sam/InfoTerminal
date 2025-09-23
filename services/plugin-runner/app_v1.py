"""
InfoTerminal Plugin Runner Service v1.0.0

Standardized *_v1.py implementation for secure plugin execution.
Provides unified API for executing OSINT and security tools in sandboxed environments.

This service replaces the legacy app.py with:
- Standard /v1 API namespace
- Error-Envelope response format  
- Health/Ready endpoints
- OpenAPI documentation
- Structured logging
- Background job processing
"""

import os
import sys
import asyncio
import tempfile
from pathlib import Path
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import structlog
import docker
from docker.errors import DockerException

# Add shared modules to path
SERVICE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from _shared.api_standards import (
    setup_standard_middleware,
    setup_standard_exception_handlers,
    setup_standard_openapi,
    get_service_tags_metadata,
    HealthChecker,
    DependencyCheck,
)
from _shared.clients.graph_ingest import GraphIngestClient
from _shared.obs.metrics_boot import enable_prometheus_metrics

# Import plugin system components
from registry import PluginRegistry
from metrics import (
    PLUGIN_RUN_DURATION_SECONDS,
    PLUGIN_RUN_FAILURE_TOTAL,
    PLUGIN_RUN_TOTAL,
)

# Import routers
from routers.core_v1 import router as core_router, set_dependencies
from routers.plugins_v1 import router as plugins_router, set_plugin_system

# Configure structured logging
logger = structlog.get_logger()

# Service Configuration
SERVICE_NAME = "plugin-runner"
SERVICE_VERSION = "1.0.0"
SERVICE_DESCRIPTION = "Secure execution of OSINT and security tools in sandboxed environments"

# Configuration from environment
PLUGINS_DIR = Path(os.getenv("PLUGINS_DIR", "/app/plugins"))
RESULTS_DIR = Path(os.getenv("RESULTS_DIR", "/app/results"))
DOCKER_ENABLED = os.getenv("PLUGIN_DOCKER_ENABLED", "1") == "1"
MAX_EXECUTION_TIME = int(os.getenv("PLUGIN_MAX_EXECUTION_TIME", "300"))  # 5 minutes
MAX_CONCURRENT_JOBS = int(os.getenv("PLUGIN_MAX_CONCURRENT", "5"))

# Global state
plugin_registry = None
running_jobs = {}
job_queue = None
job_processor_task = None
docker_client = None
health_checker = HealthChecker(SERVICE_NAME, SERVICE_VERSION)
graph_client: GraphIngestClient | None = None


async def job_processor():
    """Background job processor for plugin executions."""
    global running_jobs, job_queue, plugin_registry
    
    logger.info("Starting job processor")
    
    while True:
        try:
            # Get next job from queue
            job_id, plugin_name, parameters, output_format = await job_queue.get()
            
            # Check concurrent job limit
            active_jobs = sum(1 for job in running_jobs.values() if job["status"] == "running")
            if active_jobs >= MAX_CONCURRENT_JOBS:
                # Put job back in queue and wait
                await job_queue.put((job_id, plugin_name, parameters, output_format))
                await asyncio.sleep(5)
                continue
            
            # Update job status
            if job_id in running_jobs:
                running_jobs[job_id]["status"] = "running"
                running_jobs[job_id]["started_at"] = datetime.utcnow()
                
                logger.info("Starting plugin execution", job_id=job_id, plugin=plugin_name)
                
                try:
                    # Execute plugin
                    result = await plugin_registry.execute_plugin(
                        plugin_name, parameters, job_id, output_format
                    )
                    
                    # Update job with results
                    running_jobs[job_id].update(
                        {
                            "status": result.status,
                            "completed_at": result.completed_at,
                            "execution_time": result.execution_time,
                            "results": result.parsed_output,
                            "graph_entities": getattr(result, "graph_entities", []),
                            "search_documents": getattr(result, "search_documents", []),
                            "error": result.error,
                            "output_files": getattr(result, "output_files", []),
                        }
                    )

                    execution_time = result.execution_time or 0.0
                    PLUGIN_RUN_TOTAL.labels(plugin=plugin_name).inc()
                    if result.status != "completed":
                        PLUGIN_RUN_FAILURE_TOTAL.labels(plugin=plugin_name).inc()
                    else:
                        PLUGIN_RUN_DURATION_SECONDS.labels(plugin=plugin_name).observe(
                            execution_time
                        )

                    if graph_client is not None:
                        ingest_payload = {
                            "job_id": job_id,
                            "plugin_name": plugin_name,
                            "status": result.status,
                            "completed_at": result.completed_at.isoformat()
                            if result.completed_at
                            else None,
                            "execution_time": execution_time,
                            "graph_entities": getattr(result, "graph_entities", []),
                            "search_documents": getattr(result, "search_documents", []),
                        }
                        try:
                            ingest_result = await graph_client.ingest_plugin_run(
                                ingest_payload
                            )
                            running_jobs[job_id]["graph_ingest"] = ingest_result
                        except Exception as exc:  # pragma: no cover
                            logger.warning(
                                "Graph ingest failed", job_id=job_id, error=str(exc)
                            )
                    
                    # Save results to file if configured
                    if running_jobs[job_id].get("save_output", True):
                        result_file = RESULTS_DIR / f"{job_id}.json"
                        import json
                        import aiofiles
                        async with aiofiles.open(result_file, 'w') as f:
                            await f.write(json.dumps({
                                "job_id": job_id,
                                "plugin_name": plugin_name,
                                "status": result.status,
                                "results": result.parsed_output,
                                "execution_time": result.execution_time,
                                "completed_at": result.completed_at.isoformat() if result.completed_at else None,
                                "error": result.error
                            }, indent=2, default=str))
                    
                    logger.info("Plugin execution completed", 
                               job_id=job_id, 
                               plugin=plugin_name, 
                               status=result.status,
                               execution_time=result.execution_time)
                    
                except Exception as e:
                    PLUGIN_RUN_TOTAL.labels(plugin=plugin_name).inc()
                    PLUGIN_RUN_FAILURE_TOTAL.labels(plugin=plugin_name).inc()
                    logger.error(
                        "Plugin execution failed",
                        job_id=job_id,
                        plugin=plugin_name,
                        error=str(e),
                    )
                    if job_id in running_jobs:
                        running_jobs[job_id].update(
                            {
                                "status": "failed",
                                "error": str(e),
                                "completed_at": datetime.utcnow(),
                            }
                        )
            
        except Exception as e:
            logger.error("Job processor error", error=str(e))
            await asyncio.sleep(1)


def check_plugin_registry() -> DependencyCheck:
    """Check plugin registry health."""
    try:
        if plugin_registry is None:
            return DependencyCheck(
                status="unhealthy",
                error="Plugin registry not initialized"
            )
        
        plugin_count = len(plugin_registry.plugins)
        return DependencyCheck(
            status="healthy",
            message=f"{plugin_count} plugins loaded",
            latency_ms=1.0
        )
    except Exception as e:
        return DependencyCheck(
            status="unhealthy",
            error=str(e)
        )


def check_docker_connection() -> DependencyCheck:
    """Check Docker daemon connection."""
    if not DOCKER_ENABLED:
        return DependencyCheck(
            status="disabled",
            message="Docker execution disabled"
        )
    
    try:
        if docker_client is None:
            return DependencyCheck(
                status="unhealthy",
                error="Docker client not initialized"
            )
        
        docker_client.ping()
        return DependencyCheck(
            status="healthy",
            message="Docker daemon accessible",
            latency_ms=5.0
        )
    except Exception as e:
        return DependencyCheck(
            status="unhealthy",
            error=f"Docker unavailable: {str(e)}"
        )


def check_job_queue() -> DependencyCheck:
    """Check job queue health."""
    try:
        if job_queue is None:
            return DependencyCheck(
                status="unhealthy",
                error="Job queue not initialized"
            )
        
        queue_size = job_queue.qsize()
        active_jobs = sum(1 for job in running_jobs.values() if job["status"] == "running")
        
        return DependencyCheck(
            status="healthy",
            message=f"Queue size: {queue_size}, Active jobs: {active_jobs}",
            latency_ms=1.0
        )
    except Exception as e:
        return DependencyCheck(
            status="unhealthy",
            error=str(e)
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    global plugin_registry, job_queue, job_processor_task, docker_client, graph_client
    
    logger.info(f"Starting {SERVICE_NAME} v{SERVICE_VERSION}")
    
    try:
        # Ensure directories exist
        RESULTS_DIR.mkdir(exist_ok=True)
        
        # Initialize Docker client if enabled
        if DOCKER_ENABLED:
            try:
                docker_client = docker.from_env()
                docker_client.ping()  # Test connection
                logger.info("Docker client initialized successfully")
            except DockerException as e:
                logger.warning("Docker initialization failed", error=str(e))
                docker_client = None
        
        # Initialize plugin registry
        plugin_registry = PluginRegistry(PLUGINS_DIR)
        logger.info("Plugin registry initialized", plugins_count=len(plugin_registry.plugins))
        
        # Initialize job queue
        job_queue = asyncio.Queue()
        
        # Start job processor
        job_processor_task = asyncio.create_task(job_processor())

        # Prepare graph ingestion helper (optional when graph-api offline)
        graph_client = GraphIngestClient(
            fallback_dir=RESULTS_DIR / "graph_ingest"
        )
        
        # Set up dependency checks
        health_checker.add_dependency("plugin_registry", check_plugin_registry)
        health_checker.add_dependency("docker", check_docker_connection)
        health_checker.add_dependency("job_queue", check_job_queue)
        
        # Set dependencies in routers
        set_dependencies(plugin_registry, docker_client)
        set_plugin_system(plugin_registry, running_jobs, job_queue, job_processor_task)
        
        logger.info(f"{SERVICE_NAME} startup completed successfully")
        
    except Exception as e:
        logger.error("Failed to initialize plugin runner", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {SERVICE_NAME}")
    
    # Cancel job processor
    if job_processor_task:
        job_processor_task.cancel()
        try:
            await job_processor_task
        except asyncio.CancelledError:
            pass
    
    # Close Docker client
    if docker_client:
        docker_client.close()

    if graph_client:
        await graph_client.close()


# FastAPI application with standardized configuration
app = FastAPI(
    title="InfoTerminal Plugin Runner API",
    description=SERVICE_DESCRIPTION,
    version=SERVICE_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Apply standard middleware and exception handlers
setup_standard_middleware(app, SERVICE_NAME)
setup_standard_exception_handlers(app)

# Set up standard OpenAPI documentation
setup_standard_openapi(
    app=app,
    title="InfoTerminal Plugin Runner API",
    description=SERVICE_DESCRIPTION,
    version=SERVICE_VERSION,
    service_name=SERVICE_NAME,
    tags_metadata=get_service_tags_metadata(SERVICE_NAME)
)

# Enable Prometheus metrics if observability profile enabled
enable_prometheus_metrics(app)

# Include routers
app.include_router(core_router, tags=["Core"])
app.include_router(plugins_router, prefix="/v1", tags=["Plugins"])

# Legacy endpoints for backward compatibility
@app.get("/health", deprecated=True, include_in_schema=False)
def legacy_health():
    """DEPRECATED: Use /healthz instead."""
    return JSONResponse(
        content={"status": "healthy", "message": "Use /healthz instead"},
        headers={"X-Deprecated": "Use /healthz instead"}
    )

@app.get("/plugins", deprecated=True, include_in_schema=False)
def legacy_list_plugins():
    """DEPRECATED: Use /v1/plugins instead."""
    return JSONResponse(
        content={"error": "Endpoint moved to /v1/plugins"},
        status_code=410,
        headers={"X-Deprecated": "Use /v1/plugins instead"}
    )

@app.post("/execute", deprecated=True, include_in_schema=False)
def legacy_execute():
    """DEPRECATED: Use /v1/plugins/{plugin_name}/execute instead."""
    return JSONResponse(
        content={"error": "Endpoint moved to /v1/plugins/{plugin_name}/execute"},
        status_code=410,
        headers={"X-Deprecated": "Use /v1/plugins/{plugin_name}/execute instead"}
    )

@app.get("/jobs/{job_id}", deprecated=True, include_in_schema=False)
def legacy_job_status():
    """DEPRECATED: Use /v1/jobs/{job_id} instead."""
    return JSONResponse(
        content={"error": "Endpoint moved to /v1/jobs/{job_id}"},
        status_code=410,
        headers={"X-Deprecated": "Use /v1/jobs/{job_id} instead"}
    )


# Root endpoint
@app.get("/", include_in_schema=False)
def root():
    """Root endpoint with service information."""
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "description": SERVICE_DESCRIPTION,
        "api_version": "v1",
        "documentation": "/docs",
        "health_check": "/healthz",
        "readiness_check": "/readyz",
        "openapi_spec": "/openapi.json"
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "app_v1:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENVIRONMENT") == "development"
    )
