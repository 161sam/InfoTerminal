# Kubernetes Deployment mit Helm

Dieser Quickstart beschreibt die neuen Helm-Artefakte unter `deploy/helm/` und zeigt, wie Sie einen InfoTerminal-Dienst als Ausgangspunkt auf einem Kubernetes-Cluster ausrollen.

## Voraussetzungen

- Kubernetes-Cluster (lokal via kind/minikube oder Remote-Cluster)
- [Helm 3](https://helm.sh/)
- Optional: Prometheus-Stack, falls der `ServiceMonitor` genutzt werden soll

## Struktur des Charts

```
deploy/helm/infoterminal/
├─ Chart.yaml                # Metadaten des Charts
├─ values.yaml               # Standardwerte (Image, Service, Probes, Ingress)
└─ templates/
   ├─ _helpers.tpl           # Namens- und Label-Hilfsfunktionen
   ├─ configmap.yaml         # Optionale ConfigMaps über `values.configMaps`
   ├─ deployment.yaml        # Deployment mit Liveness/Readiness Probes
   ├─ ingress.yaml           # Optionaler Ingress (`values.ingress.enabled`)
   ├─ secret.yaml            # Optionales Secret (`values.secrets.*`)
   ├─ service.yaml           # Service (ClusterIP standardmäßig)
   ├─ serviceaccount.yaml    # ServiceAccount (abschaltbar)
   └─ servicemonitor.yaml    # Optionales Prometheus CRD
```

## Werte anpassen

1. Erstellen Sie eine eigene Werte-Datei, z. B. `values.prod.yaml`:

   ```yaml
   image:
     repository: ghcr.io/infoterminal/gateway
     tag: "v0.2.0"

   env:
     - name: GATEWAY_PORT
       value: "8080"

   probes:
     readiness:
       path: /readyz
     liveness:
       path: /healthz

   ingress:
     enabled: true
     className: traefik
     hosts:
       - host: gateway.example.local
         paths:
           - path: /
             pathType: Prefix
             servicePort: http
   ```

2. Hinterlegen Sie vertrauliche Werte getrennt in einer zweiten Datei, z. B. `values.secrets.yaml`:

   ```yaml
   secrets:
     enabled: true
     stringData:
       OAUTH_CLIENT_SECRET: "<geheim>"
   ```

   > ⚠️ Speichern Sie diese Datei nicht im Repository und nutzen Sie z. B. `sops` oder einen Secret-Manager.

## Installation

```bash
helm dependency update deploy/helm/infoterminal  # optional, sobald Dependencies bestehen
helm lint deploy/helm/infoterminal
helm upgrade --install infoterminal deploy/helm/infoterminal \
  --namespace infoterminal --create-namespace \
  --values values.prod.yaml \
  --values values.secrets.yaml
```

## Smoke-Test

```bash
kubectl -n infoterminal get pods
kubectl -n infoterminal get svc
```

Sobald der Pod im Status `Running` ist und die Readiness-Probe grün meldet, sollten Requests über den Service (oder Ingress) erreichbar sein.

## Weiteres Vorgehen

- Ergänzen Sie komponentenspezifische Umgebungsvariablen in `values.yaml`.
- Aktivieren Sie `serviceMonitor`, wenn Prometheus Metriken einsammeln soll.
- Fügen Sie zusätzliche Templates (z. B. `HorizontalPodAutoscaler`) hinzu, sobald Lasttests erforderlich sind.
