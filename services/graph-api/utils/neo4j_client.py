import time
from typing import Optional
from neo4j import GraphDatabase, exceptions

def get_driver(uri: str, user: str, password: str, max_attempts: int = 10, base_delay: float = 1.0):
    """
    Erstellt einen Neo4j-Driver mit Backoff; fängt gezielt AuthenticationRateLimit ab.
    """
    delay = base_delay
    last_err: Optional[Exception] = None
    for attempt in range(1, max_attempts + 1):
        try:
            driver = GraphDatabase.driver(uri, auth=(user, password))
            with driver.session() as s:
                s.run("RETURN 1").consume()
            return driver
        except exceptions.AuthError as e:
            code = getattr(e, "code", "") or ""
            if "AuthenticationRateLimit" in str(e) or code.endswith("AuthenticationRateLimit"):
                last_err = e
                time.sleep(delay)
                delay = min(delay * 2, 30.0)
                continue
            raise
        except Exception as e:
            last_err = e
            time.sleep(min(delay, 5.0))
            delay = min(delay * 2, 30.0)
    raise RuntimeError(f"Neo4j connect failed after {max_attempts} attempts: {last_err}")
