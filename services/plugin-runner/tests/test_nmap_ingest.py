from pathlib import Path
import json
import sys

import pytest


ROOT = Path(__file__).resolve().parents[3]
SERVICE_DIR = ROOT / "services" / "plugin-runner"
if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))
if str(ROOT / "services") not in sys.path:
    sys.path.insert(0, str(ROOT / "services"))

from registry import PluginRegistry  # type: ignore  # noqa: E402
from _shared.clients.graph_ingest import GraphIngestClient  # type: ignore  # noqa: E402


@pytest.mark.asyncio
async def test_nmap_mock_execution_ingests_graph(tmp_path, monkeypatch):
    monkeypatch.setenv("PLUGIN_TEST_MODE", "1")

    registry = PluginRegistry(Path("plugins"))
    result = await registry.execute_plugin(
        "nmap",
        {"target": "192.0.2.10", "scan_type": "basic"},
        job_id="job-nmap-demo",
    )

    assert result.status == "completed"
    assert result.graph_entities, "nmap mock output should yield graph entities"
    host_entity = result.graph_entities[0]
    assert host_entity["type"] == "Host"
    assert host_entity["properties"]["ip_address"] == "192.0.2.10"

    graph_client = GraphIngestClient(base_url=None, fallback_dir=tmp_path)
    payload = {
        "job_id": result.job_id,
        "plugin_name": result.plugin_name,
        "status": result.status,
        "completed_at": result.completed_at.isoformat() if result.completed_at else None,
        "execution_time": result.execution_time,
        "graph_entities": result.graph_entities,
        "search_documents": result.search_documents,
    }

    ingest_result = await graph_client.ingest_plugin_run(payload)
    await graph_client.close()

    stored_path = Path(ingest_result["path"])
    assert stored_path.exists()

    stored_payload = json.loads(stored_path.read_text())
    assert stored_payload["plugin_name"] == "nmap"
    assert stored_payload["graph_entities"][0]["type"] == "Host"
