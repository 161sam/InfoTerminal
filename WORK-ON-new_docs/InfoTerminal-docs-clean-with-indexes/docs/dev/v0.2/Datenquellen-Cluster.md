# 🌐 Datenquellen-Cluster für InfoTerminal

## 1) **News & Social Media**

* **RSSHub / Feeds** (NYTimes, Guardian, Spiegel, etc.)
* **Social Media**: Mastodon, Reddit, Telegram, Twitter/X (Scraper), TikTok, Instagram
* **Video-Plattformen**: YouTube/Vimeo → Transkripte (Whisper)
* **Blogs / Webseiten** via Scraper (trafilatura, Readability)

**Impact:** Hoch (erste Quelle für Fake-News, Trends)
**Aufwand:** Mittel (APIs, Scraper, Rate Limits)
**Prio:** ⭐⭐⭐ High

---

## 2) **Open Data & Behörden**

* **EU Open Data Portal**, **Bundesanzeiger**, **Parlament-Dokumente**
* **UN, WHO, OECD, Weltbank**
* **Sanktionslisten**: EU, UN, OFAC, BAFA
* **Register**: Handelsregister, NGO-Register, Firmenregister

**Impact:** Sehr hoch (verlässliche, faktenbasierte Daten → Gegengewicht zu Social)
**Aufwand:** Mittel (oft CSV/XML APIs, aber Heterogenität)
**Prio:** ⭐⭐⭐ High

---

## 3) **Cyber Threat Intelligence**

* **Threat Feeds**: MISP, AlienVault OTX, Abuse.ch, Spamhaus, CERT
* **Shodan/Censys**: Internet-weite Scans
* **VirusTotal / MalwareBazaar** (nur Hashes, keine Payloads)
* **BGP/ASN Daten**: Routing-Anomalien

**Impact:** Hoch (Sicherheits-Use-Cases, Behörden, Firmen)
**Aufwand:** Mittel bis Hoch (teilweise API-Key/Legal-Limits)
**Prio:** ⭐⭐ Mid–High

---

## 4) **Wissenschaft & Forschung**

* **arXiv, PubMed, Semantic Scholar**
* **Patente** (WIPO, DEPATISnet)
* **Konferenz-Papers** (z. B. ACM, IEEE)

**Impact:** Mittel (Nischen-Analysen, Wissenschaftler\:innen)
**Aufwand:** Mittel (APIs teils vorhanden, viele Formate)
**Prio:** ⭐⭐ Mid

---

## 5) **Sensor & Realwelt**

* **OSM Live** (Geodaten)
* **ADS-B Exchange** (Flugbewegungen)
* **AIS (MarineTraffic)** (Schiffe)
* **LoRaWAN/MQTT** IoT Feeds
* **Satellitenbilder** (NASA/ESA, SentinelHub)

**Impact:** Mittel–Hoch (Geo-/Bewegungsanalysen, Konflikte, Krisen)
**Aufwand:** Hoch (Datenmenge, Spezialformate, Lizenzen)
**Prio:** ⭐ Mid

---

# 📊 Zusammenfassung (Priorisierung)

| Cluster                   | Impact 🚀   | Aufwand ⚙️  | Prio ⭐      |
| ------------------------- | ----------- | ----------- | ----------- |
| News & Social Media       | Hoch        | Mittel      | ⭐⭐⭐ High    |
| Open Data & Behörden      | Sehr hoch   | Mittel      | ⭐⭐⭐ High    |
| Cyber Threat Intelligence | Hoch        | Mittel-Hoch | ⭐⭐ Mid–High |
| Wissenschaft & Forschung  | Mittel      | Mittel      | ⭐⭐ Mid      |
| Sensor & Realwelt         | Mittel-Hoch | Hoch        | ⭐ Mid       |

---

👉 Damit hätten wir die „**Top 2 Cluster**“ für den nächsten Ausbau klar:

1. **News & Social Media**
2. **Open Data & Behörden**

Diese beiden liefern sowohl **Volumen** (News/SoMe) als auch **verlässliche Faktdaten** (Behörden/Open Data) → perfekt für Verifikation.

---

TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können!
