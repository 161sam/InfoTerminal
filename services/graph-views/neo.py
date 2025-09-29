import os
import time
from contextlib import contextmanager
from typing import Any, Dict, Optional

from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import ClientError, ServiceUnavailable, TransientError

_driver = None


def get_driver():  # pragma: no cover - thin wrapper around driver factory
    global _driver
    if _driver:
        return _driver
    uri = os.getenv("NEO4J_URI") or "bolt://it-neo4j:7687"
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    auth = basic_auth(user, password) if user and password else None
    max_lifetime = os.getenv("NEO4J_MAX_CONN_LIFETIME")
    kwargs: Dict[str, Any] = {}
    if max_lifetime:
        try:
            kwargs["max_connection_lifetime"] = int(max_lifetime)
        except ValueError:
            pass
    _driver = GraphDatabase.driver(uri, auth=auth, **kwargs)
    return _driver


@contextmanager
def get_session(database: Optional[str] = None):  # pragma: no cover - simple wrapper
    drv = get_driver()
    db = database or os.getenv("NEO4J_DATABASE", "neo4j")
    session = drv.session(database=db)
    try:
        yield session
    finally:
        session.close()


def is_transient_error(exc: Exception) -> bool:
    if isinstance(exc, (ServiceUnavailable, TransientError)):
        return True
    if isinstance(exc, ClientError) and any(  # pragma: no cover - rarely triggered
        tok in str(exc).lower() for tok in ("connection", "transient")
    ):
        return True  # pragma: no cover
    return False


def exponential_backoff(attempt: int, base_ms: int = 120, cap_ms: int = 2000) -> float:
    delay_ms = min(base_ms * (2 ** attempt), cap_ms)
    return delay_ms / 1000.0


def run_with_retries(
    session,
    cypher: str,
    params: Optional[Dict[str, Any]] = None,
    max_attempts: int = 5,
    backoff_base_ms: int = 120,
    backoff_cap_ms: int = 2000,
):
    attempt = 0
    params = params or {}
    while True:
        try:
            return session.run(cypher, **params)
        except Exception as e:  # pragma: no cover - defensive
            if not is_transient_error(e) or attempt >= max_attempts - 1:
                raise
            delay = exponential_backoff(attempt, base_ms=backoff_base_ms, cap_ms=backoff_cap_ms)
            time.sleep(delay)
            attempt += 1
