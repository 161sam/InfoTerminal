package access

default allow = false

allow {
  input.user.roles[_] == "admin"
}

allow {
  input.user.roles[_] == "analyst"
  input.action == "read"
  input.resource.classification in {"public","internal"}
}
