package access

default allow = false

# --- helpers ---
levels := {"public": 0, "internal": 1, "confidential": 2, "secret": 3}

level(c) = n {
  n := levels[lower(c)]
} else = 1 {  # default "internal"
  true
}

user_clearance(u) = n {
  some r
  r := lower(u.roles[_])
  r == "admin"
  n := levels["secret"]
} else = n {
  lower(u.clearance) != ""
  n := level(u.clearance)
} else = n {
  # role-based default
  some r
  r := lower(u.roles[_])
  r == "investigator"
  n := levels["confidential"]
} else = n {
  n := levels["internal"]
}

tenant_match(u, res) {
  # if resource has a tenant, require equality; if not, pass
  not res.tenant
} else {
  u.tenant == res.tenant
}

labels_overlap(u, res) {
  some l
  res.labels[l]
  u.labels[l]
}

# --- rules ---
# Admins: everything
allow {
  input.user.roles[_] == "admin"
}

# Need-to-know via labels (bypass tenant/class if explicit label overlap)
allow {
  input.action == "read"
  labels_overlap(input.user, input.resource)
}

# Analysts: read up to clearance, same tenant (or tenant-less), public/internal by default
allow {
  input.action == "read"
  some r
  r := lower(input.user.roles[_])
  r == "analyst"
  tenant_match(input.user, input.resource)
  level(input.resource.classification) <= user_clearance(input.user)
}

# Investigators: same rule as analysts but default clearance higher
allow {
  input.action == "read"
  some r
  r := lower(input.user.roles[_])
  r == "investigator"
  tenant_match(input.user, input.resource)
  level(input.resource.classification) <= user_clearance(input.user)
}
