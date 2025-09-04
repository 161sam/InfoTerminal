"""Async HTTP helpers."""
from __future__ import annotations

from contextlib import asynccontextmanager

import httpx

DEFAULT_TIMEOUT = httpx.Timeout(10.0, connect=5.0)


@asynccontextmanager
async def client():
    """Provide a configured AsyncClient with sensible defaults."""
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT, follow_redirects=True) as c:
        yield c
