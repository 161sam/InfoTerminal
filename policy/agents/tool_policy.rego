package agents.tool

default decision = {
    "allow": false,
    "reason": "policy_denied",
    "message": sprintf("Tool '%s' blocked for route '%s'.", [input.tool, input.route]),
}

route_matches(route) {
    route == input.route
}

route_matches(route) {
    route == "*"
}

tool_entry(entry) {
    entry := data.agents.allowed_tools[_]
    entry.tool == input.tool
}

decision = {
    "allow": true,
    "reason": entry.reason,
    "message": entry.message,
} {
    entry := data.agents.allowed_tools[_]
    entry.tool == input.tool
    route_matches(entry.route)
    not entry.effect
}

decision = {
    "allow": false,
    "reason": entry.reason,
    "message": entry.message,
} {
    entry := data.agents.allowed_tools[_]
    entry.tool == input.tool
    route_matches(entry.route)
    entry.effect == "deny"
}

decision = {
    "allow": false,
    "reason": "unknown_tool",
    "message": sprintf("Tool '%s' is not registered in policy.", [input.tool]),
} {
    not tool_entry(_)
}
