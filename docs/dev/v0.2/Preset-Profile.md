➡ Consolidated at: ../guides/preset-profiles.md#presets-profile-berblick
# 1) Journalismus-Preset (INCognito+)

## Ziele

Quellenschutz, minimaler Footprint, kontrolliertes Scraping, starke Verifikation, schnelle Dossiers.

➡ Consolidated at: ../guides/preset-profiles.md#security-runtime
# Betriebsmodus
IT_MODE=incognito
➡ Consolidated at: ../guides/preset-profiles.md#it-egress-tor-vpn
IT_BLOCK_DNS=1
IT_NO_LOG_PERSIST=1
IT_EPHEMERAL_FS=1

# Scraper/Browser
IT_BROWSER_WEBRTC_OFF=1
➡ Consolidated at: ../guides/preset-profiles.md#it-browser-profile-strict
* `nlp_claims` → `evidence_retrieval` → `rte_scoring` → `geo_time_media` → `aggregate_upsert` (voller Verifikationspfad)
* `geo_enrich_light` (Nominatim mit aggressivem Rate-Limit + Cache)

### NiFi Parameter Context (Ausschnitt)

```yaml
JournalismContext:
  HTTP_PROXY: "http://proxy:8118"
  SOCKS_PROXY: "socks5://tor:9050"
➡ Consolidated at: ../guides/preset-profiles.md#robots-enforce-true
* **Breaking-News Watchlist**: Keywords/Entities → Alert in sicheren Kanal (z.B. Matrix/Signal via Relay)
* **Controversy Escalation**: `veracity in {likely_false,false,manipulative}` → Senior-Review
* **Auto-Dossier Lite**: Verified/Likely True → kurzes PDF mit Evidenzliste

## Verification Defaults

```yaml
➡ Consolidated at: ../guides/preset-profiles.md#verif
    false:           {score: 0.20}
  require_human_review_for_publish: true
```

## Frontend Defaults

* **/search**: Quelle=„trusted press“, Zeitraum=letzte 24–72h, Badge-Filter `veracity≥likely_true`
* **/graphx**: Entity-Fokus (People/Orgs), Geo-Heatmap aus
* **Dossier**: Kurzvorlage (Claim + 2–3 Pro/Contra Quellen, Hash/Zeitstempel)
* **Review-UI**: „Review before share“ erzwungen

## Plugin-Whitelist (Kali/Tools)

* **Allowed**: `whois`, `theHarvester` (nur passive Quellen), `exiftool`, `imagehash`, `yara` (offline), `nmap -sL` (Listing only)
* **Blocked**: aktive Exploits/Intrusion-Tools

---

➡ Consolidated at: ../guides/preset-profiles.md#2-beh-rden-firmen-preset-forensics
## Security/Runtime

```bash
IT_MODE=forensics
IT_EGRESS=proxy   # direkt oder über geprüften Enterprise-Proxy/VPN
IT_NO_LOG_PERSIST=0
IT_EPHEMERAL_FS=0
IT_WORM_BUCKETS=1  # Write Once Read Many für Exporte/Artefakte
IT_CHAIN_OF_CUSTODY=1
```

## NiFi Pipelines (aktiviert)

* `ingest_rss_enterprise` + `ingest_api_enterprise` (API Keys/SLAs)
* `ingest_file_ocr_forensics` (Tesseract + Hash/Sign)
* `video_ingest_forensics` (keyframes + hashes, chain-of-custody)
* Voller Verifikationspfad mit **mehr Evidenz-Quellen** (Gov/NGO/Datenbanken)
* `geo_enrich_enterprise` (interner Geocoder/Cache)

➡ Consolidated at: ../guides/preset-profiles.md#provenienz-hash
* **Case Lifecycle**: Intake → Triage → Corroboration → Legal Review → Dossier mit Signatur
* **Sanktions-/Threat-Checks**: MISP/OTX/OFAC/BAFA → Graph-Verknüpfung → Alert
* **Chain-of-Custody Report**: automatisch generieren & signieren

## Verification Defaults

➡ Consolidated at: ../guides/preset-profiles.md#yaml
    min_independent_sources: 3
    must_include: ["gov","ngo","reputable_press"]
  require_human_review_for_publish: true
```

## Frontend Defaults

* **/search**: Badge-Filter `verified` only, Audit-Overlay **an**
➡ Consolidated at: ../guides/preset-profiles.md#graphx-timeline-geo-standardm-ig-an-evidence-per-edge-sichtbar
## Plugin-Whitelist (Kali/Tools)

* **Allowed** (mit Sandbox & Genehmigung): `nmap` (nur passiv/Version-Scan im eigenen Netz), `tshark/wireshark` (PCAP-Import), `yara`, `exiftool`, `pdfid`, `pefile`
* **Blocked**: Exploits ohne Mandat; Standard „default no-net“ Sandbox

---

# 3) Forschung-Preset (Balanced)

## Ziele

Schnelle Exploration, gute Reproduzierbarkeit, moderate OPSEC, nachvollziehbare Ergebnisse.

## Security/Runtime
➡ Consolidated at: ../guides/preset-profiles.md#
```

## NiFi Pipelines (aktiviert)

* `ingest_rss_social_web_balanced`
* `ingest_api_generic` (öffentliche APIs + Key-Scoped)
* Verifikation komplett, aber **schneller eingestellt** (weniger tiefe Evidenzsuche)
➡ Consolidated at: ../guides/preset-profiles.md#geo-enrich-standard-cache-aggressiver
ResearchContext:
  RATE_LIMIT_RPS: "1.0"
  EVIDENCE_TOPK: "8"
  RETRIEVAL_TIMEOUT_S: "8"
➡ Consolidated at: ../guides/preset-profiles.md#
* **Auto-Cluster**: Claim-Cluster → Graph-Communities → PDF

## Verification Defaults

```yaml
verif:
  weights: {source:0.2, content:0.1, corro:0.25, rte:0.25, temporal:0.05, geo:0.05, media:0.1}
  thresholds:
    verified:     {score: 0.80, conf: 0.70}
    likely_true:  {score: 0.65, conf: 0.55}
  active_learning: true
  sample_uncertain_for_labeling: 0.2   # 20% der unsicheren Fälle in Label-Queue
```

## Frontend Defaults

* **/search**: Badge-Filter `≥uncertain` (alles sichtbar), Sortierung „Neuheit + Score“
* **/graphx**: Communities + Embeddings-Ansicht
* **Dossier**: Forschungsbericht (Methoden, Parameter, Repro-Hinweise)
➡ Consolidated at: ../guides/preset-profiles.md#review-ui-override-erlaubt-label-store-prominent

# Preset-Auswahl (Switching)

Du kannst Presets als **Config-Pakete** ablegen und per ENV aktivieren:

```bash
➡ Consolidated at: ../guides/preset-profiles.md#it-profile-journalism-agency-research
```

Beispiel: `config/presets/journalism.yaml`

```yaml
profile: journalism
security:
  mode: incognito
➡ Consolidated at: ../guides/preset-profiles.md#egress-tor-vpn
  weights: {source:0.2, content:0.1, corro:0.3, rte:0.25, temporal:0.05, geo:0.05, media:0.05}
  thresholds: {verified:{score:0.85,conf:0.70}, likely_true:{score:0.70,conf:0.60}}
nifi_context: JournalismContext
n8n_enable: [breaking_news_watchlist, controversy_escalation, auto_dossier_lite]
frontend:
  search_defaults: {badges_min: "likely_true", time_range: "72h"}
  dossier_template: "journalism_short.md"
plugins:
  whitelist: [whois, theHarvester, exiftool, imagehash, yara]
```

---

# Preset-Workflows (End-to-End Skizze)
➡ Consolidated at: ../guides/preset-profiles.md#
**Behörden/Firmen:**

1. API/Files/Video → NiFi normalize → Hash/Sign → Verifikation (Gov/NGO+Mehrfach-Evidenz)
2. n8n Case Lifecycle → Dossier (Langform) → Signatur → WORM
3. Vollständige Logs/Traces, 4-Augen-Review, Sandbox-Härtung

**Forschung:**

1. Mixed Sources → NiFi → Verifikation (schneller) → Search/Graph
2. n8n Trendreport/Anomalien → Auto-Cluster → Forschungs-Dossier
3. Reproduzierbare Settings, Active Learning an

---

# Umsetzung: Tickets (zum Master TODO-Index ergänzen)
➡ Consolidated at: ../guides/preset-profiles.md#
* **\[PRESET-6]** Plugin-Whitelist/Policy pro Preset (OPA Validation)
* **\[PRESET-7]** Dossier-Vorlagen: `journalism_short.md`, `forensics_long.md`, `research_report.md`
* **\[PRESET-8]** Security-Checks: Fail-closed Tests je Preset (Egress, DNS, Logging)

---
TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile.
