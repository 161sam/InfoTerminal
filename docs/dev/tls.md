# TLS

`cert-manager` stellt Zertifikate über Let's Encrypt aus. Die ClusterIssuer befinden sich in `infra/k8s/cert-manager/clusterissuers.yaml`.

Beispiel-Ingress mit TLS-Patch:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: infoterminal
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
    - hosts: [ "infoterminal.example.com" ]
      secretName: infoterminal-tls
```

Domain und DNS müssen auf den Ingress-Controller zeigen.
