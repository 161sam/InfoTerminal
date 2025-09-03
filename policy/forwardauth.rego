package forwardauth

default allow := false

allow if {
  input.user != ""
  startswith(input.path, "/search")
  input.roles[_] == "analyst"
}
