# Doc-Entities Database Migrations

This document tracks the zero-downtime migration flow for the `doc-entities`
service. The goal is to guarantee forward/backward compatibility, allow
rollbacks inside a compatibility window, and verify the behaviour with an
automated smoke test.

## Migration Layout

* Every migration lives in `services/doc-entities/migrations/NNN_name.py`.
* Each file exposes `revision`, `down_revision`, `description`, and the
  callable trio `upgrade(conn)`, `downgrade(conn)`, `backfill(conn)`.
* Migrations are purposely **linear** (`001 → 002 → 003 …`) to keep the
  upgrade/downgrade logic predictable.
* `backfill` is part of the expand/contract strategy: we deploy the schema,
  backfill new structures while both code versions can run, and only drop the
  compatibility artefacts after the rollout succeeds.

## Runner CLI

The CLI is implemented in `services/doc-entities/migrations/runner.py`. Run it
with plain Python:

```bash
python services/doc-entities/migrations/runner.py status
python services/doc-entities/migrations/runner.py upgrade --run-backfill
python services/doc-entities/migrations/runner.py downgrade --to 002
python services/doc-entities/migrations/runner.py backfill --revision head
```

The runner accepts either `--database-url` or the environment variables
`DOC_ENTITIES_DATABASE_URL` / `DATABASE_URL`. The version history is persisted in
`doc_entities_schema_migrations` with timestamps so we can audit when a step was
applied.

## Zero-Downtime Contract

* **Expand:** create schema changes in `upgrade` without breaking older code.
  The 003 migration, for example, captures relation rows into shadow tables
  before downgrade so that a rollback keeps the data safe.
* **Backfill:** populate new columns/tables in `backfill`. This can be invoked
  as part of the upgrade (`--run-backfill`) or separately once the system is in
  steady state.
* **Contract:** `downgrade` removes the schema additions while restoring any
  preserved data from the shadow tables. Running `upgrade` afterwards will
  detect the backup tables and restore the data losslessly.

## Smoke Test (Roundtrip)

`scripts/migrations_smoke.py` orchestrates an end-to-end test:

1. Provision a temporary SQLite database (or use `MIGRATIONS_SMOKE_DATABASE_URL`).
2. Run `upgrade --run-backfill` to head.
3. Seed a miniature dataset (documents, entities, relations + resolutions).
4. Downgrade to revision `002` and ensure base tables keep their data.
5. Upgrade to head again, restore the relation data, and remove the shadow
   tables.

The script exits with an error if any comparison fails, guaranteeing that an
`upgrade → downgrade → upgrade` roundtrip preserves the dataset.

## CI Gate

The GitHub workflow defines a `migrations_smoke` job that executes the smoke
script on every PR/push. This gate keeps migrations compatible with the zero-
downtime contract before changes land on `main`.
