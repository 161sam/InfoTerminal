import time
import logging
from types import SimpleNamespace

import pytest

from app.main import (
    TOOL_REGISTRY,
    agent_policy_denied_total,
    agent_rate_limit_block_total,
    agent_rate_limited_total,
    agent_tool_call_failed_total,
    agent_tool_call_started_total,
    agent_tool_call_succeeded_total,
    agent_tool_calls_total,
    agent_tool_latency_seconds,
    compute_user_hash,
    global_rate_limiter,
    user_tool_rate_limiter,
)
from fastapi import HTTPException

from app.policy import PolicyDecision, policy_engine
from app.main import sanitise_message, extract_user_identifier, require_agents_enabled


def get_counter_value(counter, **labels):
    if labels:
        sample = counter.labels(**labels)
        return sample._value.get()  # type: ignore[attr-defined]
    if hasattr(counter, "_value"):
        return counter._value.get()  # type: ignore[attr-defined]
    return 0.0


@pytest.fixture(autouse=True)
def stub_policy_allow(monkeypatch):
    monkeypatch.setattr(
        policy_engine,
        "authorize",
        lambda **_: PolicyDecision(allow=True, message="allowed", reason="policy_allow"),
    )


@pytest.mark.anyio
async def test_tools_endpoint_returns_exact_six_tools(client):
    response = await client.get("/tools")
    assert response.status_code == 200
    data = response.json()
    assert sorted(tool["name"] for tool in data["tools"]) == sorted(TOOL_REGISTRY.keys())
    assert len(data["tools"]) == 6
    for tool in data["tools"]:
        assert "parameters" in tool
        assert "parameters_schema" in tool
        schema = tool["parameters_schema"]
        assert schema["type"] == "object"
        assert set(schema.get("properties", {})) == set(tool["parameters"].keys())


@pytest.mark.anyio
async def test_chat_allowed_tool_succeeds(client, caplog):
    payload = {
        "message": "Generate a quick dossier",
        "tool": "dossier.build",
        "tool_params": {"subject": "ACME Corp"},
    }
    caplog.set_level(logging.INFO, logger="flowise-connector")
    start_value = get_counter_value(agent_tool_calls_total, tool="dossier.build")
    start_started = get_counter_value(
        agent_tool_call_started_total, tool="dossier.build"
    )
    start_succeeded = get_counter_value(
        agent_tool_call_succeeded_total, tool="dossier.build"
    )
    response = await client.post("/chat", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["tool_call"]["tool"] == "dossier.build"
    assert body["tool_call"]["result"]["summary"].startswith("Mocked dossier.build run")
    end_value = get_counter_value(agent_tool_calls_total, tool="dossier.build")
    assert end_value == pytest.approx(start_value + 1)
    end_started = get_counter_value(
        agent_tool_call_started_total, tool="dossier.build"
    )
    end_succeeded = get_counter_value(
        agent_tool_call_succeeded_total, tool="dossier.build"
    )
    assert end_started == pytest.approx(start_started + 1)
    assert end_succeeded == pytest.approx(start_succeeded + 1)
    joined_logs = "\n".join(record.message for record in caplog.records)
    assert '"event":"tool_call_started"' in joined_logs
    assert '"event":"tool_call_succeeded"' in joined_logs


@pytest.mark.anyio
async def test_chat_forbidden_tool_denied(client):
    start_value = get_counter_value(agent_policy_denied_total)
    response = await client.post(
        "/chat",
        json={"message": "hack", "tool": "forbidden.tool"},
    )
    assert response.status_code == 403
    body = response.json()
    assert body["error"] == "unknown_tool"
    assert "not registered" in body["message"]
    end_value = get_counter_value(agent_policy_denied_total)
    assert end_value == pytest.approx(start_value + 1)


@pytest.mark.anyio
async def test_chat_policy_denied_response(monkeypatch, client, caplog):
    def deny(**kwargs):
        return PolicyDecision(
            allow=False,
            message="Tool blocked by compliance policy.",
            reason="policy_denied",
            raw={"allow": False},
        )

    start_value = get_counter_value(agent_policy_denied_total)
    start_failed = get_counter_value(
        agent_tool_call_failed_total, tool="dossier.build", reason="policy_denied"
    )
    caplog.set_level(logging.INFO, logger="flowise-connector")
    monkeypatch.setattr(policy_engine, "authorize", deny)
    payload = {
        "message": "Generate a quick dossier",
        "tool": "dossier.build",
        "tool_params": {"subject": "ACME Corp"},
    }
    response = await client.post("/chat", json=payload)
    assert response.status_code == 403
    body = response.json()
    assert body["error"] == "policy_denied"
    assert body["message"] == "Tool blocked by compliance policy."
    end_value = get_counter_value(agent_policy_denied_total)
    assert end_value == pytest.approx(start_value + 1)
    end_failed = get_counter_value(
        agent_tool_call_failed_total, tool="dossier.build", reason="policy_denied"
    )
    assert end_failed == pytest.approx(start_failed + 1)
    joined_logs = "\n".join(record.message for record in caplog.records)
    assert '"event":"tool_call_failed"' in joined_logs
    assert '"reason":"policy_denied"' in joined_logs


@pytest.mark.anyio
async def test_rate_limit_blocks_after_five_calls(client):
    headers = {"X-User-Id": "global-tester"}
    user_hash = compute_user_hash(headers["X-User-Id"])
    start_total = get_counter_value(
        agent_rate_limited_total,
        scope="global",
        tool="dossier.build",
        user_hash=user_hash,
    )
    start_legacy = get_counter_value(agent_rate_limit_block_total)
    payload = {
        "message": "Run dossier",
        "tool": "dossier.build",
        "tool_params": {"subject": "Case"},
    }
    for _ in range(5):
        resp = await client.post("/chat", json=payload, headers=headers)
        assert resp.status_code == 200
    blocked = await client.post("/chat", json=payload, headers=headers)
    assert blocked.status_code == 429
    end_total = get_counter_value(
        agent_rate_limited_total,
        scope="global",
        tool="dossier.build",
        user_hash=user_hash,
    )
    assert end_total == pytest.approx(start_total + 1)
    end_legacy = get_counter_value(agent_rate_limit_block_total)
    assert end_legacy == pytest.approx(start_legacy + 1)


@pytest.mark.anyio
async def test_user_tool_rate_limit_blocks_per_user(client):
    headers = {"X-User-Id": "per-user"}
    user_hash = compute_user_hash(headers["X-User-Id"])
    global_rate_limiter.max_calls = 100
    global_rate_limiter.reset()
    user_tool_rate_limiter.max_calls = 5
    user_tool_rate_limiter.reset()
    start_value = get_counter_value(
        agent_rate_limited_total,
        scope="user_tool",
        tool="dossier.build",
        user_hash=user_hash,
    )
    payload = {
        "message": "Run dossier",
        "tool": "dossier.build",
        "tool_params": {"subject": "Case"},
    }
    for _ in range(5):
        resp = await client.post("/chat", json=payload, headers=headers)
        assert resp.status_code == 200
    blocked = await client.post("/chat", json=payload, headers=headers)
    assert blocked.status_code == 429
    end_value = get_counter_value(
        agent_rate_limited_total,
        scope="user_tool",
        tool="dossier.build",
        user_hash=user_hash,
    )
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
    assert "agent_rate_limited_total" in text
    assert "agent_tool_latency_seconds" in text


def test_sanitise_message_validation():
    with pytest.raises(HTTPException):
        sanitise_message("   \n\t")
    long_text = "a" * 2105
    result = sanitise_message(long_text)
    assert len(result) == 2000


def test_extract_user_identifier_fallbacks():
    request = SimpleNamespace(headers={"Authorization": "Bearer token"}, client=None)
    assert extract_user_identifier(request) == "Bearer token"
    request = SimpleNamespace(headers={}, client=SimpleNamespace(host="tester"))
    assert extract_user_identifier(request) == "tester"
    request = SimpleNamespace(headers={}, client=None)
    assert extract_user_identifier(request) == "anonymous"


def test_global_rate_limiter_evicts_old_entries():
    global_rate_limiter.reset()
    global_rate_limiter._events.append(time.monotonic() - global_rate_limiter.window_seconds - 1)
    global_rate_limiter.check(user_hash="hash", tool="dossier.build")
    assert len(global_rate_limiter._events) == 1


def test_user_tool_rate_limiter_evicts_old_entries():
    user_tool_rate_limiter.reset()
    key = ("hash", "dossier.build")
    user_tool_rate_limiter._events[key].append(
        time.monotonic() - user_tool_rate_limiter.window_seconds - 1
    )
    user_tool_rate_limiter.check(user_hash="hash", tool="dossier.build")
    assert len(user_tool_rate_limiter._events[key]) == 1


@pytest.mark.anyio
async def test_health_ready_info_and_cancel_endpoints(client):
    health = await client.get("/healthz")
    assert health.status_code == 200
    ready = await client.get("/readyz")
    assert ready.status_code == 200
    info = await client.get("/info")
    assert info.status_code == 200
    cancel = await client.post("/chat/123/cancel")
    assert cancel.status_code == 200


@pytest.mark.anyio
async def test_missing_required_parameter_returns_400(client):
    payload = {"message": "Run dossier", "tool": "dossier.build", "tool_params": {}}
    response = await client.post("/chat", json=payload)
    assert response.status_code == 400


def test_require_agents_disabled(monkeypatch):
    monkeypatch.setenv("AGENTS_ENABLED", "0")
    with pytest.raises(HTTPException):
        require_agents_enabled()
