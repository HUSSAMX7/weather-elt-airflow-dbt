from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

from insert_records import main


default_args = {
    'description': 'A DAG to orchestrate data',
    'start_date': datetime(2025, 4, 30),
    'catchup': False,
}

dag = DAG(
    dag_id='weather-api-dbt-orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=2),
)

with dag:
    task1 = PythonOperator(
        task_id='ingest_data_task',
        python_callable=main,
    )

    task2 = BashOperator(
        task_id='transform_data_task',
        bash_command=(
            'python -m dbt.cli.main run '
            '--project-dir /opt/airflow/dbt '
            '--profiles-dir /opt/airflow/dbt '
            '--log-path /tmp/dbt_logs '
            '--target-path /tmp/dbt_target'
        ),
    )

    task1 >> task2
