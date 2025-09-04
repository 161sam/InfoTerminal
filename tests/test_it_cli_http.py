"""Tests for HTTP client helper."""
from __future__ import annotations

import asyncio
import httpx

from it_cli.http import DEFAULT_TIMEOUT, client


def test_client_config_and_request(monkeypatch):
    """Client uses defaults and executes requests via mock transport."""
    called: dict[str, str] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        called["url"] = str(request.url)
        return httpx.Response(200, text="ok")

    transport = httpx.MockTransport(handler)

    original_async_client = httpx.AsyncClient

    def _async_client(*args, **kwargs):
        kwargs["transport"] = transport
        return original_async_client(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", _async_client)

    async def run() -> None:
        async with client() as c:
            resp = await c.get("https://example.com/")
            assert resp.status_code == 200
            assert resp.text == "ok"
            assert c.timeout == DEFAULT_TIMEOUT
            assert c.follow_redirects is True
        assert c.is_closed

    asyncio.run(run())
    assert called["url"] == "https://example.com/"
