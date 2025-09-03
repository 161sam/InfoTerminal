package abac

default allow := false

allow if {
  input.action == "read"
  input.resource.type == "graph"
  not deny_by_clearance
}

deny_by_clearance if {
  # TODO: Clearance vs. classification durchsetzen
  false
}
