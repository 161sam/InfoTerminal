import os
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import importlib.util

# Import the doc-entities service
service_path = Path(__file__).resolve().parents[1] / "services" / "doc-entities" / "app.py"
spec = importlib.util.spec_from_file_location("doc_entities_app", service_path)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

# Enable test mode
os.environ["ALLOW_TEST_MODE"] = "1"
client = TestClient(module.app)

def test_ner_endpoint():
    """Test NER endpoint returns proper entities."""
    response = client.post("/ner", json={"text": "Barack Obama was born in Hawaii."})
    assert response.status_code == 200
    data = response.json()
    assert "entities" in data
    assert len(data["entities"]) >= 1
    # Verify entity structure
    entity = data["entities"][0]
    assert "text" in entity
    assert "label" in entity
    assert "start" in entity
    assert "end" in entity

def test_summary_endpoint():
    """Test summary endpoint."""
    response = client.post("/summary", json={"text": "This is a test text for summarization."})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert isinstance(data["summary"], str)

def test_annotate_endpoint():
    """Test document annotation endpoint."""
    response = client.post("/annotate", json={
        "text": "John Smith works at ACME Corp in New York.",
        "title": "Test Document"
    })
    assert response.status_code == 200
    data = response.json()
    assert "doc_id" in data
    assert "entities" in data
    assert "html" in data
    assert "relations" in data
    
    # Verify entities were created
    entities = data["entities"]
    assert len(entities) >= 1
    
    # Verify entity structure
    if entities:
        entity = entities[0]
        assert "id" in entity
        assert "label" in entity
        assert "value" in entity
        assert "span_start" in entity
        assert "span_end" in entity
        assert "context" in entity
        assert "resolution" in entity
        
        # Verify resolution structure
        resolution = entity["resolution"]
        assert "status" in resolution
        assert resolution["status"] in ["pending", "processing", "resolved", "unmatched", "ambiguous", "error"]

def test_resolve_endpoints_implemented():
    """Test that resolver endpoints are no longer HTTP 501."""
    # First create a document with entities
    doc_response = client.post("/annotate", json={
        "text": "Test entity resolution for Barack Obama.",
        "title": "Test Document"
    })
    assert doc_response.status_code == 200
    doc_data = doc_response.json()
    doc_id = doc_data["doc_id"]
    
    # Test document resolution endpoint
    resolve_response = client.post(f"/resolve/{doc_id}")
    assert resolve_response.status_code == 200
    assert resolve_response.status_code != 501  # Should not be "Not Implemented"
    
    resolve_data = resolve_response.json()
    assert "doc_id" in resolve_data
    assert "status" in resolve_data
    assert "entity_count" in resolve_data
    assert "message" in resolve_data
    
    # Test entity resolution (if entities exist)
    entities = doc_data.get("entities", [])
    if entities:
        entity_id = entities[0]["id"]
        entity_resolve_response = client.post(f"/resolve/entity/{entity_id}")
        assert entity_resolve_response.status_code == 200
        assert entity_resolve_response.status_code != 501  # Should not be "Not Implemented"
        
        entity_resolve_data = entity_resolve_response.json()
        assert "entity_id" in entity_resolve_data
        assert "value" in entity_resolve_data
        assert "label" in entity_resolve_data
        assert "resolution" in entity_resolve_data
        
        resolution = entity_resolve_data["resolution"]
        assert "status" in resolution
        assert resolution["status"] in ["resolved", "unmatched", "ambiguous", "error"]

def test_get_document_endpoint():
    """Test document retrieval endpoint."""
    # First create a document
    doc_response = client.post("/annotate", json={
        "text": "Test document retrieval.",
        "title": "Test Document"
    })
    assert doc_response.status_code == 200
    doc_id = doc_response.json()["doc_id"]
    
    # Then retrieve it
    get_response = client.get(f"/docs/{doc_id}")
    assert get_response.status_code == 200
    
    data = get_response.json()
    assert "doc_id" in data
    assert data["doc_id"] == doc_id
    assert "title" in data
    assert "entities" in data

def test_health_endpoint():
    """Test health check."""
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_readiness_endpoint():
    """Test readiness check.""" 
    response = client.get("/readyz")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] == True

def test_relations_endpoint():
    """Test relations extraction endpoint."""
    response = client.post("/relations", json={"text": "Test relations extraction."})
    assert response.status_code == 200
    data = response.json()
    assert "relations" in data
    # Relations endpoint currently returns empty list, which is expected
    assert isinstance(data["relations"], list)

def test_link_entities_endpoint_disabled():
    """Test link-entities endpoint when graph-views not configured."""
    response = client.post("/link-entities", json={
        "doc_id": "test-doc-id",
        "entities": []
    })
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    # Should return disabled when GRAPH_VIEWS_LINK_URL not configured
    assert data["status"] == "disabled"
