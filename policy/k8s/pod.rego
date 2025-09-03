package k8s.policies

deny[msg] if {
  input.kind == "Pod"
  input.spec.containers[_].securityContext.privileged == true
  msg := "Privileged container forbidden"
}
