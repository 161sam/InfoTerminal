
➡ Consolidated at: ../dev/guides/flowise-agents.md#docs-export-appflowy-md
# AppFlowy Export – Integration Guide

> Ziel: Dossiers, Graphen, Tabellen, Maps aus InfoTerminal **auf Knopfdruck** in **AppFlowy** nutzen – primär via Datei-/Bundle-Export (offline, robust), optional via Adapter/API falls verfügbar.

---

## ✅ TL;DR

- **Empfohlen:** `bundle.zip` (Markdown + Assets + Meta) → in AppFlowy **„Import Markdown“**.
- **Kompatibel:** Mermaid/DOT + gerenderte SVGs, CSV-Tabellen als Anhänge.
- **Optional:** Watched-Folder-Modus (lokaler Sync), später **Adapter/API** wenn AppFlowy-API stabil verfügbar.

---

## 📦 Bundle-Struktur

```

bundle/
index.md                        # gerendertes Dossier (Front-Matter bleibt erhalten)
assets/
figures/*.png|svg
graphs/graph.mmd              # Mermaid
graphs/graph.dot              # Graphviz DOT
graphs/graph.svg              # gerendertes SVG
tables/*.csv
maps/\*.geojson
meta/export.json                # Provenienz, Hashes, Modelle, Pipelines

````

**Mermaid in `index.md`:**
```markdown
```mermaid
graph TD
  A[Actor] --> B[Event]
  B --> C[Org]
````

````
> Falls AppFlowy Mermaid nicht sofort rendert, ist `graphs/graph.svg` als sichtbarer Fallback im Text verlinkt.

---

## 🖥️ Bedienung (Frontend)

- Button **„Export → AppFlowy“**
- Optionen:
  - Inhalt: *Dossier*, *Graph*, *Canvas*, *Evidenz-Tabellen*
  - Formate: *md*, *svg*, *mermaid*, *dot*, *csv*, *geojson*
  - Ziel: *ZIP* oder *Watched Folder* (z. B. `~/AppFlowy/import/`)
- Ergebnis: Pfad/Datei + Hashes + „In AppFlowy öffnen“.

---

## 🧰 CLI

```bash
# Dossier als Bundle für AppFlowy
it export dossier \
  --template docs/dossiers/compliance_risk_report.md.tmpl \
  --data cases/123.json \
  --target appflowy \
  --out out/appflowy_bundle.zip

# Nur Graph als Mermaid+SVG
it export graph --case 123 --formats mermaid,svg --out out/graphs/
````

---

## 🔁 Watched-Folder-Modus

* Konfig: `~/.infoterminal/export.yaml`

```yaml
watched_folders:
  appflowy: "/Users/<you>/AppFlowy/import"
```

* Export schreibt automatisch in diesen Ordner; Import in AppFlowy: **„Import Markdown“** auf Ordner/ZIP.

---

## 🔒 Security & Governance

* Standard: **File-Export** (kein API-Zugriff).
* OPA-Policy: Export nur, wenn `classification ∈ {PUBLIC, INTERNAL}` (konfigurierbar).
* Hashes & Provenienz in `meta/export.json` für Audit/Forensics.
* Falls API-Adapter: Tokens via **Vault**, least-privilege Scopes, kurze TTL.

---

## 🔌 (Optional) AppFlowy-Adapter/API

> Nur nutzen, wenn eine API/Serverinstanz verfügbar ist.

**Endpoints (Design):**

* `POST /pages` – Seite anlegen `{title, markdown, assets[]}`
* `POST /assets` – Dateien/Graphen hochladen
* `POST /graphs` – Mermaid/DOT registrieren & rendern

**Fallback:** ohne API stets Bundle-Export.

---

## 🧪 Tests

* **Golden Bundle Tests:** Snapshot von `index.md` + Assets validieren.
* **Roundtrip:** Import in frische AppFlowy-Instanz → Bilder, Tabellen, Links prüfen.
* **Mermaid-Fallback:** Sichtbarkeit via `graph.svg` sicherstellen.

---

## 📎 Beispiel: `meta/export.json`

```json
{
  "case_id": "123e4567-e89b-12d3-a456-426614174000",
  "exported_at": "2025-09-05T12:34:56Z",
  "profile": "compliance_officer",
  "artifacts": {
    "dossier": "index.md",
    "graphs": ["assets/graphs/graph.mmd", "assets/graphs/graph.svg"],
    "tables": ["assets/tables/evidence.csv"],
    "maps": ["assets/maps/area.geojson"]
  },
  "hashes": {
    "index.md": "sha256-…",
    "assets/graphs/graph.svg": "sha256-…"
  },
  "provenance": {
    "pipeline": "nifi/legal_v1",
    "models": ["rag-api@2025.09", "nlp-verif@2025.09.0"],
    "request_id": "X-req-…"
  }
}
```

