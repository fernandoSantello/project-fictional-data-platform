from datetime import timedelta
from airflow.utils.dates import days_ago
from libs.python.controller.controller import Controller
from airflow.decorators import dag, task


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'email': ['fersrp1964@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}


@dag(default_args=default_args, schedule_interval=None, start_date=days_ago(0))
def taskflow_api_etl():


    @task()
    def extract_data():
        controller = Controller()
        controller.sync_currency_data()
        return True
    

    @task()
    def transform_data(step):
        controller = Controller()
        insert_currency_table, insert_rate_table, insert_process_fail_table = controller.gather_table_data()
        tables = {
            'insert_currency_table': insert_currency_table,
            'insert_rate_table': insert_rate_table,
            'insert_process_fail_table': insert_process_fail_table
        }
        return tables
    

    @task()
    def load_data(tables):
        controller = Controller()
        controller.insert_into_postgres(tables['insert_currency_table'], tables['insert_rate_table'], tables['insert_process_fail_table'])

    step_1 = extract_data()
    tables = transform_data(step=step_1)
    load_data(tables=tables)


etl_dag = taskflow_api_etl()
