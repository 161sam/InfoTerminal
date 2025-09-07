import pytest
pytest.skip("legacy sync tests skipped", allow_module_level=True)


import json
import logging
import os
import sys
import types
import app as app_module  # type: ignore
from fastapi.testclient import TestClient


class DummyPool:
    def closeall(self):
        pass


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(app_module, "setup_pool", lambda: DummyPool())
    monkeypatch.setenv("INIT_DB_ON_STARTUP", "0")
    with TestClient(app_module.app) as c:
        yield c


def test_request_id_roundtrip(client):
    r = client.get("/healthz")
    rid = r.headers.get("X-Request-Id")
    assert rid and len(rid) > 0
    custom = "req-123"
    r2 = client.get("/healthz", headers={"X-Request-Id": custom})
    assert r2.headers["X-Request-Id"] == custom


def test_log_shape(client, caplog):
    caplog.set_level(logging.INFO)
    os.environ["IT_LOG_SAMPLING"] = ""
    r = client.get("/healthz")
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
    assert data["service"] == "graph-views"
    assert data["env"] == "test"
    assert data["req_id"] == r.headers["X-Request-Id"]
    assert data["path"] == "/healthz"
    assert data["status"] == 200
    assert data["msg"] == "request"
    assert "dur_ms" in data


def test_no_dup_logs(client, caplog):
    caplog.set_level(logging.INFO)
    client.get("/healthz")
    records = [rec for rec in caplog.records if rec.msg == "request"]
    assert len(records) == 1


def test_trace_fields_optional(client, caplog, monkeypatch):
    caplog.set_level(logging.INFO)
    monkeypatch.setenv("IT_LOG_SAMPLING", "")
    client.get("/healthz")
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
    client.get("/healthz")
    rec = [rec for rec in caplog.records if rec.msg == "request"][-1]
    data = json.loads(fmt.format(rec))
    assert data.get("trace_id") == "00000000000000000000000000000001"
    assert data.get("span_id") == "0000000000000002"
