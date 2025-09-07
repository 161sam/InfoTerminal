# Presets (Profile) – Überblick

- **Journalismus (INCognito+)** → maximaler Quellenschutz, „save-nothing“, starke Verifikation & manuelle Reviews.
- **Behörden/Firmen (Forensics+)** → gerichtsfeste Nachvollziehbarkeit, Chain-of-Custody, vollständiges Auditing.
- **Forschung (Balanced)** → produktives Arbeiten, moderate OPSEC, gute Reproduzierbarkeit.

---

# 1) Journalismus-Preset (INCognito+)

## Ziele

Quellenschutz, minimaler Footprint, kontrolliertes Scraping, starke Verifikation, schnelle Dossiers.

## Security/Runtime

```bash
# Betriebsmodus
IT_MODE=incognito
IT_EGRESS=tor+vpn
IT_HTTP_PROXY=http://proxy:8118
IT_SOCKS5_PROXY=socks5://tor:9050
IT_DOH=1
IT_BLOCK_DNS=1
IT_NO_LOG_PERSIST=1
IT_EPHEMERAL_FS=1

# Scraper/Browser
IT_BROWSER_WEBRTC_OFF=1
IT_BROWSER_PROFILE=strict
IT_SCRAPER_RESPECT_ROBOTS=1
IT_SCRAPER_DOMAIN_WHITELIST=media.gov,deutsche_presse*.tld,behörden*.de,ngo*.org
IT_SCRAPER_RATE_LIMIT=low
```

## NiFi Pipelines (aktiviert)

- `ingest_rss_journalism` (RSS/Atom-Whitelist, sanfte Backoffs)
- `ingest_web_readability_incognito` (Readability/trafilatura, Playwright nur für Whitelist)
- `nlp_claims` → `evidence_retrieval` → `rte_scoring` → `geo_time_media` → `aggregate_upsert` (voller Verifikationspfad)
- `geo_enrich_light` (Nominatim mit aggressivem Rate-Limit + Cache)

### NiFi Parameter Context (Ausschnitt)

```yaml
JournalismContext:
  HTTP_PROXY: "http://proxy:8118"
  SOCKS_PROXY: "socks5://tor:9050"
  ROBOTS_ENFORCE: "true"
  DOMAIN_WHITELIST: "media.gov,deutsche_presse*.tld,ngo*.org"
  RATE_LIMIT_RPS: "0.3"
  GEO_CODER_CACHE_TTL: "86400"
```

## n8n Playbooks

- **Breaking-News Watchlist**: Keywords/Entities → Alert in sicheren Kanal (z.B. Matrix/Signal via Relay)
- **Controversy Escalation**: `veracity in {likely_false,false,manipulative}` → Senior-Review
- **Auto-Dossier Lite**: Verified/Likely True → kurzes PDF mit Evidenzliste

## Verification Defaults

```yaml
verif:
  weights:
    {
      source:0.2,
      content:0.1,
      corro:0.3,
      rte:0.25,
      temporal:0.05,
      geo:0.05,
      media:0.05,
    }
  thresholds:
    verified: { score: 0.85, conf: 0.70 }
    likely_true: { score: 0.70, conf: 0.60 }
    uncertain: { score: 0.50 }
    likely_false: { score: 0.35 }
    false: { score: 0.20 }
  require_human_review_for_publish: true
```

## Frontend Defaults

- **/search**: Quelle=„trusted press“, Zeitraum=letzte 24–72h, Badge-Filter `veracity≥likely_true`
- **/graphx**: Entity-Fokus (People/Orgs), Geo-Heatmap aus
- **Dossier**: Kurzvorlage (Claim + 2–3 Pro/Contra Quellen, Hash/Zeitstempel)
- **Review-UI**: „Review before share“ erzwungen

## Plugin-Whitelist (Kali/Tools)

- **Allowed**: `whois`, `theHarvester` (nur passive Quellen), `exiftool`, `imagehash`, `yara` (offline), `nmap -sL` (Listing only)
- **Blocked**: aktive Exploits/Intrusion-Tools

---

# 2) Behörden/Firmen-Preset (Forensics+)

## Ziele

Beweis­sicherheit, vollständiges Auditing, starke Governance, maximale Datenintegrität.

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

- `ingest_rss_enterprise` + `ingest_api_enterprise` (API Keys/SLAs)
- `ingest_file_ocr_forensics` (Tesseract + Hash/Sign)
- `video_ingest_forensics` (keyframes + hashes, chain-of-custody)
- Voller Verifikationspfad mit **mehr Evidenz-Quellen** (Gov/NGO/Datenbanken)
- `geo_enrich_enterprise` (interner Geocoder/Cache)

### Provenienz & Hash

- Jeder Flow schreibt `hash_sha256`, `signer`, `sigstore_bundle` in Metadata
- Exporte → WORM-Bucket (Retention Policy)

## n8n Playbooks

- **Case Lifecycle**: Intake → Triage → Corroboration → Legal Review → Dossier mit Signatur
- **Sanktions-/Threat-Checks**: MISP/OTX/OFAC/BAFA → Graph-Verknüpfung → Alert
- **Chain-of-Custody Report**: automatisch generieren & signieren

## Verification Defaults

```yaml
verif:
  weights:
    {
      source:0.25,
      content:0.1,
      corro:0.25,
      rte:0.25,
      temporal:0.05,
      geo:0.05,
      media:0.05,
    }
  thresholds:
    verified: { score: 0.90, conf: 0.80 } # strenger
    likely_true: { score: 0.75, conf: 0.65 }
  evidence_required:
    min_independent_sources: 3
    must_include: ["gov", "ngo", "reputable_press"]
  require_human_review_for_publish: true
```

## Frontend Defaults

- **/search**: Badge-Filter `verified` only, Audit-Overlay **an**
- **/graphx**: Timeline + Geo standardmäßig an, „Evidence per edge“ sichtbar
- **Dossier**: Langform (Kette, Hashes, Signaturen, Anhang), QR-Checksum
- **Review-UI**: 4-Augen-Freigabe erzwungen

## Plugin-Whitelist (Kali/Tools)

- **Allowed** (mit Sandbox & Genehmigung): `nmap` (nur passiv/Version-Scan im eigenen Netz), `tshark/wireshark` (PCAP-Import), `yara`, `exiftool`, `pdfid`, `pefile`
- **Blocked**: Exploits ohne Mandat; Standard „default no-net“ Sandbox

---

# 3) Forschung-Preset (Balanced)

## Ziele

Schnelle Exploration, gute Reproduzierbarkeit, moderate OPSEC, nachvollziehbare Ergebnisse.

## Security/Runtime

```bash
IT_MODE=standard
IT_EGRESS=proxy
IT_NO_LOG_PERSIST=0
IT_EPHEMERAL_FS=0
IT_DOH=1
IT_BLOCK_DNS=1
```

## NiFi Pipelines (aktiviert)

- `ingest_rss_social_web_balanced`
- `ingest_api_generic` (öffentliche APIs + Key-Scoped)
- Verifikation komplett, aber **schneller eingestellt** (weniger tiefe Evidenzsuche)
- `geo_enrich_standard` (Cache aggressiver)

### NiFi Parameter Context (Ausschnitt)

```yaml
ResearchContext:
  RATE_LIMIT_RPS: "1.0"
  EVIDENCE_TOPK: "8"
  RETRIEVAL_TIMEOUT_S: "8"
```

## n8n Playbooks

- **Trendreport**: Entitäten + Topics pro Woche → Dossier
- **Anomalie-Erkennung**: plötzlicher Anstieg für Watchlist-Entity → Alert
- **Auto-Cluster**: Claim-Cluster → Graph-Communities → PDF

## Verification Defaults

```yaml
verif:
  weights:
    {
      source:0.2,
      content:0.1,
      corro:0.25,
      rte:0.25,
      temporal:0.05,
      geo:0.05,
      media:0.1,
    }
  thresholds:
    verified: { score: 0.80, conf: 0.70 }
    likely_true: { score: 0.65, conf: 0.55 }
  active_learning: true
  sample_uncertain_for_labeling: 0.2 # 20% der unsicheren Fälle in Label-Queue
```

## Frontend Defaults

- **/search**: Badge-Filter `≥uncertain` (alles sichtbar), Sortierung „Neuheit + Score“
- **/graphx**: Communities + Embeddings-Ansicht
- **Dossier**: Forschungsbericht (Methoden, Parameter, Repro-Hinweise)
- **Review-UI**: Override erlaubt, Label-Store prominent

## Plugin-Whitelist (Kali/Tools)

- **Allowed**: alle **passiven/forensischen** Tools; aktive nur im Lab/Isolated-Netz (Preset prüft Sandbox `no-net`)

---

# Preset-Auswahl (Switching)

Du kannst Presets als **Config-Pakete** ablegen und per ENV aktivieren:

```bash
IT_PROFILE={journalism|agency|research}
# Loader setzt dann:
# - ParameterContext (NiFi)
# - n8n Workflows (enable/disable)
# - Verification weights/thresholds
# - Frontend defaults
# - Security env & proxy wiring
```

Beispiel: `config/presets/journalism.yaml`

```yaml
profile: journalism
security:
  mode: incognito
  egress: tor+vpn
  ephemeral_fs: true
  logging_persist: false
verification:
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

**Journalismus:**

1. RSS/Web → NiFi normalize → Verifikation (voll) → OpenSearch/Neo4j
2. n8n Watchlist → Alert → Analyst Review-UI → Dossier-Lite (kurz)
3. Alles über Tor+VPN, ephemerer Speicher, keine Log-Persistenz

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

- **\[PRESET-1]** Preset-Loader (`IT_PROFILE`) + Mapping auf ENV/Configs
- **\[PRESET-2]** NiFi ParameterContexts: `JournalismContext`, `AgencyContext`, `ResearchContext`
- **\[PRESET-3]** n8n Enable/Disable per Preset (Tags/Env)
- **\[PRESET-4]** Verification-Weights/Thresholds pro Preset laden
- **\[PRESET-5]** Frontend Defaults pro Preset (/search, /graphx, Dossier, Review-UI)
- **\[PRESET-6]** Plugin-Whitelist/Policy pro Preset (OPA Validation)
- **\[PRESET-7]** Dossier-Vorlagen: `journalism_short.md`, `forensics_long.md`, `research_report.md`
- **\[PRESET-8]** Security-Checks: Fail-closed Tests je Preset (Egress, DNS, Logging)

---

# **ERGANZEN:** Packe "alles" als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile
