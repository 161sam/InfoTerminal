"""
Ops Controller v1 router for service orchestration and security management.
Provides stack management, security operations, and performance monitoring.
"""

import json
import os
import shlex
import subprocess
import threading
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
import yaml
import psutil

from fastapi import APIRouter, HTTPException, Request, Query, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Import shared standards
import sys
SERVICE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SERVICE_DIR.parent.parent
for p in (SERVICE_DIR, REPO_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

try:
    from _shared.api_standards.error_schemas import raise_http_error
    from _shared.api_standards.pagination import PaginatedResponse
    from _shared.audit import audit_log
except ImportError:
    # Fallback for legacy compatibility
    def raise_http_error(code: str, message: str, details: Optional[Dict] = None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                          detail={"error": {"code": code, "message": message, "details": details or {}}})
    
    class PaginatedResponse(BaseModel):
        items: list
        total: int
        page: int = 1
        size: int = 10
    
    def audit_log(action: str, user_id: str = "", tenant_id: str = "", **extra):
        # Fallback audit logging
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"AUDIT: {action} - user:{user_id} tenant:{tenant_id} extra:{extra}")

# Import models
from ..models import (
    StackListResponse,
    StackStatusResponse,
    StackOperationResponse,
    ScaleRequest,
    ScaleResponse,
    StartIncognitoRequest,
    IncognitoSessionResponse,
    IncognitoStatusResponse,
    ContainersStatusResponse,
    WipeDataRequest,
    WipeResponse,
    DataScanResponse,
    ComprehensiveHealthResponse,
    SystemPerformanceResponse,
    ContainerOperationResponse,
    EmergencyShutdownResponse
)

# Import security manager
try:
    from ..security.session_manager import SessionManager
    HAS_SESSION_MANAGER = True
except ImportError:
    HAS_SESSION_MANAGER = False

router = APIRouter(tags=["Ops Controller"], prefix="/v1")

# Configuration
ENABLED = os.getenv("IT_OPS_ENABLE", "0") == "1"
MODE = os.getenv("IT_OPS_MODE", "docker")
COMPOSE = os.getenv("IT_OPS_COMPOSE_BIN", "docker compose")
STACKS_FILE = Path(os.getenv("IT_OPS_STACKS_FILE", "infra/ops/stacks.yaml"))
LOCK_TIMEOUT = int(os.getenv("IT_OPS_LOCK_TIMEOUT_SEC", "120"))
TAIL = os.getenv("IT_OPS_LOG_TAIL_LINES", "300")

# Global state
_lock = threading.Lock()
_lock_at = 0.0
security_manager: Optional[SessionManager] = None


def _require_enabled():
    """Check if ops is enabled."""
    if not ENABLED:
        raise_http_error("OPS_DISABLED", "Ops is disabled. Set IT_OPS_ENABLE=1")
    if MODE != "docker":
        raise_http_error("UNSUPPORTED_MODE", f"Mode {MODE} not supported yet")


def _require_rbac(req: Request):
    """Check RBAC permissions."""
    roles = (req.headers.get("X-Roles") or req.headers.get("x-roles") or "").split(",")
    if not any(r.strip() in ("admin", "ops") for r in roles):
        raise_http_error("RBAC_DENIED", "RBAC: admin|ops role required")


def _require_security_manager():
    """Check if security manager is available."""
    if not security_manager:
        raise_http_error("SECURITY_MANAGER_UNAVAILABLE", "Security manager not available")


def _stacks() -> Dict[str, Dict]:
    """Load stacks configuration."""
    if not STACKS_FILE.exists():
        return {"stacks": {}}
    try:
        data = yaml.safe_load(STACKS_FILE.read_text(encoding="utf-8")) or {}
        return {"stacks": {k: v for k, v in (data.get("stacks") or {}).items()}}
    except Exception as e:
        raise_http_error("STACKS_CONFIG_ERROR", f"Failed to load stacks config: {str(e)}")


def _compose_cmd(files: List[str], args: List[str]) -> List[str]:
    """Build docker compose command."""
    cmd = []
    for f in files:
        cmd += shlex.split(f"-f {f}")
    return shlex.split(COMPOSE) + cmd + args


def _run(files: List[str], args: List[str], timeout: int = LOCK_TIMEOUT) -> subprocess.CompletedProcess:
    """Run docker compose command."""
    env = os.environ.copy()
    try:
        return subprocess.run(
            _compose_cmd(files, args), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            timeout=timeout, 
            env=env,
            check=False
        )
    except subprocess.TimeoutExpired:
        raise_http_error("OPERATION_TIMEOUT", f"Operation timed out after {timeout} seconds")
    except Exception as e:
        raise_http_error("COMMAND_EXECUTION_FAILED", f"Command execution failed: {str(e)}")


def _lock_guard():
    """Acquire operation lock."""
    global _lock_at
    ok = _lock.acquire(timeout=LOCK_TIMEOUT)
    if not ok:
        raise_http_error("OPS_BUSY", "Ops busy, try again later")
    _lock_at = time.time()


def _unlock():
    """Release operation lock."""
    if _lock.locked():
        _lock.release()


def _audit(action: str, req: Request, **extra):
    """Audit log helper."""
    audit_log(
        action, 
        req.headers.get("X-User-Id", ""), 
        req.headers.get("X-Tenant-Id", ""), 
        **extra
    )


# ============================================================================
# OPS MANAGEMENT ENDPOINTS
# ============================================================================

@router.get("/stacks", response_model=StackListResponse)
def list_stacks(request: Request):
    """
    List available service stacks.
    
    Returns configuration for all available Docker Compose stacks.
    """
    _require_enabled()
    _require_rbac(request)
    
    try:
        stacks_data = _stacks()
        return StackListResponse(stacks=stacks_data["stacks"])
    except Exception as e:
        raise_http_error("LIST_STACKS_FAILED", f"Failed to list stacks: {str(e)}")


@router.get("/stacks/{name}/status", response_model=StackStatusResponse)
def get_stack_status(name: str, request: Request):
    """
    Get status of a specific stack.
    
    Returns current status of all services in the stack.
    """
    _require_enabled()
    _require_rbac(request)
    
    try:
        stacks = _stacks()["stacks"]
        if name not in stacks:
            raise_http_error("STACK_NOT_FOUND", f"Stack '{name}' not found")
        
        files = stacks[name]["files"]
        p = _run(files, ["ps", "--format", "json"])
        
        if p.returncode != 0:
            raise_http_error("STACK_STATUS_FAILED", f"Failed to get stack status: {p.stderr.decode()}")
        
        lines = [json.loads(l) for l in p.stdout.decode().splitlines() if l.strip()]
        return StackStatusResponse(stack=name, services=lines)
        
    except HTTPException:
        raise
    except Exception as e:
        raise_http_error("STACK_STATUS_ERROR", f"Stack status check failed: {str(e)}")


@router.post("/stacks/{name}/up", response_model=StackOperationResponse)
def start_stack(name: str, request: Request):
    """
    Start a service stack.
    
    Brings up all services in the specified stack.
    """
    _require_enabled()
    _require_rbac(request)
    
    try:
        stacks = _stacks()["stacks"]
        if name not in stacks:
            raise_http_error("STACK_NOT_FOUND", f"Stack '{name}' not found")
        
        files = stacks[name]["files"]
        _lock_guard()
        
        try:
            p = _run(files, ["up", "-d"])
            if p.returncode != 0:
                raise_http_error("STACK_UP_FAILED", f"Failed to start stack: {p.stderr.decode()}")
            
            _audit("stack_up", request, stack=name)
            return StackOperationResponse(ok=True, stack=name, message="Stack started successfully")
            
        finally:
            _unlock()
            
    except HTTPException:
        raise
    except Exception as e:
        raise_http_error("STACK_START_ERROR", f"Failed to start stack: {str(e)}")


@router.post("/stacks/{name}/down", response_model=StackOperationResponse)
def stop_stack(name: str, request: Request):
    """
    Stop a service stack.
    
    Brings down all services in the specified stack.
    """
    _require_enabled()
    _require_rbac(request)
    
    try:
        stacks = _stacks()["stacks"]
        if name not in stacks:
            raise_http_error("STACK_NOT_FOUND", f"Stack '{name}' not found")
        
        files = stacks[name]["files"]
        _lock_guard()
        
        try:
            p = _run(files, ["down"])
            if p.returncode != 0:
                raise_http_error("STACK_DOWN_FAILED", f"Failed to stop stack: {p.stderr.decode()}")
            
            _audit("stack_down", request, stack=name)
            return StackOperationResponse(ok=True, stack=name, message="Stack stopped successfully")
            
        finally:
            _unlock()
            
    except HTTPException:
        raise
    except Exception as e:
        raise_http_error("STACK_STOP_ERROR", f"Failed to stop stack: {str(e)}")


@router.post("/stacks/{name}/restart", response_model=StackOperationResponse)
def restart_stack(name: str, request: Request):
    """
    Restart a service stack.
    
    Restarts all services in the specified stack.
    """
    _require_enabled()
    _require_rbac(request)
    
    try:
        stacks = _stacks()["stacks"]
        if name not in stacks:
            raise_http_error("STACK_NOT_FOUND", f"Stack '{name}' not found")
        
        files = stacks[name]["files"]
        _lock_guard()
        
        try:
            p = _run(files, ["up", "-d", "--remove-orphans"])
            if p.returncode != 0:
                raise_http_error("STACK_RESTART_FAILED", f"Failed to restart stack: {p.stderr.decode()}")
            
            _audit("stack_restart", request, stack=name)
            return StackOperationResponse(ok=True, stack=name, message="Stack restarted successfully")
            
        finally:
            _unlock()
            
    except HTTPException:
        raise
    except Exception as e:
        raise_http_error("STACK_RESTART_ERROR", f"Failed to restart stack: {str(e)}")


@router.post("/stacks/{name}/scale", response_model=ScaleResponse)
def scale_service(name: str, scale_req: ScaleRequest, request: Request):
    """
    Scale a service within a stack.
    
    Changes the number of replicas for a specific service.
    """
    _require_enabled()
    _require_rbac(request)
    
    if scale_req.replicas < 0 or scale_req.replicas > 10:
        raise_http_error("INVALID_REPLICA_COUNT", "Replicas must be between 0 and 10")
    
    try:
        stacks = _stacks()["stacks"]
        if name not in stacks:
            raise_http_error("STACK_NOT_FOUND", f"Stack '{name}' not found")
        
        files = stacks[name]["files"]
        _lock_guard()
        
        try:
            p = _run(files, ["up", "-d", "--scale", f"{scale_req.service}={scale_req.replicas}"])
            if p.returncode != 0:
                raise_http_error("SCALE_FAILED", f"Failed to scale service: {p.stderr.decode()}")
            
            _audit("stack_scale", request, stack=name, service=scale_req.service, replicas=scale_req.replicas)
            return ScaleResponse(
                ok=True, 
                stack=name, 
                service=scale_req.service, 
                replicas=scale_req.replicas
            )
            
        finally:
            _unlock()
            
    except HTTPException:
        raise
    except Exception as e:
        raise_http_error("SCALE_ERROR", f"Failed to scale service: {str(e)}")


@router.get("/stacks/{name}/logs")
def get_stack_logs(
    name: str,
    request: Request,
    service: Optional[str] = Query(None, description="Specific service to get logs for"),
    tail: Optional[int] = Query(None, description="Number of lines to tail")
):
    """
    Stream logs from a service stack.
    
    Returns real-time log stream from the specified stack.
    """
    _require_enabled()
    _require_rbac(request)
    
    try:
        stacks = _stacks()["stacks"]
        if name not in stacks:
            raise_http_error("STACK_NOT_FOUND", f"Stack '{name}' not found")
        
        files = stacks[name]["files"]
        N = str(tail or TAIL)
        _audit("stack_logs", request, stack=name, service=service)

        def stream():
            args = ["logs", "-f", "--tail", N]
            if service:
                args.append(service)
            
            try:
                with subprocess.Popen(
                    _compose_cmd(files, args), 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT
                ) as proc:
                    try:
                        for line in iter(proc.stdout.readline, b''):
                            yield line
                    except GeneratorExit:
                        proc.terminate()
            except Exception as e:
                yield f"Error streaming logs: {str(e)}\\n".encode()

        return StreamingResponse(stream(), media_type="text/plain")
        
    except HTTPException:
        raise
    except Exception as e:
        raise_http_error("LOG_STREAM_ERROR", f"Failed to stream logs: {str(e)}")


# ============================================================================
# SECURITY ENDPOINTS  
# ============================================================================

@router.get("/security/incognito/status", response_model=IncognitoStatusResponse)
async def get_incognito_status(request: Request):
    """
    Get current incognito mode status.
    
    Returns information about active incognito sessions.
    """
    _require_enabled()
    _require_rbac(request)
    _require_security_manager()
    
    try:
        status = await security_manager.get_security_status()
        
        # Extract incognito-specific status
        incognito_status = IncognitoStatusResponse(
            active=status["active_sessions"] > 0,
            sessionId=None,
            timeRemaining=None
        )
        
        # If there are active sessions, get the first one
        if status["sessions"]:
            session_id, session_data = next(iter(status["sessions"].items()))
            incognito_status.sessionId = session_id
            if session_data["auto_wipe_at"] > 0:
                incognito_status.timeRemaining = max(0, session_data["auto_wipe_at"] - time.time() * 1000)
        
        return incognito_status
        
    except Exception as e:
        raise_http_error("INCOGNITO_STATUS_FAILED", f"Failed to get incognito status: {str(e)}")


@router.post("/security/incognito/start", response_model=IncognitoSessionResponse)
async def start_incognito_session(request_data: StartIncognitoRequest, request: Request):
    """
    Start a new incognito session.
    
    Creates an isolated environment with optional auto-wipe.
    """
    _require_enabled()
    _require_rbac(request)
    _require_security_manager()
    
    try:
        session = await security_manager.start_incognito_session(
            session_id=request_data.sessionId,
            auto_wipe_minutes=request_data.autoWipeMinutes,
            memory_only_mode=request_data.memoryOnlyMode,
            isolated_containers=request_data.isolatedContainers
        )
        
        _audit("incognito_start", request, session_id=request_data.sessionId)
        
        return IncognitoSessionResponse(
            sessionId=session.id,
            containerCount=session.container_count,
            memoryOnlyMode=session.memory_only_mode
        )
        
    except Exception as e:
        raise_http_error("INCOGNITO_START_FAILED", f"Failed to start incognito session: {str(e)}")


@router.post("/security/incognito/{session_id}/stop", response_model=WipeResponse)
async def stop_incognito_session(session_id: str, request: Request):
    """
    Stop an incognito session.
    
    Terminates the session and cleans up resources.
    """
    _require_enabled()
    _require_rbac(request)
    _require_security_manager()
    
    try:
        success = await security_manager.stop_incognito_session(session_id)
        
        if not success:
            raise_http_error("SESSION_NOT_FOUND", "Session not found or already stopped")
        
        _audit("incognito_stop", request, session_id=session_id)
        
        return WipeResponse(success=True, sessionId=session_id, message="Session stopped successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        raise_http_error("INCOGNITO_STOP_FAILED", f"Failed to stop incognito session: {str(e)}")


# ============================================================================
# PERFORMANCE MONITORING ENDPOINTS
# ============================================================================

@router.get("/health/comprehensive", response_model=ComprehensiveHealthResponse)
async def comprehensive_health_check(request: Request):
    """
    Comprehensive health check with performance metrics.
    
    Returns detailed system health and performance information.
    """
    _require_enabled()
    
    try:
        start_time = time.time()
        
        # System metrics
        from ..models.requests import SystemMetrics, RedisStatus
        system_metrics = SystemMetrics(
            cpu_usage_percent=psutil.cpu_percent(interval=1),
            memory_usage_percent=psutil.virtual_memory().percent,
            disk_usage_percent=psutil.disk_usage('/').percent,
            uptime_seconds=time.time() - psutil.boot_time()
        )
        
        # Docker service status
        service_status = {}
        try:
            import docker
            client = docker.from_env()
            containers = client.containers.list()
            
            for container in containers:
                name = container.name
                status = container.status
                service_status[name] = {
                    "status": status,
                    "healthy": status == "running",
                    "created_at": container.attrs["Created"],
                    "restart_count": container.attrs["RestartCount"]
                }
        except Exception as e:
            service_status["error"] = str(e)
        
        # Redis connection test
        redis_status = RedisStatus(available=False)
        try:
            import redis
            r = redis.Redis(host='redis', port=6379, decode_responses=True)
            r.ping()
            redis_info = r.info()
            
            keyspace_hits = redis_info.get("keyspace_hits", 0)
            keyspace_misses = redis_info.get("keyspace_misses", 0)
            hit_rate = None
            if keyspace_hits + keyspace_misses > 0:
                hit_rate = keyspace_hits / (keyspace_hits + keyspace_misses)
            
            redis_status = RedisStatus(
                available=True,
                connected_clients=redis_info.get("connected_clients", 0),
                used_memory_human=redis_info.get("used_memory_human", "N/A"),
                keyspace_hits=keyspace_hits,
                keyspace_misses=keyspace_misses,
                hit_rate=hit_rate
            )
        except Exception:
            pass
        
        response_time = time.time() - start_time
        
        health_data = ComprehensiveHealthResponse(
            status="healthy",
            timestamp=time.time(),
            response_time_ms=response_time * 1000,
            system_metrics=system_metrics,
            service_status=service_status,
            redis_status=redis_status,
            security_manager_active=security_manager is not None
        )
        
        _audit("health_check_comprehensive", request, response_time_ms=response_time * 1000)
        
        return health_data
        
    except Exception as e:
        raise_http_error("HEALTH_CHECK_FAILED", f"Health check failed: {str(e)}")


@router.get("/performance", response_model=SystemPerformanceResponse)
async def get_system_performance(request: Request):
    """
    Get detailed system performance metrics.
    
    Returns comprehensive performance data for monitoring.
    """
    _require_enabled()
    _require_rbac(request)
    
    try:
        from ..models.requests import CpuMetrics, MemoryMetrics, DiskMetrics, NetworkMetrics
        
        # CPU metrics
        cpu_metrics = CpuMetrics(
            usage_percent=psutil.cpu_percent(interval=1),
            load_avg=psutil.getloadavg() if hasattr(psutil, 'getloadavg') else [0, 0, 0],
            core_count=psutil.cpu_count()
        )
        
        # Memory metrics
        memory = psutil.virtual_memory()
        memory_metrics = MemoryMetrics(
            total_gb=round(memory.total / (1024**3), 2),
            used_gb=round(memory.used / (1024**3), 2),
            available_gb=round(memory.available / (1024**3), 2),
            usage_percent=memory.percent
        )
        
        # Disk metrics
        disk = psutil.disk_usage('/')
        disk_metrics = DiskMetrics(
            total_gb=round(disk.total / (1024**3), 2),
            used_gb=round(disk.used / (1024**3), 2),
            free_gb=round(disk.free / (1024**3), 2),
            usage_percent=round((disk.used / disk.total) * 100, 2)
        )
        
        # Network metrics
        try:
            net_io = psutil.net_io_counters()
            network_metrics = NetworkMetrics(
                bytes_sent=net_io.bytes_sent,
                bytes_recv=net_io.bytes_recv,
                packets_sent=net_io.packets_sent,
                packets_recv=net_io.packets_recv
            )
        except Exception:
            network_metrics = NetworkMetrics(
                bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0
            )
        
        performance_data = SystemPerformanceResponse(
            timestamp=time.time(),
            cpu=cpu_metrics,
            memory=memory_metrics,
            disk=disk_metrics,
            network=network_metrics,
            uptime_hours=round((time.time() - psutil.boot_time()) / 3600, 2)
        )
        
        return performance_data
        
    except Exception as e:
        raise_http_error("PERFORMANCE_METRICS_FAILED", f"Failed to get performance metrics: {str(e)}")


# Initialize security manager on module load
async def initialize_security_manager():
    """Initialize the security manager."""
    global security_manager
    if HAS_SESSION_MANAGER and ENABLED:
        try:
            security_manager = SessionManager()
            await security_manager.initialize()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to initialize security manager: {e}")
