from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime , date
import subprocess
import sys
import os

# etl scriptinin yolu
etl_script = "/Users/fatmanurbursa/Desktop/etl_main.py"


def run_etl():
    """localdeki etl scriptini tetikliyoruz."""
    result = subprocess.run([sys.executable, etl_script], capture_output=True, text=True)

    print(result.stdout)
    print(result.stderr)


default_args = {
    "owner": "fatmanur",
    "start_date": datetime(2025, 1, 1)
}

with DAG(
    dag_id="cloud_incremental_dag",
    default_args=default_args,
    schedule_interval="0 8 * * *",
    catchup=False
) as dag:
    run_cloud_etl = PythonOperator(
        task_id="run_cloud_etl",
        python_callable=run_etl
    )

run_cloud_etl
