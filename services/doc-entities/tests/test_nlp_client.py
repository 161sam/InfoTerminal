import sys, pathlib, requests
import pytest

sys.path.append(pathlib.Path(__file__).resolve().parents[1].as_posix())
from nlp_client import ner


def test_ner_fallback(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.RequestException("boom")
    monkeypatch.setattr(requests, "post", fake_post)
    assert ner("Hello") == []
