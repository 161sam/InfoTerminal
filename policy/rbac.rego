package rbac

default allow = false

allow {
  input.action == "read"
  input.resource.classification == "public"
  input.user != ""
  some r; r = input.roles[_]; r == "analyst"
}
