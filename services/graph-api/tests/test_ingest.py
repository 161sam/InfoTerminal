import pytest

from app import app as graph_app


@pytest.mark.anyio
async def test_plugin_ingest_endpoint_updates_state(client):
    graph_app.state.plugin_runs = []
    payload = {
        "job_id": "job-123",
        "plugin_name": "nmap",
        "status": "completed",
        "completed_at": "2025-01-01T00:00:00Z",
        "execution_time": 1.5,
        "graph_entities": [
            {
                "type": "Host",
                "id": "192.0.2.10",
                "properties": {"ip_address": "192.0.2.10"},
            }
        ],
        "search_documents": [],
    }

    response = await client.post("/v1/ingest/plugin-run", json=payload)
    assert response.status_code == 200
    assert graph_app.state.plugin_runs
    stored = graph_app.state.plugin_runs[-1]
    assert stored["plugin_name"] == "nmap"
    assert stored["graph_entities"][0]["type"] == "Host"


@pytest.mark.anyio
async def test_video_ingest_sets_flag_and_counts(client):
    graph_app.state.video_analyses = []
    graph_app.state.video_pipeline_enabled = False

    payload = {
        "video": {"id": "video-demo", "duration": 3.2},
        "scenes": [
            {
                "scene_id": "video-demo-scene-0",
                "frame_index": 0,
                "timestamp": 0.0,
                "objects": [
                    {
                        "object_id": "video-demo-0",
                        "label": "object",
                        "confidence": 0.9,
                        "bbox": {"x": 0, "y": 0, "width": 10, "height": 10},
                    }
                ],
            }
        ],
        "summary": {"frames_processed": 3},
    }

    response = await client.post("/v1/ingest/video", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["scenes"] == 1
    assert body["objects"] == 1
    assert graph_app.state.video_pipeline_enabled is True
    assert graph_app.state.video_analyses[-1]["video"]["id"] == "video-demo"


@pytest.mark.anyio
async def test_threat_indicator_ingest_is_idempotent(client):
    graph_app.state.driver = None
    graph_app.state.threat_indicator_store = {}
    graph_app.state.threat_indicator_seen = set()

    indicator = {
        "indicator": "1.2.3.4",
        "type": "IPv4",
        "source": "Pulse Alpha",
        "first_seen": "2024-05-01T00:00:00Z",
        "tags": ["apt", "ipv4"],
    }

    first = await client.post(
        "/v1/ingest/threat-indicators", json={"items": [indicator]}
    )
    assert first.status_code == 200
    assert first.json()["ingested"] == 1

    second = await client.post(
        "/v1/ingest/threat-indicators", json={"items": [indicator]}
    )
    assert second.status_code == 200
    assert second.json()["ingested"] == 0

    cache = getattr(graph_app.state, "threat_indicator_store")
    assert len(cache) == 1
