from .utils import DossierBuilder, GraphData, SearchEngine, ToolRegistry, load_fixture, load_seed


def test_agent_toolcall_flow() -> None:
    workflow = load_fixture("agent_toolcall_workflow.json")
    search_seed = load_seed("search_data.json")
    graph_fixture = load_fixture("graph_workflow.json")

    engine = SearchEngine(search_seed["search_entries"])
    graph = GraphData.from_fixture(graph_fixture)
    dossier_builder = DossierBuilder()
    tools = ToolRegistry(engine, graph, dossier_builder)

    context = {}
    last_result = None
    for step in workflow["plan"]:
        payload = dict(step.get("input", {}))
        referenced_context = {key: context[key] for key in step.get("context", [])}
        result = tools.dispatch(step["tool"], payload, referenced_context)
        context[step["save_as"]] = result
        last_result = result

    assert last_result is not None, "agent did not produce a dossier artefact"
    assert "markdown" in last_result

    answer = tools.final_answer(workflow["prompt"], context)
    for snippet in workflow["expected_answer_contains"]:
        assert snippet in answer
