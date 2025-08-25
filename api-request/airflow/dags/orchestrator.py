from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import sys

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
    schedule = timedelta(minutes=1)
)

def example_task():
    print('Example airflow task')

with dag:
    task1 = PythonOperator(
        task_id = 'task 1',
        python_callable = safe_main_callable
    )