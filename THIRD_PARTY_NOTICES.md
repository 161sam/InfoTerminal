# 📦 Third-Party Notices

Dieses Dokument fasst die Third-Party-Komponenten zusammen, die im InfoTerminal-Repository
über Source-Dependencies eingebunden werden. Die vollständige, maschinenlesbare Liste befindet
sich im Lizenzinventar unter `artifacts/compliance/licenses/license_inventory.csv`.

| Ökosystem | Beispiele | Lizenz |
| --- | --- | --- |
| Node.js (Frontend) | next 14.2.5, react 18.3.1, tailwindcss 4.1.13 | MIT / ISC / Apache-2.0 |
| Python (Backend) | fastapi 0.116.1, uvicorn 0.36.0, httpx 0.28.1 | MIT / BSD / Apache-2.0 |

**Hinweise:**

- Die SBOM-Dateien (`artifacts/sbom/source/*.cdx.json`) enthalten alle Komponenten mit Versionen
  im CycloneDX-Format und werden über `python scripts/generate_source_sbom.py` aktualisiert.
- Der CI-Check `python scripts/check_sbom_source_integrity.py` stellt sicher, dass SBOMs und
  Lizenzinventar vorhanden und nicht leer sind.
- Für Abhängigkeiten ohne veröffentlichte Lizenzangaben (`anyio`, `pytest-asyncio`) ist das Feld
  im Inventar als `UNKNOWN` markiert. Diese Pakete werden separat im Compliance-Backlog verfolgt.
