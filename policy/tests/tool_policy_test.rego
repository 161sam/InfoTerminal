package policy.tests.tool

import data.agents.tool

test_allow_dossier_build {
    decision := tool.decision with input as {"tool": "dossier.build", "route": "chat"}
    decision.allow
    decision.reason == "policy_allow"
}

test_unknown_tool_denied {
    decision := tool.decision with input as {"tool": "forbidden.tool", "route": "chat"}
    not decision.allow
    decision.reason == "unknown_tool"
}

test_route_mismatch_denied {
    decision := tool.decision with input as {"tool": "dossier.build", "route": "admin"}
    not decision.allow
    decision.reason == "policy_denied"
}
