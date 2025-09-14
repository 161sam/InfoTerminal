import json
import logging
from datetime import datetime
from typing import Any, Dict

log = logging.getLogger("audit")


def audit_log(action: str, user: str, tenant: str, **extra: Any) -> None:
    entry: Dict[str, Any] = {
        "ts": datetime.utcnow().isoformat(),
        "action": action,
        "user": user,
        "tenant": tenant,
    }
    entry.update(extra)
    log.info(json.dumps(entry))
