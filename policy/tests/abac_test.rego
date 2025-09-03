package abac

test_allow_graph_read {
  input := {"action":"read","resource":{"type":"graph"}}
  allow with input as input
}
