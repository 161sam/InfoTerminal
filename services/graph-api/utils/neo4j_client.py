import time
from typing import Optional
from contextlib import contextmanager

from neo4j import GraphDatabase, exceptions


def get_driver(
    uri: str,
    user: str,
    password: str,
    max_attempts: int = 10,
    backoff: float = 0.5,
):
    """Create a Neo4j driver with retry and exponential backoff.

    Returns ``None`` if the connection cannot be established after the given
    attempts. This ensures imports do not crash when Neo4j is unavailable.
    """

    delay = backoff
    last_err: Optional[Exception] = None
    for _ in range(max_attempts):
        try:
            driver = GraphDatabase.driver(uri, auth=(user, password))
            with driver.session() as s:
                s.run("RETURN 1").consume()
            return driver
        except (exceptions.AuthError, exceptions.ServiceUnavailable, OSError) as e:
            last_err = e
            time.sleep(delay)
            delay = min(delay * 2, 30.0)
        except Exception as e:  # unexpected
            last_err = e
            break
    return None


@contextmanager
def neo_session(driver, database: Optional[str] = None):
    if driver is None:
        raise RuntimeError("Neo4j driver not ready")
    if database is None:
        with driver.session() as s:
            yield s
    else:
        with driver.session(database=database) as s:
            yield s

