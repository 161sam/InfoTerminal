import pytest

from .utils import DossierBuilder, GraphData, SearchEngine, load_fixture, load_seed


@pytest.mark.parametrize("case_index", [0, 1])
def test_search_graph_dossier_flow(case_index: int) -> None:
    search_fixture = load_fixture("search_workflow.json")
    graph_fixture = load_fixture("graph_workflow.json")
    search_seed = load_seed("search_data.json")

    engine = SearchEngine(search_seed["search_entries"])
    graph = GraphData.from_fixture(graph_fixture)
    dossier_builder = DossierBuilder()

    test_case = search_fixture["test_cases"][case_index]
    results = engine.query(test_case["query"], test_case.get("filters"))

    expected = test_case["expected_results"]
    assert len(results) >= expected["min_results"], "search returned too few results"
    assert results[0].relevance_score >= expected["top_result_relevance"]
    for term in expected.get("contains_terms", []):
        haystack = (results[0].title + " " + results[0].content).lower()
        assert term.lower() in haystack

    analytics = graph.analytics()
    assert analytics["node_count"] >= graph_fixture["expected_analytics"]["min_nodes"]
    assert analytics["relationship_count"] >= graph_fixture["expected_analytics"]["min_relationships"]

    dossier = dossier_builder.build(
        focus="Federal Reserve System",
        search_results=results,
        graph=graph,
        summary_points=3,
    )

    if case_index == 0:
        assert "Federal Reserve" in dossier["summary"]
    else:
        first_term = expected["contains_terms"][0]
        assert first_term.lower() in dossier["summary"].lower()
    assert "Jerome Powell" in " ".join(dossier["sections"]["entities"])
    assert "Federal Reserve System" in dossier["markdown"]
