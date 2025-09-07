# 🛡️ VERIFICATION-BLUEPRINT.md
> AI-gestützte Verifikation von Web/Social-Signalen in InfoTerminal  
> Zielgruppen: Journalist:innen, Sicherheitsbehörden/-firmen, Forschung  
> Stand: 2025-09-05

## 🎯 Ziele
- Falschinformationen früh erkennen, markieren, priorisieren
- Transparente Begründung (Evidenz, Widersprüche, Unsicherheit)
- Human-in-the-loop: Review/Override → kontinuierliches Lernen (Active Learning)
- Forensik-taugliche Provenienz (Hashes, Pipelines, Versionen)

---

## 🧭 Architektur (High-Level)
**Flow:** Quelle → NiFi Ingest → Normalize (Kanonisches Schema) → **Verification Pipeline** → Scores/Labels → Persistenz (OpenSearch/Neo4j/S3) → n8n Alerts/Agents → Frontend (Badges, Evidence-Panel, Dossier)

**Services/Layer:**
- **nifi/** ingest + ETL
- **search-api/** indexiert & fragt OpenSearch
- **graph-api/** verknüpft Claims/Evidenzen (Neo4j)
- **nlp-verif/** (neuer Dienst): Claim-Extraktion, Retrieval, RTE/Stance, Aggregation
- **frontend/** Badges, Evidence-Panel, Review-UI
- **n8n/** Playbooks (Alerts, Escalation, Dossier)
- **S3/MinIO** raw/refined, **Vault/KMS** Keys, **Loki/Tempo** Logs/Traces

---

## 🔬 Verifikations-Pipeline (Module & IO)

### 1) Source Reputation & Bot-Likelihood  ([VERIF-1])
**Input:** `source.*`, Account/Domain-Metadaten  
**Features:** Domain-Ruf, Account-Alter, Posting-Kadenz, Netzwerk-Zentralität, Bot-Heuristiken  
**Output:** `source_reliability∈[0,1]`, `bot_likelihood∈[0,1]`, `risk_flags:[…]`

### 2) Claim-Extraktion & Dedup  ([VERIF-2])
**Input:** `content.title|summary|body_text`  
**Steps:** Claim-Spans extrahieren → normalisieren → MinHash/SimHash clustern  
**Output:** `claim_cluster_id`, `claim_text_norm`, `near_dupes:[…]`

### 3) Evidence Retrieval & Rerank  ([VERIF-3])
**Input:** Claim  
**Steps:** Hybrid Retrieval (BM25 + dense) → rerank (sentence-transformers)  
**Output:** `evidence.pro[]` & `evidence.contra[]` (Kandidaten mit Score)

### 4) RTE/Stance (Entailment)  ([VERIF-4])
**Input:** Claim + Evidenz  
**Steps:** NLI/RTE → `entails|contradicts|neutral`, Confidence  
**Output:** pro Evidenz Klassifikation + Score

### 5) Temporal & Geo-Konsistenz  ([VERIF-5])
**Input:** Zeit/Ort aus Text/Metadaten  
**Output:** `temporal_consistency∈[0,1]`, `geo_consistency∈[0,1]`

### 6) Medien-Forensik  ([VERIF-6])
**Bild/Video/Audio:** pHash/dHash, EXIF, Keyframes, Reverse Search Hits, ELA-Hinweise  
**Output:** `media_flags:[…]`, `reverse_hits:int`

### 7) Aggregation & Kalibrierung
```

veracity\_score = w1*source + w2*content + w3*corro + w4*rte + w5*temporal + w6*geo + w7\*media
veracity\_label ∈ {verified, likely\_true, uncertain, likely\_false, false, manipulative}
confidence via isotonic / platt scaling

````

### 8) Human-in-the-loop & Active Learning  ([VERIF-8],[VERIF-9])
Review-UI (Evidenz, Begründungen, Overrides) → Label-Store → periodisches Re-Training

---

## 🗃️ Kanonisches Schema (Erweiterung)
```yaml
verification:
  veracity: "verified|likely_true|uncertain|likely_false|false|manipulative"
  score: 0.0..1.0
  confidence: 0.0..1.0
  source_reliability: 0.0..1.0
  bot_likelihood: 0.0..1.0
  corroboration_count: int
  kg_consistency: 0.0..1.0
  temporal_consistency: 0.0..1.0
  geo_consistency: 0.0..1.0
  media_flags: ["repost","exif_mismatch","edited","no_exif",...]
  stance: "support|refute|discuss|unrelated"
  evidence:
    pro:    [ {url, title, snippet, entailment_score} ]
    contra: [ {url, title, snippet, contradiction_score} ]
  explain:
    top_features: [ {name:"source_reliability", contrib:0.27}, ... ]
    model_version: "verif-2025.09.0"
provenance:
  pipeline: "nifi/verif_v1"
  processed_at: "ISO-8601"
  hash_sha256: "…"
````

---

## 📦 OpenSearch: Index Settings & Mapping (news + verification)

```json
{
  "settings": {
    "index": {
      "knn": true,
      "analysis": {
        "analyzer": {
          "de_std": { "type": "standard", "stopwords": "_german_" },
          "en_std": { "type": "standard", "stopwords": "_english_" }
        }
      }
    }
  },
  "mappings": {
    "dynamic_templates": [
      { "strings": { "match_mapping_type": "string", "mapping": { "type": "keyword" } } }
    ],
    "properties": {
      "id": { "type": "keyword" },
      "source": {
        "properties": {
          "system": { "type": "keyword" },
          "handle": { "type": "keyword" },
          "channel": { "type": "keyword" },
          "url": { "type": "keyword" },
          "fetched_at": { "type": "date" }
        }
      },
      "content": {
        "properties": {
          "title": { "type": "text", "fields": { "de": { "type": "text", "analyzer": "de_std" }, "en": { "type": "text", "analyzer": "en_std" } } },
          "summary": { "type": "text" },
          "body_text": { "type": "text" }
        }
      },
      "meta": {
        "properties": {
          "lang": { "type": "keyword" },
          "published_at": { "type": "date" },
          "author": { "type": "keyword" },
          "tags": { "type": "keyword" }
        }
      },
      "embedding": { "type": "knn_vector", "dimension": 384, "method": { "name": "hnsw", "engine": "nmslib" } },
      "verification": {
        "properties": {
          "veracity": { "type": "keyword" },
          "score": { "type": "float" },
          "confidence": { "type": "float" },
          "source_reliability": { "type": "float" },
          "bot_likelihood": { "type": "float" },
          "corroboration_count": { "type": "integer" },
          "kg_consistency": { "type": "float" },
          "temporal_consistency": { "type": "float" },
          "geo_consistency": { "type": "float" },
          "media_flags": { "type": "keyword" },
          "stance": { "type": "keyword" },
          "evidence": {
            "properties": {
              "pro":    { "type": "nested", "properties": { "url": { "type": "keyword" }, "title": { "type": "text" }, "snippet": { "type": "text" }, "entailment_score": { "type": "float" } } },
              "contra": { "type": "nested", "properties": { "url": { "type": "keyword" }, "title": { "type": "text" }, "snippet": { "type": "text" }, "contradiction_score": { "type": "float" } } }
            }
          }
        }
      },
      "provenance": {
        "properties": {
          "pipeline": { "type": "keyword" },
          "processed_at": { "type": "date" },
          "hash_sha256": { "type": "keyword" }
        }
      }
    }
  }
}
```

---

## 🕸️ Neo4j: Knoten, Kanten, Constraints

**Nodes:** `(:Article {id}), (:Source {id}), (:Claim {id, text_norm}), (:Evidence {id, url})`
**Edges:**

* `(:Source)-[:PUBLISHED]->(:Article)`
* `(:Claim)-[:MENTIONED_IN {stance,confidence,ts}]->(:Article)`
* `(:Claim)-[:SUPPORTED_BY|:CONTRADICTED_BY {score,ts}]->(:Evidence)`

**Constraints/Indexes:**

```cypher
CREATE CONSTRAINT article_id IF NOT EXISTS FOR (a:Article) REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT source_id  IF NOT EXISTS FOR (s:Source)  REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT claim_id   IF NOT EXISTS FOR (c:Claim)   REQUIRE c.id IS UNIQUE;
CREATE INDEX claim_text_norm IF NOT EXISTS FOR (c:Claim) ON (c.text_norm);
CREATE INDEX evidence_url    IF NOT EXISTS FOR (e:Evidence) ON (e.url);
```

**Upsert-Beispiel:**

```cypher
MERGE (a:Article {id: $article.id})
ON CREATE SET a += $article.props
MERGE (s:Source {id: $source.id})
ON CREATE SET s += $source.props
MERGE (s)-[:PUBLISHED]->(a)
WITH a
UNWIND $claims AS cl
  MERGE (c:Claim {id: cl.id})
  ON CREATE SET c.text_norm = cl.text_norm
  MERGE (c)-[m:MENTIONED_IN {ts: cl.ts}]->(a)
  SET m.stance = cl.stance, m.confidence = cl.confidence;
```

---

## 🧰 NiFi Flows (Vorlagen)

1. `ingest_normalize`

   * `InvokeHTTP/ConsumeRSS` → `JoltTransformJSON` (kanonisch) → `UpdateAttribute` (hash) → `PutS3Object` → `PublishKafka (topic:new_items)`
2. `nlp_claims`

   * `ConsumeKafka:new_items` → `ExecuteScript(Py)` (Claim-Extract + MinHash) → `PublishKafka:claims`
3. `evidence_retrieval`

   * `ConsumeKafka:claims` → `InvokeHTTP` (search-api BM25) + `POST /embed` (dense) → `ExecuteScript(Py)` (hybrid rerank) → `PublishKafka:evidence`
4. `rte_scoring`

   * `ConsumeKafka:evidence` → `InvokeHTTP nlp-verif /rte` → `PublishKafka:rte`
5. `geo_time_media`

   * `ConsumeKafka:rte` → `ExecuteScript(Py)` (Mordecai + EXIF/pHash) → `PublishKafka:verif_partial`
6. `aggregate_upsert`

   * `ConsumeKafka:verif_partial` → `ExecuteScript(Py)` (Aggregation+Calibration) → `OpenSearchPut` + `InvokeHTTP graph-api /upsert`

**Parameter Context:** URLs, API-Keys, Rate Limits, Proxy (aus Security-Blueprint).

---

## 🤖 n8n Playbooks

* **Watchlist Veracity Alerts**: trigger bei `veracity ∈ {likely_false,false,manipulative}` → Slack/Email → Issue/Case
* **Escalation**: hoher Widerspruchsgrad → Senior Review Channel
* **Auto-Dossier**: verified/likely\_true zu bestimmten Entitäten → PDF + Superset Deep-Link
* **Agent Chain**: Investigation Agent holt Evidenz, Graph-Kontext, baut Dossier

---

## 🧪 Modelle & Runtime

* **NER/RE/Summarization:** spaCy/Transformers (DE/EN), Light-LLM optional
* **Dense Embeddings:** `sentence-transformers all-MiniLM-L6-v2` (384d) → HNSW/FAISS
* **RTE/NLI:** z. B. `multilingual-mpnet-base` oder spezialisiertes NLI-Modell
* **Calibrator:** Platt/Isotonic; Versionierung via `model_version`
* **Active Learning:** unsichere/uneinige Samples in Label-Queue

**ENV Beispiel (nlp-verif):**

```bash
VERIF_MODEL_NER=spacy_de_core_news_md
VERIF_MODEL_EMB=sentence-transformers/all-MiniLM-L6-v2
VERIF_MODEL_RTE=ckpts/rte-mpnet
VERIF_AGG_WEIGHTS="source:0.2,content:0.1,corro:0.25,rte:0.25,temporal:0.05,geo:0.05,media:0.1"
VERIF_MIN_CONFIDENCE=0.6
```

---

## 🔎 APIs (Skizze)

### nlp-verif

* `POST /claim/extract` → `[ {id, span, text_norm} ]`
* `POST /retrieval` → `{claim} → {pro:[…], contra:[…]}`
* `POST /rte` → `{claim, evidence} → {label, score}`
* `POST /aggregate` → `{signals} → {veracity, score, confidence, explain}`

### search-api

* `POST /search/bm25` → Top-k Kandidaten
* `POST /search/embed` → Embeddings + ANN Suche

### graph-api

* `POST /claims/upsert` → MERGE Claim/Edges
* `GET /claims/{id}` → Claim + Evidenz + Verlauf

---

## 📈 Metriken & Observability

**Prometheus (nlp-verif):**

* `verif_pipeline_events_total{stage=…}`
* `verif_model_latency_seconds{model=…}` (Histogram)
* `verif_veracity_distribution{label=…}`
* `verif_rte_accuracy`, `verif_calibration_error`
* `verif_retrieval_recall_at_k`

**Logs/Traces:** Korrelation via `X-Request-ID`; Sampling für Incognito anpassbar

---

## ⚖️ Ethik, Recht & Security

* **Transparenz:** Label + Score + Evidenz + Unsicherheit im UI
* **Kein Auto-Takedown:** Markieren/Ranken, Entscheidung bleibt beim Menschen
* **PII-Filter:** Redaktionsregeln, besonders bei Leaks/Quellen­schutz
* **robots.txt/ToS:** Scraping-Whitelist (Security-Blueprint)
* **Incognito-Modus:** No-persist Logs, egress nur via Tor/VPN, ephemerer FS

---

## ✅ Tickets (zum TODO-Index ergänzen)

* **\[VERIF-1]** Source Reputation & Bot-Likelihood Modul – **DoD:** Scores in OpenSearch + Graph-Kanten
* **\[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs – **DoD:** `claim_cluster_id` pro Item
* **\[VERIF-3]** Evidence Retrieval (Hybrid) – **DoD:** pro/contra Kandidaten mit Scores
* **\[VERIF-4]** RTE/Stance + Aggregation – **DoD:** `veracity_label/score/confidence` gesetzt
* **\[VERIF-5]** Temporal/Geo Checks – **DoD:** Felder `temporal_*, geo_*` gefüllt
* **\[VERIF-6]** Media Forensics – **DoD:** `media_flags`, reverse\_hits
* **\[VERIF-7]** Schema/Mappings/Constraints – **DoD:** OpenSearch Mapping & Neo4j Constraints live
* **\[VERIF-8]** Review-UI – **DoD:** Evidence-Panel, Overrides, History
* **\[VERIF-9]** Active Learning Loop – **DoD:** Label-Store, Re-Training Job
* **\[VERIF-10]** n8n Alerts/Escalations – **DoD:** produktiv, getestet
* **\[VERIF-11]** Dossier-Integration – **DoD:** PDF/MD mit Evidenzanhang + Hash

---

## 🚀 Rollout-Plan (empfohlen)

1. **VERIF-1 + VERIF-2** (sichtbarer Mehrwert, Grundlage)
2. **VERIF-3 + VERIF-4** (erste Veracity-Badges im UI)
3. **VERIF-5 + VERIF-6** (Zeit/Geo & Medien → Präzision rauf)
4. **VERIF-8 + VERIF-9** (Review & Lernen)
5. **VERIF-10 + VERIF-11** (Operationalisierung & Reporting)

---
