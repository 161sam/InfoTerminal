import os
import time
from contextlib import contextmanager
from typing import Any, Dict, Generator, Optional

from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import ServiceUnavailable, TransientError, ClientError

_driver = None


def get_driver():
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
def get_session(database: Optional[str] = None):
    drv = get_driver()
    db = database or os.getenv("NEO4J_DATABASE", "neo4j")
    session = drv.session(database=db)
    try:
        yield session
    finally:
        session.close()


def run_with_retries(session, cypher: str, params: Optional[Dict[str, Any]] = None,
                     max_attempts: int = 5, backoff_base_ms: int = 120):
    attempt = 0
    params = params or {}
    while True:
        try:
            return session.run(cypher, **params)
        except Exception as e:
            retriable = False
            if isinstance(e, (ServiceUnavailable, TransientError)):
                retriable = True
            elif isinstance(e, ClientError) and any(
                tok in str(e).lower() for tok in ("connection", "transient")
            ):
                retriable = True
            if not retriable or attempt >= max_attempts - 1:
                raise
            delay = backoff_base_ms * (2 ** attempt) / 1000.0
            time.sleep(delay)
            attempt += 1
