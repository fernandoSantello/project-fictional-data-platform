from libs.python.services.api import APIConnection

class API:
    def __init__(self, conn_param: dict):
        self.conn_param = conn_param
        self.conn_api = APIConnection(conn_param=conn_param)

    
    def get_rates(self, currency: str) -> dict:
        response = self.conn_api.get_request(f'/rates/{currency}')
        if response.status_code == 200:
            data = response.json()
            data = data['data']
            return data
        else: 
            print(response.status_code)