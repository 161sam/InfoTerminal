package access
default allow = false

# admins dürfen alles
allow { input.user.roles[_] == "admin" }

# analysts: read auf public
allow {
  input.user.roles[_] == "analyst"
  input.action == "read"
  input.resource.classification == "public"
}
