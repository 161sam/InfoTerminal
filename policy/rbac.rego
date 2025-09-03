package rbac

default allow = false

allow {
  # example RBAC: analyst can read public resources
  input.action == "read"
  input.resource.classification == "public"
  input.user != ""
  input.roles[_] == "analyst"
}
