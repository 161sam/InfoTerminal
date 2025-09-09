# 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0)

> Master-Checkliste aller Tickets / Features bis v1.0  
> Enthält Core, Gotham-Gap, Security, Verification, und alle Beyond Gotham Blueprints

---

## 1. Core APIs (FastAPI Services)
- [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints
- [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail)
- [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services
- [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration
- [ ] **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID)

## 2. Graph-API (Neo4j)
- [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties)
- [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra)
- [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff)
- [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON)
- [ ] **[GRAPH-5]** Audit: Query-Logs + Query-Metrics

## 3. Search-API (OpenSearch)
- [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization)
- [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert)
- [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“
- [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index
- [ ] **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus

## 4. Graph-Views (Postgres)
- [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency)
- [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres)
- [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views)
- [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors)

## 5. Frontend (Next.js)
- [ ] **[FE-1]** Einheitliches Theme (globals.css konsolidieren)
- [ ] **[FE-2]** /search: Facettenfilter + Ranking-Regler
- [ ] **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse
- [ ] **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre)
- [ ] **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar
- [ ] **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD)
- [ ] **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT)
- [ ] **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User)
- [ ] **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores)
- [ ] **[FE-10]** Review-UI für Claims/Evidence (Overrides, History)

## 6. Gateway & OPA
- [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation)
- [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern
- [ ] **[GATE-3]** Attribute-Level Security vorbereiten
- [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten

## 7. NiFi Pipelines
- [ ] **[NIFI-1]** RSS/Atom Ingest Flow
- [ ] **[NIFI-2]** API Ingest Flow
- [ ] **[NIFI-3]** File Watch/Upload Flow (OCR + NLP)
- [ ] **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR)
- [ ] **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference)
- [ ] **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon)
- [ ] **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation)

## 8. n8n Playbooks
- [ ] **[N8N-1]** Investigation Assistant Flow (search+graph queries)
- [ ] **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email)
- [ ] **[N8N-3]** Cross-Source Correlation (news+social+plugins)
- [ ] **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot)
- [ ] **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph)
- [ ] **[N8N-6]** Veracity Alerts (false/manipulative → escalate)
- [ ] **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review)

## 9. CLI (infoterminal-cli)
- [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs)
- [ ] **[CLI-2]** Export Command (`it export [graph|search|dossier]`)
- [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`)
- [ ] **[CLI-4]** Auth Command (`it login --oidc`)
- [ ] **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table)

## 10. Infra & Observability
- [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager)
- [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID)
- [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch)
- [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren
- [ ] **[OBS-5]** Frontend Build Konflikt (settings page) lösen

---

## 11. Security-Layer
- [ ] **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole)
- [ ] **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway
- [ ] **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion
- [ ] **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53
- [ ] **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe)
- [ ] **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys
- [ ] **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte
- [ ] **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case)
- [ ] **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone)
- [ ] **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist
- [ ] **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory)
- [ ] **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten)
- [ ] **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net)
- [ ] **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets)
- [ ] **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI

## 12. Verification-Layer
- [ ] **[VERIF-1]** Source Reputation & Bot-Likelihood Modul
- [ ] **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs
- [ ] **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense)
- [ ] **[VERIF-4]** RTE/Stance Classifier + Aggregation
- [ ] **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken)
- [ ] **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA)
- [ ] **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j)
- [ ] **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History)
- [ ] **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training)
- [ ] **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers)
- [ ] **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang)

---

## 13. Legal-Intelligence
- [ ] **[LEGAL-1]** RAG-Service für Gesetzestexte
- [ ] **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange)
- [ ] **[LEGAL-3]** NiFi ingest_laws + rag_index
- [ ] **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports
- [ ] **[LEGAL-5]** Frontend Tab „Legal/Compliance“
- [ ] **[LEGAL-6]** Dossier-Vorlage Compliance Report

## 14. Disinformation-Intelligence
- [ ] **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash)
- [ ] **[DISINFO-2]** Bot-Likelihood Modul
- [ ] **[DISINFO-3]** Temporal Pattern Detection
- [ ] **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier
- [ ] **[DISINFO-5]** Frontend Dashboard Top Narratives
- [ ] **[DISINFO-6]** Fact-Check API Integration

## 15. Supply-Chain-Intelligence
- [ ] **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions
- [ ] **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions
- [ ] **[SUPPLY-3]** Simulation Engine (Event → Impact)
- [ ] **[SUPPLY-4]** n8n Risk Alerts + Impact Reports
- [ ] **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool
- [ ] **[SUPPLY-6]** Dossier Supply Chain Risk Report

## 16. Financial-Intelligence
- [ ] **[FIN-1]** Graph-Schema Accounts/Transfers
- [ ] **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions
- [ ] **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph)
- [ ] **[FIN-4]** Anomaly Detection Module
- [ ] **[FIN-5]** n8n Red Flag Alerts + Escalations
- [ ] **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard
- [ ] **[FIN-7]** Dossier Financial Red Flags

## 17. Geopolitical-Intelligence
- [ ] **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social
- [ ] **[GEO-2]** Graph-Schema Events/Assets/Conflicts
- [ ] **[GEO-3]** Geo-Time Anomaly Detection
- [ ] **[GEO-4]** n8n Alerts + Conflict Reports
- [ ] **[GEO-5]** Frontend Map Dashboard + Timeline
- [ ] **[GEO-6]** Simulation Engine (Eskalations-Szenarien)
- [ ] **[GEO-7]** Dossier Geopolitical Report

## 18. Humanitarian-Intelligence
- [ ] **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators
- [ ] **[HUM-2]** Graph-Schema Crisis/Indicators/Regions
- [ ] **[HUM-3]** Risk Assessment Modul (ML)
- [ ] **[HUM-4]** n8n Crisis Alerts + Reports
- [ ] **[HUM-5]** Frontend Crisis Dashboard + Forecast
- [ ] **[HUM-6]** Dossier Humanitarian Crisis Report

---

## 19. Climate-Intelligence
- [ ] **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus)
- [ ] **[CLIMATE-2]** Graph-Schema ClimateIndicators
- [ ] **[CLIMATE-3]** CO₂/Emission Scoring Modul
- [ ] **[CLIMATE-4]** n8n Alerts (Emission Targets)
- [ ] **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap
- [ ] **[CLIMATE-6]** Dossier Climate Risk Report

## 20. Technology-Intelligence
- [ ] **[TECH-1]** NiFi ingest_patents + research_data
- [ ] **[TECH-2]** Graph-Schema Patents/TechTrends
- [ ] **[TECH-3]** Innovation Hotspot Detection
- [ ] **[TECH-4]** n8n Tech Trend Reports
- [ ] **[TECH-5]** Frontend Patent/Innovation Graph
- [ ] **[TECH-6]** Dossier Technology Trends

## 21. Terrorism-Intelligence
- [ ] **[TERROR-1]** Ingest Propaganda Sources (Social, Web)
- [ ] **[TERROR-2]** Graph-Schema TerrorNetworks
- [ ] **[TERROR-3]** Finance Flow Analysis
- [ ] **[TERROR-4]** n8n Alerts Suspicious Networks
- [ ] **[TERROR-5]** Frontend Terror Network Graph
- [ ] **[TERROR-6]** Dossier Terrorism Threat Report

## 22. Health-Intelligence
- [ ] **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social)
- [ ] **[HEALTH-2]** Graph-Schema HealthEvents/Regions
- [ ] **[HEALTH-3]** Epidemic Outbreak Detection
- [ ] **[HEALTH-4]** n8n Health Alerts + Reports
- [ ] **[HEALTH-5]** Frontend Health Dashboard
- [ ] **[HEALTH-6]** Dossier Health/Epidemic Report

## 23. AI-Ethics-Intelligence
- [ ] **[ETHICS-1]** Ingest Model Cards + AI Incident Data
- [ ] **[ETHICS-2]** Graph-Schema Bias/Models/Orgs
- [ ] **[ETHICS-3]** Bias Detection Modul
- [ ] **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations)
- [ ] **[ETHICS-5]** Frontend AI Ethics Dashboard
- [ ] **[ETHICS-6]** Dossier AI Ethics Report

## 24. Media-Forensics-Intelligence
- [ ] **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing)
- [ ] **[MEDIA-2]** Deepfake Detection Modul
- [ ] **[MEDIA-3]** Graph-Schema MediaAuthenticity
- [ ] **[MEDIA-4]** n8n Alerts Fake Media
- [ ] **[MEDIA-5]** Frontend Media Forensics Panel
- [ ] **[MEDIA-6]** Dossier Media Authenticity Report

## 25. Economic-Intelligence
- [ ] **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank)
- [ ] **[ECON-2]** Graph-Schema EconomicIndicators/Trades
- [ ] **[ECON-3]** Market Risk Analysis Modul
- [ ] **[ECON-4]** n8n Economic Reports
- [ ] **[ECON-5]** Frontend Economic Dashboard
- [ ] **[ECON-6]** Dossier Economic Intelligence Report

## 26. Cultural-Intelligence
- [ ] **[CULTURE-1]** Ingest Social/News/Blog Data
- [ ] **[CULTURE-2]** Graph-Schema Narratives/Discourse
- [ ] **[CULTURE-3]** Meme/Hashtag Cluster Detection
- [ ] **[CULTURE-4]** n8n Cultural Trend Reports
- [ ] **[CULTURE-5]** Frontend Cultural Trends Dashboard
- [ ] **[CULTURE-6]** Dossier Cultural Intelligence Report

---

## 📌 Priorisierung
- **Prio Muss (v0.2):** Core APIs, Ontologie, Graph-Algorithmen, NLP v1, OAuth2/OIDC, Observability, Dossier-Lite, Geospatial, NiFi, n8n, Security-Egress, Verification Basics  
- **Prio Soll (v0.3–0.5):** Legal, Disinfo, Supply, Financial, Geopolitical, Humanitarian, Collaboration v1, Video Pipeline  
- **Prio Kann (v1.0):** Climate, Tech, Terror, Health, AI-Ethics, Media Forensics, Economic, Cultural, DAO Deployments


