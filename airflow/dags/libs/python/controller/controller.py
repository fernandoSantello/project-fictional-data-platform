from libs.python.helper.coincap_api import CoincapAPI
from libs.python.helper.exchange_rate_api import ExchangeRateAPI
from libs.python.helper.mysql_db import DBMysql
from libs.python.helper.postgres_db import DBPostgres
from libs.python.helper.data_operations import tuple_to_dataframe, concatenate_dataframes, filter_specific_rate, create_rate_column
from dotenv import load_dotenv
import os

class Controller:
    def __init__(self):
        load_dotenv()
        self.db_mysql = DBMysql(conn_param={
            'user': os.getenv('MYSQL_PROD_USER'),
            'password': os.getenv('MYSQL_PROD_PASSWORD'),
            'host': os.getenv('MYSQL_PROD_HOST'),
            'database': os.getenv('MYSQL_PROD_DATABASE'),
            'database_type': 'mysql'
        })
        self.db_postgres = DBPostgres(conn_param={
            'user': os.getenv('POSTGRES_PROD_USER'),
            'password': os.getenv('POSTGRES_PROD_PASSWORD'),
            'host': os.getenv('POSTGRES_PROD_HOST'),
            'database': os.getenv('POSTGRES_PROD_DATABASE'),
            'database_type': 'postgres'
        })
        self.api_coincap = CoincapAPI(conn_param={
            'url': os.getenv('COINCAP_API_URL'),
            'api_key': os.getenv('COINCAP_API_KEY')
        })
        self.api_exchangerate = ExchangeRateAPI(conn_param={
            'url': os.getenv('EXCHANGERATE_API_URL'),
            'api_key': os.getenv('EXCHANGERATE_API_KEY')
        })
        self.currencies = ['bitcoin', 'ethereum']


    def get_currency_mysql(self) -> list:
        postgres_last_id = self.db_postgres.get_lat_id_currency()
        rows = self.db_mysql.get_currency_table(postgres_last_id=postgres_last_id)
        return rows


    def get_rate_mysql(self) -> list:
        postgres_last_id = self.db_postgres.get_lat_id_rate()
        rows = self.db_mysql.get_rate_table(postgres_last_id=postgres_last_id)
        return rows
    

    def get_process_fail_mysql(self) -> list:
        postgres_last_id = self.db_postgres.get_lat_id_process_fail()
        rows = self.db_mysql.get_process_fail_table(postgres_last_id=postgres_last_id)
        return rows


    def concatenate_rate_column(self) -> dict:
        rates_data = self.api_exchangerate.get_rates()
        rate_table_mysql = self.get_rate_mysql()
        brl_rate = filter_specific_rate(data=rates_data, currency='brl')
        eur_rate = filter_specific_rate(data=rates_data, currency='eur')
        ratebrl_column = create_rate_column(new_column='rateBRL', value=brl_rate, rate_table_mysql=rate_table_mysql)
        rateeur_column = create_rate_column(new_column='rateEUR', value=eur_rate, rate_table_mysql=rate_table_mysql)
        current_rate_table = tuple_to_dataframe(self.get_rate_mysql())
        new_rate_table = concatenate_dataframes([current_rate_table, ratebrl_column, rateeur_column])
        return new_rate_table
    

    def sync_currency_data(self) -> None:
        for element in self.currencies:
            currency_data = self.api_coincap.get_rates(currency=element)
            curency_exists = self.db_mysql.check_currency(currency_data['id'])
            self.db_mysql.insert_rate(currency_data) if curency_exists else self.db_mysql.insert_currency(currency_data)


    def gather_table_data(self) -> dict:
        insert_currency_table = self.get_currency_mysql()
        insert_rate_table = self.concatenate_rate_column()
        insert_process_fail_table = self.get_process_fail_mysql()
        return insert_currency_table, insert_rate_table, insert_process_fail_table
    

    def insert_into_postgres(self, insert_currency_table: dict, insert_rate_table: dict, insert_process_fail_table: dict ) -> None:
        for element in insert_currency_table:
            self.db_postgres.insert_currency(row_values=element)
        for element in insert_rate_table:
            self.db_postgres.insert_rate(row_values=element)
        for element in insert_process_fail_table:
            self.db_postgres.insert_process_fail(row_values=insert_process_fail_table)
        