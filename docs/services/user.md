# InfoTerminal Services – Anwenderleitfaden

Dieser Leitfaden erklärt, welche Hintergrund-Services für die sichtbaren Funktionen in InfoTerminal verantwortlich sind. Ziel ist es, Anwender*innen einen Überblick zu geben, wo Inhalte herkommen, wie Ergebnisse erzeugt werden und welche Möglichkeiten bei Störungen oder besonderen Anforderungen bestehen.

## Service-Landkarte für Anwender*innen

| Bereich | Services | Was Sie sehen | Wichtige Hinweise |
| --- | --- | --- | --- |
| Suche & Discovery | `search-api`, `doc-entities` | Suchleiste, Trefferlisten, Entitäts-Hervorhebungen | Volltext (BM25) und semantische Reranks; Entitäten werden nach der Indexierung automatisch erkannt. |
| Graph & Beziehungen | `graph-api`, `graph-views`, `doc-entities` | Graph-Ansichten, Ego-Netze, Geo-Layer | Graph-Analysen (Degree, Betweenness, Communities) stehen in Dossiers und Graph-Widgets zur Verfügung. |
| Dossiers & Verifikation | `graph-views`, `verification`, `rag-api`, `forensics`, `media-forensics` | Dossier-Export, Verifikationsberichte, Beweisanhänge | Verifikation kombiniert Suche, Graph und Medienanalyse; Dossiers lassen sich als JSON/Markdown exportieren. |
| Assistent & Plugins | `agent-connector`, `plugin-runner`, `flowise-connector`, `websocket-manager` | Chat-Assistent, Plugin-Katalog, Live-Status | Plugins benötigen Freischaltung; Statusmeldungen erscheinen live im Chat (Websocket). |
| Zusammenarbeit & Feedback | `collab-hub`, `feedback-aggregator` | Aufgabenboards, Kommentare, Feedback-Dialog | Feedback landet zentral im Aggregator, Teamaufgaben erscheinen im Collaboration-Hub. |
| Sicherheit & Zugriff | `auth-service`, `gateway`, `egress-gateway`, `policy` | Login, Rollen, sichere Proxy-Routen | Gateway bündelt APIs unter `/api/*`, Auth-Service stellt Tokens bereit, Egress regelt geschützte externe Aufrufe. |
| Spezialanalysen & Datenfeeds | `xai`, `openbb-connector`, `performance-monitor`, `cache-manager` | Erklärbare KI, Kapitalmarkt-Daten, Performance-Hinweise | KI-Erklärungen erscheinen bei Modellergebnissen; Finanzdaten werden zyklisch aus OpenBB geladen. |

## Suche & Discovery

### search-api
- Liefert alle Suchergebnisse, Filter und Sortierungen im UI.
- Unterstützt sowohl klassische Volltextsuche als auch semantisches Reranking (automatisch, wenn aktiviert).
- Tipp: Für konsistente Ergebnisse immer denselben Mandantenkontext verwenden (siehe Einstellungen → Gateway Proxy).

### doc-entities
- Markiert Personen, Organisationen, Orte und weitere Entitäten in Dokumenten.
- UI zeigt Treffer als Tooltips oder Dossier-Bausteine an.
- Status „pending“ bei Verknüpfungen bedeutet, dass die Auflösung in den Wissensgraph noch aussteht.

## Graph & Beziehungen

### graph-api
- Versorgt alle Graph-Widgets, Pfad-Analysen und Zentralitätsmetriken im Dashboard.
- Unterstützt eigens definierte Sichten (z. B. Louvain-Communities) für Dossier-Lite.
- Bei Ladeproblemen prüfen Sie zuerst Neo4j im Infrastruktur-Status (`it status -s graph-api`).

### graph-views
- Baut Ego-Netze und Graph-Ausschnitte, die in Dossiers oder Exporten erscheinen.
- CSV-Demos (siehe `services/graph-views/README.md`) ermöglichen schnelle Tests mit Beispielpersonen.
- Schreibende Aktionen (Importe) benötigen `GV_ALLOW_WRITES=1` und ggf. Basic-Auth.

### Geodaten-Layer
- GeoJSON-Dateien werden über `graph-views` und Postgres verwaltet; Frontend rendert sie mit MapLibre/Leaflet.
- Für eigene Layer Dateien nach `data/geo` legen und den Dienst neu starten (`make smoke.gv.up`).

## Dossiers & Verifikation

### verification
- Generiert Verifikationsberichte, kombiniert Texte, Graph-Beziehungen und Medien.
- CLI-Kurzbefehle (`it verify claim.json`) nutzen dieselben Endpunkte.
- Bei langen Wartezeiten prüfen, ob `media-forensics` oder `doc-entities` verfügbar sind (Statusanzeige unten rechts im UI).

### rag-api
- Liefert juristische Hintergründe („Rechtskontext“) in Dossiers, z. B. welche Paragraphen für eine Firma relevant sind.
- Standardindex heißt `laws`; lässt sich über `/law/index` mit eigenen Gesetzestexten anreichern.

### forensics & media-forensics
- `forensics` verwaltet Beweispfade und sorgt dafür, dass Dateien unverändert bleiben (Chain of Custody).
- `media-forensics` sucht nach Bilddubletten und liest EXIF-Daten aus; Ergebnisse erscheinen in der Medien-Spalte des Verifikationsberichts.

## Assistent & Plugins

### agent-connector & plugin-runner
- Chat-Assistenten und Tools (z. B. OSINT-Plugins) werden hier registriert, konfiguriert und ausgeführt.
- Das Frontend fragt `/api/plugins/tools` über den Gateway ab; freigeschaltete Plugins erscheinen sofort im Plugin-Drawer.
- Fehlermeldungen wie „write disabled“ deuten auf fehlende Freigaben oder Richtlinien hin (siehe Administrator*in).

### flowise-connector
- Steuert komplexe Flowise-Workflows; Standardport 3417.
- Tokens & Verbindungsdaten werden in den Einstellungen hinterlegt (`NEXT_PUBLIC_FLOWISE_*`).
- Bei Timeout-Meldungen die Flowise-Instanz prüfen oder den Timeout in der `.env` anpassen (`FLOWISE_TIMEOUT_S`).

### websocket-manager
- Sorgt für Live-Updates (z. B. „Plugin fertig“, „Verifikation abgeschlossen“).
- Wenn Live-Meldungen fehlen, prüfen Sie Browser-Blocker oder Gateway-Einstellungen.

## Zusammenarbeit & Feedback

### collab-hub
- Bietet Aufgabenlisten, Boards und Team-Kommentare im Dashboard.
- Benachrichtigungen laufen über denselben Websocket-Kanal wie Plugin-Updates.
- Daten werden in Postgres gespeichert; Export ist über die API `/v1/tasks/export` (Beta) möglich.

### feedback-aggregator
- Sammelt Feedback aus dem UI (Menü → Feedback geben) und CLI.
- Normalisiert Rückmeldungen und leitet sie an das Ops-Team weiter.
- Transparenz: Der Status (offen, in Arbeit, erledigt) wird im Feedback-Modul angezeigt.

## Sicherheit & Zugriff

### auth-service
- Verwaltet Logins, Passwort-Reset, MFA und Rollen.
- Nutzer*innen können ihre Sitzungen und API-Keys unter Profil → Sicherheit einsehen.
- Bei Fehlermeldung „invalid token“ hilft meist ein erneuter Login; Sessions lassen sich im Backend beenden.

### gateway
- Bündelt alle APIs unter einer URL und sorgt für OIDC/OPA-Prüfungen.
- Das Frontend kann zwischen direkter Verbindung und Gateway-Proxy umschalten (Einstellungen → Gateway Proxy).
- Health-Endpoint (`/healthz`) zeigt den Zusammenschluss aller angebundenen Services.

### egress-gateway & policy
- Steuert sensible Ausleitungen (z. B. Darknet, TOR) und erzwingt Richtlinien.
- Falls ein Plugin keinen externen Call ausführen darf, erscheint im UI ein Audit-Hinweis mit Referenz-ID.

## Spezialanalysen & Datenfeeds

### xai
- Erzeugt Erklärungen für KI-Modelle (z. B. Warum wurde ein Dokument als relevant eingestuft?).
- Erklärungen sind im UI als Informations-Box oder Tooltip verfügbar.

### openbb-connector
- Lädt Börsen- und Unternehmensdaten aus OpenBB, die im Finanz-Dossier erscheinen.
- Läuft zyklisch; Status in den Systemlogs oder im Monitoring-Bereich prüfen.

### performance-monitor & cache-manager
- Optimieren Antwortzeiten (Caching) und sammeln Performance-Metriken.
- Anwender*innen sehen Hinweise im Monitoring-Dashboard, wenn Schwellen überschritten werden.

## Was tun bei Störungen?

1. **Status prüfen:** `it status -s search-api,graph-api` oder UI → Systeme → Dienste.
2. **Gateway-Modus wechseln:** Bei lokalen Setups kann ein Wechsel zwischen Direktzugriff und Gateway helfen.
3. **Logs einsehen:** `it logs --services <name> --lines 100` liefert die letzten Ereignisse (wenn Berechtigung vorhanden ist).
4. **Feedback geben:** Über den Feedback-Dialog Probleme melden – das Ops-Team erhält automatisch Dienst- und Versionsinfos.

## Weiterführende Dokumente

- `docs/user/4.Kernfunktionen.md` – Funktionsübersicht mit Screenshots
- `docs/runbooks/stack.md` – Schritt-für-Schritt-Anleitungen für Neustarts & Checks
- `docs/PORTS_POLICY.md` – Port-Übersicht für lokale Installationen
- `docs/API_INVENTORY_ENHANCED.md` – Detail-Endpoints für Power-User*innen

Mit diesem Leitfaden können Sie nachvollziehen, welcher Service welche Oberfläche speist, wie sich Funktionen zusammensetzen und welche Schritte bei Problemen helfen. Bewahren Sie die Übersicht auf dem neuesten Stand, wenn Dienste ausgebaut oder ersetzt werden.
