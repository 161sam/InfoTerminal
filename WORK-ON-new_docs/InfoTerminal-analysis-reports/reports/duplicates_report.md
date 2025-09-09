# Deduplikations-Kandidaten (Markdown-Abschnitte)

_Ähnlichkeiten ≥ 0.88; mit Datei, Abschnittstitel, Zeilenbereich und Beispielauszug_

---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Datenquellen-Cluster.md` — *1) **News & Social Media*** — Zeilen 3-15
- B: `docs_ws/docs/dev/v0.2/Datenquellen-Cluster.md` — *1) **News & Social Media*** — Zeilen 3-15

_Auszug A:_
```
## 1) **News & Social Media**

- **RSSHub / Feeds** (NYTimes, Guardian, Spiegel, etc.)
- **Social Media**: Mastodon, Reddit, Telegram, Twitter/X (Scraper), TikTok, Instagram
- **Video-Plattformen**: YouTube/Vimeo → Transkripte (Whisper)
```

_Auszug B:_
```
## 1) **News & Social Media**

* **RSSHub / Feeds** (NYTimes, Guardian, Spiegel, etc.)
* **Social Media**: Mastodon, Reddit, Telegram, Twitter/X (Scraper), TikTok, Instagram
* **Video-Plattformen**: YouTube/Vimeo → Transkripte (Whisper)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Datenquellen-Cluster.md` — *2) **Open Data & Behörden*** — Zeilen 16-28
- B: `docs_ws/docs/dev/v0.2/Datenquellen-Cluster.md` — *2) **Open Data & Behörden*** — Zeilen 16-28

_Auszug A:_
```
## 2) **Open Data & Behörden**

- **EU Open Data Portal**, **Bundesanzeiger**, **Parlament-Dokumente**
- **UN, WHO, OECD, Weltbank**
- **Sanktionslisten**: EU, UN, OFAC, BAFA
```

_Auszug B:_
```
## 2) **Open Data & Behörden**

* **EU Open Data Portal**, **Bundesanzeiger**, **Parlament-Dokumente**
* **UN, WHO, OECD, Weltbank**
* **Sanktionslisten**: EU, UN, OFAC, BAFA
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Datenquellen-Cluster.md` — *3) **Cyber Threat Intelligence*** — Zeilen 29-41
- B: `docs_ws/docs/dev/v0.2/Datenquellen-Cluster.md` — *3) **Cyber Threat Intelligence*** — Zeilen 29-41

_Auszug A:_
```
## 3) **Cyber Threat Intelligence**

- **Threat Feeds**: MISP, AlienVault OTX, Abuse.ch, Spamhaus, CERT
- **Shodan/Censys**: Internet-weite Scans
- **VirusTotal / MalwareBazaar** (nur Hashes, keine Payloads)
```

_Auszug B:_
```
## 3) **Cyber Threat Intelligence**

* **Threat Feeds**: MISP, AlienVault OTX, Abuse.ch, Spamhaus, CERT
* **Shodan/Censys**: Internet-weite Scans
* **VirusTotal / MalwareBazaar** (nur Hashes, keine Payloads)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Datenquellen-Cluster.md` — *4) **Wissenschaft & Forschung*** — Zeilen 42-53
- B: `docs_ws/docs/dev/v0.2/Datenquellen-Cluster.md` — *4) **Wissenschaft & Forschung*** — Zeilen 42-53

_Auszug A:_
```
## 4) **Wissenschaft & Forschung**

- **arXiv, PubMed, Semantic Scholar**
- **Patente** (WIPO, DEPATISnet)
- **Konferenz-Papers** (z. B. ACM, IEEE)
```

_Auszug B:_
```
## 4) **Wissenschaft & Forschung**

* **arXiv, PubMed, Semantic Scholar**
* **Patente** (WIPO, DEPATISnet)
* **Konferenz-Papers** (z. B. ACM, IEEE)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Datenquellen-Cluster.md` — *5) **Sensor & Realwelt*** — Zeilen 54-67
- B: `docs_ws/docs/dev/v0.2/Datenquellen-Cluster.md` — *5) **Sensor & Realwelt*** — Zeilen 54-67

_Auszug A:_
```
## 5) **Sensor & Realwelt**

- **OSM Live** (Geodaten)
- **ADS-B Exchange** (Flugbewegungen)
- **AIS (MarineTraffic)** (Schiffe)
```

_Auszug B:_
```
## 5) **Sensor & Realwelt**

* **OSM Live** (Geodaten)
* **ADS-B Exchange** (Flugbewegungen)
* **AIS (MarineTraffic)** (Schiffe)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Architektur-für-Live-Datenquellen.md` — *A. „Schnell & breit“ (MVP <— v0.1.9.x)* — Zeilen 33-41
- B: `docs_ws/docs/dev/v0.2/Architektur-Live-Datenquellen.md` — *A. „Schnell & breit“ (MVP <— v0.1.9.x)* — Zeilen 34-42

_Auszug A:_
```
### A. „Schnell & breit“ (MVP <— v0.1.9.x)

- **RSS/Atom** (Nachrichten, Blogs, Behördenfeeds): NiFi `ConsumeRSS` + Parser.
- **Mastodon (ActivityPub)**: Streaming API/WebSocket; Fallback Poll.
- **Reddit**: JSON API (Subreddits, Such-Queries).
```

_Auszug B:_
```
### A. „Schnell & breit“ (MVP <— v0.1.9.x)

* **RSS/Atom** (Nachrichten, Blogs, Behördenfeeds): NiFi `ConsumeRSS` + Parser.
* **Mastodon (ActivityPub)**: Streaming API/WebSocket; Fallback Poll.
* **Reddit**: JSON API (Subreddits, Such-Queries).
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Architektur-für-Live-Datenquellen.md` — *B. „Optional/Reguliert“* — Zeilen 42-51
- B: `docs_ws/docs/dev/v0.2/Architektur-Live-Datenquellen.md` — *B. „Optional/Reguliert“* — Zeilen 43-52

_Auszug A:_
```
### B. „Optional/Reguliert“

- **Twitter/X**: Nur mit gültigem Enterprise/Academic Zugang; Rate-Limits & ToS beachten.
- **Facebook/Instagram (Graph API)**: Nur eigene Seiten/Assets; strikte ToS.
- **RSSHub**: Vorsicht bei ToS; ideal für Feeds, die keinen RSS bieten.
```

_Auszug B:_
```
### B. „Optional/Reguliert“

* **Twitter/X**: Nur mit gültigem Enterprise/Academic Zugang; Rate-Limits & ToS beachten.
* **Facebook/Instagram (Graph API)**: Nur eigene Seiten/Assets; strikte ToS.
* **RSSHub**: Vorsicht bei ToS; ideal für Feeds, die keinen RSS bieten.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Architektur-für-Live-Datenquellen.md` — *4) Anreicherungen (AI/ML/DL) – sofort nutzbare Bausteine* — Zeilen 112-125
- B: `docs_ws/docs/dev/v0.2/Architektur-Live-Datenquellen.md` — *4) Anreicherungen (AI/ML/DL) – sofort nutzbare Bausteine* — Zeilen 113-126

_Auszug A:_
```
## 4) Anreicherungen (AI/ML/DL) – sofort nutzbare Bausteine

- **Language ID**: fastText/langid.
- **NER/RE**: spaCy/Flair/Transformers; DE/EN Modelle.
- **Summarization**: PEGASUS/T5/LLM (mit Längenbudget).
```

_Auszug B:_
```
## 4) Anreicherungen (AI/ML/DL) – sofort nutzbare Bausteine

* **Language ID**: fastText/langid.
* **NER/RE**: spaCy/Flair/Transformers; DE/EN Modelle.
* **Summarization**: PEGASUS/T5/LLM (mit Längenbudget).
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Architektur-für-Live-Datenquellen.md` — *6) Scraping – rechtssicher & robust* — Zeilen 140-149
- B: `docs_ws/docs/dev/v0.2/Architektur-Live-Datenquellen.md` — *6) Scraping – rechtssicher & robust* — Zeilen 142-151

_Auszug A:_
```
## 6) Scraping – rechtssicher & robust

- **Policy-Gate**: robots.txt respektieren, ToS prüfen; **Quellen-Whitelist** für Scraping.
- **Playwright** nur bei notwendigem JS; sonst trafilatura.
- **Rate-Limiter/Backoff**, **Caching** (ETag/If-Modified-Since), **Fingerprint-Rotation** (legal!).
```

_Auszug B:_
```
## 6) Scraping – rechtssicher & robust

* **Policy-Gate**: robots.txt respektieren, ToS prüfen; **Quellen-Whitelist** für Scraping.
* **Playwright** nur bei notwendigem JS; sonst trafilatura.
* **Rate-Limiter/Backoff**, **Caching** (ETag/If-Modified-Since), **Fingerprint-Rotation** (legal!).
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Architektur-für-Live-Datenquellen.md` — *NiFi (robust ingest)* — Zeilen 152-158
- B: `docs_ws/docs/dev/v0.2/Architektur-Live-Datenquellen.md` — *NiFi (robust ingest)* — Zeilen 154-160

_Auszug A:_
```
### NiFi (robust ingest)

- `news_rss_ingest`: `GenerateTableFetch/InvokeHTTP → EvaluateJsonPath → UpdateAttribute → PutS3Object → PublishKafka`
- `web_crawl`: URL-Queue → `InvokeHTTP/PlaywrightTask` → Readability → Persist → Kafka.
- `youtube_websub`: Webhook → Normalize → S3/OpenSearch/Neo4j.
```

_Auszug B:_
```
### NiFi (robust ingest)

* `news_rss_ingest`: `GenerateTableFetch/InvokeHTTP → EvaluateJsonPath → UpdateAttribute → PutS3Object → PublishKafka`
* `web_crawl`: URL-Queue → `InvokeHTTP/PlaywrightTask` → Readability → Persist → Kafka.
* `youtube_websub`: Webhook → Normalize → S3/OpenSearch/Neo4j.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Architektur-für-Live-Datenquellen.md` — *n8n (Analyst Playbooks)* — Zeilen 159-166
- B: `docs_ws/docs/dev/v0.2/Architektur-Live-Datenquellen.md` — *n8n (Analyst Playbooks)* — Zeilen 161-168

_Auszug A:_
```
### n8n (Analyst Playbooks)

- **Breaking-News Alert**: Trigger (Kafka topic `news`) → Filter (keyword/org) → Slack/Email → Dossier anlegen.
- **Entity Watchlist**: Eingabemaske im FE → n8n setzt Filter → bei neuem Hit: Graph-Verlinkung + Superset-Deep-Link.
- **Cross-Source Correlation**: Neue Meldung → Ähnlichkeitssuche → Anreichern mit älteren Posts/News → Report exportieren.
```

_Auszug B:_
```
### n8n (Analyst Playbooks)

* **Breaking-News Alert**: Trigger (Kafka topic `news`) → Filter (keyword/org) → Slack/Email → Dossier anlegen.
* **Entity Watchlist**: Eingabemaske im FE → n8n setzt Filter → bei neuem Hit: Graph-Verlinkung + Superset-Deep-Link.
* **Cross-Source Correlation**: Neue Meldung → Ähnlichkeitssuche → Anreichern mit älteren Posts/News → Report exportieren.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Architektur-für-Live-Datenquellen.md` — *8) Collaboration & Dossier (Live-Kontext)* — Zeilen 167-174
- B: `docs_ws/docs/dev/v0.2/Architektur-Live-Datenquellen.md` — *8) Collaboration & Dossier (Live-Kontext)* — Zeilen 169-176

_Auszug A:_
```
## 8) Collaboration & Dossier (Live-Kontext)

- **Dossier-Lite v1**: Sammle Treffer (News/Posts) + Graph-Kontext → **PDF/Markdown**.
- **Live-Notizen** (CRDT/Sharedb/Yjs): Kommentiere Artikel/Edges; Mention-System.
- **Audit**: Jede Aktion als immutable Log (Loki/Tempo), korreliert via `X-Request-ID`.
```

_Auszug B:_
```
## 8) Collaboration & Dossier (Live-Kontext)

* **Dossier-Lite v1**: Sammle Treffer (News/Posts) + Graph-Kontext → **PDF/Markdown**.
* **Live-Notizen** (CRDT/Sharedb/Yjs): Kommentiere Artikel/Edges; Mention-System.
* **Audit**: Jede Aktion als immutable Log (Loki/Tempo), korreliert via `X-Request-ID`.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Architektur-für-Live-Datenquellen.md` — *9) Plugin-System (auch für Kali-Tools)* — Zeilen 175-190
- B: `docs_ws/docs/dev/v0.2/Architektur-Live-Datenquellen.md` — *9) Plugin-System (auch für Kali-Tools)* — Zeilen 177-193

_Auszug A:_
```
## 9) Plugin-System (auch für Kali-Tools)

- **Spec**:
  - Manifest (`plugin.yaml`): Name, Inputs, Outputs, Permissions, Rate-Limits.
  - Adapter (`runner.py`/`runner.ts`): I/O → **canonical schema**.
```

_Auszug B:_
```
## 9) Plugin-System (auch für Kali-Tools)

* **Spec**:

  * Manifest (`plugin.yaml`): Name, Inputs, Outputs, Permissions, Rate-Limits.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Architektur-für-Live-Datenquellen.md` — *10) Governance, Recht, Sicherheit* — Zeilen 191-201
- B: `docs_ws/docs/dev/v0.2/Architektur-Live-Datenquellen.md` — *10) Governance, Recht, Sicherheit* — Zeilen 194-204

_Auszug A:_
```
## 10) Governance, Recht, Sicherheit

- **Provenienz**: jede Transformation mit `pipeline`, `hash`, `source_url`.
- **Recht**: robots.txt, ToS, Urheberrecht; **Lizenz-Feld** im Schema.
- **GDPR**: PII-Flags, Redaktionsroutinen, Opt-out-Liste pro Domain.
```

_Auszug B:_
```
## 10) Governance, Recht, Sicherheit

* **Provenienz**: jede Transformation mit `pipeline`, `hash`, `source_url`.
* **Recht**: robots.txt, ToS, Urheberrecht; **Lizenz-Feld** im Schema.
* **GDPR**: PII-Flags, Redaktionsroutinen, Opt-out-Liste pro Domain.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Architektur-für-Live-Datenquellen.md` — *v0.1.9.1–.9.4 (MVP Live-Quellen)* — Zeilen 204-210
- B: `docs_ws/docs/dev/v0.2/Architektur-Live-Datenquellen.md` — *v0.1.9.1–.9.4 (MVP Live-Quellen)* — Zeilen 207-213

_Auszug A:_
```
### v0.1.9.1–.9.4 (MVP Live-Quellen)

- RSS/Atom + Mastodon + Reddit + YouTube(WebSub).
- Kanonisches Schema + Normalisierung + NER/Summarization.
- OpenSearch „news“ Index + Superset Dashboard.
```

_Auszug B:_
```
### v0.1.9.1–.9.4 (MVP Live-Quellen)

* RSS/Atom + Mastodon + Reddit + YouTube(WebSub).
* Kanonisches Schema + Normalisierung + NER/Summarization.
* OpenSearch „news“ Index + Superset Dashboard.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Architektur-für-Live-Datenquellen.md` — *v0.1.9.5–.9.7 (Geo + Scraping kontrolliert)* — Zeilen 211-216
- B: `docs_ws/docs/dev/v0.2/Architektur-Live-Datenquellen.md` — *v0.1.9.5–.9.7 (Geo + Scraping kontrolliert)* — Zeilen 214-219

_Auszug A:_
```
### v0.1.9.5–.9.7 (Geo + Scraping kontrolliert)

- Geoparsing Pipeline (Mordecai), Geo-Index, Map Layers.
- Whitelist-Scraper (trafilatura + Playwright fallback).
- Dedupe (MinHash) + Near-Duplicate-Merge.
```

_Auszug B:_
```
### v0.1.9.5–.9.7 (Geo + Scraping kontrolliert)

* Geoparsing Pipeline (Mordecai), Geo-Index, Map Layers.
* Whitelist-Scraper (trafilatura + Playwright fallback).
* Dedupe (MinHash) + Near-Duplicate-Merge.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Architektur-für-Live-Datenquellen.md` — *v0.1.9.8–.9.9 (Collab + Alerts)* — Zeilen 217-221
- B: `docs_ws/docs/dev/v0.2/Architektur-Live-Datenquellen.md` — *v0.1.9.8–.9.9 (Collab + Alerts)* — Zeilen 220-224

_Auszug A:_
```
### v0.1.9.8–.9.9 (Collab + Alerts)

- Dossier-Lite v1 (Export PDF/MD), Notes (Yjs in FE).
- n8n Alerts (Watchlists), Deep-Links zu Superset/Graph.
```

_Auszug B:_
```
### v0.1.9.8–.9.9 (Collab + Alerts)

* Dossier-Lite v1 (Export PDF/MD), Notes (Yjs in FE).
* n8n Alerts (Watchlists), Deep-Links zu Superset/Graph.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Architektur-für-Live-Datenquellen.md` — *v0.2.0 (Härtung + Plugins)* — Zeilen 222-229
- B: `docs_ws/docs/dev/v0.2/Architektur-Live-Datenquellen.md` — *v0.2.0 (Härtung + Plugins)* — Zeilen 225-232

_Auszug A:_
```
### v0.2.0 (Härtung + Plugins)

- Governance/PII Guard, Provenienz obligatorisch.
- Plugin-Runtime v1 (Kali & externe Quellen als Plugins).
- Tests/Docs, Backups, Dashboards finalisieren.
```

_Auszug B:_
```
### v0.2.0 (Härtung + Plugins)

* Governance/PII Guard, Provenienz obligatorisch.
* Plugin-Runtime v1 (Kali & externe Quellen als Plugins).
* Tests/Docs, Backups, Dashboards finalisieren.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Architektur-für-Live-Datenquellen.md` — *12) Konkrete Technik-Blöcke (sofort baubar)* — Zeilen 230-239
- B: `docs_ws/docs/dev/v0.2/Architektur-Live-Datenquellen.md` — *12) Konkrete Technik-Blöcke (sofort baubar)* — Zeilen 233-240

_Auszug A:_
```
## 12) Konkrete Technik-Blöcke (sofort baubar)

- **Python libs**: `trafilatura`, `readability-lxml`, `datasketch`, `mordecai`, `spacy[transformers]`, `langid`, `hnswlib` (Embeddings-ANN).
- **NiFi**: `InvokeHTTP`, `HandleHttpRequest/Response` (Webhooks), `EvaluateJsonPath`, `PublishKafkaRecord_2_0`.
- **n8n**: Standard HTTP + Function Nodes + Slack/Email; später eigene Nodes.
```

_Auszug B:_
```
## 12) Konkrete Technik-Blöcke (sofort baubar)

* **Python libs**: `trafilatura`, `readability-lxml`, `datasketch`, `mordecai`, `spacy[transformers]`, `langid`, `hnswlib` (Embeddings-ANN).
* **NiFi**: `InvokeHTTP`, `HandleHttpRequest/Response` (Webhooks), `EvaluateJsonPath`, `PublishKafkaRecord_2_0`.
* **n8n**: Standard HTTP + Function Nodes + Slack/Email; später eigene Nodes.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *📋 Überblick der Modernisierung* — Zeilen 5-8
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *📋 Überblick der Modernisierung* — Zeilen 5-8

_Auszug A:_
```
## 📋 Überblick der Modernisierung

Diese umfassende Frontend-Modernisierung verwandelt das InfoTerminal von einer einfachen UI in eine **enterprise-ready, professionelle Anwendung** mit:
```

_Auszug B:_
```
## 📋 Überblick der Modernisierung

Diese umfassende Frontend-Modernisierung verwandelt das InfoTerminal von einer einfachen UI in eine **enterprise-ready, professionelle Anwendung** mit:
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *✨ Neue Features & Verbesserungen* — Zeilen 9-23
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *✨ Neue Features & Verbesserungen* — Zeilen 9-23

_Auszug A:_
```
### ✨ Neue Features & Verbesserungen

- **🎨 Professionelles Design System** - Konsistente Farben, Typography, Spacing
- **🌗 Dark Mode Support** - Automatisches Theme-Switching + System-Sync
- **📱 Mobile-First Design** - Vollständig responsive mit Touch-Optimierung
```

_Auszug B:_
```
### ✨ Neue Features & Verbesserungen

- **🎨 Professionelles Design System** - Konsistente Farben, Typography, Spacing
- **🌗 Dark Mode Support** - Automatisches Theme-Switching + System-Sync
- **📱 Mobile-First Design** - Vollständig responsive mit Touch-Optimierung
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *🛠️ Technische Verbesserungen* — Zeilen 24-34
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *🛠️ Technische Verbesserungen* — Zeilen 32-42

_Auszug A:_
```
### 🛠️ Technische Verbesserungen

- **TypeScript** - Vollständige Typisierung
- **Tailwind CSS** - Utility-first Styling
- **Component Architecture** - Wiederverwendbare Komponenten
```

_Auszug B:_
```
### 🛠️ Technische Verbesserungen

- **TypeScript** - Vollständige Typisierung
- **Tailwind CSS** - Utility-first Styling
- **Component Architecture** - Wiederverwendbare Komponenten
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Backup bestehender Dateien* — Zeilen 42-49
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Backup bestehender Dateien* — Zeilen 50-57

_Auszug A:_
```
# Backup bestehender Dateien
cp pages/index.tsx pages/index.tsx.backup
cp pages/search.tsx pages/search.tsx.backup
cp pages/docs/[id].tsx pages/docs/[id].tsx.backup
cp pages/graphx.tsx pages/graphx.tsx.backup
```

_Auszug B:_
```
# Backup bestehender Dateien
cp pages/index.tsx pages/index.tsx.backup
cp pages/search.tsx pages/search.tsx.backup
cp pages/docs/[id].tsx pages/docs/[id].tsx.backup
cp pages/graphx.tsx pages/graphx.tsx.backup
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Core Dependencies* — Zeilen 53-55
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Core Dependencies* — Zeilen 61-63

_Auszug A:_
```
# Core Dependencies
npm install @tailwindcss/forms @tailwindcss/typography @tailwindcss/line-clamp
```

_Auszug B:_
```
# Core Dependencies
npm install @tailwindcss/forms @tailwindcss/typography @tailwindcss/line-clamp
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Optional Advanced Components* — Zeilen 56-58
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Optional Advanced Components* — Zeilen 67-69

_Auszug A:_
```
# Optional Advanced Components
npm install @headlessui/react @heroicons/react
```

_Auszug B:_
```
# Optional Advanced Components
npm install @headlessui/react @heroicons/react
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Neue Komponenten-Struktur* — Zeilen 66-71
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Neue Komponenten-Struktur* — Zeilen 77-82

_Auszug A:_
```
# Neue Komponenten-Struktur
mkdir -p src/components/{ui,forms,auth,charts,mobile,health}
mkdir -p src/lib
mkdir -p src/hooks
mkdir -p src/types
```

_Auszug B:_
```
# Neue Komponenten-Struktur
mkdir -p src/components/{ui,forms,auth,charts,mobile,health}
mkdir -p src/lib
mkdir -p src/hooks
mkdir -p src/types
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Layout Komponenten* — Zeilen 72-79
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Layout Komponenten* — Zeilen 83-90

_Auszug A:_
```
# Layout Komponenten
mkdir -p src/components/layout
mkdir -p src/components/search
mkdir -p src/components/entities
mkdir -p src/components/docs
```

_Auszug B:_
```
# Layout Komponenten
mkdir -p src/components/layout
mkdir -p src/components/search
mkdir -p src/components/entities
mkdir -p src/components/docs
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Core Files* — Zeilen 82-89
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Core Files* — Zeilen 93-100

_Auszug A:_
```
#### Core Files

1. **Design System** → `src/lib/theme.ts`
2. **Theme Provider** → `src/lib/theme-provider.tsx`
3. **Notifications** → `src/lib/notifications.tsx`
```

_Auszug B:_
```
#### Core Files

1. **Design System** → `src/lib/theme.ts`
2. **Theme Provider** → `src/lib/theme-provider.tsx`
3. **Notifications** → `src/lib/notifications.tsx`
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Layout & Navigation* — Zeilen 90-95
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Layout & Navigation* — Zeilen 101-106

_Auszug A:_
```
#### Layout & Navigation

1. **Dashboard Layout** → `src/components/layout/DashboardLayout.tsx`
2. **Mobile Navigation** → `src/components/mobile/MobileNavigation.tsx`
3. **Settings Panel** → `src/components/mobile/SettingsPanel.tsx`
```

_Auszug B:_
```
#### Layout & Navigation

1. **Dashboard Layout** → `src/components/layout/DashboardLayout.tsx`
2. **Mobile Navigation** → `src/components/mobile/MobileNavigation.tsx`
3. **Settings Panel** → `src/components/mobile/SettingsPanel.tsx`
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Form System* — Zeilen 96-100
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Form System* — Zeilen 107-111

_Auszug A:_
```
#### Form System

1. **Form Components** → `src/components/forms/FormComponents.tsx`
2. **Authentication** → `src/components/auth/AuthProvider.tsx`
```

_Auszug B:_
```
#### Form System

1. **Form Components** → `src/components/forms/FormComponents.tsx`
2. **Authentication** → `src/components/auth/AuthProvider.tsx`
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *UI Components* — Zeilen 101-106
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *UI Components* — Zeilen 112-117

_Auszug A:_
```
#### UI Components

1. **Data Table** → `src/components/ui/DataTable.tsx`
2. **Charts** → `src/components/charts/index.tsx`
3. **Error Boundary** → `src/components/ui/ErrorBoundary.tsx`
```

_Auszug B:_
```
#### UI Components

1. **Data Table** → `src/components/ui/DataTable.tsx`
2. **Charts** → `src/components/charts/index.tsx`
3. **Error Boundary** → `src/components/ui/ErrorBoundary.tsx`
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Pages (Ersetzen)* — Zeilen 107-113
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Pages (Ersetzen)* — Zeilen 118-124

_Auszug A:_
```
#### Pages (Ersetzen)

1. **Homepage** → `pages/index.tsx`
2. **Search** → `src/components/search/ModernSearch.tsx`
3. **Document Detail** → `pages/docs/[id].tsx`
```

_Auszug B:_
```
#### Pages (Ersetzen)

1. **Homepage** → `pages/index.tsx`
2. **Search** → `src/components/search/ModernSearch.tsx`
3. **Document Detail** → `pages/docs/[id].tsx`
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Configuration* — Zeilen 114-118
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Configuration* — Zeilen 125-129

_Auszug A:_
```
#### Configuration

1. **Tailwind Config** → `tailwind.config.js`
2. **Next.js Config** → Update für Fonts & optimizations
```

_Auszug B:_
```
#### Configuration

1. **Tailwind Config** → `tailwind.config.js`
2. **Next.js Config** → Update für Fonts & optimizations
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *.env.local* — Zeilen 200-209
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *.env.local* — Zeilen 211-220

_Auszug A:_
```
# .env.local
NEXT_PUBLIC_SEARCH_API=http://localhost:8001
NEXT_PUBLIC_GRAPH_API=http://localhost:8002
NEXT_PUBLIC_DOCENTITIES_API=http://localhost:8006
NEXT_PUBLIC_NLP_API=http://localhost:8003
```

_Auszug B:_
```
# .env.local
NEXT_PUBLIC_SEARCH_API=http://localhost:8001
NEXT_PUBLIC_GRAPH_API=http://localhost:8002
NEXT_PUBLIC_DOCENTITIES_API=http://localhost:8006
NEXT_PUBLIC_NLP_API=http://localhost:8003
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Phase 1: Design System (Tag 1-2)* — Zeilen 212-218
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Phase 1: Design System (Tag 1-2)* — Zeilen 223-229

_Auszug A:_
```
### Phase 1: Design System (Tag 1-2)

- ✅ Theme System installieren
- ✅ Tailwind Config updaten
- ✅ Dark Mode implementieren
```

_Auszug B:_
```
### Phase 1: Design System (Tag 1-2)

- ✅ Theme System installieren
- ✅ Tailwind Config updaten
- ✅ Dark Mode implementieren
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Phase 2: Navigation & Layout (Tag 3-4)* — Zeilen 219-225
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Phase 2: Navigation & Layout (Tag 3-4)* — Zeilen 230-236

_Auszug A:_
```
### Phase 2: Navigation & Layout (Tag 3-4)

- ✅ DashboardLayout implementieren
- ✅ Mobile Navigation hinzufügen
- ✅ Header/Sidebar modernisieren
```

_Auszug B:_
```
### Phase 2: Navigation & Layout (Tag 3-4)

- ✅ DashboardLayout implementieren
- ✅ Mobile Navigation hinzufügen
- ✅ Header/Sidebar modernisieren
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Phase 3: Core Components (Tag 5-7)* — Zeilen 226-232
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Phase 3: Core Components (Tag 5-7)* — Zeilen 237-243

_Auszug A:_
```
### Phase 3: Core Components (Tag 5-7)

- ✅ Form System implementieren
- ✅ Data Table hinzufügen
- ✅ Charts integrieren
```

_Auszug B:_
```
### Phase 3: Core Components (Tag 5-7)

- ✅ Form System implementieren
- ✅ Data Table hinzufügen
- ✅ Charts integrieren
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Phase 4: Advanced Features (Tag 8-10)* — Zeilen 233-239
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Phase 4: Advanced Features (Tag 8-10)* — Zeilen 244-250

_Auszug A:_
```
### Phase 4: Advanced Features (Tag 8-10)

- ✅ Command Palette aktivieren
- ✅ Notifications implementieren
- ✅ Real-time Updates einbauen
```

_Auszug B:_
```
### Phase 4: Advanced Features (Tag 8-10)

- ✅ Command Palette aktivieren
- ✅ Notifications implementieren
- ✅ Real-time Updates einbauen
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Phase 5: Pages Migration (Tag 11-12)* — Zeilen 240-246
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Phase 5: Pages Migration (Tag 11-12)* — Zeilen 251-257

_Auszug A:_
```
### Phase 5: Pages Migration (Tag 11-12)

- ✅ Homepage modernisieren
- ✅ Search Page übarbeiten
- ✅ Document Detail optimieren
```

_Auszug B:_
```
### Phase 5: Pages Migration (Tag 11-12)

- ✅ Homepage modernisieren
- ✅ Search Page übarbeiten
- ✅ Document Detail optimieren
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Phase 6: Polish & Testing (Tag 13-14)* — Zeilen 247-253
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Phase 6: Polish & Testing (Tag 13-14)* — Zeilen 258-264

_Auszug A:_
```
### Phase 6: Polish & Testing (Tag 13-14)

- ✅ Mobile Testing
- ✅ Performance Optimierung
- ✅ Accessibility Check
```

_Auszug B:_
```
### Phase 6: Polish & Testing (Tag 13-14)

- ✅ Mobile Testing
- ✅ Performance Optimierung
- ✅ Accessibility Check
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Manual Testing Checklist* — Zeilen 275-288
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Manual Testing Checklist* — Zeilen 286-299

_Auszug A:_
```
### Manual Testing Checklist

- [ ] **Desktop Navigation** - Sidebar funktioniert
- [ ] **Mobile Navigation** - Hamburger Menu + Bottom Tabs
- [ ] **Dark/Light Mode** - Toggle funktioniert
```

_Auszug B:_
```
### Manual Testing Checklist

- [ ] **Desktop Navigation** - Sidebar funktioniert
- [ ] **Mobile Navigation** - Hamburger Menu + Bottom Tabs
- [ ] **Dark/Light Mode** - Toggle funktioniert
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Performance Checklist* — Zeilen 309-316
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Performance Checklist* — Zeilen 320-327

_Auszug A:_
```
### Performance Checklist

- [ ] **Bundle Size** < 500KB gzipped
- [ ] **First Contentful Paint** < 1.8s
- [ ] **Largest Contentful Paint** < 2.5s
```

_Auszug B:_
```
### Performance Checklist

- [ ] **Bundle Size** < 500KB gzipped
- [ ] **First Contentful Paint** < 1.8s
- [ ] **Largest Contentful Paint** < 2.5s
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Key Metrics zu verfolgen* — Zeilen 330-343
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Key Metrics zu verfolgen* — Zeilen 341-354

_Auszug A:_
```
### Key Metrics zu verfolgen

1. **User Experience**
   - Page Load Times
   - User Interaction Response
```

_Auszug B:_
```
### Key Metrics zu verfolgen

1. **User Experience**
   - Page Load Times
   - User Interaction Response
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Dependencies* — Zeilen 383-387
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Dependencies* — Zeilen 394-398

_Auszug A:_
```
# Dependencies
rm -rf node_modules package-lock.json
npm install
```
```

_Auszug B:_
```
# Dependencies
rm -rf node_modules package-lock.json
npm install
```
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *<meta name="viewport" content="width=device-width, initial-scale=1">* — Zeilen 409-411
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *<meta name="viewport" content="width=device-width, initial-scale=1">* — Zeilen 420-422

_Auszug A:_
```
# <meta name="viewport" content="width=device-width, initial-scale=1">
```
```

_Auszug B:_
```
# <meta name="viewport" content="width=device-width, initial-scale=1">
```
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Für Entwickler* — Zeilen 414-419
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Für Entwickler* — Zeilen 425-430

_Auszug A:_
```
### Für Entwickler

1. **Component Storybook** - Komponenten-Dokumentation
2. **Style Guide** - Design System Regeln
3. **API Reference** - Hook & Utility Dokumentation
```

_Auszug B:_
```
### Für Entwickler

1. **Component Storybook** - Komponenten-Dokumentation
2. **Style Guide** - Design System Regeln
3. **API Reference** - Hook & Utility Dokumentation
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Für Designer* — Zeilen 420-425
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Für Designer* — Zeilen 431-436

_Auszug A:_
```
### Für Designer

1. **Figma Components** - Design System für Designer
2. **Brand Guidelines** - Farben, Typography, Spacing
3. **Responsive Breakpoints** - Mobile/Desktop Guidelines
```

_Auszug B:_
```
### Für Designer

1. **Figma Components** - Design System für Designer
2. **Brand Guidelines** - Farben, Typography, Spacing
3. **Responsive Breakpoints** - Mobile/Desktop Guidelines
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Vor der Modernisierung (Baseline)* — Zeilen 428-434
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Vor der Modernisierung (Baseline)* — Zeilen 439-445

_Auszug A:_
```
### Vor der Modernisierung (Baseline)

- ❌ Keine Mobile Unterstützung
- ❌ Inline Styles überall
- ❌ Keine Konsistenz im Design
```

_Auszug B:_
```
### Vor der Modernisierung (Baseline)

- ❌ Keine Mobile Unterstützung
- ❌ Inline Styles überall
- ❌ Keine Konsistenz im Design
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Nach der Modernisierung (Ziel)* — Zeilen 435-442
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Nach der Modernisierung (Ziel)* — Zeilen 446-453

_Auszug A:_
```
### Nach der Modernisierung (Ziel)

- ✅ **90%+ Mobile Satisfaction Score**
- ✅ **< 2s Page Load Time**
- ✅ **95%+ Component Reusability**
```

_Auszug B:_
```
### Nach der Modernisierung (Ziel)

- ✅ **90%+ Mobile Satisfaction Score**
- ✅ **< 2s Page Load Time**
- ✅ **95%+ Component Reusability**
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *🚀 Go-Live Checklist* — Zeilen 443-457
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *🚀 Go-Live Checklist* — Zeilen 454-468

_Auszug A:_
```
## 🚀 Go-Live Checklist

- [ ] **Alle Tests bestanden**
- [ ] **Performance Benchmarks erreicht**
- [ ] **Mobile Testing abgeschlossen**
```

_Auszug B:_
```
## 🚀 Go-Live Checklist

- [ ] **Alle Tests bestanden**
- [ ] **Performance Benchmarks erreicht**
- [ ] **Mobile Testing abgeschlossen**
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *🎉 Herzlichen Glückwunsch* — Zeilen 458-461
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *🎉 Herzlichen Glückwunsch* — Zeilen 469-472

_Auszug A:_
```
## 🎉 Herzlichen Glückwunsch

Nach der vollständigen Implementierung haben Sie InfoTerminal in eine **moderne, professionelle und benutzerfreundliche Anwendung** verwandelt, die mit aktuellen Enterprise-Standards mithalten kann.
```

_Auszug B:_
```
## 🎉 Herzlichen Glückwunsch

Nach der vollständigen Implementierung haben Sie InfoTerminal in eine **moderne, professionelle und benutzerfreundliche Anwendung** verwandelt, die mit aktuellen Enterprise-Standards mithalten kann.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Frontend-Modernisierung_Setup-Guide.md` — *Was Sie erreicht haben* — Zeilen 462-472
- B: `docs_ws/docs/dev/Frontend-Modernisierung.md` — *Was Sie erreicht haben* — Zeilen 473-483

_Auszug A:_
```
### Was Sie erreicht haben

- 🚀 **10x bessere User Experience**
- 📱 **Mobile-First Design**
- ⚡ **Performance Optimiert**
```

_Auszug B:_
```
### Was Sie erreicht haben

- 🚀 **10x bessere User Experience**
- 📱 **Mobile-First Design**
- ⚡ **Performance Optimiert**
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/RAG-Systeme.md` — *1) Zielbild* — Zeilen 3-13
- B: `docs_ws/docs/dev/v0.2/v0.3+/RAG-Systeme.md` — *1) Zielbild* — Zeilen 3-14

_Auszug A:_
```
## 1) Zielbild

- **RAG-Layer** mit Gesetzestexten (z. B. SGB, StGB, EU-Verordnungen, Finanzmarktgesetze).
- **Verknüpfung mit Datenquellen** (Firmenregister, OpenBB, Open Data, News/SoMe, Threat Feeds).
- **Fragen beantworten können wie:**
```

_Auszug B:_
```
## 1) Zielbild

* **RAG-Layer** mit Gesetzestexten (z. B. SGB, StGB, EU-Verordnungen, Finanzmarktgesetze).
* **Verknüpfung mit Datenquellen** (Firmenregister, OpenBB, Open Data, News/SoMe, Threat Feeds).
* **Fragen beantworten können wie:**
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/RAG-Systeme.md` — *a) RAG-Speicher* — Zeilen 16-21
- B: `docs_ws/docs/dev/v0.2/v0.3+/RAG-Systeme.md` — *a) RAG-Speicher* — Zeilen 17-22

_Auszug A:_
```
### a) RAG-Speicher

- **Gesetze/Regelwerke**: in Chunks (Paragraph/Artikel), mit Metadaten (Quelle, Gültigkeit, Änderungsdatum).
- **Index**: OpenSearch (BM25 + Embeddings), ergänzt durch Neo4j-Knoten „(\:Law {id, title, paragraph, domain})“.
- **Versionierung**: Jede Änderung (z. B. neue Gesetzesnovelle) als neuer Node mit `[:AMENDS]` Relation.
```

_Auszug B:_
```
### a) RAG-Speicher

* **Gesetze/Regelwerke**: in Chunks (Paragraph/Artikel), mit Metadaten (Quelle, Gültigkeit, Änderungsdatum).
* **Index**: OpenSearch (BM25 + Embeddings), ergänzt durch Neo4j-Knoten „(\:Law {id, title, paragraph, domain})“.
* **Versionierung**: Jede Änderung (z. B. neue Gesetzesnovelle) als neuer Node mit `[:AMENDS]` Relation.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/RAG-Systeme.md` — *b) Abfrage & Verknüpfung* — Zeilen 22-32
- B: `docs_ws/docs/dev/v0.2/v0.3+/RAG-Systeme.md` — *b) Abfrage & Verknüpfung* — Zeilen 23-34

_Auszug A:_
```
### b) Abfrage & Verknüpfung

- **RAG Query Flow**:
  1. User-Frage → Query Expansion (Entities, Zeit, Gesetzesbegriffe).
  2. Retrieval: relevante Gesetzesparagraphen + Unternehmensdaten + Politische Akteure.
```

_Auszug B:_
```
### b) Abfrage & Verknüpfung

* **RAG Query Flow**:

  1. User-Frage → Query Expansion (Entities, Zeit, Gesetzesbegriffe).
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/RAG-Systeme.md` — *Beispiel A – Politiker & Firmen* — Zeilen 44-55
- B: `docs_ws/docs/dev/v0.2/v0.3+/RAG-Systeme.md` — *Beispiel A – Politiker & Firmen* — Zeilen 47-58

_Auszug A:_
```
### Beispiel A – Politiker & Firmen

**Query:** „Welche Politiker der Partei X haben Verbindungen zu Firma Y und Gesetze mit Auswirkungen verabschiedet?“

- Retrieval: Partei X (Graph: Entities), Firma Y (Handelsregister, Lobbylisten), Gesetzesänderungen (Parlamentsdokumente).
```

_Auszug B:_
```
### Beispiel A – Politiker & Firmen

**Query:** „Welche Politiker der Partei X haben Verbindungen zu Firma Y und Gesetze mit Auswirkungen verabschiedet?“

* Retrieval: Partei X (Graph: Entities), Firma Y (Handelsregister, Lobbylisten), Gesetzesänderungen (Parlamentsdokumente).
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/RAG-Systeme.md` — *Beispiel B – Branchen-Compliance* — Zeilen 56-69
- B: `docs_ws/docs/dev/v0.2/v0.3+/RAG-Systeme.md` — *Beispiel B – Branchen-Compliance* — Zeilen 59-72

_Auszug A:_
```
### Beispiel B – Branchen-Compliance

**Query:** „Welche Firmen aus Branche Z stehen in Verbindung zu Gesetzesverstößen?“

- Retrieval: Firmen-Cluster (Branche Z), News/Dossiers, Gesetzestexte.
```

_Auszug B:_
```
### Beispiel B – Branchen-Compliance

**Query:** „Welche Firmen aus Branche Z stehen in Verbindung zu Gesetzesverstößen?“

* Retrieval: Firmen-Cluster (Branche Z), News/Dossiers, Gesetzestexte.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/RAG-Systeme.md` — *4) Technische Umsetzung (Integration in InfoTerminal)* — Zeilen 70-96
- B: `docs_ws/docs/dev/v0.2/v0.3+/RAG-Systeme.md` — *4) Technische Umsetzung (Integration in InfoTerminal)* — Zeilen 73-104

_Auszug A:_
```
## 4) Technische Umsetzung (Integration in InfoTerminal)

- **RAG-Service (`rag-api`)**:
  - Indexierung von Gesetzestexten, Verträgen, Regularien.
  - API-Endpunkte:
```

_Auszug B:_
```
## 4) Technische Umsetzung (Integration in InfoTerminal)

* **RAG-Service (`rag-api`)**:

  * Indexierung von Gesetzestexten, Verträgen, Regularien.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/RAG-Systeme.md` — *5) Erweiterungen & Differenzierung* — Zeilen 97-106
- B: `docs_ws/docs/dev/v0.2/v0.3+/RAG-Systeme.md` — *5) Erweiterungen & Differenzierung* — Zeilen 105-114

_Auszug A:_
```
## 5) Erweiterungen & Differenzierung

- **Predictive Impact**: Simulation, wie geplante Gesetze Branchen/Unternehmen betreffen.
- **Comparative Law**: EU vs. nationales Recht nebeneinander.
- **Compliance Alerts**: n8n Flow → „Neue Gesetzesänderung betrifft Branche Z → Firmenwarnung“.
```

_Auszug B:_
```
## 5) Erweiterungen & Differenzierung

* **Predictive Impact**: Simulation, wie geplante Gesetze Branchen/Unternehmen betreffen.
* **Comparative Law**: EU vs. nationales Recht nebeneinander.
* **Compliance Alerts**: n8n Flow → „Neue Gesetzesänderung betrifft Branche Z → Firmenwarnung“.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *🛡️ VERIFICATION-BLUEPRINT.md* — Zeilen 1-6
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *🛡️ VERIFICATION-BLUEPRINT.md* — Zeilen 188-192

_Auszug A:_
```
# 🛡️ VERIFICATION-BLUEPRINT.md

> AI-gestützte Verifikation von Web/Social-Signalen in InfoTerminal  
> Zielgruppen: Journalist:innen, Sicherheitsbehörden/-firmen, Forschung  
> Stand: 2025-09-05
```

_Auszug B:_
```
# 🛡️ VERIFICATION-BLUEPRINT.md
> AI-gestützte Verifikation von Web/Social-Signalen in InfoTerminal  
> Zielgruppen: Journalist:innen, Sicherheitsbehörden/-firmen, Forschung  
> Stand: 2025-09-05
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *🎯 Ziele* — Zeilen 7-15
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *🎯 Ziele* — Zeilen 193-200

_Auszug A:_
```
## 🎯 Ziele

- Falschinformationen früh erkennen, markieren, priorisieren
- Transparente Begründung (Evidenz, Widersprüche, Unsicherheit)
- Human-in-the-loop: Review/Override → kontinuierliches Lernen (Active Learning)
```

_Auszug B:_
```
## 🎯 Ziele
- Falschinformationen früh erkennen, markieren, priorisieren
- Transparente Begründung (Evidenz, Widersprüche, Unsicherheit)
- Human-in-the-loop: Review/Override → kontinuierliches Lernen (Active Learning)
- Forensik-taugliche Provenienz (Hashes, Pipelines, Versionen)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *🧭 Architektur (High-Level)* — Zeilen 16-31
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *🧭 Architektur (High-Level)* — Zeilen 201-214

_Auszug A:_
```
## 🧭 Architektur (High-Level)

**Flow:** Quelle → NiFi Ingest → Normalize (Kanonisches Schema) → **Verification Pipeline** → Scores/Labels → Persistenz (OpenSearch/Neo4j/S3) → n8n Alerts/Agents → Frontend (Badges, Evidence-Panel, Dossier)

**Services/Layer:**
```

_Auszug B:_
```
## 🧭 Architektur (High-Level)
**Flow:** Quelle → NiFi Ingest → Normalize (Kanonisches Schema) → **Verification Pipeline** → Scores/Labels → Persistenz (OpenSearch/Neo4j/S3) → n8n Alerts/Agents → Frontend (Badges, Evidence-Panel, Dossier)

**Services/Layer:**
- **nifi/** ingest + ETL
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *1) Source Reputation & Bot-Likelihood ([VERIF-1])* — Zeilen 34-39
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *1) Source Reputation & Bot-Likelihood  ([VERIF-1])* — Zeilen 217-221

_Auszug A:_
```
### 1) Source Reputation & Bot-Likelihood ([VERIF-1])

**Input:** `source.*`, Account/Domain-Metadaten  
**Features:** Domain-Ruf, Account-Alter, Posting-Kadenz, Netzwerk-Zentralität, Bot-Heuristiken  
**Output:** `source_reliability∈[0,1]`, `bot_likelihood∈[0,1]`, `risk_flags:[…]`
```

_Auszug B:_
```
### 1) Source Reputation & Bot-Likelihood  ([VERIF-1])
**Input:** `source.*`, Account/Domain-Metadaten  
**Features:** Domain-Ruf, Account-Alter, Posting-Kadenz, Netzwerk-Zentralität, Bot-Heuristiken  
**Output:** `source_reliability∈[0,1]`, `bot_likelihood∈[0,1]`, `risk_flags:[…]`
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *2) Claim-Extraktion & Dedup ([VERIF-2])* — Zeilen 40-45
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *2) Claim-Extraktion & Dedup  ([VERIF-2])* — Zeilen 222-226

_Auszug A:_
```
### 2) Claim-Extraktion & Dedup ([VERIF-2])

**Input:** `content.title|summary|body_text`  
**Steps:** Claim-Spans extrahieren → normalisieren → MinHash/SimHash clustern  
**Output:** `claim_cluster_id`, `claim_text_norm`, `near_dupes:[…]`
```

_Auszug B:_
```
### 2) Claim-Extraktion & Dedup  ([VERIF-2])
**Input:** `content.title|summary|body_text`  
**Steps:** Claim-Spans extrahieren → normalisieren → MinHash/SimHash clustern  
**Output:** `claim_cluster_id`, `claim_text_norm`, `near_dupes:[…]`
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *3) Evidence Retrieval & Rerank ([VERIF-3])* — Zeilen 46-51
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *3) Evidence Retrieval & Rerank  ([VERIF-3])* — Zeilen 227-231

_Auszug A:_
```
### 3) Evidence Retrieval & Rerank ([VERIF-3])

**Input:** Claim  
**Steps:** Hybrid Retrieval (BM25 + dense) → rerank (sentence-transformers)  
**Output:** `evidence.pro[]` & `evidence.contra[]` (Kandidaten mit Score)
```

_Auszug B:_
```
### 3) Evidence Retrieval & Rerank  ([VERIF-3])
**Input:** Claim  
**Steps:** Hybrid Retrieval (BM25 + dense) → rerank (sentence-transformers)  
**Output:** `evidence.pro[]` & `evidence.contra[]` (Kandidaten mit Score)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *4) RTE/Stance (Entailment) ([VERIF-4])* — Zeilen 52-57
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *4) RTE/Stance (Entailment)  ([VERIF-4])* — Zeilen 232-236

_Auszug A:_
```
### 4) RTE/Stance (Entailment) ([VERIF-4])

**Input:** Claim + Evidenz  
**Steps:** NLI/RTE → `entails|contradicts|neutral`, Confidence  
**Output:** pro Evidenz Klassifikation + Score
```

_Auszug B:_
```
### 4) RTE/Stance (Entailment)  ([VERIF-4])
**Input:** Claim + Evidenz  
**Steps:** NLI/RTE → `entails|contradicts|neutral`, Confidence  
**Output:** pro Evidenz Klassifikation + Score
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *5) Temporal & Geo-Konsistenz ([VERIF-5])* — Zeilen 58-62
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *5) Temporal & Geo-Konsistenz  ([VERIF-5])* — Zeilen 237-240

_Auszug A:_
```
### 5) Temporal & Geo-Konsistenz ([VERIF-5])

**Input:** Zeit/Ort aus Text/Metadaten  
**Output:** `temporal_consistency∈[0,1]`, `geo_consistency∈[0,1]`
```

_Auszug B:_
```
### 5) Temporal & Geo-Konsistenz  ([VERIF-5])
**Input:** Zeit/Ort aus Text/Metadaten  
**Output:** `temporal_consistency∈[0,1]`, `geo_consistency∈[0,1]`
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *6) Medien-Forensik ([VERIF-6])* — Zeilen 63-67
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *6) Medien-Forensik  ([VERIF-6])* — Zeilen 241-244

_Auszug A:_
```
### 6) Medien-Forensik ([VERIF-6])

**Bild/Video/Audio:** pHash/dHash, EXIF, Keyframes, Reverse Search Hits, ELA-Hinweise  
**Output:** `media_flags:[…]`, `reverse_hits:int`
```

_Auszug B:_
```
### 6) Medien-Forensik  ([VERIF-6])
**Bild/Video/Audio:** pHash/dHash, EXIF, Keyframes, Reverse Search Hits, ELA-Hinweise  
**Output:** `media_flags:[…]`, `reverse_hits:int`
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *8) Human-in-the-loop & Active Learning ([VERIF-8],[VERIF-9])* — Zeilen 78-83
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *8) Human-in-the-loop & Active Learning  ([VERIF-8],[VERIF-9])* — Zeilen 254-258

_Auszug A:_
```
### 8) Human-in-the-loop & Active Learning ([VERIF-8],[VERIF-9])

Review-UI (Evidenz, Begründungen, Overrides) → Label-Store → periodisches Re-Training

---
```

_Auszug B:_
```
### 8) Human-in-the-loop & Active Learning  ([VERIF-8],[VERIF-9])
Review-UI (Evidenz, Begründungen, Overrides) → Label-Store → periodisches Re-Training

---
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *🕸️ Neo4j: Knoten, Kanten, Constraints* — Zeilen 225-261
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *🕸️ Neo4j: Knoten, Kanten, Constraints* — Zeilen 368-404

_Auszug A:_
```
## 🕸️ Neo4j: Knoten, Kanten, Constraints

**Nodes:** `(:Article {id}), (:Source {id}), (:Claim {id, text_norm}), (:Evidence {id, url})`
**Edges:**

```

_Auszug B:_
```
## 🕸️ Neo4j: Knoten, Kanten, Constraints

**Nodes:** `(:Article {id}), (:Source {id}), (:Claim {id, text_norm}), (:Evidence {id, url})`
**Edges:**

```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *🧰 NiFi Flows (Vorlagen)* — Zeilen 262-285
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *🧰 NiFi Flows (Vorlagen)* — Zeilen 405-429

_Auszug A:_
```
## 🧰 NiFi Flows (Vorlagen)

1. `ingest_normalize`
   - `InvokeHTTP/ConsumeRSS` → `JoltTransformJSON` (kanonisch) → `UpdateAttribute` (hash) → `PutS3Object` → `PublishKafka (topic:new_items)`

```

_Auszug B:_
```
## 🧰 NiFi Flows (Vorlagen)

1. `ingest_normalize`

   * `InvokeHTTP/ConsumeRSS` → `JoltTransformJSON` (kanonisch) → `UpdateAttribute` (hash) → `PutS3Object` → `PublishKafka (topic:new_items)`
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *🧪 Modelle & Runtime* — Zeilen 295-314
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *🧪 Modelle & Runtime* — Zeilen 439-458

_Auszug A:_
```
## 🧪 Modelle & Runtime

- **NER/RE/Summarization:** spaCy/Transformers (DE/EN), Light-LLM optional
- **Dense Embeddings:** `sentence-transformers all-MiniLM-L6-v2` (384d) → HNSW/FAISS
- **RTE/NLI:** z. B. `multilingual-mpnet-base` oder spezialisiertes NLI-Modell
```

_Auszug B:_
```
## 🧪 Modelle & Runtime

* **NER/RE/Summarization:** spaCy/Transformers (DE/EN), Light-LLM optional
* **Dense Embeddings:** `sentence-transformers all-MiniLM-L6-v2` (384d) → HNSW/FAISS
* **RTE/NLI:** z. B. `multilingual-mpnet-base` oder spezialisiertes NLI-Modell
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *nlp-verif* — Zeilen 317-323
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *nlp-verif* — Zeilen 461-467

_Auszug A:_
```
### nlp-verif

- `POST /claim/extract` → `[ {id, span, text_norm} ]`
- `POST /retrieval` → `{claim} → {pro:[…], contra:[…]}`
- `POST /rte` → `{claim, evidence} → {label, score}`
```

_Auszug B:_
```
### nlp-verif

* `POST /claim/extract` → `[ {id, span, text_norm} ]`
* `POST /retrieval` → `{claim} → {pro:[…], contra:[…]}`
* `POST /rte` → `{claim, evidence} → {label, score}`
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *search-api* — Zeilen 324-328
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *search-api* — Zeilen 468-472

_Auszug A:_
```
### search-api

- `POST /search/bm25` → Top-k Kandidaten
- `POST /search/embed` → Embeddings + ANN Suche
```

_Auszug B:_
```
### search-api

* `POST /search/bm25` → Top-k Kandidaten
* `POST /search/embed` → Embeddings + ANN Suche
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *graph-api* — Zeilen 329-335
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *graph-api* — Zeilen 473-479

_Auszug A:_
```
### graph-api

- `POST /claims/upsert` → MERGE Claim/Edges
- `GET /claims/{id}` → Claim + Evidenz + Verlauf

```

_Auszug B:_
```
### graph-api

* `POST /claims/upsert` → MERGE Claim/Edges
* `GET /claims/{id}` → Claim + Evidenz + Verlauf

```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *📈 Metriken & Observability* — Zeilen 336-349
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *📈 Metriken & Observability* — Zeilen 480-493

_Auszug A:_
```
## 📈 Metriken & Observability

**Prometheus (nlp-verif):**

- `verif_pipeline_events_total{stage=…}`
```

_Auszug B:_
```
## 📈 Metriken & Observability

**Prometheus (nlp-verif):**

* `verif_pipeline_events_total{stage=…}`
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *⚖️ Ethik, Recht & Security* — Zeilen 350-359
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *⚖️ Ethik, Recht & Security* — Zeilen 494-503

_Auszug A:_
```
## ⚖️ Ethik, Recht & Security

- **Transparenz:** Label + Score + Evidenz + Unsicherheit im UI
- **Kein Auto-Takedown:** Markieren/Ranken, Entscheidung bleibt beim Menschen
- **PII-Filter:** Redaktionsregeln, besonders bei Leaks/Quellen­schutz
```

_Auszug B:_
```
## ⚖️ Ethik, Recht & Security

* **Transparenz:** Label + Score + Evidenz + Unsicherheit im UI
* **Kein Auto-Takedown:** Markieren/Ranken, Entscheidung bleibt beim Menschen
* **PII-Filter:** Redaktionsregeln, besonders bei Leaks/Quellen­schutz
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/VERIFICATION-BLUEPRINT.md` — *🚀 Rollout-Plan (empfohlen)* — Zeilen 376-384
- B: `docs_ws/docs/blueprints/VERIFICATION-BLUEPRINT.md` — *🚀 Rollout-Plan (empfohlen)* — Zeilen 520-528

_Auszug A:_
```
## 🚀 Rollout-Plan (empfohlen)

1. **VERIF-1 + VERIF-2** (sichtbarer Mehrwert, Grundlage)
2. **VERIF-3 + VERIF-4** (erste Veracity-Badges im UI)
3. **VERIF-5 + VERIF-6** (Zeit/Geo & Medien → Präzision rauf)
```

_Auszug B:_
```
## 🚀 Rollout-Plan (empfohlen)

1. **VERIF-1 + VERIF-2** (sichtbarer Mehrwert, Grundlage)
2. **VERIF-3 + VERIF-4** (erste Veracity-Badges im UI)
3. **VERIF-5 + VERIF-6** (Zeit/Geo & Medien → Präzision rauf)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/SECURITY-BLUEPRINT.md` — *🔐 InfoTerminal Security Blueprint* — Zeilen 1-7
- B: `docs_ws/docs/blueprints/SECURITY-BLUEPRINT.md` — *🔐 InfoTerminal Security Blueprint* — Zeilen 1-7

_Auszug A:_
```
# 🔐 InfoTerminal Security Blueprint

> Ziel: Robustes Security- & Incognito-Layer für Journalist:innen, Sicherheitsbehörden, Firmen und Forschung.  
> Motto: **Sicherheit, Anonymität, Nachvollziehbarkeit – je nach Modus.**

```

_Auszug B:_
```
# 🔐 InfoTerminal Security Blueprint

> Ziel: Robustes Security- & Incognito-Layer für Journalist:innen, Sicherheitsbehörden, Firmen und Forschung.  
> Motto: **Sicherheit, Anonymität, Nachvollziehbarkeit – je nach Modus.**

```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/SECURITY-BLUEPRINT.md` — *🎯 Grundsätze* — Zeilen 8-16
- B: `docs_ws/docs/blueprints/SECURITY-BLUEPRINT.md` — *🎯 Grundsätze* — Zeilen 8-16

_Auszug A:_
```
## 🎯 Grundsätze

- **Defense in Depth**: Sicherheit auf Netzwerk-, Speicher-, Auth-, Plugin- und Logging-Ebene.
- **Modus-Schalter**: Nutzer:innen wählen zwischen **Standard**, **Incognito** und **Forensics**.
- **Legal by Design**: robots.txt/ToS respektieren, PII-Redaktion optional.
```

_Auszug B:_
```
## 🎯 Grundsätze

- **Defense in Depth**: Sicherheit auf Netzwerk-, Speicher-, Auth-, Plugin- und Logging-Ebene.  
- **Modus-Schalter**: Nutzer:innen wählen zwischen **Standard**, **Incognito** und **Forensics**.  
- **Legal by Design**: robots.txt/ToS respektieren, PII-Redaktion optional.  
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/SECURITY-BLUEPRINT.md` — *⚙️ Betriebsmodi* — Zeilen 17-39
- B: `docs_ws/docs/blueprints/SECURITY-BLUEPRINT.md` — *⚙️ Betriebsmodi* — Zeilen 17-39

_Auszug A:_
```
## ⚙️ Betriebsmodi

| Modus         | Beschreibung                                   | Logging                       | Netzwerk                     | Speicher        | Zielgruppe          |
| ------------- | ---------------------------------------------- | ----------------------------- | ---------------------------- | --------------- | ------------------- |
| **Standard**  | Normalbetrieb, volle Funktionalität            | Persistent (Loki/Tempo)       | Direkt oder Proxy            | Normal FS       | Forschung           |
```

_Auszug B:_
```
## ⚙️ Betriebsmodi

| Modus      | Beschreibung | Logging | Netzwerk | Speicher | Zielgruppe |
|------------|--------------|---------|----------|----------|------------|
| **Standard** | Normalbetrieb, volle Funktionalität | Persistent (Loki/Tempo) | Direkt oder Proxy | Normal FS | Forschung |
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/SECURITY-BLUEPRINT.md` — *Egress-Gateway* — Zeilen 42-49
- B: `docs_ws/docs/blueprints/SECURITY-BLUEPRINT.md` — *Egress-Gateway* — Zeilen 42-49

_Auszug A:_
```
### Egress-Gateway

- **Tor** (SOCKS5) mit obfs4-Bridges.
- **VPN** (WireGuard/OpenVPN) mit Kill-Switch (iptables/nftables).
- **Proxy-Chains** (Privoxy/Dante).
```

_Auszug B:_
```
### Egress-Gateway

* **Tor** (SOCKS5) mit obfs4-Bridges.
* **VPN** (WireGuard/OpenVPN) mit Kill-Switch (iptables/nftables).
* **Proxy-Chains** (Privoxy/Dante).
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/SECURITY-BLUEPRINT.md` — *Umsetzung* — Zeilen 50-56
- B: `docs_ws/docs/blueprints/SECURITY-BLUEPRINT.md` — *Umsetzung* — Zeilen 50-56

_Auszug A:_
```
### Umsetzung

- Alle Services (NiFi, n8n, Frontend, Plugins) nutzen zentrale Proxy-Umgebungsvariablen.
- NetworkPolicies: kein Direkt-Internet, nur über Egress-Gateway.

```

_Auszug B:_
```
### Umsetzung

* Alle Services (NiFi, n8n, Frontend, Plugins) nutzen zentrale Proxy-Umgebungsvariablen.
* NetworkPolicies: kein Direkt-Internet, nur über Egress-Gateway.

```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/SECURITY-BLUEPRINT.md` — *🕵️ Headless-Browser & Scraping* — Zeilen 57-66
- B: `docs_ws/docs/blueprints/SECURITY-BLUEPRINT.md` — *🕵️ Headless-Browser & Scraping* — Zeilen 57-66

_Auszug A:_
```
## 🕵️ Headless-Browser & Scraping

- **Remote Browser Pool** (Playwright/Chromium) in isolierten Containern.
- **Fingerprint-Minimierung**: WebRTC off, Canvas-Leak blocken, konsistente Profile.
- **Cookie-Jars pro Case**.
```

_Auszug B:_
```
## 🕵️ Headless-Browser & Scraping

* **Remote Browser Pool** (Playwright/Chromium) in isolierten Containern.
* **Fingerprint-Minimierung**: WebRTC off, Canvas-Leak blocken, konsistente Profile.
* **Cookie-Jars pro Case**.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/SECURITY-BLUEPRINT.md` — *🔒 Speicher & Kryptografie* — Zeilen 67-76
- B: `docs_ws/docs/blueprints/SECURITY-BLUEPRINT.md` — *🔒 Speicher & Kryptografie* — Zeilen 67-76

_Auszug A:_
```
## 🔒 Speicher & Kryptografie

- **Incognito-Speicher**: tmpfs/overlayfs, Auto-Wipe nach Session.
- **At-rest Encryption**: Vault/KMS, AES-256 + Envelope.
- **In-transit**: TLS 1.3, mTLS für interne Services.
```

_Auszug B:_
```
## 🔒 Speicher & Kryptografie

* **Incognito-Speicher**: tmpfs/overlayfs, Auto-Wipe nach Session.
* **At-rest Encryption**: Vault/KMS, AES-256 + Envelope.
* **In-transit**: TLS 1.3, mTLS für interne Services.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/SECURITY-BLUEPRINT.md` — *📑 Logging & Audit* — Zeilen 77-85
- B: `docs_ws/docs/blueprints/SECURITY-BLUEPRINT.md` — *📑 Logging & Audit* — Zeilen 77-85

_Auszug A:_
```
## 📑 Logging & Audit

- **Standard**: Structured JSON-Logs (Loki), Traces (Tempo).
- **Incognito**: Nur in-memory Ring-Buffer, keine Persistenz.
- **Forensics**: Immutable Audit (WORM Buckets, unveränderbar).
```

_Auszug B:_
```
## 📑 Logging & Audit

* **Standard**: Structured JSON-Logs (Loki), Traces (Tempo).
* **Incognito**: Nur in-memory Ring-Buffer, keine Persistenz.
* **Forensics**: Immutable Audit (WORM Buckets, unveränderbar).
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/SECURITY-BLUEPRINT.md` — *🧩 Plugins & Tools (Kali, Scraper, Analyzer)* — Zeilen 86-94
- B: `docs_ws/docs/blueprints/SECURITY-BLUEPRINT.md` — *🧩 Plugins & Tools (Kali, Scraper, Analyzer)* — Zeilen 86-94

_Auszug A:_
```
## 🧩 Plugins & Tools (Kali, Scraper, Analyzer)

- **Isolations-Stack**: Rootless OCI, seccomp, AppArmor, readonly FS, default **no-net**.
- **Resource Guards**: CPU/Mem Limits, Timeout/Kill, Quotas.
- **Manifest-Policy**: `plugin.yaml` deklariert benötigte CAPs/Netz/Secrets → OPA validiert.
```

_Auszug B:_
```
## 🧩 Plugins & Tools (Kali, Scraper, Analyzer)

* **Isolations-Stack**: Rootless OCI, seccomp, AppArmor, readonly FS, default **no-net**.
* **Resource Guards**: CPU/Mem Limits, Timeout/Kill, Quotas.
* **Manifest-Policy**: `plugin.yaml` deklariert benötigte CAPs/Netz/Secrets → OPA validiert.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/SECURITY-BLUEPRINT.md` — *👤 Identitäten & Secrets* — Zeilen 95-102
- B: `docs_ws/docs/blueprints/SECURITY-BLUEPRINT.md` — *👤 Identitäten & Secrets* — Zeilen 95-102

_Auszug A:_
```
## 👤 Identitäten & Secrets

- **OIDC** mit pseudonymen Rollen (Research-Personas).
- **Secrets** über Vault/Param-Store, nie in Logs.
- **Admin-Härtung**: FIDO2/WebAuthn Hardware-Keys.
```

_Auszug B:_
```
## 👤 Identitäten & Secrets

* **OIDC** mit pseudonymen Rollen (Research-Personas).
* **Secrets** über Vault/Param-Store, nie in Logs.
* **Admin-Härtung**: FIDO2/WebAuthn Hardware-Keys.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/SECURITY-BLUEPRINT.md` — *🧭 Rollen-Presets* — Zeilen 103-110
- B: `docs_ws/docs/blueprints/SECURITY-BLUEPRINT.md` — *🧭 Rollen-Presets* — Zeilen 103-110

_Auszug A:_
```
## 🧭 Rollen-Presets

- **Journalismus**: Incognito Default, Save-Nothing, Tor→VPN, PII-Redaktion.
- **Behörden/Firmen**: Forensics Default, Chain-of-Custody, Immutable Logs.
- **Forschung**: Standard Default, schnelle Umschaltung möglich.
```

_Auszug B:_
```
## 🧭 Rollen-Presets

* **Journalismus**: Incognito Default, Save-Nothing, Tor→VPN, PII-Redaktion.
* **Behörden/Firmen**: Forensics Default, Chain-of-Custody, Immutable Logs.
* **Forschung**: Standard Default, schnelle Umschaltung möglich.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/SECURITY-BLUEPRINT.md` — *🚨 Limitierungen* — Zeilen 111-119
- B: `docs_ws/docs/blueprints/SECURITY-BLUEPRINT.md` — *🚨 Limitierungen* — Zeilen 111-119

_Auszug A:_
```
## 🚨 Limitierungen

- Website-Fingerprinting/Timing-Korrelation schwer vollständig zu eliminieren.
- Dritte (CDNs/Analytics) können Muster erkennen.
- OPSEC-Fehler der Nutzer\:innen kompromittieren Anonymität.
```

_Auszug B:_
```
## 🚨 Limitierungen

* Website-Fingerprinting/Timing-Korrelation schwer vollständig zu eliminieren.
* Dritte (CDNs/Analytics) können Muster erkennen.
* OPSEC-Fehler der Nutzer\:innen kompromittieren Anonymität.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/SECURITY-BLUEPRINT.md` — *✅ Tickets (Erweiterung zum TODO-Index)* — Zeilen 120-137
- B: `docs_ws/docs/blueprints/SECURITY-BLUEPRINT.md` — *✅ Tickets (Erweiterung zum TODO-Index)* — Zeilen 120-137

_Auszug A:_
```
## ✅ Tickets (Erweiterung zum TODO-Index)

- **\[SEC-EGRESS-1]** Egress-Gateway Container (Tor+VPN+Proxy), Kill-Switch, DNS-Sinkhole
- **\[SEC-EGRESS-2]** NetworkPolicy: alle Services nur via Egress-Gateway
- **\[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion
```

_Auszug B:_
```
## ✅ Tickets (Erweiterung zum TODO-Index)

* **\[SEC-EGRESS-1]** Egress-Gateway Container (Tor+VPN+Proxy), Kill-Switch, DNS-Sinkhole
* **\[SEC-EGRESS-2]** NetworkPolicy: alle Services nur via Egress-Gateway
* **\[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Release-Planv0.2-v1.0.md` — *🎯 Ziel* — Zeilen 3-8
- B: `docs_ws/docs/dev/v0.2/v0.3+/Release-Plan.md` — *🎯 Ziel* — Zeilen 3-8

_Auszug A:_
```
## 🎯 Ziel

Von „**Gotham-Level**“ (v0.2) → „**Beyond Gotham**“ (v1.0) mit Agenten, Plugins, Live-Datenquellen, Cyber-Integration und Ethical/Decentralized Features.

---
```

_Auszug B:_
```
## 🎯 Ziel

Von „**Gotham-Level**“ (v0.2) → „**Beyond Gotham**“ (v1.0) mit Agenten, Plugins, Live-Datenquellen, Cyber-Integration und Ethical/Decentralized Features.

---
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Release-Planv0.2-v1.0.md` — *📦 v0.2 (Release Candidate – Gotham-Gap Closed)* — Zeilen 9-28
- B: `docs_ws/docs/dev/v0.2/v0.3+/Release-Plan.md` — *📦 v0.2 (Release Candidate – Gotham-Gap Closed)* — Zeilen 9-28

_Auszug A:_
```
## 📦 v0.2 (Release Candidate – Gotham-Gap Closed)

**Fokus:** Parität mit Palantir Gotham Basis-Features

- Ontologie-Layer (Entities/Events/Relations)
```

_Auszug B:_
```
## 📦 v0.2 (Release Candidate – Gotham-Gap Closed)

**Fokus:** Parität mit Palantir Gotham Basis-Features

* Ontologie-Layer (Entities/Events/Relations)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Release-Planv0.2-v1.0.md` — *📦 v0.3 (Agents & Live Data)* — Zeilen 29-44
- B: `docs_ws/docs/dev/v0.2/v0.3+/Release-Plan.md` — *📦 v0.3 (Agents & Live Data)* — Zeilen 29-44

_Auszug A:_
```
## 📦 v0.3 (Agents & Live Data)

**Fokus:** Automatisierung, externe Datenquellen, erste Plugins

- External Live Data Sources (News, Social, Web, Feeds)
```

_Auszug B:_
```
## 📦 v0.3 (Agents & Live Data)

**Fokus:** Automatisierung, externe Datenquellen, erste Plugins

* External Live Data Sources (News, Social, Web, Feeds)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Release-Planv0.2-v1.0.md` — *📦 v0.5 (Beyond Gotham – Advanced Intelligence)* — Zeilen 45-60
- B: `docs_ws/docs/dev/v0.2/v0.3+/Release-Plan.md` — *📦 v0.5 (Beyond Gotham – Advanced Intelligence)* — Zeilen 45-60

_Auszug A:_
```
## 📦 v0.5 (Beyond Gotham – Advanced Intelligence)

**Fokus:** AI/ML Vertiefung, Darknet/OSINT, Forensics

- Graph ML (Link Prediction, GNNs, Embeddings)
```

_Auszug B:_
```
## 📦 v0.5 (Beyond Gotham – Advanced Intelligence)

**Fokus:** AI/ML Vertiefung, Darknet/OSINT, Forensics

* Graph ML (Link Prediction, GNNs, Embeddings)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Release-Planv0.2-v1.0.md` — *📦 v1.0 (Production-Ready & Differenzierung)* — Zeilen 61-76
- B: `docs_ws/docs/dev/v0.2/v0.3+/Release-Plan.md` — *📦 v1.0 (Production-Ready & Differenzierung)* — Zeilen 61-76

_Auszug A:_
```
## 📦 v1.0 (Production-Ready & Differenzierung)

**Fokus:** Nachhaltigkeit, Dezentralität, Ethical Edge

- Federated Learning (mehrere Organisationen, ohne Daten-Sharing)
```

_Auszug B:_
```
## 📦 v1.0 (Production-Ready & Differenzierung)

**Fokus:** Nachhaltigkeit, Dezentralität, Ethical Edge

* Federated Learning (mehrere Organisationen, ohne Daten-Sharing)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/Release-Planv0.2-v1.0.md` — *🗂 Roadmap Übersicht* — Zeilen 77-95
- B: `docs_ws/docs/dev/v0.2/v0.3+/Release-Plan.md` — *🗂 Roadmap Übersicht* — Zeilen 77-95

_Auszug A:_
```
## 🗂 Roadmap Übersicht

| Version  | Hauptthemen                                                                                           | Ziel                              |
| -------- | ----------------------------------------------------------------------------------------------------- | --------------------------------- |
| **v0.2** | Gotham-Gap schließen (Ontologie, Graph, NLP, Auth, Observability, Dossier, Geo, Pipelines, Collab v1) | Parität zu Gotham                 |
```

_Auszug B:_
```
## 🗂 Roadmap Übersicht

| Version  | Hauptthemen                                                                                           | Ziel                              |
| -------- | ----------------------------------------------------------------------------------------------------- | --------------------------------- |
| **v0.2** | Gotham-Gap schließen (Ontologie, Graph, NLP, Auth, Observability, Dossier, Geo, Pipelines, Collab v1) | Parität zu Gotham                 |
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *Presets (Profile) – Überblick* — Zeilen 1-8
- B: `docs_ws/docs/presets/Presets(Profile).md` — *Presets (Profile) – Überblick* — Zeilen 1-8

_Auszug A:_
```
# Presets (Profile) – Überblick

* **Journalismus (INCognito+)** → maximaler Quellenschutz, „save-nothing“, starke Verifikation & manuelle Reviews.
* **Behörden/Firmen (Forensics+)** → gerichtsfeste Nachvollziehbarkeit, Chain-of-Custody, vollständiges Auditing.
* **Forschung (Balanced)** → produktives Arbeiten, moderate OPSEC, gute Reproduzierbarkeit.
```

_Auszug B:_
```
# Presets (Profile) – Überblick

- **Journalismus (INCognito+)** → maximaler Quellenschutz, „save-nothing“, starke Verifikation & manuelle Reviews.
- **Behörden/Firmen (Forensics+)** → gerichtsfeste Nachvollziehbarkeit, Chain-of-Custody, vollständiges Auditing.
- **Forschung (Balanced)** → produktives Arbeiten, moderate OPSEC, gute Reproduzierbarkeit.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *Ziele* — Zeilen 11-14
- B: `docs_ws/docs/presets/Presets(Profile).md` — *Ziele* — Zeilen 11-14

_Auszug A:_
```
## Ziele

Quellenschutz, minimaler Footprint, kontrolliertes Scraping, starke Verifikation, schnelle Dossiers.
```

_Auszug B:_
```
## Ziele

Quellenschutz, minimaler Footprint, kontrolliertes Scraping, starke Verifikation, schnelle Dossiers.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *Betriebsmodus* — Zeilen 18-27
- B: `docs_ws/docs/presets/Presets(Profile).md` — *Betriebsmodus* — Zeilen 18-27

_Auszug A:_
```
# Betriebsmodus
IT_MODE=incognito
IT_EGRESS=tor+vpn
IT_HTTP_PROXY=http://proxy:8118
IT_SOCKS5_PROXY=socks5://tor:9050
```

_Auszug B:_
```
# Betriebsmodus
IT_MODE=incognito
IT_EGRESS=tor+vpn
IT_HTTP_PROXY=http://proxy:8118
IT_SOCKS5_PROXY=socks5://tor:9050
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *Scraper/Browser* — Zeilen 28-35
- B: `docs_ws/docs/presets/Presets(Profile).md` — *Scraper/Browser* — Zeilen 28-35

_Auszug A:_
```
# Scraper/Browser
IT_BROWSER_WEBRTC_OFF=1
IT_BROWSER_PROFILE=strict
IT_SCRAPER_RESPECT_ROBOTS=1
IT_SCRAPER_DOMAIN_WHITELIST=media.gov,deutsche_presse*.tld,behörden*.de,ngo*.org
```

_Auszug B:_
```
# Scraper/Browser
IT_BROWSER_WEBRTC_OFF=1
IT_BROWSER_PROFILE=strict
IT_SCRAPER_RESPECT_ROBOTS=1
IT_SCRAPER_DOMAIN_WHITELIST=media.gov,deutsche_presse*.tld,behörden*.de,ngo*.org
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *NiFi Pipelines (aktiviert)* — Zeilen 36-42
- B: `docs_ws/docs/presets/Presets(Profile).md` — *NiFi Pipelines (aktiviert)* — Zeilen 36-42

_Auszug A:_
```
## NiFi Pipelines (aktiviert)

* `ingest_rss_journalism` (RSS/Atom-Whitelist, sanfte Backoffs)
* `ingest_web_readability_incognito` (Readability/trafilatura, Playwright nur für Whitelist)
* `nlp_claims` → `evidence_retrieval` → `rte_scoring` → `geo_time_media` → `aggregate_upsert` (voller Verifikationspfad)
```

_Auszug B:_
```
## NiFi Pipelines (aktiviert)

- `ingest_rss_journalism` (RSS/Atom-Whitelist, sanfte Backoffs)
- `ingest_web_readability_incognito` (Readability/trafilatura, Playwright nur für Whitelist)
- `nlp_claims` → `evidence_retrieval` → `rte_scoring` → `geo_time_media` → `aggregate_upsert` (voller Verifikationspfad)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *n8n Playbooks* — Zeilen 55-60
- B: `docs_ws/docs/presets/Presets(Profile).md` — *n8n Playbooks* — Zeilen 55-60

_Auszug A:_
```
## n8n Playbooks

* **Breaking-News Watchlist**: Keywords/Entities → Alert in sicheren Kanal (z.B. Matrix/Signal via Relay)
* **Controversy Escalation**: `veracity in {likely_false,false,manipulative}` → Senior-Review
* **Auto-Dossier Lite**: Verified/Likely True → kurzes PDF mit Evidenzliste
```

_Auszug B:_
```
## n8n Playbooks

- **Breaking-News Watchlist**: Keywords/Entities → Alert in sicheren Kanal (z.B. Matrix/Signal via Relay)
- **Controversy Escalation**: `veracity in {likely_false,false,manipulative}` → Senior-Review
- **Auto-Dossier Lite**: Verified/Likely True → kurzes PDF mit Evidenzliste
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *Frontend Defaults* — Zeilen 75-81
- B: `docs_ws/docs/presets/Presets(Profile).md` — *Frontend Defaults* — Zeilen 84-90

_Auszug A:_
```
## Frontend Defaults

* **/search**: Quelle=„trusted press“, Zeitraum=letzte 24–72h, Badge-Filter `veracity≥likely_true`
* **/graphx**: Entity-Fokus (People/Orgs), Geo-Heatmap aus
* **Dossier**: Kurzvorlage (Claim + 2–3 Pro/Contra Quellen, Hash/Zeitstempel)
```

_Auszug B:_
```
## Frontend Defaults

- **/search**: Quelle=„trusted press“, Zeitraum=letzte 24–72h, Badge-Filter `veracity≥likely_true`
- **/graphx**: Entity-Fokus (People/Orgs), Geo-Heatmap aus
- **Dossier**: Kurzvorlage (Claim + 2–3 Pro/Contra Quellen, Hash/Zeitstempel)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *Plugin-Whitelist (Kali/Tools)* — Zeilen 82-88
- B: `docs_ws/docs/presets/Presets(Profile).md` — *Plugin-Whitelist (Kali/Tools)* — Zeilen 91-97

_Auszug A:_
```
## Plugin-Whitelist (Kali/Tools)

* **Allowed**: `whois`, `theHarvester` (nur passive Quellen), `exiftool`, `imagehash`, `yara` (offline), `nmap -sL` (Listing only)
* **Blocked**: aktive Exploits/Intrusion-Tools

```

_Auszug B:_
```
## Plugin-Whitelist (Kali/Tools)

- **Allowed**: `whois`, `theHarvester` (nur passive Quellen), `exiftool`, `imagehash`, `yara` (offline), `nmap -sL` (Listing only)
- **Blocked**: aktive Exploits/Intrusion-Tools

```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *Ziele* — Zeilen 91-94
- B: `docs_ws/docs/presets/Presets(Profile).md` — *Ziele* — Zeilen 100-103

_Auszug A:_
```
## Ziele

Beweis­sicherheit, vollständiges Auditing, starke Governance, maximale Datenintegrität.
```

_Auszug B:_
```
## Ziele

Beweis­sicherheit, vollständiges Auditing, starke Governance, maximale Datenintegrität.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *NiFi Pipelines (aktiviert)* — Zeilen 106-113
- B: `docs_ws/docs/presets/Presets(Profile).md` — *NiFi Pipelines (aktiviert)* — Zeilen 115-122

_Auszug A:_
```
## NiFi Pipelines (aktiviert)

* `ingest_rss_enterprise` + `ingest_api_enterprise` (API Keys/SLAs)
* `ingest_file_ocr_forensics` (Tesseract + Hash/Sign)
* `video_ingest_forensics` (keyframes + hashes, chain-of-custody)
```

_Auszug B:_
```
## NiFi Pipelines (aktiviert)

- `ingest_rss_enterprise` + `ingest_api_enterprise` (API Keys/SLAs)
- `ingest_file_ocr_forensics` (Tesseract + Hash/Sign)
- `video_ingest_forensics` (keyframes + hashes, chain-of-custody)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *Provenienz & Hash* — Zeilen 114-118
- B: `docs_ws/docs/presets/Presets(Profile).md` — *Provenienz & Hash* — Zeilen 123-127

_Auszug A:_
```
### Provenienz & Hash

* Jeder Flow schreibt `hash_sha256`, `signer`, `sigstore_bundle` in Metadata
* Exporte → WORM-Bucket (Retention Policy)
```

_Auszug B:_
```
### Provenienz & Hash

- Jeder Flow schreibt `hash_sha256`, `signer`, `sigstore_bundle` in Metadata
- Exporte → WORM-Bucket (Retention Policy)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *n8n Playbooks* — Zeilen 119-124
- B: `docs_ws/docs/presets/Presets(Profile).md` — *n8n Playbooks* — Zeilen 128-133

_Auszug A:_
```
## n8n Playbooks

* **Case Lifecycle**: Intake → Triage → Corroboration → Legal Review → Dossier mit Signatur
* **Sanktions-/Threat-Checks**: MISP/OTX/OFAC/BAFA → Graph-Verknüpfung → Alert
* **Chain-of-Custody Report**: automatisch generieren & signieren
```

_Auszug B:_
```
## n8n Playbooks

- **Case Lifecycle**: Intake → Triage → Corroboration → Legal Review → Dossier mit Signatur
- **Sanktions-/Threat-Checks**: MISP/OTX/OFAC/BAFA → Graph-Verknüpfung → Alert
- **Chain-of-Custody Report**: automatisch generieren & signieren
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *Frontend Defaults* — Zeilen 139-145
- B: `docs_ws/docs/presets/Presets(Profile).md` — *Frontend Defaults* — Zeilen 157-163

_Auszug A:_
```
## Frontend Defaults

* **/search**: Badge-Filter `verified` only, Audit-Overlay **an**
* **/graphx**: Timeline + Geo standardmäßig an, „Evidence per edge“ sichtbar
* **Dossier**: Langform (Kette, Hashes, Signaturen, Anhang), QR-Checksum
```

_Auszug B:_
```
## Frontend Defaults

- **/search**: Badge-Filter `verified` only, Audit-Overlay **an**
- **/graphx**: Timeline + Geo standardmäßig an, „Evidence per edge“ sichtbar
- **Dossier**: Langform (Kette, Hashes, Signaturen, Anhang), QR-Checksum
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *Plugin-Whitelist (Kali/Tools)* — Zeilen 146-152
- B: `docs_ws/docs/presets/Presets(Profile).md` — *Plugin-Whitelist (Kali/Tools)* — Zeilen 164-170

_Auszug A:_
```
## Plugin-Whitelist (Kali/Tools)

* **Allowed** (mit Sandbox & Genehmigung): `nmap` (nur passiv/Version-Scan im eigenen Netz), `tshark/wireshark` (PCAP-Import), `yara`, `exiftool`, `pdfid`, `pefile`
* **Blocked**: Exploits ohne Mandat; Standard „default no-net“ Sandbox

```

_Auszug B:_
```
## Plugin-Whitelist (Kali/Tools)

- **Allowed** (mit Sandbox & Genehmigung): `nmap` (nur passiv/Version-Scan im eigenen Netz), `tshark/wireshark` (PCAP-Import), `yara`, `exiftool`, `pdfid`, `pefile`
- **Blocked**: Exploits ohne Mandat; Standard „default no-net“ Sandbox

```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *Ziele* — Zeilen 155-158
- B: `docs_ws/docs/presets/Presets(Profile).md` — *Ziele* — Zeilen 173-176

_Auszug A:_
```
## Ziele

Schnelle Exploration, gute Reproduzierbarkeit, moderate OPSEC, nachvollziehbare Ergebnisse.
```

_Auszug B:_
```
## Ziele

Schnelle Exploration, gute Reproduzierbarkeit, moderate OPSEC, nachvollziehbare Ergebnisse.
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *NiFi Pipelines (aktiviert)* — Zeilen 170-176
- B: `docs_ws/docs/presets/Presets(Profile).md` — *NiFi Pipelines (aktiviert)* — Zeilen 188-194

_Auszug A:_
```
## NiFi Pipelines (aktiviert)

* `ingest_rss_social_web_balanced`
* `ingest_api_generic` (öffentliche APIs + Key-Scoped)
* Verifikation komplett, aber **schneller eingestellt** (weniger tiefe Evidenzsuche)
```

_Auszug B:_
```
## NiFi Pipelines (aktiviert)

- `ingest_rss_social_web_balanced`
- `ingest_api_generic` (öffentliche APIs + Key-Scoped)
- Verifikation komplett, aber **schneller eingestellt** (weniger tiefe Evidenzsuche)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *n8n Playbooks* — Zeilen 186-191
- B: `docs_ws/docs/presets/Presets(Profile).md` — *n8n Playbooks* — Zeilen 204-209

_Auszug A:_
```
## n8n Playbooks

* **Trendreport**: Entitäten + Topics pro Woche → Dossier
* **Anomalie-Erkennung**: plötzlicher Anstieg für Watchlist-Entity → Alert
* **Auto-Cluster**: Claim-Cluster → Graph-Communities → PDF
```

_Auszug B:_
```
## n8n Playbooks

- **Trendreport**: Entitäten + Topics pro Woche → Dossier
- **Anomalie-Erkennung**: plötzlicher Anstieg für Watchlist-Entity → Alert
- **Auto-Cluster**: Claim-Cluster → Graph-Communities → PDF
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *Frontend Defaults* — Zeilen 204-210
- B: `docs_ws/docs/presets/Presets(Profile).md` — *Frontend Defaults* — Zeilen 231-237

_Auszug A:_
```
## Frontend Defaults

* **/search**: Badge-Filter `≥uncertain` (alles sichtbar), Sortierung „Neuheit + Score“
* **/graphx**: Communities + Embeddings-Ansicht
* **Dossier**: Forschungsbericht (Methoden, Parameter, Repro-Hinweise)
```

_Auszug B:_
```
## Frontend Defaults

- **/search**: Badge-Filter `≥uncertain` (alles sichtbar), Sortierung „Neuheit + Score“
- **/graphx**: Communities + Embeddings-Ansicht
- **Dossier**: Forschungsbericht (Methoden, Parameter, Repro-Hinweise)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *Plugin-Whitelist (Kali/Tools)* — Zeilen 211-216
- B: `docs_ws/docs/presets/Presets(Profile).md` — *Plugin-Whitelist (Kali/Tools)* — Zeilen 238-243

_Auszug A:_
```
## Plugin-Whitelist (Kali/Tools)

* **Allowed**: alle **passiven/forensischen** Tools; aktive nur im Lab/Isolated-Netz (Preset prüft Sandbox `no-net`)

---
```

_Auszug B:_
```
## Plugin-Whitelist (Kali/Tools)

- **Allowed**: alle **passiven/forensischen** Tools; aktive nur im Lab/Isolated-Netz (Preset prüft Sandbox `no-net`)

---
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *Preset-Auswahl (Switching)* — Zeilen 217-222
- B: `docs_ws/docs/presets/Presets(Profile).md` — *Preset-Auswahl (Switching)* — Zeilen 244-249

_Auszug A:_
```
# Preset-Auswahl (Switching)

Du kannst Presets als **Config-Pakete** ablegen und per ENV aktivieren:

```bash
```

_Auszug B:_
```
# Preset-Auswahl (Switching)

Du kannst Presets als **Config-Pakete** ablegen und per ENV aktivieren:

```bash
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *- Security env & proxy wiring* — Zeilen 228-253
- B: `docs_ws/docs/presets/Presets(Profile).md` — *- Security env & proxy wiring* — Zeilen 255-280

_Auszug A:_
```
# - Security env & proxy wiring
```

Beispiel: `config/presets/journalism.yaml`

```

_Auszug B:_
```
# - Security env & proxy wiring
```

Beispiel: `config/presets/journalism.yaml`

```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Preset-Profile.md` — *Preset-Workflows (End-to-End Skizze)* — Zeilen 254-275
- B: `docs_ws/docs/presets/Presets(Profile).md` — *Preset-Workflows (End-to-End Skizze)* — Zeilen 281-302

_Auszug A:_
```
# Preset-Workflows (End-to-End Skizze)

**Journalismus:**

1. RSS/Web → NiFi normalize → Verifikation (voll) → OpenSearch/Neo4j
```

_Auszug B:_
```
# Preset-Workflows (End-to-End Skizze)

**Journalismus:**

1. RSS/Web → NiFi normalize → Verifikation (voll) → OpenSearch/Neo4j
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Ticket-Checkliste.md` — *1. Core APIs (FastAPI Services)* — Zeilen 8-14
- B: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *1. Core APIs (FastAPI Services)* — Zeilen 8-14

_Auszug A:_
```
## 1. Core APIs (FastAPI Services)
- [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints
- [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail)
- [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services
- [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration
```

_Auszug B:_
```
## 1. Core APIs (FastAPI Services)
- [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints
- [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail)
- [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services
- [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Ticket-Checkliste.md` — *1. Core APIs (FastAPI Services)* — Zeilen 8-14
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *1. Core APIs (FastAPI Services)* — Zeilen 8-14

_Auszug A:_
```
## 1. Core APIs (FastAPI Services)
- [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints
- [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail)
- [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services
- [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration
```

_Auszug B:_
```
## 1. Core APIs (FastAPI Services)
- [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints
- [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail)
- [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services
- [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *1. Core APIs (FastAPI Services)* — Zeilen 8-14
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *1. Core APIs (FastAPI Services)* — Zeilen 8-14

_Auszug A:_
```
## 1. Core APIs (FastAPI Services)
- [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints
- [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail)
- [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services
- [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration
```

_Auszug B:_
```
## 1. Core APIs (FastAPI Services)
- [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints
- [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail)
- [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services
- [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Ticket-Checkliste.md` — *2. Graph-API (Neo4j)* — Zeilen 15-21
- B: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *2. Graph-API (Neo4j)* — Zeilen 15-21

_Auszug A:_
```
## 2. Graph-API (Neo4j)
- [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties)
- [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra)
- [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff)
- [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON)
```

_Auszug B:_
```
## 2. Graph-API (Neo4j)
- [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties)
- [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra)
- [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff)
- [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Ticket-Checkliste.md` — *2. Graph-API (Neo4j)* — Zeilen 15-21
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *2. Graph-API (Neo4j)* — Zeilen 15-21

_Auszug A:_
```
## 2. Graph-API (Neo4j)
- [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties)
- [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra)
- [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff)
- [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON)
```

_Auszug B:_
```
## 2. Graph-API (Neo4j)
- [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties)
- [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra)
- [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff)
- [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *2. Graph-API (Neo4j)* — Zeilen 15-21
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *2. Graph-API (Neo4j)* — Zeilen 15-21

_Auszug A:_
```
## 2. Graph-API (Neo4j)
- [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties)
- [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra)
- [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff)
- [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON)
```

_Auszug B:_
```
## 2. Graph-API (Neo4j)
- [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties)
- [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra)
- [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff)
- [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Ticket-Checkliste.md` — *3. Search-API (OpenSearch)* — Zeilen 22-28
- B: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *3. Search-API (OpenSearch)* — Zeilen 22-28

_Auszug A:_
```
## 3. Search-API (OpenSearch)
- [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization)
- [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert)
- [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“
- [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index
```

_Auszug B:_
```
## 3. Search-API (OpenSearch)
- [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization)
- [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert)
- [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“
- [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Ticket-Checkliste.md` — *3. Search-API (OpenSearch)* — Zeilen 22-28
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *3. Search-API (OpenSearch)* — Zeilen 22-28

_Auszug A:_
```
## 3. Search-API (OpenSearch)
- [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization)
- [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert)
- [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“
- [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index
```

_Auszug B:_
```
## 3. Search-API (OpenSearch)
- [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization)
- [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert)
- [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“
- [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *3. Search-API (OpenSearch)* — Zeilen 22-28
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *3. Search-API (OpenSearch)* — Zeilen 22-28

_Auszug A:_
```
## 3. Search-API (OpenSearch)
- [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization)
- [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert)
- [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“
- [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index
```

_Auszug B:_
```
## 3. Search-API (OpenSearch)
- [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization)
- [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert)
- [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“
- [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Ticket-Checkliste.md` — *4. Graph-Views (Postgres)* — Zeilen 29-34
- B: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *4. Graph-Views (Postgres)* — Zeilen 29-34

_Auszug A:_
```
## 4. Graph-Views (Postgres)
- [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency)
- [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres)
- [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views)
- [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors)
```

_Auszug B:_
```
## 4. Graph-Views (Postgres)
- [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency)
- [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres)
- [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views)
- [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Ticket-Checkliste.md` — *4. Graph-Views (Postgres)* — Zeilen 29-34
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *4. Graph-Views (Postgres)* — Zeilen 29-34

_Auszug A:_
```
## 4. Graph-Views (Postgres)
- [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency)
- [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres)
- [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views)
- [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors)
```

_Auszug B:_
```
## 4. Graph-Views (Postgres)
- [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency)
- [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres)
- [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views)
- [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *4. Graph-Views (Postgres)* — Zeilen 29-34
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *4. Graph-Views (Postgres)* — Zeilen 29-34

_Auszug A:_
```
## 4. Graph-Views (Postgres)
- [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency)
- [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres)
- [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views)
- [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors)
```

_Auszug B:_
```
## 4. Graph-Views (Postgres)
- [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency)
- [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres)
- [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views)
- [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Ticket-Checkliste.md` — *6. Gateway & OPA* — Zeilen 45-50
- B: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *6. Gateway & OPA* — Zeilen 47-52

_Auszug A:_
```
## 6. Gateway & OPA
- [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation)
- [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern
- [ ] **[GATE-3]** Attribute-Level Security vorbereiten
- [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten
```

_Auszug B:_
```
## 6. Gateway & OPA
- [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation)
- [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern
- [ ] **[GATE-3]** Attribute-Level Security vorbereiten
- [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Ticket-Checkliste.md` — *6. Gateway & OPA* — Zeilen 45-50
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *6. Gateway & OPA* — Zeilen 47-52

_Auszug A:_
```
## 6. Gateway & OPA
- [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation)
- [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern
- [ ] **[GATE-3]** Attribute-Level Security vorbereiten
- [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten
```

_Auszug B:_
```
## 6. Gateway & OPA
- [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation)
- [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern
- [ ] **[GATE-3]** Attribute-Level Security vorbereiten
- [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *6. Gateway & OPA* — Zeilen 47-52
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *6. Gateway & OPA* — Zeilen 47-52

_Auszug A:_
```
## 6. Gateway & OPA
- [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation)
- [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern
- [ ] **[GATE-3]** Attribute-Level Security vorbereiten
- [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten
```

_Auszug B:_
```
## 6. Gateway & OPA
- [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation)
- [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern
- [ ] **[GATE-3]** Attribute-Level Security vorbereiten
- [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Ticket-Checkliste.md` — *9. CLI (infoterminal-cli)* — Zeilen 66-72
- B: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *9. CLI (infoterminal-cli)* — Zeilen 71-77

_Auszug A:_
```
## 9. CLI (infoterminal-cli)
- [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs)
- [ ] **[CLI-2]** Export Command (`it export [graph|search|dossier]`)
- [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`)
- [ ] **[CLI-4]** Auth Command (`it login --oidc`)
```

_Auszug B:_
```
## 9. CLI (infoterminal-cli)
- [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs)
- [ ] **[CLI-2]** Export Command (`it export [graph|search|dossier]`)
- [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`)
- [ ] **[CLI-4]** Auth Command (`it login --oidc`)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Ticket-Checkliste.md` — *9. CLI (infoterminal-cli)* — Zeilen 66-72
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *9. CLI (infoterminal-cli)* — Zeilen 71-77

_Auszug A:_
```
## 9. CLI (infoterminal-cli)
- [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs)
- [ ] **[CLI-2]** Export Command (`it export [graph|search|dossier]`)
- [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`)
- [ ] **[CLI-4]** Auth Command (`it login --oidc`)
```

_Auszug B:_
```
## 9. CLI (infoterminal-cli)
- [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs)
- [ ] **[CLI-2]** Export Command (`it export [graph|search|dossier]`)
- [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`)
- [ ] **[CLI-4]** Auth Command (`it login --oidc`)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *9. CLI (infoterminal-cli)* — Zeilen 71-77
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *9. CLI (infoterminal-cli)* — Zeilen 71-77

_Auszug A:_
```
## 9. CLI (infoterminal-cli)
- [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs)
- [ ] **[CLI-2]** Export Command (`it export [graph|search|dossier]`)
- [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`)
- [ ] **[CLI-4]** Auth Command (`it login --oidc`)
```

_Auszug B:_
```
## 9. CLI (infoterminal-cli)
- [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs)
- [ ] **[CLI-2]** Export Command (`it export [graph|search|dossier]`)
- [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`)
- [ ] **[CLI-4]** Auth Command (`it login --oidc`)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Ticket-Checkliste.md` — *10. Infra & Observability* — Zeilen 73-81
- B: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *10. Infra & Observability* — Zeilen 78-86

_Auszug A:_
```
## 10. Infra & Observability
- [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager)
- [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID)
- [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch)
- [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren
```

_Auszug B:_
```
## 10. Infra & Observability
- [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager)
- [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID)
- [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch)
- [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/Ticket-Checkliste.md` — *10. Infra & Observability* — Zeilen 73-81
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *10. Infra & Observability* — Zeilen 78-86

_Auszug A:_
```
## 10. Infra & Observability
- [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager)
- [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID)
- [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch)
- [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren
```

_Auszug B:_
```
## 10. Infra & Observability
- [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager)
- [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID)
- [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch)
- [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *10. Infra & Observability* — Zeilen 78-86
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *10. Infra & Observability* — Zeilen 78-86

_Auszug A:_
```
## 10. Infra & Observability
- [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager)
- [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID)
- [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch)
- [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren
```

_Auszug B:_
```
## 10. Infra & Observability
- [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager)
- [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID)
- [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch)
- [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *5. Frontend (Next.js)* — Zeilen 35-46
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *5. Frontend (Next.js)* — Zeilen 35-46

_Auszug A:_
```
## 5. Frontend (Next.js)
- [ ] **[FE-1]** Einheitliches Theme (globals.css konsolidieren)
- [ ] **[FE-2]** /search: Facettenfilter + Ranking-Regler
- [ ] **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse
- [ ] **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre)
```

_Auszug B:_
```
## 5. Frontend (Next.js)
- [ ] **[FE-1]** Einheitliches Theme (globals.css konsolidieren)
- [ ] **[FE-2]** /search: Facettenfilter + Ranking-Regler
- [ ] **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse
- [ ] **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *8. n8n Playbooks* — Zeilen 62-70
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *8. n8n Playbooks* — Zeilen 62-70

_Auszug A:_
```
## 8. n8n Playbooks
- [ ] **[N8N-1]** Investigation Assistant Flow (search+graph queries)
- [ ] **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email)
- [ ] **[N8N-3]** Cross-Source Correlation (news+social+plugins)
- [ ] **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot)
```

_Auszug B:_
```
## 8. n8n Playbooks
- [ ] **[N8N-1]** Investigation Assistant Flow (search+graph queries)
- [ ] **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email)
- [ ] **[N8N-3]** Cross-Source Correlation (news+social+plugins)
- [ ] **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot)
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *11. Security-Layer* — Zeilen 87-105
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *11. Security-Layer* — Zeilen 87-103

_Auszug A:_
```
## 11. Security-Layer
- [ ] **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole)
- [ ] **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway
- [ ] **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion
- [ ] **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53
```

_Auszug B:_
```
## 11. Security-Layer
- [ ] **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole)
- [ ] **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway
- [ ] **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion
- [ ] **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53
```
---
**Ähnlichkeit:** 1.00

- A: `docs_ws/docs/dev/v0.2/TODO-Index.md` — *12. Verification-Layer* — Zeilen 106-120
- B: `docs_ws/docs/dev/v0.2/v0.3+/Master-TODO-Index.md` — *12. Verification-Layer* — Zeilen 104-118

_Auszug A:_
```
## 12. Verification-Layer
- [ ] **[VERIF-1]** Source Reputation & Bot-Likelihood Modul
- [ ] **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs
- [ ] **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense)
- [ ] **[VERIF-4]** RTE/Stance Classifier + Aggregation
```

_Auszug B:_
```
## 12. Verification-Layer
- [ ] **[VERIF-1]** Source Reputation & Bot-Likelihood Modul
- [ ] **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs
- [ ] **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense)
- [ ] **[VERIF-4]** RTE/Stance Classifier + Aggregation
```
