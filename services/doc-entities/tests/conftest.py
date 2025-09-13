import os, sys
from pathlib import Path
import pytest

# ensure in-memory DB and test mode to avoid external dependencies
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("ALLOW_TEST_MODE", "1")
os.environ.setdefault("OTEL_SDK_DISABLED", "1")
# enable metrics for coverage of /metrics endpoint when requested
os.environ.setdefault("IT_ENABLE_METRICS", "1")

sys.path.append(Path(__file__).resolve().parents[1].as_posix())

class DummyEnt:
    text = "Alice"
    label_ = "PERSON"
    start_char = 0
    end_char = 5

class DummyDoc:
    ents = [DummyEnt()]


def _fake_load(model: str):
    def _nlp(text: str):
        return DummyDoc()
    return _nlp


@pytest.fixture(autouse=True)
def stub_spacy(monkeypatch):
    monkeypatch.setattr("spacy.load", _fake_load)
