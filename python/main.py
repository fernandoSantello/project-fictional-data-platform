from database.mysqlconnect import MysqlDatabase
from database.exceptions.exceptions import DatabaseException, InsertException, SelectException
from api.api import API
from api.exceptions.exceptions import ApiException, NotExceptedResponseException
from apscheduler.schedulers.blocking import BlockingScheduler


def main():
    try:
        database = MysqlDatabase()
    except Exception as e:
        print(f'Could not connect to Database due to the following exception: {e}. Breaking this execution loop and waiting for the next.')
        exit()
    api = API()
    currencies = ['bitcoin', 'ethereum']
    for element in currencies:
        try:
            currency_data = api.fetch_currency_data(currency=element)
        except (ApiException, NotExceptedResponseException) as error:
            try:
                id_currency = database.get_id_currency(currency=element)
                values = {
                    'id_currency': id_currency,
                    'error': error.message
                }
                database.insert_statment(table_name='process_fail', column_values=values)
            except InsertException as error:
                id_currency = database.get_id_currency(currency=element)
                values = {
                    'id_currency': id_currency,
                    'error': error.message
                }
                database.insert_statment(table_name='process_fail', column_values=values)
            continue
        check = database.check_currency(currency_data['id'])
        if check:
            id_currency = database.get_id_currency(currency=currency_data['id'])
            values = {
                    'id_currency': id_currency,
                    'rate': currency_data['rateUsd']
            }
            try:
                database.insert_statment(table_name='rate', column_values=values)
            except InsertException as error:
                id_currency = database.get_id_currency(currency=element)
                values = {
                    'id_currency': id_currency,
                    'error': error.message
                }
                database.insert_statment(table_name='process_fail', column_values=values)
        else:
            values = {'id_currency': currency_data['id'],
                        'symbol': currency_data['symbol'],
                        'currency_symbol': currency_data['currencySymbol'],
                        'type': currency_data['type']
                        }
            try:
                database.insert_statment(table_name='currency', column_values=values)
            except InsertException as error:
                id_currency = database.get_id_currency(currency=element)
                values = {
                    'id_currency': id_currency,
                    'error': error.message
                }
                database.insert_statment(table_name='process_fail', column_values=values)

if __name__ == '__main__':
    main()