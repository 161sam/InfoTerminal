"""Tests for graph CLI commands."""
from __future__ import annotations

import json

import pytest

pytest.importorskip("httpx")
pytest.importorskip("typer")
import httpx
from typer.testing import CliRunner

from it_cli.__main__ import app
from it_cli.config import get_settings

runner = CliRunner()


def run(args: list[str]):
    return runner.invoke(app, args)


@pytest.fixture(autouse=True)
def reset_settings(monkeypatch):
    get_settings.cache_clear()
    monkeypatch.setenv("IT_GRAPH_API", "http://graph")
    yield
    get_settings.cache_clear()


def _mock_transport(response_data, status_code=200, expected_path=None, expected_method="POST"):
    async def handler(request: httpx.Request) -> httpx.Response:
        if expected_path:
            assert str(request.url).endswith(expected_path)
        assert request.method.upper() == expected_method
        return httpx.Response(status_code, json=response_data)

    transport = httpx.MockTransport(handler)
    original_async_client = httpx.AsyncClient

    def _factory(*args, **kwargs):
        kwargs["transport"] = transport
        return original_async_client(*args, **kwargs)

    return _factory


def test_graph_cypher(monkeypatch):
    captured = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["body"] = json.loads(request.content.decode("utf-8"))
        return httpx.Response(200, json={"records": [{"result": 1}]})

    transport = httpx.MockTransport(handler)
    original_async_client = httpx.AsyncClient

    def _factory(*args, **kwargs):
        kwargs["transport"] = transport
        return original_async_client(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", _factory)

    result = run(["graph", "cypher", "RETURN 1"])
    assert result.exit_code == 0
    assert captured["url"].endswith("/v1/cypher")
    assert captured["body"] == {"query": "RETURN 1", "parameters": {}, "read_only": True}
    assert "records" in result.stdout


def test_graph_neighbors(monkeypatch):
    data = {
        "center_node": {"id": 1},
        "neighbors": [{"id": 2}, {"id": 3}],
        "relationships": [
            {"source": 1, "target": 2},
            {"source": 1, "target": 3},
        ],
    }
    monkeypatch.setattr(httpx, "AsyncClient", _mock_transport(data, expected_path="/v1/nodes/1/neighbors", expected_method="GET"))

    result = run(["graph", "neighbors", "1", "--limit", "10"])
    assert result.exit_code == 0
    assert "neighbors" in result.stdout


def test_graph_shortest_path(monkeypatch):
    payload = {"found": True, "path": {"length": 2}}
    monkeypatch.setattr(httpx, "AsyncClient", _mock_transport(payload, expected_path="/v1/shortest-path"))

    result = run([
        "graph",
        "shortest-path",
        "--source",
        "1",
        "--target",
        "2",
    ])
    assert result.exit_code == 0
    assert "length" in result.stdout
