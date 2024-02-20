import os
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.decorators import dag, task
from dotenv import load_dotenv, find_dotenv
from libs.python.controller.controller import Controller
from libs.python.helper.coincap_api import CoincapAPI
from libs.python.services.coincap_api import CoincapConnection
from libs.python.helper.exchange_rate_api import ExchangeRateAPI
from libs.python.services.exchange_rate_api import ExchangeRateConnection
from libs.python.helper.mysql_db import DBMysql
from libs.python.services.mysql_db import MysqlDBConnection
from libs.python.helper.postgres_db import DBPostgres
from libs.python.services.postgress_db import PostgresDBConnection


load_dotenv(find_dotenv())


postgres_db = DBPostgres(conn_db=PostgresDBConnection(conn_param={
            'user': os.getenv('POSTGRES_PROD_USER'),
            'password': os.getenv('POSTGRES_PROD_PASSWORD'),
            'host': os.getenv('POSTGRES_PROD_HOST'),
            'database': os.getenv('POSTGRES_PROD_DATABASE'),
            'database_type': 'postgres'
        }))


mysql_db = DBMysql(conn_db=MysqlDBConnection(conn_param={
            'user': os.getenv('MYSQL_PROD_USER'),
            'password': os.getenv('MYSQL_PROD_PASSWORD'),
            'host': os.getenv('MYSQL_PROD_HOST'),
            'database': os.getenv('MYSQL_PROD_DATABASE'),
        }))


api_exchangerate = ExchangeRateAPI(conn_api=ExchangeRateConnection(conn_param={
            'url': os.getenv('EXCHANGERATE_API_URL'),
            'api_key': os.getenv('EXCHANGERATE_API_KEY')
        }))


api_coincap = CoincapAPI(conn_api=CoincapConnection(conn_param={
            'url': os.getenv('COINCAP_API_URL'),
            'api_key': os.getenv('COINCAP_API_KEY')
            }))


controller = Controller(api_coincap=api_coincap, api_exchangerate=api_exchangerate, mysql_db=mysql_db, postgres_db=postgres_db)


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'email': ['fersrp1964@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}


@dag(default_args=default_args, schedule_interval='0,30 * * * *', start_date=days_ago(0))
def taskflow_api_etl():


    @task()
    def extract_data():
        controller.sync_currency_data()
        return True
    

    @task()
    def transform_data(step):
        insert_currency_table, insert_rate_table, insert_process_fail_table = controller.gather_table_data()
        tables = {
            'insert_currency_table': insert_currency_table,
            'insert_rate_table': insert_rate_table,
            'insert_process_fail_table': insert_process_fail_table
        }
        return tables
    

    @task()
    def load_data(tables):
        controller.insert_into_postgres(tables['insert_currency_table'], tables['insert_rate_table'], tables['insert_process_fail_table'])

    step_1 = extract_data()
    tables = transform_data(step=step_1)
    load_data(tables=tables)


etl_dag = taskflow_api_etl()
