from database.mysqlconnect import MysqlDatabase
from api.api import API
from api.exceptions.exceptions import ApiException, NotExceptedResponseException
from apscheduler.schedulers.blocking import BlockingScheduler


def main():
    #TODO except na hora de criar database
    database = MysqlDatabase()
    api = API()
    #TODO dá para fazer ele puxar essa lista de algum luga  r
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
            except Exception as e:
                print(e)
            continue
        check = database.check_currency(currency_data['id'])
        if check:
            id_currency = database.get_id_currency(currency=currency_data['id'])
            values = {
                    'id_currency': id_currency,
                    'rate': currency_data['rateUsd']
            }
            database.insert_statment(table_name='rate', column_values=values)
        else:
            values = {currency_data['id'],
                        currency_data['symbol'],
                        currency_data['currencySymbol'],
                        currency_data['type']}
            database.insert_statment(table_name='currency', column_values=values)


if __name__ == '__main__':
    main()