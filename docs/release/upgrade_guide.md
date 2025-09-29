# InfoTerminal Upgrade Guide (v0.2 → v1.0)

This guide documents the supported path to upgrade an InfoTerminal deployment from **version 0.2** to **version 1.0**. Follow every step in order. Each section lists the expected inputs, required flags, and verification commands. The accompanying demo script located at `artifacts/upgrade/v02_to_v10_demo.sh` provides a synthetic end-to-end walk-through that can be adapted for real environments.

---

## Audience & Scope
- **Audience:** Platform engineers and operators responsible for on-prem or cloud deployments.
- **Scope:** Application services (`gateway`, `search-api`, `graph-api`, `doc-entities`, `graph-views`), supporting data stores (PostgreSQL, Neo4j, OpenSearch, MinIO object storage), and the observability stack (Prometheus, Grafana, Loki, Tempo).
- **Out of scope:** Helm chart packaging and Flowise tooling (covered in their own upgrade notes).

> ℹ️ **Downtime expectations:** Plan for a rolling maintenance window of 30–45 minutes. The gateway can remain available if blue/green deployment is supported; otherwise expect a 15 minute outage while migrations complete.

---

## Quick Reference Checklist

| Phase | Description | Key Commands |
| --- | --- | --- |
| 0 | Pre-flight validation | `make upgrade-precheck` |
| 1 | Back up data & configs | `make upgrade-backup` |
| 2 | Enable v1.0 feature flags | `./deploy/set_flag.sh --release v1.0 --enable` |
| 3 | Run schema migrations | `make db-migrate` |
| 4 | Upgrade services | `docker compose -f docker-compose.prod.yml up -d --build` |
| 5 | Validate post-upgrade health | `./scripts/healthcheck.sh --targets all` |
| 6 | Execute smoke tests | `make smoke` |

The `make` targets reference shared automation added for v1.0. Adjust paths if your deployment uses custom tooling.

---

## 0. Pre-flight Validation
1. **Freeze automation**: Pause CI/CD jobs that auto-deploy `main`.
2. **Confirm versions**:
   - `git fetch && git checkout tags/v1.0.0`
   - `cat VERSION` (should read `1.0.0`).
3. **Check dependencies**:
   - Docker Engine ≥ 24.0, Compose V2.
   - Python 3.10+ for admin scripts.
   - Helm 3.12+ (if using Kubernetes).
4. **Run validation target**:
   ```bash
   make upgrade-precheck
   ```
   The target runs static config validation, checks for deprecated environment keys, and ensures that all required secrets are present. Resolve any failures before proceeding.

---

## 1. Back Up Critical Data
Perform backups immediately before applying migrations.

### 1.1 PostgreSQL (application metadata)
```bash
./scripts/backup/postgres.sh \
  --database infoterminal \
  --output /backups/infoterminal-postgres-v0_2.sql.gz \
  --verify
```
- Stores schema + data with checksum verification.
- Set `DRY_RUN=1` to preview commands without executing.

### 1.2 Neo4j (graph store)
```bash
./scripts/backup/neo4j.sh \
  --edition enterprise \
  --output /backups/neo4j-v0_2.dump \
  --quiesce-cluster
```
- Requires enterprise backup privileges.
- Confirm `dbms.backup.enabled=true` in `neo4j.conf`.

### 1.3 OpenSearch (document index)
```bash
./scripts/backup/opensearch_snapshot.sh \
  --repo infoterminal-upgrade \
  --snapshot pre-v1_0 \
  --region local
```
- Ensure repository path has read/write access for the OpenSearch nodes.

### 1.4 MinIO Object Storage
```bash
mc mirror --overwrite minio/infoterminal /backups/minio-pre-v1_0
```

> ✅ **Verification:** List all artifacts in `/backups` and confirm timestamps before continuing.

---

## 2. Enable v1.0 Feature Flags
Version 1.0 introduces capability toggles to stage new functionality safely.

| Flag | Target Service | Default | Action |
| --- | --- | --- | --- |
| `DOC_ENTITY_V1` | `doc-entities` | `false` | Set to `true` once migrations succeed. |
| `GRAPH_ALGO_V1` | `graph-api` | `false` | Enable to expose Louvain/community APIs. |
| `GATEWAY_OIDC_ENFORCE` | `gateway` | `false` | Turn on after validating IdP connectivity. |
| `OBS_ENRICH_TRACES` | `observability` | `false` | Enable after Tempo schema upgrade. |

Apply flags using the bundled helper script:
```bash
./deploy/set_flag.sh --flag DOC_ENTITY_V1 --value true --release v1.0
```
The script writes to Consul/etcd (depending on your configuration) and restarts services if `--apply` is passed. Always begin with `--dry-run` to preview changes.

---

## 3. Run Database & Index Migrations
Execute the migrations in the listed order to maintain referential integrity.

1. **PostgreSQL**
   ```bash
   make db-migrate scope=postgres target=v1_0
   ```
   - Adds dossier templates table.
   - Normalizes audit log timestamps to UTC.
2. **Neo4j**
   ```bash
   make db-migrate scope=neo4j target=v1_0
   ```
   - Introduces `COMMUNITY` relationship labels.
   - Recomputes node centrality scores.
3. **OpenSearch**
   ```bash
   make db-migrate scope=opensearch target=v1_0
   ```
   - Recreates document embeddings index with cosine similarity.

> ⚠️ **Important:** Each migration step is idempotent. Re-running will skip completed changes based on migration logs stored in the respective databases.

After migrations finish, re-run `make upgrade-precheck` to confirm no pending operations remain.

---

## 4. Upgrade Application Services
1. Update configuration overlays:
   ```bash
   cp deploy/overlays/v1.0/*.yaml deploy/current/
   git diff deploy/current
   ```
2. Apply container updates:
   ```bash
   docker compose -f docker-compose.prod.yml pull
   docker compose -f docker-compose.prod.yml up -d --build
   ```
3. Monitor startup logs for each service:
   ```bash
   docker compose logs -f gateway search-api graph-api doc-entities
   ```
4. For Kubernetes deployments, use the Helm chart:
   ```bash
   helm upgrade infoterminal charts/infoterminal \
     --values deploy/overlays/v1.0/values.yaml \
     --install --wait
   ```

---

## 5. Post-Upgrade Validation
1. **Health checks**
   ```bash
   ./scripts/healthcheck.sh --targets gateway,graph-api,search-api,doc-entities
   ```
2. **Data verification**
   - Confirm new dossier templates appear in the UI.
   - Run `GET /graph/communities` and expect HTTP 200 with `louvain` metadata.
   - Execute `POST /doc-entities/summarize` and confirm `model_version: "1.0"`.
3. **Observability**
   - Check Grafana dashboards for new panels `v1.0 - Graph Algorithms`.
   - Ensure Loki ingests structured JSON logs with `trace_id` field.
4. **Smoke tests**
   ```bash
   make smoke
   ```

Document all results in your change management ticket.

---

## 6. Rollback & Recovery Plan
- **If migrations fail**: Restore from backups in reverse order (OpenSearch → Neo4j → PostgreSQL) using the corresponding restore scripts with the `--restore` flag.
- **If services fail post-upgrade**: Re-deploy the v0.2 compose bundle or Helm release and toggle feature flags back to `false`.
- **Audit**: Capture logs from failing pods/containers and attach them to the incident report.

---

## Appendix A. Demo Script
Run the synthetic upgrade to verify tooling and operator familiarity:
```bash
bash artifacts/upgrade/v02_to_v10_demo.sh \
  --workspace /tmp/infoterminal-upgrade-demo \
  --dry-run
```
The script provisions a mock v0.2 dataset, executes mock migrations, and produces a v1.0 artifact folder. Inspect the generated report at `artifacts/upgrade/report.md` for a summary of operations.

