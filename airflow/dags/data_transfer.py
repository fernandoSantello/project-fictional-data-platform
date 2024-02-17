from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from libs.python.controller.controller import Controller


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'email': ['fersrp1964@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


dag = DAG(
    'Currency_Data_Pipeline',
    default_args=default_args,
    description='Ongoing',
    schedule_interval=timedelta(minutes=5),
)


def etl_currency_info():
    controller = Controller()
    controller.execution_process()


testing = PythonOperator(
    task_id='etl_currency_info',
    python_callable=etl_currency_info,
    dag=dag,
)

testing