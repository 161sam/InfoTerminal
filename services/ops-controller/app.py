import os, subprocess, shlex, time, json, threading, asyncio
from pathlib import Path
from typing import List, Dict, Optional, Any
import yaml
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from _shared.audit import audit_log

# Import security components
from security.session_manager import SessionManager

APP = FastAPI(title="Ops Controller", version="0.2.0")

ENABLED = os.getenv("IT_OPS_ENABLE","0") == "1"
MODE = os.getenv("IT_OPS_MODE","docker")
COMPOSE = os.getenv("IT_OPS_COMPOSE_BIN","docker compose")
STACKS_FILE = Path(os.getenv("IT_OPS_STACKS_FILE","infra/ops/stacks.yaml"))
LOCK_TIMEOUT = int(os.getenv("IT_OPS_LOCK_TIMEOUT_SEC","120"))
TAIL = os.getenv("IT_OPS_LOG_TAIL_LINES","300")
SOCKET = os.getenv("IT_DOCKER_SOCKET","/var/run/docker.sock")

_lock = threading.Lock()
_lock_at = 0.0

# Global security session manager
security_manager: Optional[SessionManager] = None

# Pydantic models for security endpoints
class StartIncognitoRequest(BaseModel):
    sessionId: str
    autoWipeMinutes: Optional[int] = None
    memoryOnlyMode: bool = True
    isolatedContainers: bool = True

class WipeDataRequest(BaseModel):
    sessionId: str
    secure: bool = True
    overwritePasses: int = 3

@APP.on_event("startup")
async def startup_event():
    """Initialize security manager on startup."""
    global security_manager
    
    if ENABLED:
        security_manager = SessionManager()
        await security_manager.initialize()

@APP.on_event("shutdown")
async def shutdown_event():
    """Cleanup security manager on shutdown."""
    global security_manager
    
    if security_manager:
        await security_manager.cleanup()

def _require_enabled():
    if not ENABLED:
        raise HTTPException(403, "Ops is disabled. Set IT_OPS_ENABLE=1")
    if MODE != "docker":
        raise HTTPException(400, f"Mode {MODE} not supported yet")

def _require_rbac(req: Request):
    roles = (req.headers.get("X-Roles") or req.headers.get("x-roles") or "").split(",")
    scope = req.headers.get("X-Scope","")
    if not any(r.strip() in ("admin","ops") for r in roles):
        raise HTTPException(403, "RBAC: admin|ops required")

def _require_security_manager():
    if not security_manager:
        raise HTTPException(503, "Security manager not available")

def _stacks() -> Dict[str, Dict]:
    if not STACKS_FILE.exists():
        return {"stacks": {}}
    data = yaml.safe_load(STACKS_FILE.read_text(encoding="utf-8")) or {}
    return { "stacks": {k:v for k,v in (data.get("stacks") or {}).items()} }

def _compose_cmd(files: List[str], args: List[str]) -> List[str]:
    cmd = []
    for f in files:
        cmd += shlex.split(f"-f {f}")
    return shlex.split(COMPOSE) + cmd + args

def _run(files: List[str], args: List[str], timeout: int=LOCK_TIMEOUT) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    return subprocess.run(_compose_cmd(files,args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, env=env)

def _lock_guard():
    global _lock_at
    ok = _lock.acquire(timeout=LOCK_TIMEOUT)
    if not ok:
        raise HTTPException(423, "Ops busy, try again later")
    _lock_at = time.time()

def _unlock():
    if _lock.locked(): _lock.release()

def _audit(action: str, req: Request, **extra):
    audit_log(action, req.headers.get("X-User-Id", ""), req.headers.get("X-Tenant-Id", ""), **extra)

# ============================================================================
# EXISTING OPS ENDPOINTS
# ============================================================================

@APP.get("/ops/stacks")
def list_stacks(request: Request):
    _require_enabled(); _require_rbac(request)
    return _stacks()

@APP.get("/ops/stacks/{name}/status")
def stack_status(name: str, request: Request):
    _require_enabled(); _require_rbac(request)
    stacks = _stacks()["stacks"]
    if name not in stacks: raise HTTPException(404,"unknown stack")
    files = stacks[name]["files"]
    p = _run(files, ["ps", "--format", "json"])
    if p.returncode != 0:
        raise HTTPException(500, p.stderr.decode())
    lines = [json.loads(l) for l in p.stdout.decode().splitlines() if l.strip()]
    return {"stack": name, "services": lines}

@APP.post("/ops/stacks/{name}/up")
def stack_up(name: str, request: Request):
    _require_enabled(); _require_rbac(request)
    stacks = _stacks()["stacks"]
    if name not in stacks: raise HTTPException(404,"unknown stack")
    files = stacks[name]["files"]
    _lock_guard()
    try:
        p = _run(files, ["up","-d"])
        if p.returncode != 0: raise HTTPException(500, p.stderr.decode())
        _audit("stack_up", request, stack=name)
        return {"ok": True, "stack": name}
    finally: _unlock()

@APP.post("/ops/stacks/{name}/down")
def stack_down(name: str, request: Request):
    _require_enabled(); _require_rbac(request)
    stacks = _stacks()["stacks"]
    if name not in stacks: raise HTTPException(404,"unknown stack")
    files = stacks[name]["files"]
    _lock_guard()
    try:
        p = _run(files, ["down"])
        if p.returncode != 0: raise HTTPException(500, p.stderr.decode())
        _audit("stack_down", request, stack=name)
        return {"ok": True, "stack": name}
    finally: _unlock()

@APP.post("/ops/stacks/{name}/restart")
def stack_restart(name: str, request: Request):
    _require_enabled(); _require_rbac(request)
    stacks = _stacks()["stacks"]
    if name not in stacks: raise HTTPException(404,"unknown stack")
    files = stacks[name]["files"]
    _lock_guard()
    try:
        p = _run(files, ["up","-d","--remove-orphans"])
        if p.returncode != 0: raise HTTPException(500, p.stderr.decode())
        _audit("stack_restart", request, stack=name)
        return {"ok": True, "stack": name}
    finally: _unlock()

@APP.post("/ops/stacks/{name}/scale")
def stack_scale(name: str, service: str, replicas: int, request: Request):
    _require_enabled(); _require_rbac(request)
    if replicas < 0 or replicas > 10:
        raise HTTPException(400, "replicas out of range (0..10)")
    stacks = _stacks()["stacks"]
    if name not in stacks: raise HTTPException(404,"unknown stack")
    files = stacks[name]["files"]
    _lock_guard()
    try:
        p = _run(files, ["up","-d","--scale", f"{service}={replicas}"])
        if p.returncode != 0: raise HTTPException(500, p.stderr.decode())
        _audit("stack_scale", request, stack=name, service=service, replicas=replicas)
        return {"ok": True, "stack": name, "service": service, "replicas": replicas}
    finally: _unlock()

@APP.get("/ops/stacks/{name}/logs")
def stack_logs(name: str, service: Optional[str]=None, tail: Optional[int]=None, request: Request=None):
    _require_enabled(); _require_rbac(request)
    stacks = _stacks()["stacks"]
    if name not in stacks: raise HTTPException(404,"unknown stack")
    files = stacks[name]["files"]
    N = str(tail or TAIL)
    _audit("stack_logs", request, stack=name, service=service)

    def stream():
        args = ["logs","-f","--tail", N]
        if service: args.append(service)
        with subprocess.Popen(_compose_cmd(files, args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
            try:
                for line in iter(proc.stdout.readline, b''):
                    yield line
            except GeneratorExit:
                proc.terminate()
    return StreamingResponse(stream(), media_type="text/plain")

# ============================================================================
# SECURITY ENDPOINTS (NEW v0.2.0)
# ============================================================================

@APP.get("/security/incognito/status")
async def get_incognito_status(request: Request):
    """Get current incognito mode status."""
    _require_enabled(); _require_rbac(request)
    _require_security_manager()
    
    status = await security_manager.get_security_status()
    
    # Extract incognito-specific status
    incognito_status = {
        "active": status["active_sessions"] > 0,
        "sessionId": None,
        "timeRemaining": None
    }
    
    # If there are active sessions, get the first one for demo
    if status["sessions"]:
        session_id, session_data = next(iter(status["sessions"].items()))
        incognito_status["sessionId"] = session_id
        if session_data["auto_wipe_at"] > 0:
            incognito_status["timeRemaining"] = max(0, session_data["auto_wipe_at"] - time.time() * 1000)
    
    return incognito_status

@APP.get("/security/containers/status")
async def get_containers_status(request: Request):
    """Get container security status."""
    _require_enabled(); _require_rbac(request)
    _require_security_manager()
    
    status = await security_manager.get_security_status()
    
    return {
        "ephemeralContainers": status["ephemeral_containers"],
        "memoryOnlyMode": status["memory_only_mode"],
        "autoWipeEnabled": status["auto_wipe_enabled"]
    }

@APP.post("/security/incognito/start")
async def start_incognito_session(request_data: StartIncognitoRequest, request: Request):
    """Start a new incognito session."""
    _require_enabled(); _require_rbac(request)
    _require_security_manager()
    
    try:
        session = await security_manager.start_incognito_session(
            session_id=request_data.sessionId,
            auto_wipe_minutes=request_data.autoWipeMinutes,
            memory_only_mode=request_data.memoryOnlyMode,
            isolated_containers=request_data.isolatedContainers
        )
        
        _audit("incognito_start", request, session_id=request_data.sessionId)
        
        return {
            "sessionId": session.id,
            "containerCount": session.container_count,
            "memoryOnlyMode": session.memory_only_mode
        }
        
    except Exception as e:
        raise HTTPException(500, f"Failed to start incognito session: {str(e)}")

@APP.post("/security/incognito/{session_id}/stop")
async def stop_incognito_session(session_id: str, request: Request):
    """Stop an incognito session."""
    _require_enabled(); _require_rbac(request)
    _require_security_manager()
    
    try:
        success = await security_manager.stop_incognito_session(session_id)
        
        if not success:
            raise HTTPException(404, "Session not found or already stopped")
        
        _audit("incognito_stop", request, session_id=session_id)
        
        return {"success": True, "sessionId": session_id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Failed to stop incognito session: {str(e)}")

@APP.post("/security/incognito/{session_id}/wipe")
async def wipe_incognito_session(session_id: str, wipe_data: WipeDataRequest, request: Request):
    """Wipe all data for an incognito session."""
    _require_enabled(); _require_rbac(request)
    _require_security_manager()
    
    try:
        success = await security_manager.wipe_incognito_session(
            session_id=session_id,
            secure=wipe_data.secure
        )
        
        if not success:
            raise HTTPException(404, "Session not found")
        
        _audit("incognito_wipe", request, session_id=session_id, secure=wipe_data.secure)
        
        return {"success": True, "sessionId": session_id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Failed to wipe incognito session: {str(e)}")

@APP.get("/security/incognito/{session_id}/containers")
async def get_session_containers(session_id: str, request: Request):
    """Get containers for a specific incognito session."""
    _require_enabled(); _require_rbac(request)
    _require_security_manager()
    
    try:
        containers = await security_manager.get_session_containers(session_id)
        return {"containers": containers}
        
    except Exception as e:
        # Return empty list on error to avoid breaking the UI
        return {"containers": []}

@APP.get("/security/incognito/{session_id}/data-scan")
async def scan_session_data(session_id: str, request: Request):
    """Scan data categories for a session."""
    _require_enabled(); _require_rbac(request)
    _require_security_manager()
    
    try:
        categories = await security_manager.get_data_categories(session_id)
        return {"categories": categories}
        
    except Exception as e:
        raise HTTPException(500, f"Failed to scan data: {str(e)}")

@APP.post("/security/data-wipe/{category_id}")
async def wipe_data_category(category_id: str, wipe_data: WipeDataRequest, request: Request):
    """Wipe a specific data category."""
    _require_enabled(); _require_rbac(request)
    _require_security_manager()
    
    try:
        progress = await security_manager.wipe_data_category(
            category_id=category_id,
            session_id=wipe_data.sessionId,
            secure=wipe_data.secure
        )
        
        _audit("data_wipe", request, category_id=category_id, session_id=wipe_data.sessionId)
        
        return progress
        
    except Exception as e:
        raise HTTPException(500, f"Failed to wipe data category: {str(e)}")

@APP.post("/security/containers/{container_id}/restart")
async def restart_container(container_id: str, request: Request):
    """Restart a specific container."""
    _require_enabled(); _require_rbac(request)
    
    try:
        # Use Docker API directly for container operations
        import docker
        client = docker.from_env()
        container = client.containers.get(container_id)
        container.restart()
        
        _audit("container_restart", request, container_id=container_id)
        
        return {"success": True, "containerId": container_id}
        
    except docker.errors.NotFound:
        raise HTTPException(404, "Container not found")
    except Exception as e:
        raise HTTPException(500, f"Failed to restart container: {str(e)}")

@APP.post("/security/containers/{container_id}/stop")
async def stop_container(container_id: str, request: Request):
    """Stop a specific container."""
    _require_enabled(); _require_rbac(request)
    
    try:
        import docker
        client = docker.from_env()
        container = client.containers.get(container_id)
        container.stop()
        
        _audit("container_stop", request, container_id=container_id)
        
        return {"success": True, "containerId": container_id}
        
    except docker.errors.NotFound:
        raise HTTPException(404, "Container not found")
    except Exception as e:
        raise HTTPException(500, f"Failed to stop container: {str(e)}")

@APP.post("/security/emergency-shutdown")
async def emergency_shutdown(request: Request):
    """Emergency shutdown with secure data wiping."""
    _require_enabled(); _require_rbac(request)
    _require_security_manager()
    
    try:
        await security_manager.emergency_shutdown()
        
        _audit("emergency_shutdown", request)
        
        return {"success": True, "message": "Emergency shutdown completed"}
        
    except Exception as e:
        raise HTTPException(500, f"Emergency shutdown failed: {str(e)}")

# ============================================================================
# PERFORMANCE MONITORING ENDPOINTS (v0.3.0+)
# ============================================================================

@APP.get("/health/comprehensive")
async def comprehensive_health_check(request: Request):
    """Comprehensive health check with performance metrics."""
    _require_enabled()
    
    import psutil
    import time
    
    start_time = time.time()
    
    # System metrics
    system_metrics = {
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "memory_usage_percent": psutil.virtual_memory().percent,
        "disk_usage_percent": psutil.disk_usage('/').percent,
        "uptime_seconds": time.time() - psutil.boot_time()
    }
    
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
    
    # Redis connection test (if available)
    redis_status = {"available": False}
    try:
        import redis
        r = redis.Redis(host='redis', port=6379, decode_responses=True)
        r.ping()
        redis_info = r.info()
        redis_status = {
            "available": True,
            "connected_clients": redis_info.get("connected_clients", 0),
            "used_memory_human": redis_info.get("used_memory_human", "N/A"),
            "keyspace_hits": redis_info.get("keyspace_hits", 0),
            "keyspace_misses": redis_info.get("keyspace_misses", 0)
        }
        if redis_status["keyspace_hits"] + redis_status["keyspace_misses"] > 0:
            redis_status["hit_rate"] = redis_status["keyspace_hits"] / (redis_status["keyspace_hits"] + redis_status["keyspace_misses"])
    except Exception:
        pass
    
    response_time = time.time() - start_time
    
    health_data = {
        "status": "healthy",
        "timestamp": time.time(),
        "response_time_ms": response_time * 1000,
        "system_metrics": system_metrics,
        "service_status": service_status,
        "redis_status": redis_status,
        "security_manager_active": security_manager is not None
    }
    
    _audit("health_check_comprehensive", request, response_time_ms=response_time * 1000)
    
    return health_data

@APP.get("/api/system/performance")
async def get_system_performance(request: Request):
    """Get detailed system performance metrics."""
    _require_enabled(); _require_rbac(request)
    
    import psutil
    import time
    
    # CPU metrics
    cpu_metrics = {
        "usage_percent": psutil.cpu_percent(interval=1),
        "load_avg": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else [0, 0, 0],
        "core_count": psutil.cpu_count()
    }
    
    # Memory metrics
    memory = psutil.virtual_memory()
    memory_metrics = {
        "total_gb": round(memory.total / (1024**3), 2),
        "used_gb": round(memory.used / (1024**3), 2),
        "available_gb": round(memory.available / (1024**3), 2),
        "usage_percent": memory.percent
    }
    
    # Disk metrics
    disk = psutil.disk_usage('/')
    disk_metrics = {
        "total_gb": round(disk.total / (1024**3), 2),
        "used_gb": round(disk.used / (1024**3), 2),
        "free_gb": round(disk.free / (1024**3), 2),
        "usage_percent": round((disk.used / disk.total) * 100, 2)
    }
    
    # Network metrics (basic)
    try:
        net_io = psutil.net_io_counters()
        network_metrics = {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }
    except Exception:
        network_metrics = {"error": "Network metrics unavailable"}
    
    performance_data = {
        "timestamp": time.time(),
        "cpu": cpu_metrics,
        "memory": memory_metrics,
        "disk": disk_metrics,
        "network": network_metrics,
        "uptime_hours": round((time.time() - psutil.boot_time()) / 3600, 2)
    }
    
    return performance_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(APP, host="0.0.0.0", port=8000)
