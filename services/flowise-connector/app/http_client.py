import asyncio
import os
from typing import Any, Optional

import httpx

DEFAULT_TIMEOUT = float(os.getenv("IT_HTTP_TIMEOUT", "15"))


async def request(
    method: str,
    url: str,
    *,
    headers: Optional[dict[str, str]] = None,
    params: Optional[dict[str, Any]] = None,
    json: Any | None = None,
) -> httpx.Response:
    """Perform an HTTP request with unified timeout and optional retry for GET."""
    timeout = httpx.Timeout(DEFAULT_TIMEOUT)
    async with httpx.AsyncClient(timeout=timeout) as client:
        attempts = 3 if method.upper() == "GET" else 1
        delay = 0.5
        last_exc: Exception | None = None
        for attempt in range(attempts):
            try:
                resp = await client.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    json=json,
                )
                resp.raise_for_status()
                return resp
            except httpx.HTTPError as exc:  # pragma: no cover - exercised via tests
                last_exc = exc
                if attempt + 1 == attempts:
                    raise
                await asyncio.sleep(delay)
                delay *= 2
        assert last_exc  # for mypy
        raise last_exc
