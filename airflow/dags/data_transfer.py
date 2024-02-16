from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.python import PythonOperator
from datetime import timedelta
import pandas as pd
from libs.python.controller.controller import Controller


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'email': ['fersrp1964@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'mysql_to_postgres_staging',
    default_args=default_args,
    description='Tranfers data from MySQL Database "currency_data" to Postgres Database "currency_data".'
)


def process():
    controller = Controller()
    controller.execution_process()

testing = PythonOperator(
    task_id='testing',
    python_callable=process,
    dag=dag,
)

testing