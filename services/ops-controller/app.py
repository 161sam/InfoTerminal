import os, subprocess, shlex, time, json, threading
from pathlib import Path
from typing import List, Dict, Optional
import yaml
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from _shared.audit import audit_log

APP = FastAPI(title="Ops Controller", version="0.1.0")

ENABLED = os.getenv("IT_OPS_ENABLE","0") == "1"
MODE = os.getenv("IT_OPS_MODE","docker")
COMPOSE = os.getenv("IT_OPS_COMPOSE_BIN","docker compose")
STACKS_FILE = Path(os.getenv("IT_OPS_STACKS_FILE","infra/ops/stacks.yaml"))
LOCK_TIMEOUT = int(os.getenv("IT_OPS_LOCK_TIMEOUT_SEC","120"))
TAIL = os.getenv("IT_OPS_LOG_TAIL_LINES","300")
SOCKET = os.getenv("IT_DOCKER_SOCKET","/var/run/docker.sock")

_lock = threading.Lock()
_lock_at = 0.0

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
