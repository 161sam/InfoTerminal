package access

import data.access

# admin can read any tenant/classification
test_admin_all {
  input := {"user":{"roles":["admin"],"tenant":"A"}, "action":"read", "resource":{"tenant":"B","classification":"secret"}}
  access.allow with input as input
}

# analyst same tenant, internal -> allowed
test_analyst_same_tenant_internal {
  input := {"user":{"roles":["analyst"],"tenant":"A"}, "action":"read", "resource":{"tenant":"A","classification":"internal"}}
  access.allow with input as input
}

# analyst different tenant -> denied
test_analyst_other_tenant_denied {
  input := {"user":{"roles":["analyst"],"tenant":"A"}, "action":"read", "resource":{"tenant":"B","classification":"internal"}}
  not access.allow with input as input
}

# investigator: default clearance confidential → can read confidential in same tenant
test_investigator_confidential_allowed {
  input := {"user":{"roles":["investigator"],"tenant":"A"}, "action":"read", "resource":{"tenant":"A","classification":"confidential"}}
  access.allow with input as input
}

# need-to-know label bypass (labels overlap)
test_need_to_know_label_bypass {
  input := {
    "user":{"roles":["analyst"],"tenant":"A","labels":{"case:42":true}},
    "action":"read",
    "resource":{"tenant":"B","classification":"secret","labels":{"case:42":true}}
  }
  access.allow with input as input
}

# public without tenant should be readable for analyst with internal clearance
test_public_no_tenant_allowed {
  input := {"user":{"roles":["analyst"],"tenant":"A"}, "action":"read", "resource":{"classification":"public"}}
  access.allow with input as input
}

# analyst with explicit higher clearance can read confidential
test_analyst_with_clearance_confidential {
  input := {"user":{"roles":["analyst"],"tenant":"A","clearance":"confidential"}, "action":"read", "resource":{"tenant":"A","classification":"confidential"}}
  access.allow with input as input
}
