# InfoTerminal — Open, Modular Intelligence Platform (Gotham-style, OSS)

  ```
  +--------------------------------------------------------+
  |                      Benutzer                         |
  |  - Analysten, Ermittler, Data Scientists              |
  +------------+--------------------+---------------------+
               |                    |                       
       +-------v------+      +------v-------+               
       |  Visualisierung |    |   Frontend UI |                 
       |  (Apache Superset|  | (React, Vue.js) |               
       |  Metabase)      |    |                |               
       +-------+--------+      +-------+-------+               
               |                       |                      
         +-----v-----------------------v-----+                
         |       API Gateway / Backend           |               
         |  (Node.js, Flask, FastAPI)            |               
         +----------------+----------------------+               
                          |                                    
       +------------------+--------------------+                 
       |     Datenanalyse & KI Layer           |                 
       |  (Apache Spark, TensorFlow, PyTorch)  |                 
       +------------------+--------------------+                 
                          |                                    
           +--------------+---------------+                     
           |   Datenmanagement & Storage    |                     
           |  - PostgreSQL / ClickHouse     |                     
           |  - Elasticsearch               |                     
           |  - Neo4j (Graph DB)            |                     
           +--------------+----------------+                     
                          |                                    
          +---------------+----------------+                     
          |   Datenintegration & ETL Layer   |                     
          |  - Apache NiFi / Airflow          |                     
          |  - dbt (Transformation)          |                     
          +---------------+----------------+                     
                          |                                    
         +----------------+----------------+                     
         |        Data Catalog & Security  |                     
         |  - Amundsen / DataHub            |                     
         |  - Keycloak (Auth)               |                     
         +--------------------------------+                     
                          |                                    
            +-------------+--------------+                     
            |     Dokumentenmanagement    |                     
            |          Aleph              |                     
            +----------------------------+
  ```



## 0) TL;DR (MVP in 90 Tagen)

* **Woche 1–2:** Monorepo, IaC, CI/CD, Dev-Cluster (Kind), Keycloak + Gateway, basic ETL (NiFi/Airflow), Postgres + Elastic online.
* **Woche 3–4:** Schema + Ontologie (LinkML/JSON Schema), Entity Resolution (basic), Aleph für Doku-Intake, erste Dashboards (Superset).
* **Woche 5–6:** Graph-Layer (Neo4j), Relationship Explorer UI, Volltextsuche mit Cross-Linking zu Graph/Docs.
* **Woche 7–8:** KI-Services (NER, Linking), n8n/Flowise Agents, OpenBB-Integration (Finanzdaten).
* **Woche 9–10:** Security & Governance (OPA Policies, Audit), Lineage/Metadata (DataHub/Amundsen).
* **Woche 11–12:** Hardening, E2E-Tests, Demo Datasets & Playbooks, Release v0.1.

---

## 1) Projektziele & Nicht-Ziele

**Ziele**

* Heterogene Datenquellen integrieren (Batch/Stream), **durchsuchbar**, **verknüpfbar** und **visuell analysierbar** machen.
* Graph- & Dokumenten-Ermittlungsworkflows, Dashboards, KI-unterstützte Mustererkennung.
* **Transparenz, Reproduzierbarkeit, Data Lineage, Governance** by default.

**Nicht-Ziele (v0.1)**

* Keine mission-kritischen Realtime-Command-&-Control Workflows.
* Kein proprietärer Datentransport; alles standardisiert (APIs, connectors, open formats).

---

## 2) Architektur (High Level)

```mermaid
flowchart LR
  subgraph UI["Frontend & Analytics"]
    FE[Next.js/React App]
    SUP[Superset / Metabase]
    ALEPH[Aleph UI]
  end

  subgraph GATE["API Gateway + AuthZ"]
    GW[Kong | Traefik]
    KC[Keycloak]
    OPA[Open Policy Agent]
  end

  subgraph SVC["Microservices"]
    S1[Ingest API<br/>FastAPI]
    S2[Search API<br/>FastAPI]
    S3[Graph API<br/>FastAPI]
    S4[Entity Resolution<br/>service]
    S5[LLM/NLP Services<br/>NER, Linking]
    S6[OpenBB Connector<br/>scheduler]
  end

  subgraph ETL["Pipelines"]
    NIFI[Apache NiFi]
    AF[Apache Airflow]
    DBT[dbt]
  end

  subgraph DATA["Storage & Indexes"]
    PG[(PostgreSQL)]
    CH[(ClickHouse)]
    ES[(Elasticsearch/OpenSearch)]
    NEO[(Neo4j)]
    OBJ[(Object Store: S3/MinIO)]
    CATALOG[(DataHub / Amundsen)]
  end

  FE --> GW
  SUP --> GW
  ALEPH --> GW

  GW -->|OIDC| KC
  GW -->|AuthZ| OPA

  GW --> SVC
  SVC --> ETL
  ETL --> PG & CH & ES & NEO & OBJ
  ETL --> CATALOG
  FE --> SUP
  FE -->|Graph/Docs/Search| SVC
```

**Kerneigenschaften**

* **API-first**: Jede Funktion als Service mit OpenAPI.
* **Storage-Spezialisierung**: Relational (PG/CH), Suchindex (ES), Graph (Neo4j), Doks (Aleph + S3).
* **Governance**: OIDC (Keycloak), Policies (OPA), Lineage/Glossar (DataHub/Amundsen).
* **Observability**: OpenTelemetry → Grafana/Prometheus/Loki/Tempo.

---

## 3) Monorepo Layout (pnpm + uv + Docker + Helm)

```
info-terminal/
├─ apps/
│  ├─ frontend/               # Next.js (React), OIDC login, viewers (graph, map, doc)
│  ├─ superset/               # Helm chart values + presets/dashboards
│  ├─ aleph/                  # Aleph deployment manifests + config
│  └─ agents/                 # Flowise graphs, n8n workflows (JSON)
├─ services/
│  ├─ gateway/                # Kong/Traefik configs, OIDC/OAuth
│  ├─ auth/                   # Keycloak realm/clients/roles (exported JSON)
│  ├─ policy/                 # OPA Rego policies + tests
│  ├─ ingest-api/             # FastAPI: source mgmt, file intake, validations
│  ├─ search-api/             # FastAPI: search across ES/Aleph + entity links
│  ├─ graph-api/              # FastAPI: Neo4j cypher endpoints (path/query)
│  ├─ entity-resolution/      # Python: dedupe, fuzzy, embeddings, blocking
│  ├─ nlp/                    # NER, RE, summarization (spaCy/transformers)
│  └─ openbb-connector/       # OpenBB pulls, cache, schema mapping, DAG hooks
├─ etl/
│  ├─ nifi/                   # NiFi templates/process-groups
│  ├─ airflow/                # DAGs (Py), sensors, dbt operators
│  ├─ dbt/                    # models/, seeds/, sources/
│  └─ schemas/                # LinkML/JSON Schema, contracts
├─ infra/
│  ├─ helm/                   # charts: postgres, clickhouse, elastic, neo4j, minio, superset, aleph
│  ├─ k8s/                    # kustomize bases/overlays (dev, staging, prod)
│  ├─ terraform/              # optional: cluster & bucket provisioning
│  └─ otel/                   # otel-collector, grafana, prom/loki/tempo
├─ datasets/
│  ├─ demo/                   # synthetic data + fixtures
│  └─ openbb/                 # sample pulls, static snapshots for tests
├─ .github/workflows/         # CI: lint, test, build images, scan, helmfile apply
└─ docs/
   ├─ architecture/           # diagrams, ADRs
   ├─ runbooks/               # on-call, incident, data recovery
   ├─ governance/             # DPIA, SoD, roles, RBAC matrices
   └─ tutorials/              # “from zero to query”
```

---

## 4) Datenmodell & Ontologie

* **Basis:** Entity-Relationship für Kernobjekte (Person, Organisation, Asset, Ort, Ereignis, Dokument, Transaktion).
* **Erweiterbar:** LinkML/JSON Schema, versioniert, im Repo unter `etl/schemas/`.
* **Identität & Auflösung:** deterministische Keys + probabilistische Matching-Pipelines (blocking keys, fuzzy match, embeddings, clerical review queue).
* **Lineage:** dbt + OpenLineage & DataHub; jede Transformation dokumentiert und nachvollziehbar.

---

## 5) Security, Privacy, Compliance

* **AuthN:** Keycloak (OIDC/OAuth2), Clients: frontend, superset, apis.
* **AuthZ:** OPA (Rego) + „attribute-based access control“ (ABAC): Rollen, Mandanten, Datenklassifizierung.
* **Audit:** Gateway & Service Logs, immutable in Loki; Data-Access Events → CH/PG.
* **PII/GDPR:** Datenminimierung, Pseudonymisierungspfade, DPIA-Templates, Retention per Policy.
* **Secrets:** External Secrets Operator, Vault/Sealed Secrets.

---

## 6) Observability

* **Tracing:** OpenTelemetry SDKs in allen Python/Node Services → Tempo.
* **Metrics:** Prometheus (service & db exporters).
* **Logs:** Loki; Correlation-IDs propagieren via Gateway.
* **SLOs:** Such-API p95, Graph-Query p95, Pipeline-Latenz, Freshness (dbt tests).

---

## 7) CI/CD & Qualität

* **CI:** Ruff/Flake8 + pytest + mypy; ESLint + Vitest/Playwright. Trivy/Grype für Images.
* **CD:** Helmfile/Kustomize nach dev → staging → prod, manuell approvable.
* **Data Tests:** dbt tests + Great Expectations optional.
* **Testdaten:** `datasets/demo` (synthetisch, DSGVO-sicher).

---

## 8) OpenBB Terminal — **Integrations-Blueprint**

### 8.1 Ziele

* Finanz-/Marktdaten als optionale Quelle in Ermittlungs-/Risikomodellen.
* Kombinierbar mit anderen Spuren: Firmenregister, Sanktionslisten, OSINT, Aleph-Dokumente, Graphpfade.

### 8.2 Architektur

* **OpenBB Connector Service** (`services/openbb-connector`):

  * Periodische Pulls (Airflow DAG) & on-demand API.
  * Caching (Redis/CH), Rate-Limit & Backoff.
  * **Schema-Mapping**: Rohdaten → Staging (CH/PG) → dbt Models → Gold (Analytics + ES index).
* **Pipelines**

  * **Airflow**: `openbb_equities_daily.py`, `openbb_macro_weekly.py`, `openbb_news_intraday.py`.
  * **dbt**: Normalisierung, Dimensionstabellen (assets, issuers, prices, events), Snapshots (SCD2).
  * **Elasticsearch**: Indexe für News/Filings mit Entity-Tags & Cross-refs zu Graph (isin, lei, org\_id).

### 8.3 Datenvertrag (vereinfachtes Beispiel)

* **Staging** (`stg_openbb_prices` / CH)

  * `as_of_date` (Date), `symbol` (String), `isin` (String, nullable), `open`,`high`,`low`,`close` (Float64), `volume` (UInt64), `vendor_ts` (DateTime).
* **Dim** (`dim_asset`, `dim_issuer`) – gemappt via ISIN/LEI, optional Name-Match.
* **Fact** (`fct_eod_prices`) – Surrogate Keys auf `asset_id`, Partition by `as_of_date`.
* **Search** (`idx_openbb_news` / ES)

  * `title`, `body`, `published_at`, `symbols`, `entities` (NER), `doc_url`, `source`, `confidence`.

### 8.4 Airflow DAG (Snippet, Python)

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from utils.openbb import fetch_prices, to_clickhouse
from utils.dbt import run_dbt_models

with DAG(
    "openbb_equities_daily",
    schedule="0 4 * * 1-5",
    start_date=datetime(2025, 9, 1),
    catchup=False,
    max_active_runs=1,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=10)},
) as dag:

    def _pull_prices(ds, **_):
        syms = ["AAPL","MSFT","NVDA","SAP.DE"]
        df = fetch_prices(syms, start=ds, end=ds)
        to_clickhouse(df, table="stg_openbb_prices")

    pull = PythonOperator(task_id="pull", python_callable=_pull_prices)
    transform = PythonOperator(task_id="dbt_transform", python_callable=lambda: run_dbt_models(["stg_openbb","dim_asset","fct_eod"]))
    pull >> transform
```

### 8.5 NiFi Alternative (Low-Code)

* Processor chain: `InvokeHTTP (OpenBB API)` → `EvaluateJsonPath` → `PutDatabaseRecord (ClickHouse JDBC)` → `PutElasticsearchJson`.
* FlowFiles mit `symbol`, `window`, `as_of=now()` als dynamic props.

### 8.6 Graph-Verknüpfung

* **Neo4j**: `(:Asset {isin})-[:ISSUED_BY]->(:Organization {lei})`
* Nachrichten/Filings als `(:Document)-[:MENTIONS]->(:Asset|:Organization)`.
* Kürzester Pfad-Abfragen im **Graph Explorer** der UI, kombiniert mit Datum/Region/Quelle.

### 8.7 Frontend / Analytics

* **Superset**: Price-Volatility, Event-Impact, Cross-Filter mit Ermittlungsmerkmalen.
* **Frontend**: Asset-Detailseite: Kursverlauf (EOD), News-Timeline, Graph-Snippets (betroffene Entitäten).

### 8.8 Governance

* Lizenz/ToS der jeweiligen OpenBB-Datenquellen respektieren.
* Mandantentrennung (project\_id) & Tagging (public/commercial/internal) für Data Access Policies.

---

## 9) AI Layer & Agents (n8n / Flowise / lokale LLMs)

* **NLP Services** (`services/nlp`): NER (Person/Org/Ort), Relation Extraction (Org↔Asset), Summarization (docs/news), Embeddings (search rerank).
* **Agents** (`apps/agents`):

  * „Investigation Assistant“: nimmt Fälle (IDs), erstellt Abfragepläne, ruft Search/Graph APIs, fertigt Notizen/Reports.
  * „Financial Risk Assistant“: joint OpenBB Daten mit Firmenregistern/Sanktionslisten, markiert Red Flags.
* **Pipelines**: n8n flows triggern Airflow DAGs, speichern Ergebnisse, erzeugen Superset Links.

---

## 10) Dokumentenmanagement (Aleph)

* Ingest: Uploads, Web Crawler, Watch-Folders (NiFi ListenFile + PutAleph).
* Pipeline: OCR (Tesseract), Language ID, NER, Fingerprinting (shingling), ES-Index.
* Cross-Links: NER Entities → Graph IDs (resolver), Anzeige in Doc-Viewer inkl. „open in Graph“.

---

## 11) Deployment (lokal → k8s)

* **Dev**: Kind Cluster, Tilt/Skaffold für Hot-Reload der Services.
* **Stateful**: Postgres (operator), ClickHouse, Elastic, Neo4j, MinIO via Helm charts.
* **Bootstrap**: `make dev-up` – startet stack, seedet Demo-Daten, erstellt Keycloak Realm/Clients.
* **Config**: alles als code (values.yaml, kustomize overlays), Secrets per ExternalSecrets/Vault.

---

## 12) Risiken & Gegenmaßnahmen

* **Datenlizenzen**: klare Klassifizierung & Policy Enforcement → OPA.
* **PII/DSGVO**: Pseudonymisierungspfade, DPIA, rollenbasierte Sichtbarkeit.
* **Komplexität**: modulare Services, ADRs, klare SLOs, On-call Runbooks.
* **Kosten**: ClickHouse statt Big Spark-Cluster; elastic optimiert; kalte Daten in S3/MinIO.

---

## 13) Roadmap (Detail 0–12 Wochen)

**W1–2 (Foundation)**

* Monorepo scaffold, Coding-Standards, pre-commit, Ruff/ESLint, GitHub Actions.
* Helmfile/Kustomize, Kind Dev-Cluster; Keycloak + Gateway + OPA „allow-by-default in dev“.
* Elastic + Postgres + MinIO up; NiFi oder Airflow wählbar.

**W3–4 (Data Basics)**

* LinkML/JSON Schemas für Kernobjekte; dbt Setup; erste Seeds.
* Search-API (FastAPI) mit Basic Queries; Frontend OIDC Login + simple search UI.
* Aleph deployment + minimaler File Intake Pfad.

**W5–6 (Graph & Relations)**

* Neo4j online, Graph-API Endpunkte (neighbors, shortest\_path, ego-net).
* Entity Resolution v0 (deterministisch + fuzzy), Clerical Review UI in Frontend.

**W7–8 (AI & OpenBB)**

* NER + Linking pipeline; embeddings für rerank.
* OpenBB Connector + DAGs; Superset Dashboards; Cross-refs zu Graph/Aleph.

**W9–10 (Governance & Metadata)**

* OPA Policies (ABAC), Audit Trails; DataHub (sources, lineage, glossary).
* dbt tests & Great Expectations (optional) für gold layer.

**W11–12 (Hardening & Release)**

* E2E-Tests, Load Tests, Security Review; Demo-Walkthrough + Tutorials; v0.1 tag.

---

## 14) „Day-1“ Aufgaben (konkret)

1. **Repo anlegen** `info-terminal` mit obiger Struktur.
2. **Dev-Cluster**: `make dev-up` (Kind + Helmfile für PG/ES/MinIO/Keycloak/Gateway/OPA).
3. **Auth**: Keycloak realm `infoterminal`, clients `frontend`, `superset`, `apis`, roles `analyst`, `investigator`, `admin`.
4. **Search-API** Skelett (FastAPI) + OpenAPI + ES client; endpoint `/search?q=...`.
5. **Frontend**: Next.js + OIDC; simple search page & result list.
6. **Airflow**: basic DAG „hello\_etl“ + dbt bootstrap.
7. **Aleph**: deploy; seed 20 PDFs; verknüpfe `doc_id` → ES index.
8. **Observability**: otel-collector + basic tracing im Search-API.
9. **Policies**: OPA sample policy (analyst read, admin write).
10. **Docs**: ADR-000-stack.md, RUNBOOK-stack.md, CONTRIBUTING.md.

---

## 15) Beispiel-Policies (OPA Rego, skizze)

```rego
package access

default allow = false

allow {
  input.user.roles[_] == "admin"
}

allow {
  input.user.roles[_] == "analyst"
  input.action == "read"
  input.resource.classification in {"public","internal"}
  input.resource.tenant == input.user.tenant
}
```

---

## 16) Beispiel: Search-API (FastAPI Skizze)

```python
from fastapi import FastAPI, Depends
from auth import oidc_user
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=["http://elasticsearch:9200"])
app = FastAPI(title="Search API")

@app.get("/search")
def search(q: str, user=Depends(oidc_user)):
    body = {"query": {"multi_match": {"query": q, "fields": ["title^2","body","entities.name^3"]}}}
    hits = es.search(index="docs,news", body=body)["hits"]["hits"]
    # TODO: filter by OPA decision (resource tags vs user attributes)
    return [{"id": h["_id"], "score": h["_score"], **h["_source"]} for h in hits]
```

---

## 17) Dokus & Playbooks (erste Kapitel)

* **Tutorial 01**: „In 15 Minuten zu Search+Docs“ (Kind, Helmfile, Aleph seed, Search UI).
* **Tutorial 02**: „Graph abfragen: Who-is-connected-to-whom?“
* **Tutorial 03**: „OpenBB Daten laden & visualisieren“ (Airflow DAG + Superset).

---


Sag einfach „**bootstrap**“, dann generiere ich die Dateien als Copy-Paste-Blöcke.
