import requests
from requests.models import Response

class APIConnection:
    def __init__(self, conn_param: dict):
        self.url = conn_param['url']
        self.api_key = conn_param['api_key']
        self.header = {
            "Accept-Encoding": "gzip, deflate",
            "Authorization": f"Bearer {self.api_key}"
        }

    def get_request(self, route: str) -> Response:
        response = requests.get(f'{self.url}{route}', headers=self.header)
        return response
    