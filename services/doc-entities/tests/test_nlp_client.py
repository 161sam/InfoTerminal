from nlp_client import ner


def test_ner_handles_error(monkeypatch):
    monkeypatch.setenv("NLP_URL", "http://0.0.0.0:1")
    assert ner("Alice") == []
