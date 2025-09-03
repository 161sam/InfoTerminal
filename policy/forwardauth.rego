package forwardauth

default allow = false

allow {
  input.user != ""
  startswith(input.path, "/search")
  input.roles[_] == "analyst"
}
