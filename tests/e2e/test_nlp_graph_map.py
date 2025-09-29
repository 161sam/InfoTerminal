from collections import Counter

from .utils import GraphData, MapProjector, NlpExtractor, load_fixture


def test_nlp_graph_map_flow() -> None:
    fixture = load_fixture("nlp_workflow.json")
    document = fixture["documents"][0]

    extractor = NlpExtractor()
    extraction = extractor.extract(document)

    assert len(extraction["entities"]) == len(document["expected_entities"])
    assert Counter(rel["type"] for rel in extraction["relationships"]) == Counter(
        rel["type"] for rel in document["expected_relationships"]
    )

    graph = GraphData.from_entities(
        (
            {
                "name": entity["text"],
                "type": entity["type"],
                "properties": {"confidence": entity["confidence"]},
            }
            for entity in extraction["entities"]
        ),
        extraction["relationships"],
    )

    analytics = graph.analytics()
    assert analytics["node_count"] >= len(document["expected_entities"])
    assert analytics["relationship_count"] == len(document["expected_relationships"])

    projector = MapProjector()
    feature_collection = projector.project(
        {
            "text": entity["text"],
            "type": entity["type"],
            "confidence": entity["confidence"],
        }
        for entity in extraction["entities"]
    )

    assert feature_collection["features"], "no map features projected"
    assert any(
        feature["properties"]["name"] == "Washington D.C."
        for feature in feature_collection["features"]
    )
