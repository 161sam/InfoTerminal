from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
try:
    from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
except Exception:  # pragma: no cover
    KubernetesPodOperator = None
import os, requests


def notify_failure(context):
    hook = os.getenv("AIRFLOW_ALERT_WEBHOOK")
    if not hook:
        return
    try:
        requests.post(hook, json={"text": f"DAG {context['dag'].dag_id} failed at {context['ts']}"}, timeout=10)
    except Exception as exc:
        print("alert warn:", exc)

default_args = {
    "owner": "data-eng",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
    "on_failure_callback": notify_failure,
}

SCHEDULE = "0 3 * * *"  # täglich 03:00
DBT_DIR = os.getenv("DBT_DIR", "/opt/airflow/etl/dbt")
SUPERSET_URL = os.getenv("SUPERSET_URL", "http://superset.default.svc:8088")
SUPERSET_TOKEN = os.getenv("SUPERSET_TOKEN", None)  # via Airflow Conn/Var

def superset_refresh():
    # Beispiel: Warmup Charts & Refresh Datasets via REST (vereinfacht, nicht auth-hart)
    headers = {"Authorization": f"Bearer {SUPERSET_TOKEN}"} if SUPERSET_TOKEN else {}
    try:
        requests.get(f"{SUPERSET_URL}/api/v1/cached_keys/", headers=headers, timeout=30)
    except Exception as e:
        print("Superset refresh warn:", e)

with DAG(
    dag_id="openbb_dbt_superset",
    default_args=default_args,
    schedule=SCHEDULE,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["etl","openbb","dbt","superset"],
) as dag:

    openbb_extract = BashOperator(
        task_id="openbb_extract",
        bash_command="python /opt/airflow/etl/openbb/run_openbb_pull.py --symbols SPY,AAPL,BTC-USD --out /opt/airflow/data/openbb/{{ ds }}/",
        env={"OPENBB_API_KEY": "{{ var.value.OPENBB_API_KEY | default('') }}"},
    )

    if KubernetesPodOperator and os.getenv("DBT_USE_K8S"):
        dbt_build = KubernetesPodOperator(
            task_id="dbt_build",
            name="dbt-build",
            namespace=os.getenv("DBT_K8S_NAMESPACE", "default"),
            image=os.getenv("DBT_IMAGE", "ghcr.io/dbt-labs/dbt-postgres:latest"),
            cmds=["dbt"],
            arguments=["deps", "&&", "dbt", "seed", "--full-refresh", "&&", "dbt", "run", "&&", "dbt", "test"],
            env_vars={"DBT_PROFILES_DIR": DBT_DIR, "DBT_TARGET": "{{ var.value.DBT_TARGET | default('dev') }}"},
            get_logs=True,
            is_delete_operator_pod=True,
        )
    else:
        dbt_build = BashOperator(
            task_id="dbt_build",
            cwd=DBT_DIR,
            bash_command="dbt deps && dbt seed --full-refresh && dbt run && dbt test",
            env={
                "DBT_PROFILES_DIR": DBT_DIR,
                "DBT_TARGET": "{{ var.value.DBT_TARGET | default('dev') }}",
            },
        )

    superset_sync = PythonOperator(
        task_id="superset_sync",
        python_callable=superset_refresh,
    )

    openbb_extract >> dbt_build >> superset_sync
