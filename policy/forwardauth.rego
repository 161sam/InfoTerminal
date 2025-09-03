package forwardauth

default allow = false

allow {
  input.user != ""
  startswith(input.path, "/search")
  some r; r = input.roles[_]; r == "analyst"
}
