package forwardauth

default allow = false

# Inputs expected from Edge: user, roles, path, method, labels
allow {
  input.user != ""
  allow_path
  allow_role
}

allow_path {
  startswith(input.path, "/search")
}

allow_role {
  input.roles[_] == "analyst"
}
