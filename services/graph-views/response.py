from typing import Any, Dict, Optional


def ok(data: Any = None, counts: Optional[Dict[str, int]] = None):
    return {"ok": True, "data": data or None, "counts": counts or {}, "error": None}


def err(code: str, message: str, status: int):
    return {"ok": False, "data": None, "counts": {}, "error": {"code": code, "message": message}}, status


def bool_qp(val: Optional[str]) -> bool:
    return str(val).lower() in ("1", "true", "yes", "on")


def safe_counts(counters) -> Dict[str, int]:
    if not counters:
        return {}
    nodes = getattr(counters, "nodes_created", 0) + getattr(counters, "nodes_deleted", 0) * 0
    rels = getattr(counters, "relationships_created", 0)
    return {"nodes": int(nodes), "relationships": int(rels)}
