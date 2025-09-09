# 7. CLI-Handbuch

Die **InfoTerminal CLI** (`infoterminal-cli`, Kurzform: `it`) ist das zentrale Werkzeug zur Steuerung, Analyse und Automatisierung.
Sie kann parallel zum Frontend genutzt werden oder eigenständig in Skripten und Automationen.

---

## 7.1 Installation

Die CLI wird über **pipx** installiert:

```bash
pipx install infoterminal-cli
```

Überprüfung der Installation:

```bash
it --version
```

Ausgabe (Beispiel):

```
InfoTerminal CLI v0.2.0
```

---

## 7.2 Grundbefehle

Diese Befehle steuern die gesamte Plattform:

| Befehl       | Beschreibung                                                                       |
| ------------ | ---------------------------------------------------------------------------------- |
| `it start`   | Startet InfoTerminal (lokal oder Docker)                                           |
| `it stop`    | Stoppt alle laufenden Dienste                                                      |
| `it restart` | Führt `docker compose restart` aus                                                 |
| `it rm`      | Entfernt Container & verwaiste Ressourcen (`docker compose down --remove-orphans`) |
| `it status`  | Zeigt den aktuellen Status aller Dienste an                                        |
| `it logs`    | Zeigt Logs aller Dienste (optional: `--service`)                                   |

👉 Diese Kommandos ersetzen komplexe `docker compose`-Befehle.

---

## 7.3 Suchfunktionen

Mit der CLI lassen sich Suchabfragen direkt ausführen.

**Beispiel: Volltextsuche**

```bash
it search.query "Beispiel AG"
```

**Optionen**:

- `--limit 20` – Anzahl der Ergebnisse begrenzen
- `--format json` – Ausgabeformat ändern

---

## 7.4 Graph-Funktionen

Die CLI unterstützt direkte Graph-Abfragen.

**Ping-Test**

```bash
it graph.ping
```

**Cypher-Abfrage**

```bash
it graph.cypher "MATCH (n:Person) RETURN count(n)"
```

**Nachbarschaften**

```bash
it graph.neighbors "Beispiel AG"
```

---

## 7.5 Views & KPIs

Für strukturierte Abfragen (z. B. aus Postgres-Views oder aggregierten Kennzahlen):

**SQL-ähnliche Query**

```bash
it views.query "SELECT * FROM org_overview LIMIT 10"
```

**KPIs abrufen**

```bash
it analytics.kpis --format table
```

---

## 7.6 Einstellungen anzeigen

Systemkonfiguration prüfen:

```bash
it settings.show
```

Beispielausgabe:

```yaml
frontend_url: http://localhost:3411
search_api: http://localhost:8401
graph_api: http://localhost:8402
views_api: http://localhost:8403
```

---

## 7.7 UI starten

Das Frontend lässt sich auch direkt aus der CLI starten:

```bash
it ui.run
```

---

## 7.8 Ausgabeformate

Alle Befehle können Ergebnisse in unterschiedlichen Formaten ausgeben:

- **Tabelle** (Standard)
- **JSON** – maschinenlesbar
- **YAML** – lesbar & konfigurationsnah
- **Text** – für einfache Shell-Pipes

**Beispiel:**

```bash
it search.query "Beispiel AG" --format json
```

---

## 7.9 Best Practices

- Nutze `it status` regelmäßig, um die Gesundheit der Services zu prüfen
- Mit `it logs --service search-api` gezielt nur ein Service debuggen
- Automatisiere mit Pipes:

  ```bash
  it search.query "Cyber Angriff" --format json | jq .
  ```

---
