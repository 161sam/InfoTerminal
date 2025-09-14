import logging

import httpx
import pytest

import app.main as main


@pytest.mark.anyio
async def test_chat_upstream_error(client, monkeypatch, caplog):
    caplog.set_level(logging.ERROR)

    async def boom(method, url, **kwargs):
        request = httpx.Request("POST", url)
        response = httpx.Response(500, request=request)
        raise httpx.HTTPStatusError("server error", request=request, response=response)

    monkeypatch.setenv("AGENT_BASE_URL", "http://agent")
    main.AGENT_BASE_URL = "http://agent"
    monkeypatch.setattr(main, "http_request", boom)

    resp = await client.post("/chat", json={"messages": []})
    assert resp.status_code == 500
    assert resp.json() == {
        "status": 500,
        "detail": "server error",
        "upstream": "http://agent/api/v1/prediction",
    }
    rec = next(rec for rec in caplog.records if rec.msg == "agent_error")
    assert rec.req_id == resp.headers["X-Request-Id"]


@pytest.mark.anyio
async def test_workflow_timeout(client, monkeypatch, caplog):
    caplog.set_level(logging.ERROR)

    async def boom(method, url, **kwargs):
        raise httpx.TimeoutException("timeout")

    monkeypatch.setenv("N8N_WEBHOOK", "http://n8n/hook")
    main.N8N_WEBHOOK = "http://n8n/hook"
    monkeypatch.setattr(main, "http_request", boom)

    resp = await client.post("/workflows/trigger", json={"name": "x"})
    assert resp.status_code == 408
    assert resp.json()["upstream"] == "http://n8n/hook"
    rec = next(rec for rec in caplog.records if rec.msg == "workflow_error")
    assert rec.req_id == resp.headers["X-Request-Id"]
