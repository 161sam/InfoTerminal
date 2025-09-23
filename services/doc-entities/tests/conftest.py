import os, sys
from pathlib import Path
import pytest
import spacy

# ensure in-memory DB and test mode to avoid external dependencies
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("ALLOW_TEST_MODE", "1")
os.environ.setdefault("OTEL_SDK_DISABLED", "1")
# enable metrics for coverage of /metrics endpoint when requested
os.environ.setdefault("IT_ENABLE_METRICS", "1")

sys.path.append(Path(__file__).resolve().parents[1].as_posix())

_CALLS = {"count": 0}

class DummyEnt:
    text = "Alice"
    label_ = "PERSON"
    start_char = 0
    end_char = 5

class DummyDoc:
    ents = [DummyEnt()]


def _fake_load(model: str):
    _CALLS["count"] += 1

    def _nlp(text: str):
        return DummyDoc()
    return _nlp


spacy.load = _fake_load  # type: ignore[assignment]


@pytest.fixture(autouse=True)
def stub_spacy(monkeypatch):
    monkeypatch.setattr("spacy.load", _fake_load)


@pytest.fixture
def spacy_calls():
    from nlp_loader import get_nlp

    get_nlp.cache_clear()
    _CALLS["count"] = 0
    yield _CALLS
