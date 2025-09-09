# Preset Profiles

---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L15-L17
merged_at: 2025-09-09T13:55:10.862233Z
---

## Security/Runtime

```bash
---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L1-L8
merged_at: 2025-09-09T13:55:10.875158Z
---

# Presets (Profile) – Überblick

* **Journalismus (INCognito+)** → maximaler Quellenschutz, „save-nothing“, starke Verifikation & manuelle Reviews.
* **Behörden/Firmen (Forensics+)** → gerichtsfeste Nachvollziehbarkeit, Chain-of-Custody, vollständiges Auditing.
* **Forschung (Balanced)** → produktives Arbeiten, moderate OPSEC, gute Reproduzierbarkeit.

---

---
merged_from:
  - docs/presets/Presets(Profile).md#L1-L8
merged_at: 2025-09-09T13:55:10.876616Z
---

# Presets (Profile) – Überblick

- **Journalismus (INCognito+)** → maximaler Quellenschutz, „save-nothing“, starke Verifikation & manuelle Reviews.
- **Behörden/Firmen (Forensics+)** → gerichtsfeste Nachvollziehbarkeit, Chain-of-Custody, vollständiges Auditing.
- **Forschung (Balanced)** → produktives Arbeiten, moderate OPSEC, gute Reproduzierbarkeit.

---

---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L11-L14
merged_at: 2025-09-09T13:55:10.879103Z
---

IT_EGRESS=tor+vpn
IT_HTTP_PROXY=http://proxy:8118
IT_SOCKS5_PROXY=socks5://tor:9050
IT_DOH=1
---
merged_from:
  - docs/presets/Presets(Profile).md#L11-L14
merged_at: 2025-09-09T13:55:10.880522Z
---

# Betriebsmodus
IT_MODE=incognito
IT_EGRESS=tor+vpn
IT_HTTP_PROXY=http://proxy:8118
---
merged_from:
  - docs/presets/Presets(Profile).md#L15-L17
merged_at: 2025-09-09T13:55:10.882039Z
---

IT_NO_LOG_PERSIST=1
IT_EPHEMERAL_FS=1

---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L18-L27
merged_at: 2025-09-09T13:55:10.883958Z
---

IT_BROWSER_PROFILE=strict
IT_SCRAPER_RESPECT_ROBOTS=1
IT_SCRAPER_DOMAIN_WHITELIST=media.gov,deutsche_presse*.tld,behörden*.de,ngo*.org
IT_SCRAPER_RATE_LIMIT=low
```

## NiFi Pipelines (aktiviert)

* `ingest_rss_journalism` (RSS/Atom-Whitelist, sanfte Backoffs)
* `ingest_web_readability_incognito` (Readability/trafilatura, Playwright nur für Whitelist)
---
merged_from:
  - docs/presets/Presets(Profile).md#L18-L27
merged_at: 2025-09-09T13:55:10.885772Z
---

IT_BROWSER_PROFILE=strict
IT_SCRAPER_RESPECT_ROBOTS=1
IT_SCRAPER_DOMAIN_WHITELIST=media.gov,deutsche_presse*.tld,behörden*.de,ngo*.org
IT_SCRAPER_RATE_LIMIT=low
```

## NiFi Pipelines (aktiviert)

- `ingest_rss_journalism` (RSS/Atom-Whitelist, sanfte Backoffs)
- `ingest_web_readability_incognito` (Readability/trafilatura, Playwright nur für Whitelist)
---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L28-L35
merged_at: 2025-09-09T13:55:10.887624Z
---

  ROBOTS_ENFORCE: "true"
  DOMAIN_WHITELIST: "media.gov,deutsche_presse*.tld,ngo*.org"
  RATE_LIMIT_RPS: "0.3"
  GEO_CODER_CACHE_TTL: "86400"
```

## n8n Playbooks

---
merged_from:
  - docs/presets/Presets(Profile).md#L28-L35
merged_at: 2025-09-09T13:55:10.889508Z
---

  ROBOTS_ENFORCE: "true"
  DOMAIN_WHITELIST: "media.gov,deutsche_presse*.tld,ngo*.org"
  RATE_LIMIT_RPS: "0.3"
  GEO_CODER_CACHE_TTL: "86400"
```

## n8n Playbooks

---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L36-L42
merged_at: 2025-09-09T13:55:10.891957Z
---

verif:
  weights: {source:0.2, content:0.1, corro:0.3, rte:0.25, temporal:0.05, geo:0.05, media:0.05}
  thresholds:
    verified:        {score: 0.85, conf: 0.70}
    likely_true:     {score: 0.70, conf: 0.60}
    uncertain:       {score: 0.50}
    likely_false:    {score: 0.35}
---
merged_from:
  - docs/presets/Presets(Profile).md#L36-L42
merged_at: 2025-09-09T13:55:10.893745Z
---

verif:
  weights:
    {
      source:0.2,
      content:0.1,
      corro:0.3,
      rte:0.25,
---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L55-L60
merged_at: 2025-09-09T13:55:10.895745Z
---

# 2) Behörden/Firmen-Preset (Forensics+)

## Ziele

Beweis­sicherheit, vollständiges Auditing, starke Governance, maximale Datenintegrität.

---
merged_from:
  - docs/presets/Presets(Profile).md#L55-L60
merged_at: 2025-09-09T13:55:10.897660Z
---

- **Review-UI**: „Review before share“ erzwungen

## Plugin-Whitelist (Kali/Tools)

- **Allowed**: `whois`, `theHarvester` (nur passive Quellen), `exiftool`, `imagehash`, `yara` (offline), `nmap -sL` (Listing only)
- **Blocked**: aktive Exploits/Intrusion-Tools
---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L75-L81
merged_at: 2025-09-09T13:55:10.899266Z
---

### Provenienz & Hash

* Jeder Flow schreibt `hash_sha256`, `signer`, `sigstore_bundle` in Metadata
* Exporte → WORM-Bucket (Retention Policy)

## n8n Playbooks

---
merged_from:
  - docs/presets/Presets(Profile).md#L84-L90
merged_at: 2025-09-09T13:55:10.901163Z
---

### Provenienz & Hash

- Jeder Flow schreibt `hash_sha256`, `signer`, `sigstore_bundle` in Metadata
- Exporte → WORM-Bucket (Retention Policy)

## n8n Playbooks

---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L82-L88
merged_at: 2025-09-09T13:55:10.902919Z
---

```yaml
verif:
  weights: {source:0.25, content:0.1, corro:0.25, rte:0.25, temporal:0.05, geo:0.05, media:0.05}
  thresholds:
    verified:     {score: 0.90, conf: 0.80}   # strenger
    likely_true:  {score: 0.75, conf: 0.65}
  evidence_required:
---
merged_from:
  - docs/presets/Presets(Profile).md#L91-L97
merged_at: 2025-09-09T13:55:10.904502Z
---

```yaml
verif:
  weights:
    {
      source:0.25,
      content:0.1,
      corro:0.25,
---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L91-L94
merged_at: 2025-09-09T13:55:10.905979Z
---

* **/graphx**: Timeline + Geo standardmäßig an, „Evidence per edge“ sichtbar
* **Dossier**: Langform (Kette, Hashes, Signaturen, Anhang), QR-Checksum
* **Review-UI**: 4-Augen-Freigabe erzwungen

---
merged_from:
  - docs/presets/Presets(Profile).md#L100-L103
merged_at: 2025-09-09T13:55:10.907575Z
---

  evidence_required:
    min_independent_sources: 3
    must_include: ["gov", "ngo", "reputable_press"]
  require_human_review_for_publish: true
---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L106-L113
merged_at: 2025-09-09T13:55:10.909106Z
---


```bash
IT_MODE=standard
IT_EGRESS=proxy
IT_NO_LOG_PERSIST=0
IT_EPHEMERAL_FS=0
IT_DOH=1
IT_BLOCK_DNS=1
---
merged_from:
  - docs/presets/Presets(Profile).md#L115-L122
merged_at: 2025-09-09T13:55:10.910789Z
---

---

# 3) Forschung-Preset (Balanced)

## Ziele

Schnelle Exploration, gute Reproduzierbarkeit, moderate OPSEC, nachvollziehbare Ergebnisse.

---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L114-L118
merged_at: 2025-09-09T13:55:10.912401Z
---

* `geo_enrich_standard` (Cache aggressiver)

### NiFi Parameter Context (Ausschnitt)

```yaml
---
merged_from:
  - docs/presets/Presets(Profile).md#L123-L127
merged_at: 2025-09-09T13:55:10.913963Z
---

IT_DOH=1
IT_BLOCK_DNS=1
```

## NiFi Pipelines (aktiviert)
---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L119-L124
merged_at: 2025-09-09T13:55:10.915484Z
---

```

## n8n Playbooks

* **Trendreport**: Entitäten + Topics pro Woche → Dossier
* **Anomalie-Erkennung**: plötzlicher Anstieg für Watchlist-Entity → Alert
---
merged_from:
  - docs/presets/Presets(Profile).md#L128-L133
merged_at: 2025-09-09T13:55:10.916918Z
---

- `geo_enrich_standard` (Cache aggressiver)

### NiFi Parameter Context (Ausschnitt)

```yaml
ResearchContext:
---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L139-L145
merged_at: 2025-09-09T13:55:10.918506Z
---

* **Review-UI**: Override erlaubt, Label-Store prominent

## Plugin-Whitelist (Kali/Tools)

* **Allowed**: alle **passiven/forensischen** Tools; aktive nur im Lab/Isolated-Netz (Preset prüft Sandbox `no-net`)

---
---
merged_from:
  - docs/presets/Presets(Profile).md#L157-L163
merged_at: 2025-09-09T13:55:10.920007Z
---

  active_learning: true
  sample_uncertain_for_labeling: 0.2 # 20% der unsicheren Fälle in Label-Queue
```

## Frontend Defaults

- **/search**: Badge-Filter `≥uncertain` (alles sichtbar), Sortierung „Neuheit + Score“
---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L146-L152
merged_at: 2025-09-09T13:55:10.921641Z
---

IT_PROFILE={journalism|agency|research}
# Loader setzt dann:
# - ParameterContext (NiFi)
# - n8n Workflows (enable/disable)
# - Verification weights/thresholds
# - Frontend defaults
# - Security env & proxy wiring
---
merged_from:
  - docs/presets/Presets(Profile).md#L164-L170
merged_at: 2025-09-09T13:55:10.923280Z
---

- **Allowed**: alle **passiven/forensischen** Tools; aktive nur im Lab/Isolated-Netz (Preset prüft Sandbox `no-net`)

---

# Preset-Auswahl (Switching)

Du kannst Presets als **Config-Pakete** ablegen und per ENV aktivieren:
---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L155-L158
merged_at: 2025-09-09T13:55:10.924990Z
---

  egress: tor+vpn
  ephemeral_fs: true
  logging_persist: false
verification:
---
merged_from:
  - docs/presets/Presets(Profile).md#L173-L176
merged_at: 2025-09-09T13:55:10.926628Z
---

# - Security env & proxy wiring
```

Beispiel: `config/presets/journalism.yaml`
---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L170-L176
merged_at: 2025-09-09T13:55:10.928252Z
---


**Journalismus:**

1. RSS/Web → NiFi normalize → Verifikation (voll) → OpenSearch/Neo4j
2. n8n Watchlist → Alert → Analyst Review-UI → Dossier-Lite (kurz)
3. Alles über Tor+VPN, ephemerer Speicher, keine Log-Persistenz

---
merged_from:
  - docs/presets/Presets(Profile).md#L188-L194
merged_at: 2025-09-09T13:55:10.929901Z
---

  search_defaults: {badges_min: "likely_true", time_range: "72h"}
  dossier_template: "journalism_short.md"
plugins:
  whitelist: [whois, theHarvester, exiftool, imagehash, yara]
```

---
---
merged_from:
  - docs/dev/v0.2/Preset-Profile.md#L186-L191
merged_at: 2025-09-09T13:55:10.931508Z
---


* **\[PRESET-1]** Preset-Loader (`IT_PROFILE`) + Mapping auf ENV/Configs
* **\[PRESET-2]** NiFi ParameterContexts: `JournalismContext`, `AgencyContext`, `ResearchContext`
* **\[PRESET-3]** n8n Enable/Disable per Preset (Tags/Env)
* **\[PRESET-4]** Verification-Weights/Thresholds pro Preset laden
* **\[PRESET-5]** Frontend Defaults pro Preset (/search, /graphx, Dossier, Review-UI)
---
merged_from:
  - docs/presets/Presets(Profile).md#L204-L209
merged_at: 2025-09-09T13:55:10.933016Z
---

**Forschung:**

1. Mixed Sources → NiFi → Verifikation (schneller) → Search/Graph
2. n8n Trendreport/Anomalien → Auto-Cluster → Forschungs-Dossier
3. Reproduzierbare Settings, Active Learning an
