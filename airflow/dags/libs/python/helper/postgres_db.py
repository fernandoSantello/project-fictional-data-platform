from libs.python.services.postgress_db import PostgresDBConnection

class DBPostgres:
    def __init__(self, conn_db: dict):
        self.conn_db = conn_db
    
    def get_id_currency(self, currency: str) -> int:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id FROM currency WHERE name = %s', (currency,))
            row = conn_db.select_statement(sql=sql, fetch_single=True)
            return row['id']


    def insert_process_fail(self, row_values: dict) -> None:
        with self.conn_db as (conn_db, now):
            sql = ('INSERT INTO process_fail (id, id_currency, error, timestamp) VALUES (%s, %s, %s, %s)', (row_values['id'], row_values['id_currency'], row_values['error'], now,))
            conn_db.insert_statement(sql=sql)


    def insert_currency(self, row_values: dict) -> None:
        with self.conn_db as (conn_db, now):
            sql = ('INSERT INTO currency (id, name, symbol, currencySymbol, type, createdAt) VALUES (%s, %s, %s, %s, %s, %s)', (row_values['id'], row_values['name'], row_values['symbol'], row_values['currencySymbol'], row_values['type'] , now,))
            conn_db.insert_statement(sql=sql)


    def insert_rate(self, row_values: dict) -> None:
        with self.conn_db as (conn_db, now):
            sql = ('INSERT INTO rate (id, id_currency, rateUSD, rateBRL, rateEUR, timestamp) VALUES (%s, %s, %s, %s, %s, %s)', (row_values['id'], row_values['id_currency'], row_values['rateUSD'],row_values['rateBRL'], row_values['rateEUR'], now,))
            conn_db.insert_statement(sql=sql)

    
    def get_lat_id_currency(self) -> int:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id FROM currency WHERE id = (SELECT MAX(id) FROM currency)',())
            row = conn_db.select_statement(sql=sql, fetch_single=True)
            return row['id']


    def get_lat_id_rate(self) -> int:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id FROM rate WHERE id = (SELECT MAX(id) FROM rate)',())
            row = conn_db.select_statement(sql=sql, fetch_single=True)
            return row['id']
        

    def get_lat_id_process_fail(self) -> int:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id FROM process_fail WHERE id = (SELECT MAX(id) FROM process_fail)',())
            row = conn_db.select_statement(sql=sql, fetch_single=True)
            return row['id']
