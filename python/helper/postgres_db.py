from python.services.postgress_db import PostgresDBConnection

class DBPostgres:
    def __init__(self, conn_db: PostgresDBConnection):
        self.conn_db = conn_db
    
    def get_id_currency(self, currency: str) -> int:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id FROM currency WHERE name = %s', (currency,))
            row = conn_db.select_statement(sql=sql, fetch_single=True)
            return row['id']


    def insert_currency_statement(self, row_values: dict) -> None:
        with self.conn_db as (conn_db, now):
            sql = ('INSERT INTO currency (id, name, symbol, currencysymbol, type, createdAt) VALUES (%s, %s, %s, %s, %s, %s)', (row_values['id'], row_values['name'], row_values['symbol'], row_values['currencysymbol'], row_values['type'] , now,))
            conn_db.insert_statement(sql=sql)


    def insert_rate_statement(self, row_values: dict) -> None:
        with self.conn_db as (conn_db, now):
            sql = ('INSERT INTO rate (id, id_currency, rateusd, ratebrl, rateeur, timestamp) VALUES (%s, %s, %s, %s, %s, %s)', (row_values['id'], row_values['id_currency'], row_values['rateusd'], row_values['ratebrl'], row_values['rateeur'], now,))
            conn_db.insert_statement(sql=sql)


    def insert_process_fail_statement(self, row_values: dict) -> None:
        with self.conn_db as (conn_db, now):
            sql = ('INSERT INTO process_fail (id, error, timestamp) VALUES (%s, %s, %s)', (row_values['id'], row_values['error'], now,))
            conn_db.insert_statement(sql=sql)

    
    def get_last_id_currency(self) -> int:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id FROM currency WHERE id = (SELECT MAX(id) FROM currency)',())
            row = conn_db.select_statement(sql=sql, fetch_single=True)
            return 0 if row == None else row['id']


    def get_last_id_rate(self) -> int:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id FROM rate WHERE id = (SELECT MAX(id) FROM rate)',())
            row = conn_db.select_statement(sql=sql, fetch_single=True)
            return 0 if row == None else row['id']
        

    def get_last_id_process_fail(self) -> int:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id FROM process_fail WHERE id = (SELECT MAX(id) FROM process_fail)',())
            row = conn_db.select_statement(sql=sql, fetch_single=True)
            return 0 if row == None else row['id']
        
    
    def get_currency_table(self, target_last_id: int) -> list:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id, name, symbol, currencysymbol, type, createdAt FROM currency WHERE id > %s', (target_last_id,))
            rows = conn_db.select_statement(sql=sql, fetch_single=False)
            return rows
        

    def get_rate_table(self, target_last_id: int) -> list:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id, id_currency, rateusd, ratebrl, rateeur, timestamp FROM rate WHERE id > %s',(target_last_id,))
            rows = conn_db.select_statement(sql=sql, fetch_single=False)
            return rows
        

    def get_process_fail_table(self, target_last_id: int) -> list:
        with self.conn_db as (conn_db, now):
            sql = ('SELECT id, error, timestamp FROM process_fail WHERE id > %s', (target_last_id,))
            rows = conn_db.select_statement(sql=sql, fetch_single=False)
            return rows
