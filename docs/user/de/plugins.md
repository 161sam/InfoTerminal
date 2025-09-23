# Plugins verwalten

Die Seite **/plugins** zeigt registrierte Plugins (aus `plugins/*.yaml`). Für jedes Plugin:

- **Status**: Aktiviert pro Benutzer oder global (Rolle `admin`).
- **Beschreibung & Version**: Metadaten aus der Registry.
- **Konfiguration**: Formular für nicht-sensitive Parameter. Geheimnisse bleiben in `.env` oder Vaults.
- **Health**: API-Check gegen den Plugin-Runner (`/v1/plugins/health/<name>`). Warnhinweise erscheinen bei Fehlern.
- **Aktionen**: Starten (Job anlegen), Logs einsehen, Ergebnisse herunterladen.

Der Plugin-Runner führt Tools isoliert (Docker optional) aus und legt Resultate in `plugins/results` ab.
