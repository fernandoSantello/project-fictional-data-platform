import requests
from requests.models import Response

class ExchangeRateConnection:
    def __init__(self, conn_param: dict):
        self.url = conn_param['url']
        self.api_key = conn_param['api_key']

    def get_request(self, route: str) -> Response:
        response = requests.get(f'{self.url}/{self.api_key}{route}')
        return response
    