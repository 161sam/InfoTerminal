# Architektur für Live-Datenquellen

## 1) Datenfluss (End-to-End)

**Quelle → Aufnahme → Normalisierung → Anreicherung → Persistenz → Index/Graph → Benachrichtigung**

1. **Aufnahme**

   * **Webhooks/PubSub** (sofortig): Twitter/X (falls Zugang), Reddit, GitHub Events, Telegram Bots, Slack, Mastodon (ActivityPub), YouTube (PubSubHubbub/WebSub), RSSHub.
   * **Pull/Scheduler** (nahe Echtzeit): **RSS/Atom**, JSON/REST APIs, **Scraping** (legal/robots.txt-konform).
   * Orchestrierung: **NiFi** für robuste Flows (Backoff/Retry/Secrets/Queues), **n8n** für Playbooks und Querverknüpfungen.
2. **Normalisierung**

   * Canonical Schema (siehe unten), **URL-Kanonisierung**, Encoding-Sanitizer, HTML→Text (Readability/trafilatura).
3. **Anreicherung**

   * Sprach­erkennung (langid), **NER/RE**, **Geoparsing**, **Event- & Zeit-Extraktion**, Sentiment/Topics, **Deduplikation** (shingling/MinHash/SimHash).
4. **Persistenz**

   * **Raw**: Objektspeicher (S3/GCS/MinIO) + Hash (SHA-256) + Provenienz.
   * **Refined**: Postgres (struct), **OpenSearch** (Volltext), **Neo4j** (Entitäten/Beziehungen).
5. **Index/Graph**

   * OpenSearch Indizes je Quelle + vereinheitlichter „news“ Index.
   * Neo4j: Nodes (Article, Post, Account, Org, Person, Place, Event), Rels (MENTIONS, PUBLISHED\_BY, LINKS\_TO, LOCATED\_IN…).
6. **Benachrichtigung/Action**

   * n8n Flows (Alerts, Dossiers, Analyst-Tasks), **Superset Deep-Links** (Dashboards), Webhooks an externe Systeme.

---

## 2) Quell-Connectors (Startpaket → Ausbau)

### A. „Schnell & breit“ (MVP <— v0.1.9.x)

* **RSS/Atom** (Nachrichten, Blogs, Behördenfeeds): NiFi `ConsumeRSS` + Parser.
* **Mastodon (ActivityPub)**: Streaming API/WebSocket; Fallback Poll.
* **Reddit**: JSON API (Subreddits, Such-Queries).
* **YouTube**: WebSub (Push) + API (Backfill).
* **Telegram**: Bot API (Kanäle/Groups mit Opt-in).
* **Webseiten**: trafilatura/Readability + (Playwright) für JS-heavy Seiten; Quellen-Whitelist.

### B. „Optional/Reguliert“

* **Twitter/X**: Nur mit gültigem Enterprise/Academic Zugang; Rate-Limits & ToS beachten.
* **Facebook/Instagram (Graph API)**: Nur eigene Seiten/Assets; strikte ToS.
* **RSSHub**: Vorsicht bei ToS; ideal für Feeds, die keinen RSS bieten.

> Jede Quelle als **Plugin**: `source.yaml` (Metadaten/Scopes), `runner.py` (Fetcher), `normalize.py` (Mapper), Tests. Deployment als eigener Container oder n8n/NiFi-Baustein.

---

## 3) Einheitliches Kanonisches Schema

```yaml
id: <uuid> # stable, aus URL+published_at+source gehasht
source:
  system: "rss|reddit|mastodon|youtube|web|telegram|twitter|facebook|…"
  handle: "@account"           # falls verfügbar
  channel: "subreddit|hashtag|feed|channel_id|…"
  url: "https://…"
  fetched_at: "ISO-8601"
content:
  title: "string"
  summary: "string"
  body_text: "string"
  html: "optional"
  media: 
    - kind: "image|video"
      url: "…"
      thumb_url: "…"
  links:
    - url: "…"
      rel: "canonical|cite|embed|…"
meta:
  lang: "de|en|…"
  published_at: "ISO-8601|null"
  author: "string|null"
  tags: ["…"]
  license: "source terms|CC-BY|…"
nlp:
  entities:
    - type: "PERSON|ORG|LOC|EVENT|…"
      text: "…"
      canonical: "…"
      offset_start: 123
      offset_end: 145
  relations:
    - type: "AFFILIATED_WITH|LOCATED_IN|…"
      head: <entity-id>
      tail: <entity-id>
  sentiment: "pos|neu|neg"
  topics: ["election", "finance", …]
  geoparsed:
    - place: "Leipzig"
      lat: 51.3397
      lon: 12.3731
      method: "CLAVIN|Mordecai|heuristic"
dedupe:
  fingerprint: "minhash:…"
  near_duplicates: ["id1","id2"]
provenance:
  pipeline: "nifi/news_v1"
  processing_at: "ISO-8601"
  hash_sha256: "…"
privacy:
  pii_flags: ["name","location","…"]
  redactions: [{"type":"email","span":[…]}]
```

---

## 4) Anreicherungen (AI/ML/DL) – sofort nutzbare Bausteine

* **Language ID**: fastText/langid.
* **NER/RE**: spaCy/Flair/Transformers; DE/EN Modelle.
* **Summarization**: PEGASUS/T5/LLM (mit Längenbudget).
* **Topic Modeling**: BERTopic / zero-shot (LLM).
* **Sentiment**: domain-angepasste Modelle.
* **Geoparsing**: **Mordecai** (spaCy + Geonames), ggf. CLAVIN.
* **Temporal Extraction**: HeidelTime/Rule-based.
* **Dedupe**: `datasketch` (MinHash/LSH) + URL-Canonicals + Title+Body Hashing.
* **Event Extraction** (v2): ACE-ähnliche Trigger + Arg-Füllung; feingranulare “Events” ins Graph-Schema.

---

## 5) Geospatial-Layer (Live)

* **Frontend**: MapLibre/Leaflet; Layer:

  * Heatmap „Erwähnungen pro Ort/Zeitraum“,
  * Trajectories (Posts/News mit Geo),
  * Entitäten-Clusters.
* **Backend**:

  * OpenSearch mit `geo_point`,
  * Neo4j „LOCATED\_IN“/„OCCURRED\_AT“,
  * **NiFi**-Prozessor “GeoEnrich” (Geocoding via Nominatim/Photon, mit Rate-Limit & Cache).

---

## 6) Scraping – rechtssicher & robust

* **Policy-Gate**: robots.txt respektieren, ToS prüfen; **Quellen-Whitelist** für Scraping.
* **Playwright** nur bei notwendigem JS; sonst trafilatura.
* **Rate-Limiter/Backoff**, **Caching** (ETag/If-Modified-Since), **Fingerprint-Rotation** (legal!).
* **Content-Fingerprinting** (Shingles) gegen Reposts.
* **Moderation/PII-Guard**: Redaktionsfilter (E-Mail, Telefonnummern optional schwärzen), Flags.

---

## 7) NiFi & n8n – konkrete Flows

### NiFi (robust ingest)

* `news_rss_ingest`: `GenerateTableFetch/InvokeHTTP → EvaluateJsonPath → UpdateAttribute → PutS3Object → PublishKafka`
* `web_crawl`: URL-Queue → `InvokeHTTP/PlaywrightTask` → Readability → Persist → Kafka.
* `youtube_websub`: Webhook → Normalize → S3/OpenSearch/Neo4j.
* `geo_enrich`: `QueryOpenSearch` → fehlende Geo → Geocoder → Update.

### n8n (Analyst Playbooks)

* **Breaking-News Alert**: Trigger (Kafka topic `news`) → Filter (keyword/org) → Slack/Email → Dossier anlegen.
* **Entity Watchlist**: Eingabemaske im FE → n8n setzt Filter → bei neuem Hit: Graph-Verlinkung + Superset-Deep-Link.
* **Cross-Source Correlation**: Neue Meldung → Ähnlichkeitssuche → Anreichern mit älteren Posts/News → Report exportieren.

---

## 8) Collaboration & Dossier (Live-Kontext)

* **Dossier-Lite v1**: Sammle Treffer (News/Posts) + Graph-Kontext → **PDF/Markdown**.
* **Live-Notizen** (CRDT/Sharedb/Yjs): Kommentiere Artikel/Edges; Mention-System.
* **Audit**: Jede Aktion als immutable Log (Loki/Tempo), korreliert via `X-Request-ID`.

---

## 9) Plugin-System (auch für Kali-Tools)

* **Spec**:

  * Manifest (`plugin.yaml`): Name, Inputs, Outputs, Permissions, Rate-Limits.
  * Adapter (`runner.py`/`runner.ts`): I/O → **canonical schema**.
  * Container-Policy: Netzwerk/FS-Sandbox, Secrets via env.
* **APIs**:

  * **Gateway** `/plugins/run` (JWT) → async job id → status/results.
  * **CLI** `infoterminal-cli plugin run nmap --target 10.0.0.1 --json`.
* **Kali Beispiele**: `nmap`, `whois`, `theHarvester`, `dnsrecon`, `exiftool`, `pdfid`, `yara`.

  * Output → Graph (Host→Service, File→Indicator), Search, Dossier.

---

## 10) Governance, Recht, Sicherheit

* **Provenienz**: jede Transformation mit `pipeline`, `hash`, `source_url`.
* **Recht**: robots.txt, ToS, Urheberrecht; **Lizenz-Feld** im Schema.
* **GDPR**: PII-Flags, Redaktionsroutinen, Opt-out-Liste pro Domain.
* **Secrets**: Vault/.env (nicht im Repo), NiFi Parameter Contexts, n8n Credentials.
* **Rate Limits**: global pro Quelle + pro Domain; Backoff.
* **Abuse-Schutz**: DoH/DNS-Schutz, Request-budget.

---

## 11) Deliverables nach Version (v0.1.9.1 → v0.2)

### v0.1.9.1–.9.4 (MVP Live-Quellen)

* RSS/Atom + Mastodon + Reddit + YouTube(WebSub).
* Kanonisches Schema + Normalisierung + NER/Summarization.
* OpenSearch „news“ Index + Superset Dashboard.
* Frontend: /search Filter „Quelle/Zeit/Entitäten“, **erste Map** (Geo Heatmap).

### v0.1.9.5–.9.7 (Geo + Scraping kontrolliert)

* Geoparsing Pipeline (Mordecai), Geo-Index, Map Layers.
* Whitelist-Scraper (trafilatura + Playwright fallback).
* Dedupe (MinHash) + Near-Duplicate-Merge.

### v0.1.9.8–.9.9 (Collab + Alerts)

* Dossier-Lite v1 (Export PDF/MD), Notes (Yjs in FE).
* n8n Alerts (Watchlists), Deep-Links zu Superset/Graph.

### v0.2.0 (Härtung + Plugins)

* Governance/PII Guard, Provenienz obligatorisch.
* Plugin-Runtime v1 (Kali & externe Quellen als Plugins).
* Tests/Docs, Backups, Dashboards finalisieren.

---

## 12) Konkrete Technik-Blöcke (sofort baubar)

* **Python libs**: `trafilatura`, `readability-lxml`, `datasketch`, `mordecai`, `spacy[transformers]`, `langid`, `hnswlib` (Embeddings-ANN).
* **NiFi**: `InvokeHTTP`, `HandleHttpRequest/Response` (Webhooks), `EvaluateJsonPath`, `PublishKafkaRecord_2_0`.
* **n8n**: Standard HTTP + Function Nodes + Slack/Email; später eigene Nodes.
* **OpenSearch**: Index mit `text`, `keyword`, `date`, `geo_point`.
* **Neo4j**: Merge-Policies (idempotent), Constraints, APOC für Upserts.
* **Frontend**: MapLibre + Deck.gl (später) ; Filter UI (Quelle, Zeitfenster, Entitäten).
