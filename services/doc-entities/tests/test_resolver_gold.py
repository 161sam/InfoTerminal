"""Gold-sample regression tests for entity linking and relations."""

import os
import sys
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

SERVICE_ROOT = Path(__file__).resolve().parents[1]
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))


@pytest.fixture(scope="module")
def db_setup():
    os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    os.environ.setdefault("ALLOW_TEST_MODE", "1")
    from db import engine
    from models import Base

    Base.metadata.create_all(bind=engine)
    yield


def test_resolver_alias_gold_sample(db_setup):
    """Alias matching should resolve Barack Obama to the canonical node."""

    from db import SessionLocal
    from models import Document, Entity, EntityResolution
    from resolver import resolve_entities

    doc_id = uuid.uuid4()
    with SessionLocal() as session:
        session.add(Document(id=doc_id, title="Test Doc"))
        entity = Entity(
            doc_id=doc_id,
            label="PERSON",
            value="Barack Obama",
            span_start=0,
            span_end=12,
            confidence=0.99,
        )
        session.add(entity)
        session.commit()
        entity_id = str(entity.id)

    results = resolve_entities([entity_id], mode="gold")
    assert results, "resolver should return payloads"
    payload = results[0]
    assert payload["status"] == "resolved"
    assert payload["node_id"] == "person:barack-obama"
    assert payload["score"] >= 0.9
    assert payload["candidates"], "resolver should surface candidate list"

    with SessionLocal() as session:
        stored = session.get(EntityResolution, uuid.UUID(entity_id))
        assert stored is not None
        assert stored.status == "resolved"
        assert stored.node_id == "person:barack-obama"
        assert stored.score >= 0.9


def test_annotation_metadata_exposes_linking_counts():
    """Annotate endpoint should surface linking metadata and statuses."""

    from app import app

    payload = {
        "text": "Barack Obama met Donald Trump in Berlin.",
        "language": "en",
        "extract_entities": True,
        "extract_relations": True,
        "generate_summary": False,
        "resolve_entities": True,
    }

    with TestClient(app) as client:
        response = client.post("/v1/documents/annotate", json=payload)
        assert response.status_code == 200
        body = response.json()

    assert any(ent.get("resolution_status") == "pending" for ent in body["entities"])
    metadata = body["metadata"]
    assert "linking_status_counts" in metadata
    assert metadata["linking_status_counts"]["pending"] >= 1
    assert "linking_pending" in metadata


def test_nlp_loader_stubbed(spacy_calls, monkeypatch):
    """Ensure the nlp_loader helpers use the stubbed spaCy backend and cache."""

    from nlp_loader import get_nlp, ner_spacy, summarize

    results = ner_spacy("Alice went to Berlin.", "en")
    assert results == [{"text": "Alice", "label": "PERSON", "start": 0, "end": 5}]
    assert spacy_calls["count"] == 1

    # Cached call should not trigger another spaCy load
    ner_spacy("Another text", "en")
    assert spacy_calls["count"] == 1

    cached_nlp = get_nlp("en")
    assert callable(cached_nlp)

    # Summarize should fall back to naive implementation when transformers disabled
    summary = summarize("Sentence one. Sentence two.", "en")
    assert isinstance(summary, str) and summary

    # Exercise optional transformers branch and ensure graceful fallback
    try:
        import transformers as hf_transformers

        monkeypatch.setattr(
            hf_transformers,
            "pipeline",
            lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom")),
        )
    except ImportError:
        import sys
        from types import SimpleNamespace

        fake_transformers = SimpleNamespace(
            pipeline=lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom"))
        )
        monkeypatch.setitem(sys.modules, "transformers", fake_transformers)
    monkeypatch.setattr("nlp_loader.BACKEND", "transformers")
    transformed = summarize("Sentence one. Sentence two.", "en")
    assert isinstance(transformed, str) and transformed

