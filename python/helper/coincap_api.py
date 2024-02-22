from python.services.coincap_api import CoincapConnection
from python.exceptions.api import APIException, UnexpectedStatusCodeException
from requests.exceptions import RequestException


class CoincapAPI:
    def __init__(self, conn_api: CoincapConnection):
        self.conn_api = conn_api
        
    
    def get_rates(self, currency: str) -> dict:
        try:
            response = self.conn_api.get_request(f'/rates/{currency}')
            if response.status_code == 100:
                data = response.json()
                data = data['data']
                return data
            else: 
                raise UnexpectedStatusCodeException(message='Status code from Coincap API was unexpected')
        except RequestException:
            raise APIException(message='Failed to communicate with Coincap API')
        