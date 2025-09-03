from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {"owner":"airflow","retries":0}
with DAG("openbb_equities_daily", start_date=datetime(2024,1,1),
         schedule="0 6 * * 1-5", catchup=False, default_args=default_args) as dag:
    t1 = BashOperator(task_id="fetch_prices", bash_command="echo TODO: openbb-connector")
    t2 = BashOperator(task_id="dbt_run", bash_command="echo TODO: dbt run")
    t1 >> t2
