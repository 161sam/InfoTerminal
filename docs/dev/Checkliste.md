# Status auf einen Blick
<!-- markdownlint-disable MD013 MD059 MD026 MD024 -->

* **Dev-Infra (Kind + Helmfile + Basisdienste)** — ✅ lauffähig (Postgres, OpenSearch, MinIO, Traefik, Keycloak)
* **Auth & Gateway** — 🟨 Keycloak-Realm/Clients vorhanden; Edge-OIDC via oauth2-proxy + OPA-ForwardAuth lauffähig; Feinschliff (Role Claims, Secrets) offen
* **OPA** — 🟨 Policies (ForwardAuth, RBAC, ABAC), Tests (opa test) und Bundle-Modus vorhanden; noch Feinschliff für Service-Inputs & CI Gate Coverage
* **Search** — ✅ Search-API (FastAPI) + Facetten + Frontend-Suche (Next.js)
* **Graph** — ✅ Graph-API (Neo4j) + Viewer (Basis & GraphX mit Expand/Pin/Save); Server-Side Views (CRUD + Share) ✅
* **AI Layer & Agents** — 🟨 NLP-Service (NER/Summary) erreichbar; Agent-Flows offen
* **Dokumentenmanagement (Aleph)** — 🟨 Aleph UI + Worker/Redis laufen; kein automatischer NiFi-Ingest, keine NER-Crosslinks im Viewer
* **ETL** — 🟨 NiFi UI + Registry stehen; Demo-Template deployed; Airflow via Helm + DAG-ConfigMap ✅; KPO-DAG + CronJob für OpenBB 🟨 (Image/secret polishing)
* **Analytics** — 🟨 Superset Helm + OIDC + Preset-Job + dbt→Superset Sync; RLS-Beispiel (Gamma) gesetzt; weitere Datasets/Charts offen
* **Datenmodell** — 🟨 dbt Staging/Dim/Fact/Returns + Seeds vorhanden; weitere Modelle/Tests/Docs offen
* **OpenBB** — 🟨 Connector (lokal/K8s-Cron), Symbols konfigurierbar; ClickHouse-Pfad optional offen (aktuell PG)
* **CI/CD & Policy Gate** — 🟨 GH Actions: CI minimal + Conftest Gate; Image Scans / e2e Tests offen
* **Observability** — ⬜️ Otel/Prom/Grafana/Loki noch nicht integriert

---

## Checkliste (End-to-End)

## 1) Grundbetrieb & Seed

* [ ] `make dev-up` läuft fehlerfrei
  *Check:* `kubectl get pods -A` → alle Deployments „Running“
* [ ] Seeds ausgeführt
  *Befehle:* `make seed-demo` · `make seed-graph`
* [ ] Apps lokal gestartet
  *Befehl:* `make apps-up` → Frontend [localhost:3000](http://localhost:3000)

## 2) Auth / Edge-OIDC / OPA

* [ ] Keycloak Realm importiert
  *Befehl:* `make auth-up` (admin/adminadmin lokal)
* [ ] oauth2-proxy erreichbar
  *URL:* [auth.127.0.0.1.nip.io](http://auth.127.0.0.1.nip.io)
* [ ] OPA ForwardAuth aktiv
  *Test:* `curl -I http://search.127.0.0.1.nip.io/search?q=info` → `401` wenn nicht eingeloggt, `200` mit Session
* [ ] OPA Tests grün
  *Befehl:* `make opa-test`
* [ ] OPA Bundle geladen
  *Befehle:* `make opa-bundle && make bundle-server-up` · `kubectl -n policy rollout restart deploy/opa`

## 3) Search + Facetten + OPA

* [ ] Search-API Health
  *URL:* [127.0.0.1:8001](http://127.0.0.1:8001/healthz)
* [ ] Faceted Search UI liefert Treffer
  *URL:*  [localhost:3000](http://localhost:3000) · Query „InfoTerminal“
* [ ] OPA-Enforcement (Gateway-Variante)
  *URL:* [search.127.0.0.1.nip.io](http://search.127.0.0.1.nip.io/search?q=info)

## 4) Graph

* [ ] Graph-API Health
  *URL:* [127.0.0.1:8002](http://127.0.0.1:8002/healthz)
* [ ] Graph Viewer Basis
  *URL:* [localhost:3000](http://localhost:3000/graph)
* [ ] GraphX (Expand/Pin/Save)
  *URL:* [localhost:3000](http://localhost:3000/graphx)
* [ ] Graph Views Service (CRUD + Share)
  *URL:* [127.0.0.1:8004](http://127.0.0.1:8004/healthz)
  *Flow:* Save Server → List → Load funktioniert

## 5) Aleph (Docs)

* [ ] Aleph UI erreichbar (via Edge-OIDC + OPA)
  *URL:* [aleph.127.0.0.1.nip.io](http://aleph.127.0.0.1.nip.io)
* [ ] Worker & Ingestor laufen
  *Check:* `kubectl -n docs get pods` → `aleph`, `aleph-worker`, `aleph-ingestor`, `redis` Running
* [ ] Test-Upload & Suche ok (manuell via UI)

## 6) NiFi & Registry

* [ ] NiFi UI erreichbar
  *URL:* [nifi.127.0.0.1.nip.io](http://nifi.127.0.0.1.nip.io)
* [ ] NiFi Registry erreichbar & verbunden
  *URL:* [nifi-registry.127.0.0.1.nip.io](http://nifi-registry.127.0.0.1.nip.io)
  *Befehl:* `bash infra/nifi/scripts/connect-registry.sh`
* [ ] Demo-Template instanziert & läuft
  *Befehl:* `bash infra/nifi/scripts/upload-template.sh`

## 7) Airflow + Jobs

* [ ] Airflow UI erreichbar
  *URL:* [localhost:8084](http://localhost:8084)
* [ ] DAGs sichtbar (`openbb_equities_daily`, `openbb_kpo_daily`)
  *Check:* Airflow UI → Activate
* [ ] OpenBB CronJob (K8s) lädt Daten

### Befehle

  `kind load docker-image openbb-connector:local --name infoterminal`
  `kubectl -n openbb create job --from=cronjob/openbb-prices-daily openbb-test`
  `kubectl -n openbb logs job/openbb-test -f`

## 8) dbt Modelle & Tests

* [ ] dbt deps/seed/run/test grün

### Befehle:

  `cd etl/dbt && dbt deps && dbt seed && dbt run && dbt test`

* [ ] Modelle vorhanden: `stg_openbb_prices`, `dim_asset`, `fct_eod_prices`, `fct_returns_daily`, `dim_asset_enriched`

## 9) AI Layer & Agents

*Mini-Blueprint:* FastAPI-Service (`services/nlp-service`) für NER/Embeddings/Summary + optionale `/resolve`-Route; n8n/Flowise für Agent-Flows.

* [ ] `services/nlp-service` deployen (NER, Embed, Summarize)
  *Befehl:* `uv run --python 3.11 -q --directory services/nlp-service uvicorn app:app --port 8003`
* [ ] NLP-Service Health
  *URL:* [127.0.0.1:8003](http://127.0.0.1:8003/healthz)
* [ ] Search-Rerank aktivieren (Cosine Top-N)
    *Env:* `export RERANK=1 NLP_URL=http://127.0.0.1:8005`
* [ ] Entity-Resolver `/resolve` aktiv
  *URL:* `[127.0.0.1:8005](http://127.0.0.1:8005/resolve)`
* [ ] Frontend: `/docs` Upload & NER-Highlights testen
  *Flow:* Text eingeben → Annotieren → Entitäten erscheinen
* [ ] n8n Flow „Investigation Assistant“

### Snippet

  ```json
  {
    "name":"Investigation Assistant",
    "nodes":[{"id":"webhook","type":"n8n-nodes-base.webhook"}]
  }
  ```

* [ ] n8n Flow „Financial Risk Assistant“ (OpenBB + Sanktionsliste)
* [ ] (Optional) Flowise Agent mit HTTP-Tools auf Search/Graph/NLP

## 10) Dokumentenmanagement (Aleph)

*Mini-Blueprint:* NiFi → Aleph Upload, Aleph Worker für OCR/LID, Batch-Script verknüpft NER mit Graph.

* [ ] NiFi Flow: ListenFile → PutAleph (Upload)

### Snippet

  ```bash
  HTTP Method: POST
  Content-Type: application/octet-stream
  ```

* [ ] OCR/Language-ID über Aleph Worker aktiv
  *Check:* `kubectl -n docs get pods`
* [ ] NER→Graph Crosslinks patchen

### Snippet

  ```python
  ents = requests.post(f"{NLP}/ner", {"text":txt}).json()["ents"]
  ```

## 11) Superset (OIDC, Preset, dbt-Sync)

* [ ] OIDC Login via Edge (oder direkt) klappt
  *URL:* [superset.127.0.0.1.nip.io](http://superset.127.0.0.1.nip.io)
* [ ] Preset-Job gelaufen (Dashboard „OpenBB Overview“)
  *Check:* `kubectl -n analytics logs job/superset-preset`
* [ ] dbt→Superset Sync ok
  *Lokal:* `python3 infra/analytics/superset_dbt_sync.py`
  *K8s Job:* `kubectl apply -f infra/k8s/analytics/superset-dbt-sync-job.yaml`
* [ ] RLS-Beispiel aktiv (Gamma sieht nur `SAP.DE`)
  *Check:* `kubectl -n analytics logs job/superset-rls`

## 12) CI/CD & Policy Gate

* [ ] CI durchläuft (Python/Node Checks)
  *Check:* GitHub Actions „ci“ Pipeline
* [ ] Conftest Gate prüft K8s-Manifeste
  *Check:* Action „policy-gate“ grün

## 13) Housekeeping & Security

* [ ] Secrets: Dummy-Passwörter durch sichere Werte ersetzt (Keycloak admin, oauth2-proxy cookie secret, DB-Passwörter)
* [ ] TLS/Ingress: Dev okay, Prod-Pfad (LetsEncrypt/Cert-Manager) geplant
* [ ] Backups: PG/OpenSearch/Neo4j (Dev: optional; Prod: definieren)

---

## Quick Verifications (Copy/Paste)

```bash
# Core health
kubectl get pods -A
curl -s http://127.0.0.1:8001/healthz
curl -s http://127.0.0.1:8002/healthz
curl -s http://127.0.0.1:8004/healthz
make opa-test
```

---

## Nächste 7 Tage – Fokusvorschlag

1. **Security sweep**
   ⬜️ Secrets rotieren · ⬜️ OPA Inputs pro Service vereinheitlichen (tenant/labels/classification) · ⬜️ Traefik mTLS (intern) optional.
2. **Data quality**
   ⬜️ dbt docs & exposures · ⬜️ zusätzliche Tests (unique, accepted\_values) · ⬜️ Snapshotting (SCD2) für `dim_asset`.
3. **Analytics UX**
   ⬜️ Superset: weitere Charts (OHLC, Returns, Volume), Native-Filters & Cross-Filters · ⬜️ Dashboard Links zu Graph/Docs.
4. **Pipelines**
   ⬜️ Airflow: OpenBB KPO mit dbt-Run & Superset-Sync als Task-Kette · ⬜️ NiFi Flow für Aleph Uploads (PutHTTP → Aleph).
5. **Observability**
   ⬜️ Otel Collector + basic traces in Search/Graph APIs · ⬜️ Prom Exporter (PG/OS/Neo4j) + Grafana Dashboards.
6. **Docs & DX**
   ⬜️ README Quickstart aktualisieren · ⬜️ ADR zu OPA-ABAC · ⬜️ Runbook „Auth & Gateway“.

---

## Bekannte Lücken / Risiken

* **Prod-Härte:** TLS, HPA, PDBs, Requests/Limits, Backups/Restore – noch Dev-Default.
* **Lizenz & Datenquellen:** OpenBB/3P terms prüfen; Klassifizierung & RLS/OPA abstimmen.
* **Search Relevanz:** BM25-Tuning/Embeddings-Rerank später ergänzen.
* **Multi-Tenant UX:** RLS in Superset ist begrenzt; OPA bleibt „source of truth“ für APIs.

---
<!-- markdownlint-enable MD013 MD059 MD026 MD024 -->
