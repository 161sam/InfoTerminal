"""
Plugin Runner Service for InfoTerminal
Safely executes security and investigation tools in sandboxed environments.
"""

import os
import json
import uuid
import asyncio
import tempfile
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
import yaml
import aiofiles
import docker
from docker.errors import DockerException

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel, validator
import structlog

# Import our plugin registry
import sys
SERVICE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_DIR.parent.parent
for p in (SERVICE_DIR, REPO_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from registry import PluginRegistry, PluginExecutionResult

try:
    from _shared.cors import apply_cors, get_cors_settings_from_env
    from _shared.health import make_healthz, make_readyz
    from common.request_id import RequestIdMiddleware
    from _shared.obs.otel_boot import setup_otel
except ImportError:
    # Fallback for development
    def apply_cors(app, settings): pass
    def get_cors_settings_from_env(): return {}
    def make_healthz(name, version, ts): return {"status": "ok"}
    def make_readyz(name, version, ts, checks): return {"status": "ready"}, 200
    def setup_otel(app, service_name, version): pass
    class RequestIdMiddleware: pass

# Configure structured logging
logger = structlog.get_logger()

app = FastAPI(
    title="InfoTerminal Plugin Runner",
    description="Secure execution of OSINT and security tools",
    version="0.2.0"
)

# Setup middleware
try:
    apply_cors(app, get_cors_settings_from_env())
    app.add_middleware(RequestIdMiddleware)
    setup_otel(app, service_name="plugin-runner", version="0.2.0")
except:
    pass

# Configuration
PLUGINS_DIR = Path(os.getenv("PLUGINS_DIR", "/app/plugins"))
RESULTS_DIR = Path(os.getenv("RESULTS_DIR", "/app/results"))
DOCKER_ENABLED = os.getenv("PLUGIN_DOCKER_ENABLED", "1") == "1"
MAX_EXECUTION_TIME = int(os.getenv("PLUGIN_MAX_EXECUTION_TIME", "300"))  # 5 minutes
MAX_CONCURRENT_JOBS = int(os.getenv("PLUGIN_MAX_CONCURRENT", "5"))

# Global state
plugin_registry = None
running_jobs = {}
job_queue = asyncio.Queue()


class PluginExecutionRequest(BaseModel):
    plugin_name: str
    parameters: Dict[str, Any]
    timeout: Optional[int] = 300
    output_format: str = "json"
    priority: int = 1
    
    @validator('plugin_name')
    def validate_plugin_name(cls, v):
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Plugin name must be alphanumeric with hyphens/underscores only')
        return v


class PluginExecutionResponse(BaseModel):
    job_id: str
    status: str  # "queued", "running", "completed", "failed"
    plugin_name: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time: Optional[float] = None
    results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    output_files: List[str] = []
    graph_entities: List[Dict[str, Any]] = []
    search_documents: List[Dict[str, Any]] = []


class JobStatus(BaseModel):
    job_id: str
    status: str
    plugin_name: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: Optional[str] = None
    error: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize plugin registry and start job processor."""
    global plugin_registry
    
    # Ensure directories exist
    RESULTS_DIR.mkdir(exist_ok=True)
    
    # Initialize plugin registry
    plugin_registry = PluginRegistry(PLUGINS_DIR)
    
    # Start job processor
    asyncio.create_task(job_processor())
    
    logger.info("Plugin Runner service started", 
               plugins_count=len(plugin_registry.plugins),
               docker_enabled=DOCKER_ENABLED)


async def job_processor():
    """Background job processor for plugin executions."""
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
            running_jobs[job_id]["status"] = "running"
            running_jobs[job_id]["started_at"] = datetime.utcnow()
            
            logger.info("Starting plugin execution", job_id=job_id, plugin=plugin_name)
            
            # Execute plugin
            result = await plugin_registry.execute_plugin(
                plugin_name, parameters, job_id, output_format
            )
            
            # Update job with results
            running_jobs[job_id].update({
                "status": result.status,
                "completed_at": result.completed_at,
                "execution_time": result.execution_time,
                "results": result.parsed_output,
                "graph_entities": result.graph_entities,
                "search_documents": result.search_documents,
                "error": result.error
            })
            
            # Save results to file
            result_file = RESULTS_DIR / f"{job_id}.json"
            async with aiofiles.open(result_file, 'w') as f:
                await f.write(json.dumps(result.dict(), indent=2, default=str))
            
            logger.info("Plugin execution completed", 
                       job_id=job_id, 
                       plugin=plugin_name, 
                       status=result.status,
                       execution_time=result.execution_time)
            
        except Exception as e:
            logger.error("Job processor error", error=str(e))
            if job_id in running_jobs:
                running_jobs[job_id].update({
                    "status": "failed",
                    "error": str(e),
                    "completed_at": datetime.utcnow()
                })
            await asyncio.sleep(1)


@app.get("/healthz")
def healthz():
    return make_healthz("plugin-runner", "0.2.0", 0)


@app.get("/readyz")
def readyz():
    checks = {
        "plugin_registry": {
            "status": "ok" if plugin_registry else "fail",
            "plugins_loaded": len(plugin_registry.plugins) if plugin_registry else 0
        }
    }
    if DOCKER_ENABLED:
        try:
            docker_client = docker.from_env()
            docker_client.ping()
            checks["docker"] = {"status": "ok"}
        except Exception as e:
            checks["docker"] = {"status": "fail", "error": str(e)}
    
    all_ok = all(check.get("status") == "ok" for check in checks.values())
    status_code = 200 if all_ok else 503
    
    return {"status": "ready" if all_ok else "not_ready", "checks": checks}, status_code


@app.get("/plugins")
def list_plugins(category: Optional[str] = None):
    """List available plugins with optional category filter."""
    if not plugin_registry:
        raise HTTPException(503, "Plugin registry not initialized")
    
    plugins = plugin_registry.list_plugins(category)
    return {
        "plugins": plugins,
        "total": len(plugins),
        "categories": list(set(p["category"] for p in plugins))
    }


@app.get("/plugins/{plugin_name}")
def get_plugin_info(plugin_name: str):
    """Get detailed information about a specific plugin."""
    if not plugin_registry:
        raise HTTPException(503, "Plugin registry not initialized")
    
    plugin_config = plugin_registry.get_plugin(plugin_name)
    if not plugin_config:
        raise HTTPException(404, f"Plugin '{plugin_name}' not found")
    
    return {
        "name": plugin_config.name,
        "version": plugin_config.version,
        "description": plugin_config.description,
        "category": plugin_config.category,
        "author": plugin_config.author,
        "risk_level": plugin_config.risk_level,
        "requires_network": plugin_config.requires_network,
        "requires_root": plugin_config.requires_root,
        "parameters": plugin_config.parameters,
        "output_formats": plugin_config.output_format,
        "security": plugin_config.security
    }


@app.post("/execute")
async def execute_plugin(request: PluginExecutionRequest, background_tasks: BackgroundTasks):
    """Execute a plugin with given parameters."""
    if not plugin_registry:
        raise HTTPException(503, "Plugin registry not initialized")
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Validate plugin exists
    if not plugin_registry.get_plugin(request.plugin_name):
        raise HTTPException(404, f"Plugin '{request.plugin_name}' not found")
    
    # Create job record
    job_record = {
        "job_id": job_id,
        "plugin_name": request.plugin_name,
        "status": "queued",
        "created_at": datetime.utcnow(),
        "started_at": None,
        "completed_at": None,
        "parameters": request.parameters,
        "output_format": request.output_format,
        "results": None,
        "error": None,
        "graph_entities": [],
        "search_documents": []
    }
    
    running_jobs[job_id] = job_record
    
    # Add to execution queue
    await job_queue.put((job_id, request.plugin_name, request.parameters, request.output_format))
    
    logger.info("Plugin execution queued", job_id=job_id, plugin=request.plugin_name)
    
    return {
        "job_id": job_id,
        "status": "queued",
        "plugin_name": request.plugin_name,
        "message": "Plugin execution queued"
    }


@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    """Get status and results of a plugin execution job."""
    if job_id not in running_jobs:
        raise HTTPException(404, "Job not found")
    
    job = running_jobs[job_id]
    
    response = PluginExecutionResponse(
        job_id=job_id,
        status=job["status"],
        plugin_name=job["plugin_name"],
        started_at=job.get("started_at"),
        completed_at=job.get("completed_at"),
        execution_time=job.get("execution_time"),
        results=job.get("results"),
        error=job.get("error"),
        graph_entities=job.get("graph_entities", []),
        search_documents=job.get("search_documents", [])
    )
    
    return response


@app.get("/jobs")
def list_jobs(status: Optional[str] = None, limit: int = 50):
    """List recent plugin execution jobs."""
    jobs = []
    
    for job_id, job_data in list(running_jobs.items())[-limit:]:
        if status is None or job_data["status"] == status:
            jobs.append(JobStatus(
                job_id=job_id,
                status=job_data["status"],
                plugin_name=job_data["plugin_name"],
                created_at=job_data["created_at"],
                started_at=job_data.get("started_at"),
                completed_at=job_data.get("completed_at"),
                error=job_data.get("error")
            ))
    
    return {
        "jobs": jobs,
        "total": len(jobs)
    }


@app.delete("/jobs/{job_id}")
def cancel_job(job_id: str):
    """Cancel a queued or running job."""
    if job_id not in running_jobs:
        raise HTTPException(404, "Job not found")
    
    job = running_jobs[job_id]
    
    if job["status"] == "completed":
        raise HTTPException(400, "Cannot cancel completed job")
    
    if job["status"] == "failed":
        raise HTTPException(400, "Cannot cancel failed job")
    
    # Mark as cancelled
    job["status"] = "cancelled"
    job["completed_at"] = datetime.utcnow()
    job["error"] = "Job cancelled by user"
    
    logger.info("Job cancelled", job_id=job_id)
    
    return {"message": "Job cancelled", "job_id": job_id}


@app.get("/categories")
def get_plugin_categories():
    """Get available plugin categories."""
    if not plugin_registry:
        raise HTTPException(503, "Plugin registry not initialized")
    
    categories = {}
    
    for plugin_name, plugin_config in plugin_registry.plugins.items():
        category = plugin_config.category
        if category not in categories:
            categories[category] = {
                "name": category,
                "plugins": [],
                "risk_levels": set()
            }
        
        categories[category]["plugins"].append({
            "name": plugin_name,
            "description": plugin_config.description,
            "risk_level": plugin_config.risk_level
        })
        categories[category]["risk_levels"].add(plugin_config.risk_level)
    
    # Convert sets to lists
    for category in categories.values():
        category["risk_levels"] = list(category["risk_levels"])
    
    return {
        "categories": list(categories.values()),
        "total_categories": len(categories)
    }


@app.get("/statistics")
def get_statistics():
    """Get plugin execution statistics."""
    stats = {
        "total_plugins": len(plugin_registry.plugins) if plugin_registry else 0,
        "total_jobs": len(running_jobs),
        "job_status_counts": {},
        "plugin_usage_counts": {},
        "average_execution_time": 0,
        "docker_enabled": DOCKER_ENABLED
    }
    
    # Count job statuses
    execution_times = []
    for job in running_jobs.values():
        status = job["status"]
        stats["job_status_counts"][status] = stats["job_status_counts"].get(status, 0) + 1
        
        # Count plugin usage
        plugin_name = job["plugin_name"]
        stats["plugin_usage_counts"][plugin_name] = stats["plugin_usage_counts"].get(plugin_name, 0) + 1
        
        # Collect execution times
        if job.get("execution_time"):
            execution_times.append(job["execution_time"])
    
    # Calculate average execution time
    if execution_times:
        stats["average_execution_time"] = sum(execution_times) / len(execution_times)
    
    return stats


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
