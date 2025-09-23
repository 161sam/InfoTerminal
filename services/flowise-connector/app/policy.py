"""Agent policy engine integrating with OPA decisions."""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger("flowise-connector.policy")


@dataclass
class PolicyDecision:
    """Structured policy decision returned by OPA."""

    allow: bool
    message: str = ""
    reason: str = "policy_allow"
    raw: Dict[str, Any] = field(default_factory=dict)


class AgentPolicyEngine:
    """Thin wrapper around OPA's HTTP API for agent tool decisions."""

    def __init__(self) -> None:
        policy_path_env = os.getenv("AGENT_POLICY_PATH")
        if policy_path_env:
            self.policy_path = Path(policy_path_env)
        else:
            self.policy_path = (
                Path(__file__).resolve().parents[3]
                / "policy"
                / "agents"
                / "tool_policy.rego"
            )
        self.decision_base_url = os.getenv(
            "AGENT_OPA_URL", "http://localhost:8181/v1/data"
        )
        decision_path = os.getenv(
            "AGENT_OPA_DECISION", "agents/tool/decision"
        ).strip("/")
        self.decision_url = f"{self.decision_base_url.rstrip('/')}/{decision_path}"
        self.fail_open = os.getenv("AGENT_OPA_FAIL_OPEN", "1") == "1"
        self.enabled = os.getenv("AGENT_OPA_ENABLED", "1") != "0"
        self.timeout_seconds = float(os.getenv("AGENT_OPA_TIMEOUT", "2.0"))
        self._policy_source = self._load_policy_source()

    def _load_policy_source(self) -> Optional[str]:
        try:
            source = self.policy_path.read_text(encoding="utf-8")
            logger.info(
                "agent_policy_loaded",
                extra={
                    "policy_path": str(self.policy_path),
                    "decision_url": self.decision_url,
                },
            )
            return source
        except FileNotFoundError:
            logger.warning(
                "agent_policy_missing",
                extra={
                    "policy_path": str(self.policy_path),
                    "decision_url": self.decision_url,
                },
            )
            return None

    def authorize(
        self,
        *,
        tool: str,
        route: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> PolicyDecision:
        """Evaluate the policy for the provided tool and route."""

        if not self.enabled:
            return PolicyDecision(
                allow=True,
                message="OPA enforcement disabled (AGENT_OPA_ENABLED=0).",
                reason="policy_disabled",
            )

        payload = {"input": {"tool": tool, "route": route, "context": context or {}}}

        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.post(self.decision_url, json=payload)
                response.raise_for_status()
                decision_body = response.json()
        except Exception as exc:  # pragma: no cover - exercised via fail-open path
            logger.warning(
                "agent_policy_error",
                exc_info=exc,
                extra={"decision_url": self.decision_url},
            )
            if self.fail_open:
                return PolicyDecision(
                    allow=True,
                    message="OPA unavailable – falling back to allow.",
                    reason="policy_fail_open",
                )
            return PolicyDecision(
                allow=False,
                message="Policy engine unavailable.",
                reason="policy_unavailable",
            )

        result = decision_body.get("result", decision_body)
        if isinstance(result, dict):
            allow = bool(result.get("allow"))
            message = str(
                result.get("message")
                or ("Tool allowed." if allow else "Tool blocked by policy.")
            )
            reason = str(
                result.get("reason")
                or ("policy_allow" if allow else "policy_denied")
            )
            return PolicyDecision(
                allow=allow,
                message=message,
                reason=reason,
                raw=result,
            )

        allow = bool(result)
        return PolicyDecision(
            allow=allow,
            message="Tool allowed." if allow else "Tool blocked by policy.",
            reason="policy_allow" if allow else "policy_denied",
            raw={"allow": allow},
        )


policy_engine = AgentPolicyEngine()

__all__ = ["AgentPolicyEngine", "PolicyDecision", "policy_engine"]
