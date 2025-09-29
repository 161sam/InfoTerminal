from .utils import build_dashboard_metrics, ingest_feed, load_fixture


def test_feed_ingest_dashboard_flow() -> None:
    workflow = load_fixture("feed_ingest_dashboard_workflow.json")

    ingested = []
    for feed in workflow["feeds"]:
        normalized = ingest_feed(feed["entries"])
        assert len(normalized) == feed["expected_ingested"]
        ingested.append(normalized)

    metrics = build_dashboard_metrics(ingested)
    expected = workflow["dashboard_expectations"]

    assert metrics["total_items"] == expected["total_items"]
    assert metrics["regional_breakdown"] == expected["regional_breakdown"]
    for topic, count in expected["top_topics"].items():
        assert metrics["top_topics"].get(topic) == count
    assert abs(metrics["average_sentiment"] - expected["average_sentiment"]) < 0.0001
