# Ops Controller

FastAPI-Service zur Steuerung erlaubter Docker-Compose-Stacks.

## Endpoints
- `GET /ops/stacks` – Liste erlaubter Stacks aus `infra/ops/stacks.yaml`
- `GET /ops/stacks/{name}/status`
- `POST /ops/stacks/{name}/up|down|restart`
- `POST /ops/stacks/{name}/scale?service=x&replicas=n`
- `GET /ops/stacks/{name}/logs`

## Sicherheit
- Aktivierung über `IT_OPS_ENABLE=1`
- RBAC per `X-Roles` Header (`admin|ops`)
- Keine Shell-Ausführung, nur whitelisted Compose-Dateien
- Docker-Socket wird benötigt; nur in vertrauenswürdigen Umgebungen nutzen

## Audit
Alle Mutationen und Log-Aufrufe werden mit `_shared.audit.audit_log` protokolliert.
