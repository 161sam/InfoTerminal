import os
import json
import glob
import time
from pathlib import Path
from typing import List, Dict, Any
import httpx
import yaml
from fastapi import APIRouter, HTTPException, Request
from services.common.audit import audit_log
from pydantic import BaseModel

PLUGINS_DIR = Path(os.getenv("IT_PLUGINS_DIR", "plugins"))
API_VERSION = os.getenv("IT_PLUGIN_API_VERSION", "v1")
CACHE_TTL = int(os.getenv("IT_PLUGINS_CACHE_TTL_SEC", "30"))
router = APIRouter(prefix="/plugins", tags=["plugins"])

try:
    import jsonschema  # type: ignore
except Exception:
    jsonschema = None


class Loaded(BaseModel):
    manifest: Dict[str, Any]


_cache = {"ts": 0.0, "items": []}


def _read_manifest(p: Path) -> Dict[str, Any]:
    t = p.suffix.lower()
    data = (
        yaml.safe_load(p.read_text(encoding="utf-8"))
        if t in (".yml", ".yaml")
        else json.loads(p.read_text(encoding="utf-8"))
    )
    if data.get("apiVersion") != API_VERSION:
        raise HTTPException(422, f"plugin apiVersion mismatch for {p.name}")
    return data


def _discover() -> List[Loaded]:
    now = time.time()
    if _cache["items"] and now - _cache["ts"] < CACHE_TTL:
        return _cache["items"]
    items = []
    for mf in glob.glob(str(PLUGINS_DIR / "*" / "plugin.*")):
        items.append(Loaded(manifest=_read_manifest(Path(mf))))
    _cache.update(ts=now, items=items)
    return items


@router.get("/tools")
def tools():
    items = []
    for lp in _discover():
        m = lp.manifest
        for t in (m.get("capabilities") or {}).get("tools", []):
            items.append({"plugin": m["name"], **t})
    return {"apiVersion": API_VERSION, "tools": items}


@router.post("/invoke/{plugin}/{tool}")
async def invoke(plugin: str, tool: str, payload: Dict[str, Any], request: Request):
    lp = next((x for x in _discover() if x.manifest["name"] == plugin), None)
    if not lp:
        raise HTTPException(404, "plugin not found")
    m = lp.manifest
    base = (m.get("endpoints") or {}).get("baseUrl")
    if not base:
        raise HTTPException(502, "plugin missing baseUrl")
    # optional args validation
    spec = next(
        (
            t
            for t in (m.get("capabilities") or {}).get("tools", [])
            if t.get("name") == tool
        ),
        None,
    )
    if spec and jsonschema and (schema := spec.get("argsSchema")):
        try:
            jsonschema.validate(instance=payload, schema=schema)  # type: ignore
        except Exception as e:
            raise HTTPException(400, f"argsSchema validation failed: {e}")
    url = f"{base.rstrip('/')}/tools/{tool}"
    headers = {}
    for h in ("Authorization", "X-Request-Id", "X-Tenant-Id"):
        v = request.headers.get(h)
        if v:
            headers[h] = v
    timeout = httpx.Timeout(15.0)
    actor = getattr(request.state, "user_id", None) or "anon"
    tenant = request.headers.get("X-Tenant-Id", "default")
    try:
        async with httpx.AsyncClient(timeout=timeout) as c:
            r = await c.post(url, json=payload, headers=headers)
            if r.status_code >= 400:
                raise HTTPException(r.status_code, r.text)
            res = r.json()
        audit_log(
            "plugin.invoke",
            actor,
            tenant,
            {"plugin": plugin, "tool": tool},
            "ok",
            req_id=headers.get("X-Request-Id"),
        )
        return res
    except HTTPException as e:
        audit_log(
            "plugin.invoke",
            actor,
            tenant,
            {"plugin": plugin, "tool": tool},
            "error",
            {"detail": str(e)},
            req_id=headers.get("X-Request-Id"),
        )
        raise
