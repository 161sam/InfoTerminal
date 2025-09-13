import importlib
import sys
import types

from nlp_loader import get_nlp, ner_spacy, summarize


def test_get_nlp_cached():
    nlp1 = get_nlp("en")
    nlp2 = get_nlp("en")
    assert nlp1 is nlp2
    res = ner_spacy("Alice", "en")
    assert res[0]["label"] == "PERSON"


def test_summarize_fallback(monkeypatch):
    monkeypatch.setenv("NLP_BACKEND", "transformers")
    fake = types.SimpleNamespace(pipeline=lambda *a, **k: (_ for _ in ()).throw(Exception("boom")))
    monkeypatch.setitem(sys.modules, "transformers", fake)
    nl = importlib.reload(__import__("nlp_loader"))
    assert nl.summarize("Hello. World", "en").startswith("Hello")
