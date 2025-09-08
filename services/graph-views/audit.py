import json, os, time, uuid
from typing import Any, Dict

GV_AUDIT_LOG = os.getenv("GV_AUDIT_LOG", "0") in ("1", "true", "True")

def new_request_id() -> str:
    return uuid.uuid4().hex

def log_event(event: Dict[str, Any]):
    if not GV_AUDIT_LOG:
        return
    print(json.dumps(event, ensure_ascii=False))
