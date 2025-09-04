import enum
import time
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Tuple
from urllib import request as urlrequest
import concurrent.futures

class HealthStatus(str, enum.Enum):
    ok = "ok"
    degraded = "degraded"
    fail = "fail"
    skipped = "skipped"

def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def uptime_seconds(start_ts: float) -> float:
    return time.monotonic() - start_ts

def aggregate_status(checks: Dict[str, Dict[str, Any]]) -> str:
    if any(c.get("status") == "fail" for c in checks.values()):
        return "fail"
    if any(c.get("status") == "skipped" for c in checks.values()):
        return "degraded"
    return "ok"

def make_healthz(service: str, version: str, start_ts: float) -> Dict[str, Any]:
    return {
        "service": service,
        "version": version,
        "status": "ok",
        "time": utcnow_iso(),
        "uptime_s": uptime_seconds(start_ts),
    }

def make_readyz(service: str, version: str, start_ts: float, checks: Dict[str, Dict[str, Any]]) -> Tuple[Dict[str, Any], int]:
    status = aggregate_status(checks)
    payload = {
        "service": service,
        "version": version,
        "status": status,
        "time": utcnow_iso(),
        "uptime_s": uptime_seconds(start_ts),
        "checks": checks,
    }
    http_status = 200 if status != "fail" else 503
    return payload, http_status

def probe_http(url: str, timeout_s: float = 0.8) -> Dict[str, Any]:
    start = time.perf_counter()
    try:
        with urlrequest.urlopen(url, timeout=timeout_s) as resp:
            code = resp.getcode()
        latency = (time.perf_counter() - start) * 1000
        if 200 <= code < 300 or code == 401:
            return {"status": "ok", "latency_ms": round(latency, 3), "error": None, "reason": None}
        return {"status": "fail", "latency_ms": round(latency, 3), "error": f"http {code}", "reason": None}
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        err = "timeout" if "timed out" in str(e) else str(e)
        return {"status": "fail", "latency_ms": round(latency, 3), "error": err, "reason": None}

def probe_db(callable_fn: Callable[[], Any], timeout_s: float = 0.8) -> Dict[str, Any]:
    start = time.perf_counter()
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
            future = ex.submit(callable_fn)
            future.result(timeout=timeout_s)
        latency = (time.perf_counter() - start) * 1000
        return {"status": "ok", "latency_ms": round(latency, 3), "error": None, "reason": None}
    except concurrent.futures.TimeoutError:
        latency = (time.perf_counter() - start) * 1000
        return {"status": "fail", "latency_ms": round(latency, 3), "error": "timeout", "reason": None}
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return {"status": "fail", "latency_ms": round(latency, 3), "error": str(e), "reason": None}
