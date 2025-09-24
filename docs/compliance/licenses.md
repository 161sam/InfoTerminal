# 📄 Compliance – Source SBOM & License Inventory

Die Source-SBOMs und das konsolidierte Lizenzinventar werden automatisiert unter `artifacts/` abgelegt.
Die Artefakte dienen als Nachweis für Phase-2-Lieferumfang (Supply-Chain/SBOM Gate `SEC-SBX-3`).

## Artefakte

| Typ | Pfad | Beschreibung |
| --- | --- | --- |
| SBOM (Backend, Python) | `artifacts/sbom/source/backend-python.cdx.json` | CycloneDX 1.6 JSON, generiert aus `services/graph-views/requirements-dev.txt` + `pyproject.toml`. |
| SBOM (Frontend, Node) | `artifacts/sbom/source/frontend-node.cdx.json` | CycloneDX 1.6 JSON, erzeugt via `@appthreat/cdxgen` für `apps/frontend`. |
| Lizenzinventar | `artifacts/compliance/licenses/license_inventory.csv`<br>`artifacts/compliance/licenses/license_inventory.json` | Zusammengeführte Lizenz-/Repository-Liste (Python + Node), sortiert nach Ökosystem und Paketname. |

Die CSV enthält die Spalten `ecosystem`, `name`, `version`, `license`, `url`, `source_bom`. Für Pakete ohne Lizenzangaben in den Upstream-Metadaten bleibt das Feld auf `UNKNOWN` gesetzt (derzeit `anyio` und `pytest-asyncio`).

## Generierung / Aktualisierung

```bash
python scripts/generate_source_sbom.py
```

Der Generator führt zwei Schritte aus:

1. **Python:** `cyclonedx_py requirements` (inkl. `--output-reproducible`) über die `graph-views`-Runtime-Dependencies.
2. **Node:** `npx --yes @appthreat/cdxgen@7.0.5 -t npm -p apps/frontend -o artifacts/sbom/source/frontend-node.cdx.json` gegen den Frontend-Workspace. Lizenz- und Repository-Informationen werden direkt aus `node_modules/*/package.json` extrahiert.

Anschließend werden beide SBOMs zu einem gemeinsamen Lizenzinventar zusammengeführt. Für Python-Pakete werden, falls nötig, Projekt-URLs & Lizenzen über die PyPI JSON API ergänzt.

## Validierung in CI

```bash
python scripts/check_sbom_source_integrity.py
```

Der Check schlägt fehl, wenn

- eines der oben genannten Artefakte fehlt,
- eine Datei leer ist oder
- die JSON-Struktur keine `components` enthält.

In der GitHub Action `CI` läuft das Gate als Job `sbom_source_integrity`.

## Bekannte Lücken / Nächste Schritte

- **Unvollständige Lizenzdaten (Python):** `anyio` und `pytest-asyncio` veröffentlichen keine Lizenzklassifizierungen im PyPI-Metadatum. Ticket offen im Compliance-Backlog (`SEC-SBX-3`), Workaround: manuelle Pflege im Inventar, sobald Upstream nachzieht.
- **Zusätzliche Services:** Sobald weitere Backends/Services produktiv gehen, müssen deren Manifest-/Lock-Dateien im Generator ergänzt werden.
- **Binary SBOMs:** Container-/Image-SBOMs bleiben außerhalb des Scopes und sind separat (Trivy/Cosign) zu implementieren.
