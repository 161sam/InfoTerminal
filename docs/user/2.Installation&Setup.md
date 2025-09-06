# 2. Installation & Setup

## 2.1 Systemvoraussetzungen

Um **InfoTerminal** nutzen zu können, wird eine moderne Umgebung benötigt:

* **Betriebssystem**: Linux (Ubuntu 22.04/24.04 empfohlen), macOS oder Windows 11
* **Prozessor**: 4+ Kerne (x86\_64 oder ARM64)
* **RAM**: mindestens 8 GB (16 GB empfohlen)
* **Speicherplatz**: ca. 10 GB für Basis-Setup
* **Software**:

  * [Docker & Docker Compose](https://docs.docker.com/get-docker/)
  * [Python 3.10+](https://www.python.org/downloads/)
  * [pipx](https://pipx.pypa.io/stable/installation/) (für CLI)
  * [Node.js 20+](https://nodejs.org/en) (falls Frontend lokal entwickelt wird)

---

## 2.2 Installation der CLI

Die **CLI** ist das zentrale Werkzeug, um InfoTerminal zu starten und zu verwalten.

```bash
pipx install infoterminal-cli
```

Anschließend prüfen:

```bash
it --version
```

Beispielausgabe:

```
InfoTerminal CLI v0.2.0
```

---

## 2.3 Schnellstart

InfoTerminal unterstützt **zwei Betriebsmodi**:

### A) Lokaler Entwicklungsmodus (empfohlen für Entwickler)

* Startet Frontend und APIs direkt (Next.js + FastAPI im Reload-Modus)
* Datenbanken & Such-Engine laufen in Docker-Containern

```bash
scripts/dev_up.sh
```

Die Dienste laufen danach auf folgenden Ports:

| Service            | Port |
| ------------------ | ---- |
| Frontend (Next.js) | 3411 |
| Search API         | 8401 |
| Graph API          | 8402 |
| Graph Views        | 8403 |
| Gateway            | 8610 |
| Flowise Connector  | 3417 |

👉 Zugriff auf das Frontend: [http://localhost:3411](http://localhost:3411)

---

### B) Vollständig Dockerisierte Umgebung (empfohlen für Tests & Deployments)

* Alle Services laufen als Container
* Ports und Umgebungsvariablen werden automatisch gesetzt

```bash
docker compose up -d
```

Wichtig: Für Observability-Tools kann das Profil `observability` aktiviert werden:

```bash
docker compose --profile observability up -d
```

---

## 2.4 Port- und Umgebungsvariablen

Damit es **keine Port-Konflikte** gibt, verwendet InfoTerminal **keine Standard-Ports**.
Alle Zuordnungen sind in `.env.dev.ports` dokumentiert und werden von `scripts/patch_ports.sh` gepflegt.

**Beispiel-Variablen (.env.local):**

```env
FRONTEND_PORT=3411
SEARCH_API_PORT=8401
GRAPH_API_PORT=8402
VIEWS_PORT=8403
GATEWAY_PORT=8610
FLOWISE_CONNECTOR_PORT=3417
```

---

## 2.5 Troubleshooting

* **Frontend startet nicht?**
  Prüfe, ob `node -v` mindestens Version 20 anzeigt.
* **Neo4j-Fehler beim Login?**
  Lokales Dev-Password ist:

  ```
  user: neo4j
  pass: test12345
  ```
* **Port-Konflikte?**
  Nutze:

  ```bash
  scripts/patch_ports.sh
  ```

  um alle Ports konsistent neu zu setzen.
* **CLI funktioniert nicht?**
  Prüfe, ob `pipx` im PATH ist:

  ```bash
  pipx ensurepath
  ```

---
