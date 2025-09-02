package access

import data.access

test_admin_can_read_anything {
  input := {"user":{"roles":["admin"]},"action":"read","resource":{"classification":"secret"}}
  access.allow with input as input
}

test_analyst_can_read_public {
  input := {"user":{"roles":["analyst"]},"action":"read","resource":{"classification":"public"}}
  access.allow with input as input
}

test_analyst_cannot_read_secret {
  input := {"user":{"roles":["analyst"]},"action":"read","resource":{"classification":"secret"}}
  not access.allow with input as input
}

test_anonymous_denied {
  input := {"user":{"roles":["anonymous"]},"action":"read","resource":{"classification":"public"}}
  not access.allow with input as input
}
