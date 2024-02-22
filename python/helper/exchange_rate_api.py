from python.services.exchange_rate_api import ExchangeRateConnection
from python.exceptions.api import APIException, UnexpectedStatusCodeException


class ExchangeRateAPI:
    def __init__(self, conn_api: ExchangeRateConnection):
        self.conn_api = conn_api

    
    def get_rates(self) -> dict:
        try:
            response = self.conn_api.get_request(f'/latest/USD')
            if response.status_code == 200:
                data = response.json()
                data = data['conversion_rates']
                return data
            else: 
                raise UnexpectedStatusCodeException(message='Status code from Exchange Rate API was unexpected')
        except:
            raise APIException(message='Failed to communicate with Exchange Rate API')
