package kube.security

deny[msg] {
  input.kind == "ConfigMap"
  contains(lower(input.metadata.name), "secret")
  msg := sprintf("ConfigMap %s sieht nach Secret aus – Secrets dürfen nicht in ConfigMaps landen", [input.metadata.name])
}

deny[msg] {
  input.kind == "Deployment"
  some c
  c := input.spec.template.spec.containers[_]
  some e
  e := c.env[_]
  re_match("(?i)password|secret|key", e.name)
  e.value != ""
  msg := sprintf("Hartkodiertes Secret in %s/%s: %s", [input.metadata.namespace, input.metadata.name, e.name])
}
