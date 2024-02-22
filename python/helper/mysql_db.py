from python.services.mysql_db import MysqlDBConnection

class DBMysql:
    def __init__(self, conn_db: MysqlDBConnection):
        self.conn_db = conn_db
    
    def get_id_currency(self, currency: str) -> int:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id FROM currency WHERE name = %s', (currency,))
            row = conn_db.select_statement(sql=sql, fetch_single=True)
            return row['id']
        

    def check_currency(self, currency: str) -> bool:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id FROM currency WHERE name = %s', (currency,))
            row = conn_db.select_statement(sql=sql, fetch_single=True)
            return bool(row)


    def insert_process_fail_statement(self, row_values: dict) -> None:
        with self.conn_db as (conn_db, now):
            sql = ('INSERT INTO process_fail (currency_name, error, timestamp) VALUES (%s, %s, %s)', (row_values['currency_name'], row_values['error'], now,))
            conn_db.insert_statement(sql=sql)


    def insert_currency_statement(self, row_values: dict) -> None:
        with self.conn_db as (conn_db, now):
            sql = ('INSERT INTO currency (name, symbol, currencysymbol, type, createdAt) VALUES (%s, %s, %s, %s, %s)', (row_values['name'], row_values['symbol'], row_values['currencysymbol'], row_values['type'] , now,))
            conn_db.insert_statement(sql=sql)


    def insert_rate_statement(self, row_values: dict) -> None:
        with self.conn_db as (conn_db, now):
            sql = ('INSERT INTO rate (id_currency, rateusd, timestamp) VALUES (%s, %s, %s)', (row_values['id_currency'], row_values['rateusd'], now,))
            conn_db.insert_statement(sql=sql)

    
    def insert_rate(self, currency_data: dict) -> None:
        id_currency = self.get_id_currency(currency=currency_data['id'])
        row_values = {
            'id_currency': id_currency,
            'rateusd': currency_data['rateUsd']
        }
        self.insert_rate_statement(row_values=row_values)

    
    def insert_currency(self, currency_data: dict) -> None:
        row_values = {
            'name': currency_data['id'],
            'symbol': currency_data['symbol'],
            'currencysymbol': currency_data['currencySymbol'],
            'type': currency_data['type']
        }
        self.insert_currency_statement(row_values=row_values)

    
    def insert_process_fail(self, currency_data):
        row_values = {
            'currency_name': currency_data['name'],
            'error': currency_data['error']
        }
        self.insert_process_fail_statement(row_values=row_values)


    def get_currency_table(self, postgres_last_id: int) -> list:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id, name, symbol, currencysymbol, type, createdAt FROM currency WHERE id > %s', (postgres_last_id,))
            rows = conn_db.select_statement(sql=sql, fetch_single=False)
            return rows
    

    def get_rate_table(self, postgres_last_id: int) -> list:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id, id_currency, rateusd, timestamp FROM rate WHERE id > %s',(postgres_last_id,))
            rows = conn_db.select_statement(sql=sql, fetch_single=False)
            return rows


    def get_process_fail_table(self, postgres_last_id: int) -> list:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id, currency_name, error, timestamp FROM process_fail WHERE id > %s', (postgres_last_id,))
            rows = conn_db.select_statement(sql=sql, fetch_single=False)
            return rows
    