# ETL Automation Runbook

## NiFi

* Configure Parameter Context with values from `etl/nifi/params/aleph_ingest.env.example`.
* Import template via `make etl-nifi-deploy` and bind the Parameter Context.
* Start controller services then processors.
* Successful files move to `$NIFI_SUCCESS_DIR`, failures to `$NIFI_FAILURE_DIR` (DLQ).
* Monitor bulletins or use `etl/nifi/scripts/bulletin_webhook.sh` for webhook alerts.

## Airflow

* Bootstrap variables and connections using `etl/airflow/scripts/bootstrap_airflow.sh`.
* DAG `openbb_dbt_superset` extracts data, runs dbt, then refreshes Superset.
* Trigger manually with `airflow dags trigger openbb_dbt_superset`.
* Retries configured; failures call `AIRFLOW_ALERT_WEBHOOK` if set.

## dbt

* Configure profiles using `etl/dbt/profiles.example.yml` as reference.
* Run builds via `make etl-dbt-build` or from Airflow.
* Common issues: missing profiles, target schema permissions.

## Superset

* Set `SUPERSET_URL` and optional `SUPERSET_TOKEN`.
* Warm caches with `make etl-superset-warmup`.

## Troubleshooting

* Aleph HTTP errors: check API key and network.
* Rate limits or large CSVs may slow runs; adjust batch sizes.
* For Airflow task logs, check the web UI or scheduler logs.
