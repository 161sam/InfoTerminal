package main

deny[msg] {
  input.kind == "Service"
  input.spec.type == "LoadBalancer"
  msg := sprintf("LoadBalancer not allowed for %s/%s", [input.metadata.namespace, input.metadata.name])
}
