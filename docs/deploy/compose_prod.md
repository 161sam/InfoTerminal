# Produktions-Compose-Stack

Diese Anleitung beschreibt den produktionsnahen Docker-Compose-Stack (`docker-compose.prod.yml`).
Der Stack fokussiert sich auf die Kern-APIs (Gateway, Search, Graph, Doc-Entities, Auth) plus die
benötigten Datenbanken. Alle Applikationscontainer verfügen über `/healthz`- und `/readyz`-Endpunkte,
und die Compose-Datei nutzt nur immutable Image-Digests.

## Voraussetzungen

- Docker Engine ≥ 24 mit `docker compose` Plugin
- Zugriff auf die Container Registry `ghcr.io/infoterminal`
- Port-Policy respektieren (z. B. Gateway 8610, Frontend 3411, Search 8611, Graph 8612)
- Optional: Datei `.env` zur Konfiguration der Secrets (z. B. `JWT_SECRET_KEY`, `NEO4J_PASSWORD`)

## Stack starten

```bash
# Images vorab laden (empfohlen für CI)
docker compose -f docker-compose.prod.yml pull

# Stack im Hintergrund starten
docker compose -f docker-compose.prod.yml up -d

# Übersicht der laufenden Services
docker compose -f docker-compose.prod.yml ps
```

Nach dem Start stehen die zentralen Endpunkte wie folgt bereit:

| Service       | URL (Host)                 | Readiness-Prüfung                            |
| ------------- | -------------------------- | -------------------------------------------- |
| Gateway       | http://localhost:8610      | `curl -fsS http://localhost:8610/readyz`     |
| Frontend      | http://localhost:3411      | `curl -fsS http://localhost:3411/api/health` |
| Search API    | http://localhost:8611      | `curl -fsS http://localhost:8611/readyz`     |
| Graph API     | http://localhost:8612      | `curl -fsS http://localhost:8612/readyz`     |
| Doc-Entities  | http://localhost:8613      | `curl -fsS http://localhost:8613/readyz`     |
| Auth-Service  | http://localhost:8616      | `curl -fsS http://localhost:8616/readyz`     |

Datenbanken (Postgres, Neo4j, OpenSearch) werden intern betrieben und sind per Healthcheck geschützt.

## Stack stoppen & aktualisieren

```bash
# Geordnet stoppen
docker compose -f docker-compose.prod.yml down

# Mit persistenten Volumes stoppen
docker compose -f docker-compose.prod.yml down --volumes

# Nach Image-Updates erneut deployen
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d --detach --force-recreate
```

## Immutable Image-Digests

Die folgenden Container werden mit beiden Tags (`v1.0-rc`, `v1.0`) ausgeliefert. Der Digest bleibt
identisch pro Tag-Version und erlaubt reproduzierbare Deployments.

| Service        | Image                                 | Tag           | Digest                                                              |
| -------------- | ------------------------------------- | ------------- | ------------------------------------------------------------------- |
| gateway        | `ghcr.io/infoterminal/gateway`        | `v1.0-rc`     | `sha256:3b8473d6eab71b3c70663bb5ad84fc4b755233f15f3f827938a7042640f0a0fd` |
| gateway        | `ghcr.io/infoterminal/gateway`        | `v1.0`        | `sha256:6f08e99775fa8fb90753c9709cbf3f1d1b9d20c92a4cf3b64db24edfcf3b8f40` |
| frontend       | `ghcr.io/infoterminal/frontend`       | `v1.0-rc`     | `sha256:5bcb63c3ef8a5c1e8a2b4f5a8e3339693d42be5bd7781c622f4ef5c31c8283f0` |
| frontend       | `ghcr.io/infoterminal/frontend`       | `v1.0`        | `sha256:b731de6d032ab2f1a745a72a5a585d1151a0d0b2686d7c9fbb0ad75461bfc3c1` |
| search-api     | `ghcr.io/infoterminal/search-api`     | `v1.0-rc`     | `sha256:57af0fa86d32db1dd9d8a1a68cf76d6e4e2915aa7618683d2f6b2a444ef98a33` |
| search-api     | `ghcr.io/infoterminal/search-api`     | `v1.0`        | `sha256:9c86a5fe9b0d9dba80a1e9c2ba4cfe65379b780a5ad54837b2548113610b8024` |
| graph-api      | `ghcr.io/infoterminal/graph-api`      | `v1.0-rc`     | `sha256:47d2396220b81df20bff7bcdadc982d08b85742f1ce31779042f2f1c0730bde5` |
| graph-api      | `ghcr.io/infoterminal/graph-api`      | `v1.0`        | `sha256:7b4e9b3097c55cbe7c7de79b0f1f6ab0b250f893b5bc21b2f75a386a68b018c9` |
| doc-entities   | `ghcr.io/infoterminal/doc-entities`   | `v1.0-rc`     | `sha256:16a6ed0e385bc0e1ebb8d65f4f704b9cda2ec3316f82a229f0e67285ba0f516d` |
| doc-entities   | `ghcr.io/infoterminal/doc-entities`   | `v1.0`        | `sha256:cc4a65f1cd6fb2e2bdb9e7fb0d25e705671c47e4d4cc2dc8b4457e4f15d66147` |
| auth-service   | `ghcr.io/infoterminal/auth-service`   | `v1.0-rc`     | `sha256:6c4dfcb4a590c3a218efdbadaeaf2dfabf341361af8489ad9d7816d52c44362a` |
| auth-service   | `ghcr.io/infoterminal/auth-service`   | `v1.0`        | `sha256:d2b4a8cf9f74b4fd3f019ed592df3fe6e6ccdd0bb3e6132f2b1c7e1a9c2bc6c8` |

Für abhängige Datenbanken werden ebenfalls feste Versionen mit Digest genutzt:

- `opensearchproject/opensearch:2.11.1@sha256:cbca8e35fb333af938289ac0f370abdcbde46dbe7629acc1af0cd4219da85b62`
- `neo4j:5.18.0@sha256:b018c04b0d01e7b6b3ff001d297fe2b80d0612a49516a7d20b0beb7f784994bb`
- `postgres:16.2@sha256:4aea012537edfad80f98d870a36e6b90b4c09b27be7f4b4759d72db863baeebb`

## CI-Build für den Prod-Stack

Der CI-Job **Compose (Prod)** validiert die Datei `docker-compose.prod.yml` bei jedem Commit/PR:

- `docker compose -f docker-compose.prod.yml config` prüft die Syntax.
- `docker compose -f docker-compose.prod.yml config --services` stellt sicher, dass alle Services
  korrekt aufgelistet sind.
- Job schlägt fehl, wenn Healthchecks/Volumes nicht korrekt definiert sind (Parsing-Fehler).

Damit ist gewährleistet, dass der Prod-Compose-Stack fehlerfrei bleibt.
