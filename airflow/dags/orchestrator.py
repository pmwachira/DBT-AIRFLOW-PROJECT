from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import sys
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

sys.path.append('/opt/airflow/api-request')

default_args = {
    'description':'first dag',
    'start_date': datetime(2025,8,15),
    'catch-up': False
}

def safe_main_callable():
    from store_to_db import main
    return main()

dag = DAG(
    dag_id='weather_api_orchestrator',
    default_args = default_args,
    schedule = timedelta(minutes=5)
)

def example_task():
    print('Example airflow task')

with dag:
    task_ingest = PythonOperator(
        task_id = 'task_ingest',
        python_callable = safe_main_callable
    )

    dbt_task = DockerOperator(
        task_id = 'dbt_task',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run',
        working_dir='/usr/app',
        mounts=[
            Mount(
                source='/Users/MAC/Desktop/dbt-airflow-project/dbt/myproject',
                target='/usr/app',
                type='bind'
            ),
            Mount(
                source='/Users/MAC/Desktop/dbt-airflow-project/dbt/profiles.yml',
                target='/root/.dbt/profiles.yml',
                type='bind'
            )
        ],
        network_mode='dbt-airflow-project_my-network',
        docker_url='unix://var/run/docker.sock',
        mount_tmp_dir=True,  # ensures Airflow creates a known /tmp folder
        tmp_dir="/tmp/airflowtmp",  # inside the container
        auto_remove='success'
    )

    task_ingest >> dbt_task