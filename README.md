# InfoTerminal

> **Modulares Open-Source-Framework für Datenintegration, Suche, Graph-Analyse, Dokumentenmanagement & KI – inspiriert von Palantir Gotham.**

[![Status](https://img.shields.io/badge/status-v0.1.0--pre-blue)](#) [![License](https://img.shields.io/badge/license-Apache--2.0-green)](#) [![K8s](https://img.shields.io/badge/kubernetes-ready-326ce5)](#) [![Python](https://img.shields.io/badge/python-3.10%2B-yellow)](#) [![Made with Love](https://img.shields.io/badge/made%20with-love-ff69b4.svg)](#)

---

## 🎯 Ziel

**InfoTerminal** liefert die Bausteine einer “Gotham-ähnlichen” Plattform – vollständig mit Open-Source-Technologien:

* **Datenintegration (Batch & Stream)** aus Dateien, APIs und Datenbanken
* **Volltextsuche** über große Text- & Metadatensammlungen
* **Graph-/Beziehungsanalyse** über Entitäten & Ereignisse
* **Dokumentenmanagement** inkl. OCR/NER & Cross-Links
* **Visualisierung** mit Dashboards, Charts & interaktiven Graphen
* **KI-Layer** (NLP, Summaries, Embeddings, Agents)
* **Security & Governance** (OIDC/RBAC/ABAC, Audit, RLS)

---

## 🧱 Architektur (Kurzüberblick)

```
 Benutzer (Analysten, Ermittler, Data Scientists)
                │
     ┌──────────┴──────────┐
     │  Web-UI (Next.js)   │  — React-Komponenten: Suche, Docs, Graph
     └──────────┬──────────┘
            Ingress / API-Gateway (Traefik + oauth2-proxy + OPA)
 ┌──────────────┼─────────────────────────────────────────────────────┐
 │        Backend Microservices (FastAPI)                             │
 │  - search-api     (OpenSearch)   Volltext + Facetten + Reranking   │
 │  - graph-api      (Neo4j)        Neighbours, Shortest Path         │
 │  - doc-entities   (Postgres)     NER-Annotation & Links            │
 │  - nlp-service    (NLP)          NER, Resolve, Summaries           │
 │  - openbb-connector (ETL)        Markt-/Makrodaten → DW/DBT        │
 └──────────────┼─────────────────────────────────────────────────────┘
        ETL/Orchestrierung: Apache NiFi, Apache Airflow, dbt
      Storage/Index: Postgres • OpenSearch • Neo4j • MinIO (S3)
     Dokumenten-Analyse: Aleph (OCR, Ingest, Explore, Index)
        Visualisierung: Apache Superset (Dashboards, RLS)
          KI/Agents: Flowise (LLM-Tools) • n8n (Workflows)
               Observability: Prometheus/Grafana • OTel
```

---

## ✅ Features (v0.1.0 – MVP)

* **Suche:** REST-API auf OpenSearch (Query, Filter, Facetten) + UI-Suche
* **Graph:** REST-API auf Neo4j (Nachbarschaft, kürzeste Pfade) + interaktiver Graph-Viewer
* **Dokumente:** Aleph integriert; Doc-Annotation-Service für NER/Links vorbereitet
* **ETL/Analytics:** Airflow-DAGs + dbt-Modelle + Superset-Dashboard (Beispiel)
* **Security (Dev-Modus):** Keycloak-Login (OIDC), OPA-ForwardAuth Policies
* **Dev-Cluster:** Reproduzierbare lok. Umgebung (Docker/K8s) & Make-Targets

> **In Arbeit**: NLP-Service (NER/Resolve/Summary), NiFi→Aleph Auto-Ingest, Embedding-Reranking, Flowise-Agent, RLS-Beispiele, Observability-Stack

---

## 🚀 Schnellstart (Dev)

Voraussetzungen: **Docker**, **kubectl**, **helm**, **make** (optional: **kind**)

```bash
# 1) Dev-Stack booten (K8s-Local mit Basiskomponenten)
make dev-up        # installiert: Traefik, Keycloak, Postgres, OpenSearch, Neo4j, MinIO, Aleph, Superset, Airflow, NiFi

# 2) Services deployen
make services-up   # FastAPI Microservices builden/deployen (search-api, graph-api, doc-entities, …)

# 3) Frontend starten (lokal)
make web-up        # Next.js Dev-Server (alternativ: npm run dev im web/)

# 4) Zugänge (Dev-Defaults)
# - Web-UI:          http://localhost:3000
# - Keycloak:        http://localhost:8081 (Realm: info-terminal)
# - Aleph UI:        http://localhost:8082
# - Superset:        http://localhost:8083
# - Airflow UI:      http://localhost:8084
# - NiFi UI:         http://localhost:8085
# - MinIO Console:   http://localhost:9001
```

> **Hinweis:** Die Port-URLs können je nach Setup variieren. Siehe `docs/dev/checklist.md` / `.env.example`.

---

## 🔌 Wichtige Endpunkte (Beispiele)

```http
# Suche
GET /api/search?q=acme&entity_type=Organization&limit=20

# Graph
GET /api/graph/neighbors?id=O:acme&limit=20
GET /api/graph/shortest_path?src=P:alice&dst=O:acme

# Dokument-Annotation
POST /api/docs/annotate  { "text": "...", "meta": {...} }
GET  /api/docs/{id}
GET  /api/docs/{id}/html

# Health
GET /api/*/healthz
```

---

## 🧰 Tech-Stack

* **UI:** Next.js (React), interaktiver Graph-Viewer, integrierte Suche/Docs
* **APIs:** FastAPI-Microservices (Python 3.10+), OpenAPI, OTel
* **Search:** OpenSearch (Elasticsearch-kompatibel)
* **Graph:** Neo4j (Knowledge Graph, Beziehungen)
* **DW/DB:** Postgres (OLTP/DW; optional ClickHouse für große Zeitreihen)
* **Docs:** Aleph (OCR/Index/Explore), MinIO (S3 Storage)
* **ETL/Orchestration:** Apache NiFi, Apache Airflow, **dbt**
* **Dashboards:** Apache Superset (OIDC, RLS möglich)
* **KI/Agents:** NLP-Service (spaCy/Transformers), Flowise (LLM Tools), n8n (Workflows)
* **Security:** Keycloak (OIDC), oauth2-proxy, **OPA** (ABAC)
* **Ops:** Kubernetes/Helm, Prometheus/Grafana, OpenTelemetry

---

## 📚 Verzeichnisstruktur (vereinfacht)

```
/docs                # Handbücher, Checklisten, ADRs
/web                 # Next.js Frontend
/services
  /search-api        # FastAPI + OpenSearch
  /graph-api         # FastAPI + Neo4j
  /doc-entities      # FastAPI + Postgres (NER-Links, HTML-Render)
  /nlp-service       # (geplant) NER/Resolve/Summary
  /openbb-connector  # ETL für Markt-/Makrodaten
/etl
  /airflow           # DAGs
  /dbt               # Modelle, Seeds, Tests
  /nifi              # Templates/Flows
/deploy              # Helm/Manifeste/values
```

---

## 🔐 Sicherheit & Governance

* **AuthN:** OIDC via Keycloak (Realms, Clients, Rollen)
* **AuthZ:** OPA-Policies (ForwardAuth am Gateway, ABAC/RBAC)
* **RLS:** Row-Level-Security beispielhaft in Superset/dbt
* **Audit:** Gateway/OPA/Service-Logs; OTel-Traces (aktivierbar)
* **Secrets:** K8s-Secrets/External Secrets (für Prod rotieren)

> Für Produktion: TLS (cert-manager), HPA/Resources, Backups, Mandantentrennung (tenant\_id & Policies) – siehe `docs/dev/hardening.md`.

---

## 🗺️ Roadmap

**v0.1.x (MVP Polishing)**

* NiFi → Aleph Auto-Ingest & OCR-Status
* NLP-Service (NER/Resolve/Summary) + UI-Highlights
* Search-Reranking (Embeddings) optional zuschaltbar
* Observability-Stack (Prom, Grafana, OTel Collector)

**v0.2**

* Flowise-Agent (“Investigation Assistant”) mit Tools (search\_docs, graph\_neighbors, annotate\_doc, summarize\_text)
* n8n-Playbooks (z. B. “Financial Risk Assistant”)
* Superset-Dashboards: Cross-Filter, Deep-Links (→ Graph/Docs)

**v0.3**

* Graph-Algorithmen (Centrality, Communities), Export/Sharing
* Data Quality (erweiterte dbt-Tests), Data Catalog (DataHub/Amundsen – optional)
* ClickHouse-Option für große Zeitreihen

**v1.0 (Production)**

* Hardening (TLS, Secrets, RBAC/ABAC, Audit Trails)
* Multi-Tenancy & Mandantentrennung
* Backups/Restore-Runbooks, SLO/SLI-Dashboards
* Dokumentation (Admin/User), Migrations, Onboarding

---

## 🧪 Entwicklung & Tests

```bash
# Lint & Tests
make test

# Einzelservice lokal starten (Beispiel)
cd services/search-api && uvicorn app:app --reload --port 8001
```

---

## 🤝 Beiträge

Contributions sind willkommen!
Bitte **Issues**/Feature-Requests anlegen oder direkt **PRs** erstellen.

* Lies: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`
* Branch-Strategie: `feat/*`, `fix/*`, `docs/*`
* CI-Checks sollten grün sein; bitte aussagekräftige PR-Beschreibung mit Testhinweisen.

---

## 📄 Lizenz

Apache-2.0 (siehe `LICENSE`)

---

## 💬 Kontakt & Support

* Fragen, Ideen, Bug-Reports: Issues im Repo
* (Optional) Community-Chat/Forum/Discord – siehe `docs/community.md`

---

## 🔍 Warum InfoTerminal?

* **Open Source & modular:** Keine Vendor-Lock-ins, klare APIs
* **Polyglot Storage:** Je Datendomäne das passende System
* **Transparenz:** Nachvollziehbare Pipelines, Policies, Lineage (optional)
* **Erweiterbar:** KI-/Agent-Integrationen, neue Konnektoren & Visualisierungen

> Unser Ziel: **Ein praktisches, erschwingliches & anpassbares Framework**, das Kern-Workflows von Datenanalyse & Investigation in Organisationen beschleunigt – mit vollem Kontrolle über Daten & Architektur.

---

### Anhang: Nützliche Make-Targets (Beispiele)

```bash
make dev-up         # Dev-Cluster + Basisdienste
make services-up    # Microservices build/deploy
make web-up         # Frontend Dev
make dev-down       # Alles stoppen/aufräumen
```

> Details & Alternativen in `docs/dev/checklist.md` und per-Service-READMEs.


############################
# Old Readme:

# InfoTerminal — Open, Modular Intelligence Platform

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

* [Purpose](#purpose)
* [Prerequisites](#prerequisites)
* [Quickstart (Dev)](#quickstart-dev)
* [Health Checks](#health-checks)
* [Common Tasks](#common-tasks)
* [Further Reading](#further-reading)
* [DE Appendix](#de-appendix)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Purpose

InfoTerminal stitches together search, graph and analytics services to explore heterogeneous data.
The platform runs on Kubernetes and is optimized for local development.
See the [developer docs](docs/dev/README.md) for details on architecture and components.

## Prerequisites

* Docker 24+
* Kubernetes / Kind 0.20+
* Helm 3+
* pnpm 8+
* uv 0.1+

## Quickstart (Dev)

```bash
make dev-up         # infra (kind/helmfile) + base services
make apps-up        # backend services + frontend
make seed-demo      # demo data into search/graph
```

## Health Checks

* Frontend: [localhost:3000](http://localhost:3000)
* Search API: [localhost:8001](http://localhost:8001/health)
* Graph API: [localhost:8002](http://localhost:8002/health)

## Common Tasks

```bash
make dev-down       # tear down cluster
make logs           # tail all service logs
make restart <svc>  # restart a specific service
```

## Further Reading

* [Developer Docs](docs/README.md)
* [Runbooks](docs/dev/runbooks)
* [Architecture Decisions](docs/adr)

---

## DE Appendix

Kurzanleitung auf Deutsch ist in [docs/dev/Checkliste.md](docs/dev/Checkliste.md) zu finden.
Neue Dokumentation erfolgt primär auf Englisch.
