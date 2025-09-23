# InfoTerminal Plugin Benutzerhandbuch

## 1. Einstieg
- Öffne **Plugins** in der Navigation, um alle verfügbaren Integrationen zu sehen. Jede Karte zeigt Name, Anbieter, Version, Kategorie und den aktuellen Gesundheitszustand.
- Nutze Suchfeld oder Kategorienschalter, um die Liste einzugrenzen. Der Zähler oberhalb des Rasters zeigt, wie viele Plugins zu deinen Filtern passen.
- Die Ansicht kombiniert deine persönlichen Einstellungen mit unternehmensweiten Defaults. Globale Umschalter von Administrator:innen werden daher eventuell bereits angewendet.

## 2. Plugins aktivieren
1. Wähle die gewünschte Plugin-Karte aus.
2. Entscheide zwischen **User** (persönlich) oder – mit Admin-Rechten – **Global** im Scope-Auswahlfeld.
3. Betätige den Toggle. Während des Speicherns erscheint ein Spinner. Fehlende Admin-Rechte beim globalen Scope werden mit einer Fehlermeldung erklärt.
4. Aktivierte Plugins stehen sofort in den Modulen zur Verfügung, die sie nutzen (z. B. Investigations, Dashboards, Automationen).

## 3. Plugins konfigurieren
- Über **Configure** auf der Karte passt du nicht sensible Optionen an, etwa Standardparameter oder Anzeigepräferenzen. Globale Defaults und persönliche Overrides werden zusammengeführt; speichere deshalb nur Werte, die für dich abweichen.
- Geheimnisse (API-Keys, Passwörter, Tokens) sind bewusst blockiert. Hinterlege sie in der Umgebung oder im Secrets-Manager; das System verwendet sie automatisch beim Verbinden.
- Änderungen lassen sich pro Benutzer oder – für Admins – global speichern. Ein Bestätigungs-Toast meldet den erfolgreichen Abschluss.

## 4. Gesundheit überwachen
- Das Badge rechts oben zeigt den aktuellen Status: **up** (grün), **degraded** (gelb), **down** (rot) oder **unknown** (grau).
- Verwende das Refresh-Symbol auf der Karte oder **Refresh** in der Toolbar, um den Check erneut auszulösen. Latenz und Zeitstempel erscheinen in der Plugin-Detailansicht.
- Das Panel **Health Overview** fasst die Anzahl pro Status zusammen, damit du priorisieren kannst.

## 5. Tools ausführen
- Viele Plugins stellen interaktive Tools bereit (z. B. „workflow.investigate_person“ für n8n oder „agent.chat“ für Flowise). Mit **Quick Test** führst du das Standardszenario aus und prüfst die Erreichbarkeit.
- Workflows in anderen Modulen (Graph, Search, Dossier usw.) leiten Tool-Aufrufe automatisch durch das Plugin-System. Sobald ein Plugin aktiviert ist, erscheinen die Funktionen kontextabhängig.
- Schlägt ein Tool fehl, wird die Originalfehlermeldung des Providers angezeigt. So erkennst du falsche Parameter oder fehlende Zugangsdaten.

## 6. Sammlungen verwalten
- Mit **Export** in der Toolbar lädst du die aktuelle Konfiguration als JSON herunter. Die Datei enthält Benutzer- und Globaleinstellungen für Audits oder Migrationen.
- Weitere Aktionen wie „Install Plugin“ oder „Bulk Enable“ stehen im Panel **Quick Actions** bereit, wenn Administrator:innen passende Pakete hinterlegen.

## 7. Troubleshooting
| Problem | Maßnahme |
|---------|----------|
| Plugin bleibt nach Umschalten deaktiviert | Prüfe, ob du den richtigen Scope bearbeitest; persönliche Overrides überschreiben globale Defaults. Öffne die Karte erneut, um den aktuellen Status zu sehen. |
| Gesundheitsstatus `unknown` | Manifest enthält keinen Health-Endpunkt oder der Provider ist offline. Aktualisiere und kontaktiere bei Bedarf die Administration. |
| Fehler `Forbidden` beim Tool-Aufruf | Eine Organisationsrichtlinie (OPA) blockiert den Zugriff. Bitte Admins um Prüfung der Regel. |
| Hinweis auf fehlende Secrets | Hinterlege benötigte Zugangsdaten in `.env` oder Vault; die UI verhindert aus Sicherheitsgründen das Speichern sensibler Werte. |

## 8. Best Practices
- Führe vor wichtigen Aufgaben einen Health-Refresh durch, um Verfügbarkeit zu bestätigen.
- Halte persönliche Overrides schlank, damit zentrale Wartung einfach bleibt.
- Stimme dich beim Export mit Administrator:innen ab, da Konfigurationsdateien umgebungsspezifische Details enthalten können.
- Melde unerwartete Tool-Antworten mit der angezeigten Request-ID; Support-Teams können sie im Audit-Log nachvollziehen.

## 9. Weiterführende Informationen
- Technischer Hintergrund: `docs/plugin/DEVELOPER.md`
- Port-Policy: `docs/PORTS_POLICY.md`
- Historische Referenz: `docs/LEGACY/dev/roadmap/v0.3-plus/master-todo.md`
