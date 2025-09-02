from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

with DAG(
    dag_id="openbb_kpo_daily",
    schedule="15 4 * * 1-5",
    start_date=datetime(2025, 9, 1),
    catchup=False,
    default_args={"retries": 1, "retry_delay": timedelta(minutes=10)},
    tags=["openbb","kpo"]
) as dag:

    run_connector = KubernetesPodOperator(
        task_id="run_openbb_connector",
        name="openbb-connector",
        namespace="openbb",
        image="openbb-connector:local",
        image_pull_policy="IfNotPresent",
        env_vars={
            "PG_HOST": "postgres-postgresql.data.svc.cluster.local",
            "PG_PORT": "5432",
            "PG_DB": "infoterminal",
            "PG_USER": "app",
            "PG_PASS": "app",
            "OPENBB_SYMBOLS": "AAPL,MSFT,SAP.DE,NVDA"
        },
        get_logs=True,
        is_delete_operator_pod=True,
    )
