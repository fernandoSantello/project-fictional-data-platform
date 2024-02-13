from mysqlconnect import MysqlDatabase
from api import API
from apscheduler.schedulers.blocking import BlockingScheduler


def process():
    database = MysqlDatabase()
    api = API()
    currency_data = api.fetch_currency_data(currencies=['bitcoin', 'ethereum'])
    for row in currency_data:
            check = database.check_currency(row['id'])
            if check:
                id_currency = database.get_id_currency(currency=row.get('id'))
                values = [id_currency, row.get('rateUsd')]
                database.insert_statment(table_name='rate', column_values=values)
            else:
                values = [row.get('id'), row.get('symbol'), row.get('currencySymbol'), row.get('type')]
                database.insert_statment(table_name='currency', column_values=values)



def main():
    
    process()




if __name__ == '__main__':
    main()