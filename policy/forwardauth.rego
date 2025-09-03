package forwardauth

default allow = false

allow {
  input.user != ""
  startswith(input.path, "/search")
  some i
  r := input.roles[i]
  r == "analyst"
}
