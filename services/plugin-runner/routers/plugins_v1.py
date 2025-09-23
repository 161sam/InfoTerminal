"""
Plugins router for Plugin Runner v1 API.

Handles all plugin-related operations including execution, management, and monitoring.
"""

import uuid
import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query, Depends
from fastapi.responses import JSONResponse

import sys

# Add shared modules to path
SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from _shared.api_standards import (
    PaginatedResponse,
    PaginationParams,
    APIError,
    ErrorCodes
)

from ..models.requests import (
    PluginExecutionRequest,
    PluginBatchRequest,
    PluginConfigRequest,
    PluginSearchRequest
)

from ..models.responses import (
    PluginInfo,
    PluginExecutionResponse,
    JobStatus,
    PluginCategory,
    PluginStatistics,
    PluginCapabilities,
    BatchExecutionResponse,
    PluginHealthStatus
)

router = APIRouter()

# Global references - will be set by main app
plugin_registry = None
running_jobs = {}
job_queue = None
job_processor_task = None


def set_plugin_system(registry, jobs_dict, queue, processor):
    """Set plugin system references from main application."""
    global plugin_registry, running_jobs, job_queue, job_processor_task
    plugin_registry = registry
    running_jobs = jobs_dict
    job_queue = queue
    job_processor_task = processor


# ===== PLUGIN DISCOVERY & INFORMATION =====

@router.get(
    "/plugins",
    response_model=PaginatedResponse[PluginInfo],
    summary="List Plugins",
    description="Get a paginated list of available plugins with optional filtering"
)
def list_plugins(
    pagination: PaginationParams = Depends(),
    category: Optional[str] = Query(None, description="Filter by category"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level"),
    enabled_only: bool = Query(True, description="Only return enabled plugins"),
    q: Optional[str] = Query(None, description="Search query")
) -> PaginatedResponse[PluginInfo]:
    """
    List available plugins with filtering and pagination.
    
    Supports filtering by category, risk level, and search query.
    Returns comprehensive plugin information including capabilities and parameters.
    """
    if not plugin_registry:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Plugin registry not initialized",
            status_code=503
        )
    
    try:
        # Get all plugins
        all_plugins = []
        for plugin_name, plugin_config in plugin_registry.plugins.items():
            # Apply filters
            if category and plugin_config.category != category:
                continue
            if risk_level and plugin_config.risk_level != risk_level:
                continue
            if enabled_only and not getattr(plugin_config, 'enabled', True):
                continue
            if q and q.lower() not in plugin_name.lower() and q.lower() not in plugin_config.description.lower():
                continue
            
            plugin_info = PluginInfo(
                name=plugin_config.name,
                version=plugin_config.version,
                description=plugin_config.description,
                category=plugin_config.category,
                author=getattr(plugin_config, 'author', None),
                risk_level=plugin_config.risk_level,
                requires_network=plugin_config.requires_network,
                requires_root=plugin_config.requires_root,
                enabled=getattr(plugin_config, 'enabled', True),
                parameters=plugin_config.parameters,
                output_formats=plugin_config.output_format if isinstance(plugin_config.output_format, list) else [plugin_config.output_format],
                security=plugin_config.security,
                capabilities=getattr(plugin_config, 'capabilities', [])
            )
            all_plugins.append(plugin_info)
        
        # Apply pagination
        total = len(all_plugins)
        start = pagination.offset
        end = start + pagination.limit
        plugins_page = all_plugins[start:end]
        
        return PaginatedResponse.create(plugins_page, total, pagination)
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve plugins",
            status_code=500,
            details={"error": str(e)}
        )


@router.get(
    "/plugins/{plugin_name}",
    response_model=PluginInfo,
    summary="Get Plugin Details",
    description="Get detailed information about a specific plugin"
)
def get_plugin_info(plugin_name: str) -> PluginInfo:
    """
    Get detailed information about a specific plugin.
    
    Returns comprehensive plugin metadata including parameters, capabilities,
    security requirements, and execution information.
    """
    if not plugin_registry:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Plugin registry not initialized",
            status_code=503
        )
    
    plugin_config = plugin_registry.get_plugin(plugin_name)
    if not plugin_config:
        raise APIError(
            code=ErrorCodes.RESOURCE_NOT_FOUND,
            message=f"Plugin '{plugin_name}' not found",
            status_code=404
        )
    
    try:
        return PluginInfo(
            name=plugin_config.name,
            version=plugin_config.version,
            description=plugin_config.description,
            category=plugin_config.category,
            author=getattr(plugin_config, 'author', None),
            risk_level=plugin_config.risk_level,
            requires_network=plugin_config.requires_network,
            requires_root=plugin_config.requires_root,
            enabled=getattr(plugin_config, 'enabled', True),
            parameters=plugin_config.parameters,
            output_formats=plugin_config.output_format if isinstance(plugin_config.output_format, list) else [plugin_config.output_format],
            security=plugin_config.security,
            capabilities=getattr(plugin_config, 'capabilities', []),
            last_updated=getattr(plugin_config, 'last_updated', None)
        )
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message=f"Failed to retrieve plugin info for '{plugin_name}'",
            status_code=500,
            details={"error": str(e)}
        )


@router.get(
    "/plugins/{plugin_name}/health",
    response_model=Dict[str, Any],
    summary="Check Plugin Health",
    description="Check the health and availability of a specific plugin"
)
def check_plugin_health(plugin_name: str) -> Dict[str, Any]:
    """
    Check the health and availability of a specific plugin.
    
    Performs basic validation and dependency checks for the plugin.
    """
    if not plugin_registry:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Plugin registry not initialized",
            status_code=503
        )
    
    plugin_config = plugin_registry.get_plugin(plugin_name)
    if not plugin_config:
        raise APIError(
            code=ErrorCodes.RESOURCE_NOT_FOUND,
            message=f"Plugin '{plugin_name}' not found",
            status_code=404
        )
    
    health_status = {
        "plugin_name": plugin_name,
        "status": "healthy",
        "checks": {},
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Basic availability check
    health_status["checks"]["available"] = {"status": "ok", "message": "Plugin is available"}
    
    # Check if plugin is enabled
    enabled = getattr(plugin_config, 'enabled', True)
    health_status["checks"]["enabled"] = {
        "status": "ok" if enabled else "warning",
        "message": f"Plugin is {'enabled' if enabled else 'disabled'}"
    }
    
    # Check plugin file existence (if applicable)
    try:
        plugin_path = plugin_registry.plugins_dir / plugin_name
        if plugin_path.exists():
            health_status["checks"]["files"] = {"status": "ok", "message": "Plugin files found"}
        else:
            health_status["checks"]["files"] = {"status": "warning", "message": "Plugin directory not found"}
    except Exception as e:
        health_status["checks"]["files"] = {"status": "error", "message": str(e)}
    
    # Overall status
    has_errors = any(check["status"] == "error" for check in health_status["checks"].values())
    if has_errors:
        health_status["status"] = "unhealthy"
    elif not enabled:
        health_status["status"] = "disabled"
    
    return health_status


# ===== PLUGIN EXECUTION =====

@router.post(
    "/plugins/{plugin_name}/execute",
    response_model=PluginExecutionResponse,
    status_code=202,
    summary="Execute Plugin",
    description="Execute a plugin with specified parameters"
)
async def execute_plugin(
    plugin_name: str,
    request: PluginExecutionRequest,
    background_tasks: BackgroundTasks
) -> PluginExecutionResponse:
    """
    Execute a plugin with given parameters.
    
    Creates an asynchronous job and returns immediately with job details.
    Use the job_id to check status and retrieve results.
    """
    if not plugin_registry:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Plugin registry not initialized",
            status_code=503
        )
    
    # Validate plugin exists
    if not plugin_registry.get_plugin(plugin_name):
        raise APIError(
            code=ErrorCodes.RESOURCE_NOT_FOUND,
            message=f"Plugin '{plugin_name}' not found",
            status_code=404
        )
    
    # Override plugin name from URL parameter
    request.plugin_name = plugin_name
    
    try:
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        # Create job record
        job_record = {
            "job_id": job_id,
            "plugin_name": plugin_name,
            "status": "queued",
            "created_at": datetime.utcnow(),
            "started_at": None,
            "completed_at": None,
            "parameters": request.parameters,
            "output_format": request.output_format,
            "priority": request.priority,
            "timeout": request.timeout,
            "results": None,
            "error": None,
            "graph_entities": [],
            "search_documents": [],
            "tags": request.tags,
            "save_output": request.save_output,
            "notification_webhook": request.notification_webhook
        }
        
        running_jobs[job_id] = job_record
        
        # Add to execution queue
        if job_queue:
            await job_queue.put((job_id, plugin_name, request.parameters, request.output_format))
        else:
            raise APIError(
                code=ErrorCodes.SERVICE_UNAVAILABLE,
                message="Job queue not available",
                status_code=503
            )
        
        return PluginExecutionResponse(
            job_id=job_id,
            status="queued",
            plugin_name=plugin_name,
            tags=request.tags
        )
        
    except APIError:
        raise
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to queue plugin execution",
            status_code=500,
            details={"error": str(e)}
        )


@router.post(
    "/plugins/batch",
    response_model=BatchExecutionResponse,
    status_code=202,
    summary="Execute Plugin Batch",
    description="Execute multiple plugins in batch mode"
)
async def execute_plugin_batch(
    request: PluginBatchRequest,
    background_tasks: BackgroundTasks
) -> BatchExecutionResponse:
    """
    Execute multiple plugins in batch mode.
    
    Supports both sequential and parallel execution patterns.
    Returns batch ID for monitoring overall progress.
    """
    if not plugin_registry:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Plugin registry not initialized",
            status_code=503
        )
    
    try:
        batch_id = str(uuid.uuid4())
        job_ids = []
        
        # Validate all plugins exist before starting
        for execution in request.executions:
            if not plugin_registry.get_plugin(execution.plugin_name):
                raise APIError(
                    code=ErrorCodes.RESOURCE_NOT_FOUND,
                    message=f"Plugin '{execution.plugin_name}' not found",
                    status_code=404
                )
        
        # Create individual jobs
        for i, execution in enumerate(request.executions):
            job_id = f"{batch_id}-{i:03d}"
            job_ids.append(job_id)
            
            job_record = {
                "job_id": job_id,
                "batch_id": batch_id,
                "plugin_name": execution.plugin_name,
                "status": "queued",
                "created_at": datetime.utcnow(),
                "parameters": execution.parameters,
                "output_format": execution.output_format,
                "priority": execution.priority,
                "timeout": execution.timeout,
                "sequential": request.sequential,
                "stop_on_error": request.stop_on_error,
                "batch_index": i
            }
            
            running_jobs[job_id] = job_record
            
            # Queue the job
            if job_queue:
                await job_queue.put((job_id, execution.plugin_name, execution.parameters, execution.output_format))
        
        return BatchExecutionResponse(
            batch_id=batch_id,
            status="queued",
            total_jobs=len(request.executions),
            job_ids=job_ids,
            started_at=datetime.utcnow()
        )
        
    except APIError:
        raise
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to create batch execution",
            status_code=500,
            details={"error": str(e)}
        )


# ===== JOB MANAGEMENT =====

@router.get(
    "/jobs",
    response_model=PaginatedResponse[JobStatus],
    summary="List Jobs",
    description="Get a paginated list of plugin execution jobs"
)
def list_jobs(
    pagination: PaginationParams = Depends(),
    status: Optional[str] = Query(None, description="Filter by job status"),
    plugin_name: Optional[str] = Query(None, description="Filter by plugin name"),
    batch_id: Optional[str] = Query(None, description="Filter by batch ID")
) -> PaginatedResponse[JobStatus]:
    """
    List plugin execution jobs with filtering and pagination.
    
    Supports filtering by status, plugin name, and batch ID.
    """
    try:
        # Filter jobs
        filtered_jobs = []
        for job_id, job_data in running_jobs.items():
            # Apply filters
            if status and job_data.get("status") != status:
                continue
            if plugin_name and job_data.get("plugin_name") != plugin_name:
                continue
            if batch_id and job_data.get("batch_id") != batch_id:
                continue
            
            job_status = JobStatus(
                job_id=job_id,
                status=job_data["status"],
                plugin_name=job_data["plugin_name"],
                created_at=job_data["created_at"],
                started_at=job_data.get("started_at"),
                completed_at=job_data.get("completed_at"),
                error=job_data.get("error"),
                priority=job_data.get("priority", 1),
                timeout=job_data.get("timeout", 300),
                resource_usage=job_data.get("resource_usage")
            )
            filtered_jobs.append(job_status)
        
        # Sort by creation time (newest first)
        filtered_jobs.sort(key=lambda x: x.created_at, reverse=True)
        
        # Apply pagination
        total = len(filtered_jobs)
        start = pagination.offset
        end = start + pagination.limit
        jobs_page = filtered_jobs[start:end]
        
        return PaginatedResponse.create(jobs_page, total, pagination)
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve jobs",
            status_code=500,
            details={"error": str(e)}
        )


@router.get(
    "/jobs/{job_id}",
    response_model=PluginExecutionResponse,
    summary="Get Job Status",
    description="Get detailed status and results for a specific job"
)
def get_job_status(job_id: str) -> PluginExecutionResponse:
    """
    Get status and results of a plugin execution job.
    
    Returns comprehensive job information including results, output files,
    and any graph entities or search documents generated.
    """
    if job_id not in running_jobs:
        raise APIError(
            code=ErrorCodes.RESOURCE_NOT_FOUND,
            message=f"Job '{job_id}' not found",
            status_code=404
        )
    
    job = running_jobs[job_id]
    
    try:
        return PluginExecutionResponse(
            job_id=job_id,
            status=job["status"],
            plugin_name=job["plugin_name"],
            started_at=job.get("started_at"),
            completed_at=job.get("completed_at"),
            execution_time=job.get("execution_time"),
            results=job.get("results"),
            error=job.get("error"),
            output_files=job.get("output_files", []),
            graph_entities=job.get("graph_entities", []),
            search_documents=job.get("search_documents", []),
            tags=job.get("tags", []),
            metadata=job.get("metadata", {})
        )
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message=f"Failed to retrieve job status for '{job_id}'",
            status_code=500,
            details={"error": str(e)}
        )


@router.delete(
    "/jobs/{job_id}",
    response_model=Dict[str, Any],
    summary="Cancel Job",
    description="Cancel a queued or running job"
)
def cancel_job(job_id: str) -> Dict[str, Any]:
    """
    Cancel a queued or running job.
    
    Jobs that are already completed cannot be cancelled.
    """
    if job_id not in running_jobs:
        raise APIError(
            code=ErrorCodes.RESOURCE_NOT_FOUND,
            message=f"Job '{job_id}' not found",
            status_code=404
        )
    
    job = running_jobs[job_id]
    
    if job["status"] in ["completed", "failed"]:
        raise APIError(
            code=ErrorCodes.VALIDATION_ERROR,
            message=f"Cannot cancel job with status '{job['status']}'",
            status_code=400
        )
    
    try:
        # Mark as cancelled
        job["status"] = "cancelled"
        job["completed_at"] = datetime.utcnow()
        job["error"] = "Job cancelled by user"
        
        return {
            "message": "Job cancelled successfully",
            "job_id": job_id,
            "status": "cancelled",
            "cancelled_at": job["completed_at"].isoformat()
        }
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to cancel job",
            status_code=500,
            details={"error": str(e)}
        )


# ===== PLUGIN CATEGORIES & STATISTICS =====

@router.get(
    "/categories",
    response_model=List[PluginCategory],
    summary="Get Plugin Categories",
    description="Get available plugin categories with statistics"
)
def get_plugin_categories() -> List[PluginCategory]:
    """
    Get available plugin categories.
    
    Returns category information including plugin counts and risk level distribution.
    """
    if not plugin_registry:
        raise APIError(
            code=ErrorCodes.SERVICE_UNAVAILABLE,
            message="Plugin registry not initialized",
            status_code=503
        )
    
    try:
        categories = {}
        
        for plugin_name, plugin_config in plugin_registry.plugins.items():
            category = plugin_config.category
            if category not in categories:
                categories[category] = {
                    "name": category,
                    "plugins": [],
                    "risk_levels": set(),
                    "total_plugins": 0,
                    "enabled_plugins": 0
                }
            
            plugin_info = {
                "name": plugin_name,
                "description": plugin_config.description,
                "risk_level": plugin_config.risk_level,
                "enabled": getattr(plugin_config, 'enabled', True)
            }
            
            categories[category]["plugins"].append(plugin_info)
            categories[category]["risk_levels"].add(plugin_config.risk_level)
            categories[category]["total_plugins"] += 1
            if plugin_info["enabled"]:
                categories[category]["enabled_plugins"] += 1
        
        # Convert to response models
        category_list = []
        for category_data in categories.values():
            category_list.append(PluginCategory(
                name=category_data["name"],
                plugins=category_data["plugins"],
                risk_levels=list(category_data["risk_levels"]),
                total_plugins=category_data["total_plugins"],
                enabled_plugins=category_data["enabled_plugins"]
            ))
        
        return category_list
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve plugin categories",
            status_code=500,
            details={"error": str(e)}
        )


@router.get(
    "/statistics",
    response_model=PluginStatistics,
    summary="Get Plugin Statistics",
    description="Get comprehensive plugin execution statistics"
)
def get_statistics() -> PluginStatistics:
    """
    Get plugin execution statistics.
    
    Returns comprehensive statistics including job counts, success rates,
    and performance metrics.
    """
    try:
        # Basic counts
        total_plugins = len(plugin_registry.plugins) if plugin_registry else 0
        enabled_plugins = sum(1 for p in plugin_registry.plugins.values() 
                            if getattr(p, 'enabled', True)) if plugin_registry else 0
        total_jobs = len(running_jobs)
        
        # Job status counts
        job_status_counts = {}
        plugin_usage_counts = {}
        execution_times = []
        
        for job in running_jobs.values():
            status = job["status"]
            job_status_counts[status] = job_status_counts.get(status, 0) + 1
            
            # Count plugin usage
            plugin_name = job["plugin_name"]
            plugin_usage_counts[plugin_name] = plugin_usage_counts.get(plugin_name, 0) + 1
            
            # Collect execution times
            if job.get("execution_time"):
                execution_times.append(job["execution_time"])
        
        # Calculate success rate
        completed_jobs = job_status_counts.get("completed", 0)
        failed_jobs = job_status_counts.get("failed", 0)
        total_finished = completed_jobs + failed_jobs
        success_rate = (completed_jobs / total_finished * 100) if total_finished > 0 else 0.0
        
        # Calculate average execution time
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0.0
        
        return PluginStatistics(
            total_plugins=total_plugins,
            enabled_plugins=enabled_plugins,
            total_jobs=total_jobs,
            job_status_counts=job_status_counts,
            plugin_usage_counts=plugin_usage_counts,
            average_execution_time=avg_execution_time,
            success_rate=success_rate,
            docker_enabled=True,  # This should come from config
            system_resources={}  # Could be expanded with actual system metrics
        )
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve statistics",
            status_code=500,
            details={"error": str(e)}
        )


@router.get(
    "/capabilities",
    response_model=PluginCapabilities,
    summary="Get System Capabilities",
    description="Get plugin runner system capabilities and configuration"
)
def get_capabilities() -> PluginCapabilities:
    """
    Get plugin runner system capabilities.
    
    Returns information about system limits, supported features,
    and available plugin categories.
    """
    try:
        categories = set()
        risk_levels = set()
        
        if plugin_registry:
            for plugin_config in plugin_registry.plugins.values():
                categories.add(plugin_config.category)
                risk_levels.add(plugin_config.risk_level)
        
        return PluginCapabilities(
            max_concurrent_jobs=5,  # From config
            max_execution_time=3600,  # From config
            supported_formats=["json", "yaml", "xml", "text"],
            docker_available=True,  # This should come from actual Docker check
            security_sandbox=True,
            categories=list(categories),
            risk_levels=list(risk_levels),
            features={
                "batch_execution": True,
                "priority_queuing": True,
                "output_file_storage": True,
                "webhook_notifications": True,
                "graph_entity_extraction": True,
                "search_document_generation": True,
                "resource_monitoring": True,
                "audit_logging": True
            }
        )
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve system capabilities",
            status_code=500,
            details={"error": str(e)}
        )


@router.get(
    "/health",
    response_model=PluginHealthStatus,
    summary="Get Plugin System Health",
    description="Get comprehensive health status of the plugin system"
)
def get_plugin_system_health() -> PluginHealthStatus:
    """
    Get comprehensive health status of the plugin system.
    
    Returns detailed health information including registry status,
    Docker availability, and current system load.
    """
    try:
        # Check plugin registry
        registry_loaded = plugin_registry is not None
        total_plugins = len(plugin_registry.plugins) if registry_loaded else 0
        
        # Check Docker (this would need actual Docker client)
        docker_available = True  # Placeholder
        
        # Count active jobs
        active_jobs = sum(1 for job in running_jobs.values() if job["status"] == "running")
        queued_jobs = sum(1 for job in running_jobs.values() if job["status"] == "queued")
        
        # Find last execution
        last_execution = None
        for job in running_jobs.values():
            if job.get("completed_at"):
                if last_execution is None or job["completed_at"] > last_execution:
                    last_execution = job["completed_at"]
        
        return PluginHealthStatus(
            plugin_registry_loaded=registry_loaded,
            docker_available=docker_available,
            total_plugins=total_plugins,
            active_jobs=active_jobs,
            queue_length=queued_jobs,
            resource_usage={
                "memory_usage": "N/A",  # Could be expanded
                "cpu_usage": "N/A",
                "disk_usage": "N/A"
            },
            last_plugin_execution=last_execution
        )
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve plugin system health",
            status_code=500,
            details={"error": str(e)}
        )
