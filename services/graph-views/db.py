import os
import asyncio
import random
import time
import logging
from typing import Optional, Tuple

import asyncpg


logger = logging.getLogger("graph-views.db")


def build_database_url_from_env(env: os._Environ = os.environ) -> str:
    url = env.get("GV_DATABASE_URL")
    if url:
        return url
    host = env.get("GV_PG_HOST", "127.0.0.1")
    port = env.get("GV_PG_PORT", "5432")
    user = env.get("GV_PG_USER", "it_user")
    password = env.get("GV_PG_PASSWORD", "it_pass")
    db = env.get("GV_PG_DB", "it_graph")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


async def create_pool_with_retry(
    dsn: str,
    *,
    min_size: int,
    max_size: int,
    connect_timeout: float,
    max_retries: int,
    backoff_base_ms: int,
    backoff_max_ms: int,
    logger: logging.Logger = logger,
) -> Optional[asyncpg.Pool]:
    attempt = 0
    while True:
        try:
            pool = await asyncpg.create_pool(
                dsn=dsn,
                min_size=min_size,
                max_size=max_size,
                timeout=connect_timeout,
            )
            logger.info("pg pool ready")
            return pool
        except Exception as e:  # pragma: no cover - error path
            logger.warning("pg pool init failed: %s", e)
            attempt += 1
            if max_retries != -1 and attempt > max_retries:
                return None
            backoff = min(backoff_base_ms * (2 ** (attempt - 1)), backoff_max_ms)
            backoff += random.randint(0, 250)
            logger.info("retrying pg pool in %sms", backoff)
            await asyncio.sleep(backoff / 1000)


async def close_pool(pool: Optional[asyncpg.Pool]) -> None:
    if pool is not None:
        await pool.close()


async def probe_select_1(pool: asyncpg.Pool, timeout_s: float) -> Tuple[bool, Optional[float], Optional[str]]:
    start = time.perf_counter()
    try:
        async with pool.acquire() as conn:
            await asyncio.wait_for(conn.fetchval("SELECT 1"), timeout=timeout_s)
        latency = (time.perf_counter() - start) * 1000
        return True, round(latency, 3), None
    except asyncio.TimeoutError:
        latency = (time.perf_counter() - start) * 1000
        return False, round(latency, 3), "timeout"
    except Exception as e:
        latency = (time.perf_counter() - start) * 1000
        return False, round(latency, 3), str(e)
