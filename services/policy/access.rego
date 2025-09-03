package access

default allow = false

# Always allow health/metrics
allow { input.request.path == "/healthz" }
allow { input.request.path == "/readyz" }
allow { input.request.path == "/metrics" }

# Example RBAC:
viewer {
  some r
  r := input.user.roles[_]
  r == "viewer"
}
analyst {
  some r
  r := input.user.roles[_]
  r == "analyst"
}
admin {
  some r
  r := input.user.roles[_]
  r == "admin"
}

# Search: allow viewer+
allow {
  startswith(input.request.path, "/api/search")
  viewer
}

# Graph: allow analyst+
allow {
  startswith(input.request.path, "/api/graph")
  (analyst or admin)
}

# Flowise: allow analyst+
allow {
  startswith(input.request.path, "/api/flowise")
  (analyst or admin)
}
