import python.helper.data_operations as data_operations
from python.exceptions.api import APIException, UnexpectedStatusCodeException
from python.exceptions.database import DatabaseException, StatementException


class Controller:
    def __init__(self, api_rate, api_exchange_rate, source_database, target_database):
        self.source_database = source_database
        self.target_database = target_database
        self.api_rate = api_rate
        self.api_exchange_rate = api_exchange_rate
        self.currencies = ['bitcoin', 'ethereum']
    
    
    def get_rate(self) -> list:
        source_last_id = self.target_database.get_last_id_rate()
        rows = self.source_database.get_rate_table(postgres_last_id=source_last_id)
        return rows
    

    def get_currency(self) -> list:
        source_last_id = self.target_database.get_last_id_currency()
        rows = self.source_database.get_currency_table(postgres_last_id=source_last_id)
        return rows
    
    
    def get_process_fail(self) -> list:
        source_last_id = self.target_database.get_last_id_process_fail()
        rows = self.source_database.get_process_fail_table(postgres_last_id=source_last_id)
        return rows


    def concatenate_rate_column(self) -> dict:
        try:
            rates_data = self.api_exchange_rate.get_rates()
        except (APIException, UnexpectedStatusCodeException) as ex:
                data = {
                    'error': ex.message
                }
                self.source_database.insert_process_fail(data)
                return
        rate_table = self.get_rate()
        treated_rate_table = data_operations.concatenate_dataframe(rates_data=rates_data, rate_table=rate_table)
        return treated_rate_table
    

    def sync_currency_data(self) -> None:
        for element in self.currencies:
            try:
                currency_data = self.api_rate.get_rates(currency=element)
            except (APIException, UnexpectedStatusCodeException) as ex:
                data = {
                    'error': ex.message
                }
                self.source_database.insert_process_fail(data)
                return
            try:
                curency_exists = self.source_database.check_currency(currency_data['id'])
                if not curency_exists:
                    self.source_database.insert_currency(currency_data)
                self.source_database.insert_rate(currency_data)
            except (DatabaseException, StatementException):
                return


    def gather_table_data(self, treat_data: bool) -> dict:
        try:
            insert_currency_table = self.get_currency()
            if treat_data:
                insert_rate_table = self.concatenate_rate_column()
            else:
                insert_rate_table = self.get_rate()
            insert_process_fail_table = self.get_process_fail()
            return insert_currency_table, insert_rate_table, insert_process_fail_table
        except (DatabaseException, StatementException):
            return

    def insert_into_target_database(self, insert_currency_table: dict, insert_rate_table: dict, insert_process_fail_table: dict ) -> None:
        try:
            for element in insert_currency_table:
                self.target_database.insert_currency(row_values=element)
            for element in insert_rate_table:
                self.target_database.insert_rate(row_values=element)
            for element in insert_process_fail_table:
                self.target_database.insert_process_fail(row_values=element)
        except (DatabaseException, StatementException):
            return