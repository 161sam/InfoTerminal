import pytest

from app.main import (
    TOOL_REGISTRY,
    agent_policy_denied_total,
    agent_rate_limit_block_total,
    agent_tool_calls_total,
)


def get_counter_value(counter, **labels):
    if labels:
        metric = counter._metrics.get(tuple(labels.values()))  # type: ignore[attr-defined]
        if metric is None:
            return 0.0
        return metric._value.get()  # type: ignore[attr-defined]
    return counter._value.get()  # type: ignore[attr-defined]


@pytest.mark.anyio
async def test_tools_endpoint_returns_exact_three_tools(client):
    response = await client.get("/tools")
    assert response.status_code == 200
    data = response.json()
    assert sorted(tool["name"] for tool in data["tools"]) == sorted(TOOL_REGISTRY.keys())


@pytest.mark.anyio
async def test_chat_allowed_tool_succeeds(client):
    payload = {
        "message": "Generate a quick dossier",
        "tool": "dossier.build",
        "tool_params": {"subject": "ACME Corp"},
    }
    start_value = get_counter_value(agent_tool_calls_total, tool="dossier.build")
    response = await client.post("/chat", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["tool_call"]["tool"] == "dossier.build"
    assert body["tool_call"]["result"]["summary"].startswith("Mocked dossier.build run")
    end_value = get_counter_value(agent_tool_calls_total, tool="dossier.build")
    assert end_value == pytest.approx(start_value + 1)


@pytest.mark.anyio
async def test_chat_forbidden_tool_denied(client):
    start_value = get_counter_value(agent_policy_denied_total)
    response = await client.post(
        "/chat",
        json={"message": "hack", "tool": "video.analyze"},
    )
    assert response.status_code == 403
    end_value = get_counter_value(agent_policy_denied_total)
    assert end_value == pytest.approx(start_value + 1)


@pytest.mark.anyio
async def test_rate_limit_blocks_after_five_calls(client):
    start_value = get_counter_value(agent_rate_limit_block_total)
    payload = {
        "message": "Run dossier",
        "tool": "dossier.build",
        "tool_params": {"subject": "Case"},
    }
    for _ in range(5):
        resp = await client.post("/chat", json=payload)
        assert resp.status_code == 200
    blocked = await client.post("/chat", json=payload)
    assert blocked.status_code == 429
    end_value = get_counter_value(agent_rate_limit_block_total)
    assert end_value == pytest.approx(start_value + 1)


@pytest.mark.anyio
async def test_metrics_endpoint_exposes_counters(client):
    await client.post(
        "/chat",
        json={"message": "Run dossier", "tool": "dossier.build", "tool_params": {"subject": "Case"}},
    )
    metrics = await client.get("/metrics")
    assert metrics.status_code == 200
    text = metrics.text
    assert "agent_tool_calls_total" in text
    assert "agent_policy_denied_total" in text
    assert "agent_rate_limit_block_total" in text
