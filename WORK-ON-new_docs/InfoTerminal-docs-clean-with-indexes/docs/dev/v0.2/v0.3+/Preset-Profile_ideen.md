# 📑 Neue Preset-Profile

## 1. **Climate Researcher**

🌍 Fokus: Klimarisiken, Emissionen, Naturkatastrophen

* **Security:** Standard, Proxy+DoH; keine Incognito nötig (offene Daten).
* **NiFi Pipelines:**

  * `ingest_climate_data` (Copernicus, ESA, NASA)
  * `ingest_open_data` (CO₂-Bilanzen, Wetter, Landwirtschaft)
* **n8n Flows:**

  * Climate Alerts (Temperaturanstieg, Emissionsverstöße)
  * Quarterly Climate Report (Risiko-Heatmap)
* **Verification:** weniger Fake-News, mehr Data Quality Check (PII irrelevant).
* **Frontend Defaults:** Climate Dashboard + Heatmap aktiv, Dossier „Climate Risk Report“.

---

## 2. **Compliance Officer**

⚖️ Fokus: Legal & Financial Intelligence für Unternehmen/Behörden

* **Security:** Forensics Mode (vollständiges Logging, WORM-Storage).
* **NiFi Pipelines:**

  * `ingest_laws` + `rag_index` (Gesetze)
  * `ingest_financial_data` + `enrich_sanctions`
* **n8n Flows:**

  * Compliance Alerts (Verstoß gegen Gesetz X)
  * Red Flag Financial Reports
* **Verification:** sehr strenge Schwellen (verified > 0.9).
* **Frontend Defaults:** Legal/Compliance Tab, Financial Risk Dashboard, Dossier „Compliance & Risk Report“.

---

## 3. **Crisis Analyst**

🕊️ Fokus: Humanitarian & Geopolitical Intelligence

* **Security:** Incognito Mode möglich (NGO/Field Reports), Logging optional.
* **NiFi Pipelines:**

  * `ingest_health_weather_data`
  * `ingest_adsb` + `ingest_ais` (Geo-Daten)
* **n8n Flows:**

  * Crisis Alerts („Region X → Hunger/Epidemie“)
  * Conflict Reports (Truppenbewegung, Proteste)
* **Verification:** mittel, kombiniert NGO+News+Social.
* **Frontend Defaults:** Crisis Dashboard (Ampel), Geopolitical Map, Dossier „Humanitarian Crisis Report“.

---

## 4. **Disinformation Watchdog**

🛰️ Fokus: Desinformationskampagnen, Narrative, Propaganda

* **Security:** Incognito Default (um Fingerprinting zu vermeiden).
* **NiFi Pipelines:**

  * `ingest_social` (Telegram, Reddit, Mastodon, ggf. Twitter-Scraper)
  * `claim_extract_cluster`
* **n8n Flows:**

  * Narrative Alerts (Cluster > N Accounts)
  * BotNet Dossiers
* **Verification:** strenge Content Checks, Active Learning aktiv.
* **Frontend Defaults:** Narrative Dashboard + Review-UI prominent.

---

## 5. **Economic Analyst**

💰 Fokus: Märkte, Handelsströme, Wirtschaftliche Risiken

* **Security:** Standard; Logging aktiv für Reproduzierbarkeit.
* **NiFi Pipelines:**

  * `ingest_economic_data` (IMF, OECD, World Bank, OpenBB)
* **n8n Flows:**

  * Economic Reports (wöchentliche Trends, Risikoszenarien)
* **Verification:** Balanced; Scorecards wichtig.
* **Frontend Defaults:** Economic Dashboard, Dossier „Economic Intelligence Report“.

---

# 📂 Preset-Übersicht (zusätzlich zu Journalismus, Behörden/Firmen, Forschung)

| Preset             | Cluster/Blueprints             | Zielgruppe          |
| ------------------ | ------------------------------ | ------------------- |
| Climate Researcher | Climate-Intelligence           | NGOs, Forschung     |
| Compliance Officer | Legal + Financial-Intelligence | Behörden, Firmen    |
| Crisis Analyst     | Humanitarian + Geopolitical    | NGOs, UN, Politik   |
| Disinfo Watchdog   | Disinformation-Intelligence    | Medien, Forschung   |
| Economic Analyst   | Economic-Intelligence          | Think Tanks, Firmen |

---

# 📌 Tickets (zum TODO-Index ergänzen)

* **\[PRESET-9]** Preset Climate Researcher (Pipelines, Flows, Dashboards)
* **\[PRESET-10]** Preset Compliance Officer (Legal + Financial, Forensics Mode)
* **\[PRESET-11]** Preset Crisis Analyst (Humanitarian + Geopolitical)
* **\[PRESET-12]** Preset Disinfo Watchdog (Social Ingest + Cluster)
* **\[PRESET-13]** Preset Economic Analyst (Economic Data + Dashboards)

---
