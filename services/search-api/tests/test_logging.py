import json
import logging
import os
import sys
import types

import pytest


@pytest.mark.anyio
async def test_request_id_roundtrip(client):
    r = await client.get("/healthz")
    rid = r.headers.get("X-Request-Id")
    assert rid and len(rid) > 0
    custom = "req-123"
    r2 = await client.get("/healthz", headers={"X-Request-Id": custom})
    assert r2.headers["X-Request-Id"] == custom


@pytest.mark.anyio
async def test_log_shape(client, caplog):
    caplog.set_level(logging.INFO)
    os.environ["IT_LOG_SAMPLING"] = ""
    r = await client.get("/healthz")
    rec = [rec for rec in caplog.records if rec.msg == "request"][-1]
    fmt = logging.getLogger().handlers[0].formatter
    data = json.loads(fmt.format(rec))
    expected_order = [
        k
        for k in [
            "ts",
            "level",
            "service",
            "env",
            "req_id",
            "trace_id",
            "span_id",
            "client_ip",
            "method",
            "path",
            "status",
            "dur_ms",
            "msg",
        ]
        if k in data
    ]
    assert list(data.keys()) == expected_order
    assert data["service"] == "search-api"
    assert data["env"] == "test"
    assert data["req_id"] == r.headers["X-Request-Id"]
    assert data["path"] == "/healthz"
    assert data["status"] == 200
    assert data["msg"] == "request"
    assert "dur_ms" in data


@pytest.mark.anyio
async def test_no_dup_logs(client, caplog):
    caplog.set_level(logging.INFO)
    await client.get("/healthz")
    records = [rec for rec in caplog.records if rec.msg == "request"]
    assert len(records) == 1


@pytest.mark.anyio
async def test_trace_fields_optional(client, caplog, monkeypatch):
    caplog.set_level(logging.INFO)
    monkeypatch.setenv("IT_LOG_SAMPLING", "")
    await client.get("/healthz")
    rec = [rec for rec in caplog.records if rec.msg == "request"][-1]
    fmt = logging.getLogger().handlers[0].formatter
    data = json.loads(fmt.format(rec))
    assert "trace_id" not in data and "span_id" not in data
    caplog.clear()
    monkeypatch.setenv("IT_OTEL", "1")

    class Ctx:
        trace_id = 0x1
        span_id = 0x2

    class Span:
        def get_span_context(self):
            return Ctx()

    monkeypatch.setitem(
        sys.modules,
        "opentelemetry.trace",
        types.SimpleNamespace(get_current_span=lambda: Span()),
    )
    await client.get("/healthz")
    rec = next(rec for rec in caplog.records if rec.msg == "request")
    data = json.loads(fmt.format(rec))
    assert data.get("trace_id") == "00000000000000000000000000000001"
    assert data.get("span_id") == "0000000000000002"
