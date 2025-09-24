# 📄 Compliance – Source SBOM & License Inventory

Die Source-SBOMs und das konsolidierte Lizenzinventar werden automatisiert unter `artifacts/` abgelegt.
Die Artefakte dienen als Nachweis für Phase-2-Lieferumfang (Supply-Chain/SBOM Gate `SEC-SBX-3`).

## Artefakte

| Typ | Pfad | Beschreibung |
| --- | --- | --- |
| SBOM (Backend, Python) | `artifacts/sbom/source/backend-python.cdx.json` | CycloneDX 1.6 JSON, generiert aus `services/graph-views/requirements-dev.txt` + `pyproject.toml`. |
| SBOM (Frontend, Node) | `artifacts/sbom/source/frontend-node.cdx.json` | CycloneDX 1.6 JSON, erzeugt via `@appthreat/cdxgen` für `apps/frontend`. |
| Lizenzinventar | `artifacts/compliance/licenses/license_inventory.csv`<br>`artifacts/compliance/licenses/license_inventory.json` | Zusammengeführte Lizenz-/Repository-Liste (Python + Node), sortiert nach Ökosystem und Paketname. |
| SBOMs (Container-Images) | `artifacts/sbom/images/*.cdx.json` | CycloneDX 1.6 JSON pro Image aus `docker-compose*.yml` und `deploy/kubernetes/production.yaml`. Initiale Platzhalter bestehen, bis der Generator mit Docker-Zugriff läuft. |
| Lizenzmatrix (Container-Images) | `artifacts/compliance/licenses/images.json` | Mapping `Image → Lizenzen/Quellen`, erzeugt aus den Image-SBOMs. |

Die CSV enthält die Spalten `ecosystem`, `name`, `version`, `license`, `url`, `source_bom`. Für Pakete ohne Lizenzangaben in den Upstream-Metadaten bleibt das Feld auf `UNKNOWN` gesetzt (derzeit `anyio` und `pytest-asyncio`).

## Generierung / Aktualisierung

```bash
python scripts/generate_source_sbom.py
```

Der Generator führt zwei Schritte aus:

1. **Python:** `cyclonedx_py requirements` (inkl. `--output-reproducible`) über die `graph-views`-Runtime-Dependencies.
2. **Node:** `npx --yes @appthreat/cdxgen@7.0.5 -t npm -p apps/frontend -o artifacts/sbom/source/frontend-node.cdx.json` gegen den Frontend-Workspace. Lizenz- und Repository-Informationen werden direkt aus `node_modules/*/package.json` extrahiert.

Anschließend werden beide SBOMs zu einem gemeinsamen Lizenzinventar zusammengeführt. Für Python-Pakete werden, falls nötig, Projekt-URLs & Lizenzen über die PyPI JSON API ergänzt.

## Container-Image SBOMs

```bash
python scripts/generate_image_sboms.py --auto-build
```

Der Generator liest alle `docker-compose*.yml` sowie `deploy/kubernetes/production.yaml`, erstellt (falls notwendig) lokale Images via `docker compose build` bzw. `docker build` und erzeugt anschließend CycloneDX-SBOMs. Standardmäßig wird `docker sbom` bzw. `syft` genutzt; alternativ kann über `SBOM_IMAGE_TOOL="syft"` ein anderes CLI erzwungen werden. Platzhalter-SBOMs (`UNKNOWN`-Lizenz) liegen bereits im Repository – ein Lauf mit realen Images überschreibt sie deterministisch.

> Anforderungen: Docker-Engine mit Pull-Zugriff auf alle referenzierten Images. Für lokale Builds `AUTO_BUILD=1` setzen oder `--auto-build` nutzen.

## Validierung in CI

```bash
python scripts/check_sbom_source_integrity.py
python scripts/check_sbom_image_integrity.py
```

Der Check schlägt fehl, wenn

- eines der oben genannten Artefakte fehlt,
- eine Datei leer ist oder
- die JSON-Struktur keine `components` enthält (Source-Gate)
- für Images ein Eintrag ohne SBOM/Lizenzen existiert.

In der GitHub Action `CI` laufen die Gates als Jobs `sbom_source_integrity` und `sbom_image_integrity`.

## Bekannte Lücken / Nächste Schritte

- **Unvollständige Lizenzdaten (Python):** `anyio` und `pytest-asyncio` veröffentlichen keine Lizenzklassifizierungen im PyPI-Metadatum. Ticket offen im Compliance-Backlog (`SEC-SBX-3`), Workaround: manuelle Pflege im Inventar, sobald Upstream nachzieht.
- **Zusätzliche Services:** Sobald weitere Backends/Services produktiv gehen, müssen deren Manifest-/Lock-Dateien im Generator ergänzt werden.
- **Signierte Artefakte:** Auslieferung & Signierung der Container-SBOMs (Cosign/OCI-Refs) stehen noch aus.
- **Platzhalter für interne Images:** Für `infoterminal/*`-Images existieren aktuell nur Platzhalter-SBOMs (`UNKNOWN`-Lizenz). Sobald die Container-Build-Pipeline aktiv ist, muss `scripts/generate_image_sboms.py` mit Docker-Zugriff ausgeführt werden.
