import pytest

from app import app as graph_app
import app.routes.analytics as analytics_routes
from metrics import GRAPH_ANALYSIS_QUERIES, GRAPH_SUBGRAPH_EXPORTS


class _FakeGraphAnalytics:
    def __init__(self, driver):
        self.driver = driver

    def degree_centrality(self, **_: int):
        return [
            {"node_id": "n1", "name": "Alpha", "labels": ["Person"], "degree": 3},
            {"node_id": "n2", "name": "Beta", "labels": ["Company"], "degree": 2},
        ]

    def louvain_communities(self, **_: int):
        return {
            "algorithm": "louvain",
            "community_count": 1,
            "communities": [
                {"id": 0, "size": 2, "members": [{"node_id": "n1"}, {"node_id": "n2"}]}
            ],
        }

    def subgraph_export(self, **_: int):
        return {
            "center": {"id": "n1", "labels": ["Person"], "properties": {"name": "Alpha"}},
            "nodes": [
                {"id": "n1", "labels": ["Person"], "properties": {"name": "Alpha"}},
                {"id": "n2", "labels": ["Company"], "properties": {"name": "Beta"}},
            ],
            "relationships": [
                {"id": 1, "type": "OWNS", "source": "n1", "target": "n2", "properties": {}},
            ],
            "markdown": "### demo",
        }


class _FakeResult:
    def single(self):
        return {
            "nodes": [
                {"id": "n1", "name": "Alpha", "labels": ["Person"]},
                {"id": "n2", "name": "Beta", "labels": ["Company"]},
            ],
            "relationships": ["OWNS"],
            "path_length": 1,
        }


class _FakeSession:
    def run(self, *args, **kwargs):  # pragma: no cover - signature compatibility
        return _FakeResult()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _fake_neo_session(_driver):
    class _Context:
        def __enter__(self):
            return _FakeSession()

        def __exit__(self, exc_type, exc, tb):
            return False

    return _Context()


@pytest.mark.anyio
async def test_analysis_endpoints_emit_metrics(client, monkeypatch):
    graph_app.state.driver = object()

    GRAPH_ANALYSIS_QUERIES.labels(algorithm="degree", status="success")._value.set(0)
    GRAPH_SUBGRAPH_EXPORTS.labels(format="markdown", status="success")._value.set(0)

    monkeypatch.setattr(analytics_routes, "GraphAnalytics", _FakeGraphAnalytics)
    monkeypatch.setattr(analytics_routes, "neo_session", _fake_neo_session)

    # Degree centrality
    resp = await client.get("/graphs/analysis/degree", params={"limit": 2})
    assert resp.status_code == 200
    body = resp.json()
    assert body["algorithm"] == "degree"
    assert body["pagination"]["limit"] == 2

    # Louvain communities
    resp = await client.get("/graphs/analysis/communities")
    assert resp.status_code == 200
    assert resp.json()["community_count"] == 1

    # Shortest path via legacy alias to ensure backwards compatibility
    payload = {"start_node_id": "n1", "end_node_id": "n2"}
    resp = await client.post("/analytics/paths/shortest", json=payload)
    assert resp.status_code == 200
    assert resp.json()["path_found"] is True

    # Subgraph export (markdown format)
    resp = await client.get(
        "/graphs/analysis/subgraph-export",
        params={"center_id": "n1", "format": "markdown"},
    )
    assert resp.status_code == 200
    assert "markdown" in resp.json()

    # Metrics counters incremented
    assert (
        GRAPH_ANALYSIS_QUERIES.labels(algorithm="degree", status="success")._value.get()
        >= 1
    )
    assert (
        GRAPH_SUBGRAPH_EXPORTS.labels(format="markdown", status="success")._value.get()
        >= 1
    )
