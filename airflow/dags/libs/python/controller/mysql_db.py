from libs.python.helper.coincap_api import CoincapAPI
from libs.python.helper.mysql_db import DBMysql
from typing import Union
from dotenv import load_dotenv
import os

class DBMysqlOperator:
    def __init__(self):
        load_dotenv()
        self.db_mysql = DBMysql(conn_param={
            'user': os.getenv('MYSQL_PROD_USER'),
            'password': os.getenv('MYSQL_PROD_PASSWORD'),
            'host': os.getenv('MYSQL_PROD_HOST'),
            'database': os.getenv('MYSQL_PROD_DATABASE'),
            'database_type': 'mysql'
        })
        self.api_coincap = CoincapAPI(conn_param={
            'url': os.getenv('COINCAP_API_URL'),
            'api_key': os.getenv('COINCAP_API_KEY')
        })
        self.currencies = ['bitcoin', 'ethereum']

    
    def get_currency_info(self, currency: str) -> Union[bool, dict]:
        currency_data = self.api_coincap.get_rates(currency=currency)
        check = self.db_mysql.check_currency(currency_data['id'])
        return (True, currency_data) if check else (False, currency_data)
    

    def insert_rate(self, currency_data: dict) -> None:
        id_currency = self.db_mysql.get_id_currency(currency=currency_data['id'])
        row_values = {
            'id_currency': id_currency,
            'rateUsd': currency_data['rateUsd']
        }
        self.db_mysql.insert_rate(row_values=row_values)


    def insert_currency(self, currency_data: dict) -> None:
        row_values = {
            'name': currency_data['id'],
            'symbol': currency_data['symbol'],
            'currencySymbol': currency_data['currencySymbol'],
            'type': currency_data['type']
        }
        self.db_mysql.insert_currency(row_values=row_values)


    def sync_currency_data(self) -> None:
        for element in self.currencies:
            curency_exists, currency_data = self.get_currency_info(element)
            self.insert_rate(currency_data) if curency_exists else self.insert_currency(currency_data)
