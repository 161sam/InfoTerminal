from nlp_client import ner


def test_ner_returns_entity():
    res = ner("Alice meets Bob")
    assert res and res[0]["text"] == "Alice"
