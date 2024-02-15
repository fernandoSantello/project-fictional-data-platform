from services.database import DBConnection

class DB:
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


    def insert_process_fail(self, row_values: dict) -> None:
        with DBConnection(conn_param=self.conn_param) as (db_conn, now):
            sql = ('INSERT INTO process_fail (id_currency, error, timestamp) VALUES (%s, %s, %s)', (row_values['id_currency'], row_values['error'], now,))
            db_conn.insert_statement(sql=sql)


    def insert_currency(self, row_values: dict) -> None:
        with DBConnection(conn_param=self.conn_param) as (db_conn, now):
            sql = ('INSERT INTO currency (name, symbol, currencySymbol, type, createdAt) VALUES (%s, %s, %s, %s, %s)', (row_values['name'], row_values['symbol'], row_values['currencySymbol'], row_values['type'] , now,))
            db_conn.insert_statement(sql=sql)


    def insert_rate(self, row_values: dict) -> None:
        with DBConnection(conn_param=self.conn_param) as (db_conn, now):
            sql = ('INSERT INTO rate (id_currency, rateUSD, timestamp) VALUES (%s, %s, %s)', (row_values['id_currency'], row_values['rateUsd'], now,))
            db_conn.insert_statement(sql=sql)
