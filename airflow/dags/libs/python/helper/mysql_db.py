from libs.python.services.database import DBConnection

class DBMysql:
    def __init__(self, conn_param: dict):
        self.conn_param = conn_param
    
    def get_id_currency(self, currency: str) -> int:
        with DBConnection(conn_param=self.conn_param) as (db_conn, now):
            sql = ('SELECT id FROM currency WHERE name = %s', (currency,))
            row = db_conn.select_statement(sql=sql, fetch_single=True)
            return row['id']
        

    def check_currency(self, currency: str) -> bool:
        with DBConnection(conn_param=self.conn_param) as (db_conn, now):
            sql = ('SELECT id FROM currency WHERE name = %s', (currency,))
            row = db_conn.select_statement(sql=sql, fetch_single=True)
            return bool(row)


    def insert_process_fail_statement(self, row_values: dict) -> None:
        with DBConnection(conn_param=self.conn_param) as (db_conn, now):
            sql = ('INSERT INTO process_fail (id_currency, error, timestamp) VALUES (%s, %s, %s)', (row_values['id_currency'], row_values['error'], now,))
            db_conn.insert_statement(sql=sql)


    def insert_currency_statement(self, row_values: dict) -> None:
        with DBConnection(conn_param=self.conn_param) as (db_conn, now):
            sql = ('INSERT INTO currency (name, symbol, currencySymbol, type, createdAt) VALUES (%s, %s, %s, %s, %s)', (row_values['name'], row_values['symbol'], row_values['currencySymbol'], row_values['type'] , now,))
            db_conn.insert_statement(sql=sql)


    def insert_rate_statement(self, row_values: dict) -> None:
        with DBConnection(conn_param=self.conn_param) as (db_conn, now):
            sql = ('INSERT INTO rate (id_currency, rateUSD, timestamp) VALUES (%s, %s, %s)', (row_values['id_currency'], row_values['rateUsd'], now,))
            db_conn.insert_statement(sql=sql)

    
    def insert_rate(self, currency_data: dict) -> None:
        id_currency = self.get_id_currency(currency=currency_data['id'])
        row_values = {
            'id_currency': id_currency,
            'rateUsd': currency_data['rateUsd']
        }
        self.insert_rate_statement(row_values=row_values)

    
    def insert_currency(self, currency_data: dict) -> None:
        row_values = {
            'name': currency_data['id'],
            'symbol': currency_data['symbol'],
            'currencySymbol': currency_data['currencySymbol'],
            'type': currency_data['type']
        }
        self.insert_currency_statement(row_values=row_values)



    def get_currency_table(self, postgres_last_id: int) -> list:
        with DBConnection(conn_param=self.conn_param) as (db_conn, now):
            sql = ('SELECT id, name, symbol, currencySymbol, type, createdAt FROM currency WHERE id > %s', (postgres_last_id,))
            rows = db_conn.select_statement(sql=sql, fetch_single=False)
            return rows
    

    def get_rate_table(self, postgres_last_id: int) -> list:
        with DBConnection(conn_param=self.conn_param) as (db_conn, now):
            sql = ('SELECT id, id_currency, rateUSD, timestamp FROM rate WHERE id > %s',(postgres_last_id,))
            rows = db_conn.select_statement(sql=sql, fetch_single=False)
            return rows


    def get_process_fail_table(self, postgres_last_id: int) -> list:
        with DBConnection(conn_param=self.conn_param) as (db_conn, now):
            sql = ('SELECT id, id_currency, error, timestamp FROM process_fail WHERE id > %s', (postgres_last_id,))
            rows = db_conn.select_statement(sql=sql, fetch_single=False)
            return rows
    