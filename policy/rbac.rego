package rbac

default allow = false

allow {
  input.action == "read"
  input.resource.classification == "public"
  input.user != ""
  some i
  r := input.roles[i]
  r == "analyst"
}
