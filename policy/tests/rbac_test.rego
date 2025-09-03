package rbac

test_allow_public_analyst {
  input := {"user":"dev","roles":["analyst"],"action":"read","resource":{"classification":"public"}}
  allow with input as input
}
