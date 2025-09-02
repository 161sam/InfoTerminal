from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

DEFAULTS = {"retries": 1, "retry_delay": timedelta(minutes=5)}

with DAG(
    "openbb_to_dashboard",
    schedule="30 4 * * 1-5",
    start_date=datetime(2025, 9, 1),
    catchup=False,
    default_args=DEFAULTS,
    tags=["openbb","dbt","superset"],
) as dag:

    openbb = KubernetesPodOperator(
        task_id="openbb_connector",
        name="openbb-connector",
        namespace="openbb",
        image="openbb-connector:local",
        image_pull_policy="IfNotPresent",
        env_vars={
            "PG_HOST":"postgres-postgresql.data.svc.cluster.local",
            "PG_PORT":"5432","PG_DB":"infoterminal","PG_USER":"app","PG_PASS":"app",
            "OPENBB_SYMBOLS":"AAPL,MSFT,SAP.DE,NVDA"
        },
        get_logs=True, is_delete_operator_pod=True,
    )

    dbt = KubernetesPodOperator(
        task_id="dbt_run_test",
        name="dbt",
        namespace="workflow",
        image="ghcr.io/dbt-labs/dbt-core:1.7.10",
        cmds=["/bin/bash","-lc"],
        arguments=[
            "mkdir -p /root/.dbt && echo 'profiles-dir: /workspace' >/tmp/n && "
            "dbt deps --project-dir /workspace/etl/dbt && "
            "dbt seed --project-dir /workspace/etl/dbt && "
            "dbt run --project-dir /workspace/etl/dbt --select tag:openbb && "
            "dbt test --project-dir /workspace/etl/dbt"
        ],
        env_vars={
            "DBT_PROFILES_DIR":"/workspace/etl/dbt",
            "DBT_TARGET":"dev",
            "DBT_USER":"app","DBT_PASS":"app","DBT_HOST":"postgres-postgresql.data.svc.cluster.local",
            "DBT_DB":"infoterminal","DBT_PORT":"5432"
        },
        volume_mounts=[{"name":"repo","mountPath":"/workspace"}],
        volumes=[{"name":"repo","hostPath":{"path":"/workspace"}}],  # in dev: mount lokalen Repo-Pfad ins Worker-Node!
        get_logs=True, is_delete_operator_pod=True,
    )

    sync = KubernetesPodOperator(
        task_id="superset_sync",
        name="superset-sync",
        namespace="analytics",
        image="python:3.11-slim",
        cmds=["/bin/sh","-c"],
        arguments=[
            "pip install -q requests && python /work/superset_dbt_sync.py"
        ],
        env_vars={
            "SUPERSET_URL":"http://superset.analytics.svc.cluster.local:8088",
            "SUPERSET_USER":"admin","SUPERSET_PASS":"adminadmin",
            "PG_HOST":"postgres-postgresql.data.svc.cluster.local","PG_PORT":"5432",
            "PG_DB":"infoterminal","PG_USER":"app","PG_PASS":"app",
            "DBT_ARTIFACTS":"/work/dbt_artifacts"
        },
        volume_mounts=[{"name":"work","mountPath":"/work"}],
        volumes=[{"name":"work","configMap":{"name":"superset-dbt-sync-scripts"}}],
        get_logs=True, is_delete_operator_pod=True,
    )

    openbb >> dbt >> sync
