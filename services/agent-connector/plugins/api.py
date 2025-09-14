import os, time, httpx, json, glob, yaml
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from pathlib import Path
from .state import read_global, write_global, read_user, write_user
from ..auth import require_user, require_admin
from services.common.audit import audit_log

PLUGINS_DIR = Path(os.getenv("IT_PLUGINS_DIR","plugins"))
TTL = int(os.getenv("IT_PLUGINS_CACHE_TTL_SEC","30"))

router = APIRouter(prefix="/plugins", tags=["plugins"])
_CACHE = {"ts":0, "registry":[]}


def _load_registry():
    now=time.time()
    if _CACHE["registry"] and now - _CACHE["ts"] < TTL:
        return _CACHE["registry"]
    items=[]
    for mf in glob.glob(str(PLUGINS_DIR / "*" / "plugin.*")):
        data = yaml.safe_load(Path(mf).read_text(encoding="utf-8")) if mf.endswith((".yml",".yaml")) else json.loads(Path(mf).read_text(encoding="utf-8"))
        items.append(data)
    _CACHE.update(ts=now, registry=items)
    return items


@router.get("/registry")
def registry(_: dict = Depends(require_user)):
    return {"items": _load_registry()}


@router.get("/state")
def state(request: Request, user: dict = Depends(require_user)):
    uid = user.get("sub") or user.get("email") or "anon"
    reg = _load_registry()
    g = read_global()
    u = read_user(uid)
    out=[]
    for p in reg:
        name=p["name"]
        base={"name":name,"version":p.get("version"),"provider":p.get("provider")}
        merged={**base, **(g.get(name,{})), **(u.get(name,{}))}
        out.append(merged)
    return {"items": out}


class ToggleIn(BaseModel):
    enabled: bool
    scope: str = "user"  # user|global


@router.post("/{name}/enable")
def toggle(name: str, body: ToggleIn, request: Request, user: dict = Depends(require_user)):
    uid = user.get("sub") or user.get("email") or "anon"
    if body.scope == "global":
        require_admin(user)
        g = read_global(); g[name] = {**g.get(name,{}), "enabled": body.enabled}; write_global(g)
        audit_log("plugin.enable", uid, request.headers.get("X-Tenant-Id","default"), {"name": name, "scope":"global"})
        return {"name": name, "enabled": body.enabled, "scope": "global"}
    u = read_user(uid); u[name] = {**u.get(name,{}), "enabled": body.enabled}; write_user(uid,u)
    audit_log("plugin.enable", uid, request.headers.get("X-Tenant-Id","default"), {"name": name, "scope":"user"})
    return {"name": name, "enabled": body.enabled, "scope": "user"}


class ConfigIn(BaseModel):
    config: dict
    scope: str = "user"  # user|global


@router.get("/{name}/config")
def get_config(name: str, user: dict = Depends(require_user)):
    uid = user.get("sub") or user.get("email") or "anon"
    g = read_global().get(name,{}).get("config",{})
    u = read_user(uid).get(name,{}).get("config",{})
    merged={**g, **u}
    return {"name": name, "config": merged}


@router.post("/{name}/config")
def set_config(name: str, body: ConfigIn, request: Request, user: dict = Depends(require_user)):
    if any(k.lower() in ("secret","token","password","apikey","api_key") for k in body.config.keys()):
        raise HTTPException(400,"secrets must be configured via ENV/Vault")
    uid = user.get("sub") or user.get("email") or "anon"
    if body.scope == "global":
        require_admin(user)
        g = read_global(); cur = g.get(name,{}); cur["config"]= {**cur.get("config",{}), **body.config}; g[name]=cur; write_global(g)
        audit_log("plugin.config", uid, request.headers.get("X-Tenant-Id","default"), {"name": name, "scope":"global"})
        return {"name": name, "scope":"global", "config": cur["config"]}
    u = read_user(uid); cur = u.get(name,{}); cur["config"]= {**cur.get("config",{}), **body.config}; u[name]=cur; write_user(uid,u)
    audit_log("plugin.config", uid, request.headers.get("X-Tenant-Id","default"), {"name": name, "scope":"user"})
    return {"name": name, "scope":"user", "config": cur["config"]}


@router.get("/{name}/health")
async def health(name: str, request: Request, user: dict = Depends(require_user)):
    base = None; p=None
    for p in _load_registry():
        if p.get("name")==name:
            base = (p.get("endpoints") or {}).get("baseUrl"); break
    if not base: return {"status":"unknown"}
    url = f"{base.rstrip('/')}/{(p.get('endpoints') or {}).get('health','healthz')}"
    t0=time.time()
    headers={"X-Request-Id": request.headers.get("X-Request-Id",""), "X-Tenant-Id": request.headers.get("X-Tenant-Id","")}
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            r= await c.get(url, headers=headers)
            status = "up" if r.status_code<400 else "degraded"
    except Exception:
        status="down"
    return {"status": status, "latency_ms": int((time.time()-t0)*1000), "checked_at": int(time.time()*1000)}
