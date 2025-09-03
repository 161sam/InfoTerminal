package abac

default allow = false

allow {
  input.action == "read"
  input.resource.type == "graph"
  not deny_by_clearance
}

deny_by_clearance {
  # TODO: Clearance vs. classification durchsetzen
  false
}
