# Superset-Filter-Composer, NiFi → Aleph Upload & Flowise Agent

Diese Anleitung enthält drei Bausteine inklusive Copy-Paste-Snippets und Mini-Checks.

---

## 1) Superset Native-Filter URL Composer

Ziel: Einen Link erzeugen, der ein Dashboard mit **vorbelegten Filtern** öffnet (z. B. Symbol/Datum).

### 1.1 JS-Utility (Frontend)

Datei: `apps/frontend/lib/superset.ts`

```ts
// Compose Superset dashboard URL with native filters (hash fragment)
export type NativeFilter = {
  id: string; // stable filter id (or auto)
  column: string; // column name in dataset
  datasetId: number; // Superset dataset id
  values?: (string | number)[]; // for select/filter_box
  timeRange?: string; // e.g. "Last 30 days", "No filter"
};

export function supersetDashboardUrl(
  base: string,
  slug: string,
  filters: NativeFilter[],
) {
  // Superset accepts native_filters_key or full state via # or ?native_filters=...
  // We inline state via hash for portability.
  const filterState = {
    native_filters: filters.map((f, i) => ({
      id: f.id || `auto-${i}`,
      filterState: {
        value: f.values ?? null,
        validateMessage: null,
      },
      targets: [
        {
          column: f.column,
          datasetId: f.datasetId,
        },
      ],
      type: "select",
    })),
    time_range: filters.find((f) => f.timeRange)?.timeRange || "No filter",
  };
  const encoded = encodeURIComponent(JSON.stringify(filterState));
  // Example final URL:
  // http://superset.host/superset/dashboard/<slug>/?standalone=0#<encoded>
  const u = new URL(`/superset/dashboard/${slug}/`, base);
  u.searchParams.set("standalone", "0");
  return `${u.toString()}#${encoded}`;
}
```

**Beispiel:**

```ts
const url = supersetDashboardUrl(
  "http://superset.127.0.0.1.nip.io",
  "openbb-overview-dbt-sync",
  [
    { column: "symbol", datasetId: 42, values: ["SAP.DE"] },
    {
      id: "time",
      column: "as_of_date",
      datasetId: 42,
      timeRange: "Last 30 days",
    },
  ],
);
```

### 1.2 Python-Helper (für n8n/Jobs)

```python
import json, urllib.parse

def superset_url(base:str, slug:str, filters:list[dict]):
    state = {"native_filters": [], "time_range": "No filter"}
    for i,f in enumerate(filters):
        state["native_filters"].append({
            "id": f.get("id", f"auto-{i}"),
            "filterState": {"value": f.get("values"), "validateMessage": None},
            "targets": [{"column": f["column"], "datasetId": f["datasetId"]}],
            "type": "select",
        })
        if f.get("timeRange"): state["time_range"] = f["timeRange"]
    frag = urllib.parse.quote(json.dumps(state))
    return f"{base}/superset/dashboard/{slug}/?standalone=0#{frag}"
```

**Smoke-Check:** URL erzeugen, im Browser öffnen → Dashboard lädt mit aktivem Filter.

---

## 2) Aleph Upload via NiFi — exakte Prozessor-Konfiguration

Wir verwenden Variante **A** (Multipart Upload `ingest`).

### NiFi Flow

1. **ListenFile** – Input Directory: `/data/watch`, Keep Source File: `true`
2. **UpdateAttribute** – setzt u. a. `filename_original`, `aleph_title`, `aleph_meta`, `aleph_coll`, `aleph_token`
3. **InvokeHTTP** – `POST http://aleph.docs.svc.cluster.local:8080/api/2/collections/${aleph_coll}/ingest?sync=1`
   - Content-Type `multipart/form-data`
   - Header `Authorization: ApiKey ${aleph_token}`
   - Multipart: FlowFile als `file`, zusätzliche Teile `meta` (JSON) und `title`
4. **LogAttribute** – loggt `filename_original, aleph_response`

#### Quick-cURL zum Abgleich

```bash
curl -X POST "http://aleph.127.0.0.1.nip.io/api/2/collections/<COLL_ID>/ingest?sync=1" \
  -H "Authorization: ApiKey <YOUR_API_KEY>" \
  -F 'meta={"languages":["de"],"countries":["DE"]};type=application/json' \
  -F "title=Test PDF" \
  -F "file=@/path/to/test.pdf;type=application/pdf"
```

Erwartung: `200/202` mit `document_id` im JSON.

---

## 3) Flowise LLM-Agent — Prompt, Tools, Guardrails

### 3.1 Tools (Function-Schemas)

`search_docs`, `graph_neighbors`, `summarize_text`, `annotate_doc` (per HTTP Request Node).

### 3.2 System-Prompt

```yaml
You are the InfoTerminal Investigation Assistant.
Tools: search_docs, graph_neighbors, summarize_text, annotate_doc.

Rules / Guardrails:
- Always plan briefly (bullet list) BEFORE calling tools; keep plans to <= 4 bullets.
- Never call more than 3 tools per user turn.
- Prefer search_docs first, then summarize_text the top result, optionally annotate_doc.
- Only call graph_neighbors when the user asks for connections or you extracted a concrete node_id.
- For graph_neighbors, limit ≤ 100 and never enumerate PII or secrets beyond the returned data.
- Respect tenant & classification constraints: do not fabricate data. If a call fails, report minimal error.
- Token budget: keep your final answer ≤ 250 words. Prefer bullet points.
Output format:
1) Findings (bullets),
2) Evidence (links or ids),
3) Next steps (bullets).
```

### 3.3 Flowise Setup (High-level)

- **LLM Node**: Ollama Llama‑3 (oder OpenAI-kompatibel), Max Tokens 512‑800, Temp 0.2
- **Agent Node**: Function-Calling, Tool-Limit 3, Tools wie oben
- **Memory**: ConversationBuffer (max. 5 Messages)
- **Output Parser**: passt durch
- Optionaler Pre-Tool Hook begrenzt `graph_neighbors.limit` auf 100

### 3.4 Beispiel-User-Prompt

> „Analysiere Fall 42: Fokus ACME Berlin. Was sind die Top-Dokumente, kurze Zusammenfassung.
> Zeig mir direkte Verbindungen zu ‘O\:acme’.“

Erwartetes Tool-Pattern:

1. `search_docs(query="ACME Berlin")`
2. `summarize_text(text=top_doc.body)`
3. `graph_neighbors(node_id="O:acme", limit=50)`

Antwortformat:

```text
* Findings: • …
* Evidence: • doc links, graph link (`http://localhost:3000/graphx?focus=O:acme`)
* Next steps: • …
```

---

## Mini-Checkliste

- [ ] **Superset-Composer**: JS/Python Helper eingebaut → Link öffnet Dashboard mit Filtern
- [ ] **NiFi→Aleph**: InvokeHTTP Multipart konfiguriert, 200/202 Rückgabe sichtbar
- [ ] **Flowise Agent**: Tools/Schemas registriert, Guardrail-Prompt gesetzt, Tool-Limit aktiv
- [ ] **Smoke Tests**:
  - `POST /annotate` → `/docs/{id}/html` zeigt Entities → GraphX
  - Flowise Prompt ausführen → Tool-Aufrufe im Log sichtbar
