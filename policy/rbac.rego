package rbac

default allow := false

allow if {
  input.action == "read"
  input.resource.classification == "public"
  input.user != ""
  input.roles[_] == "analyst"
}
