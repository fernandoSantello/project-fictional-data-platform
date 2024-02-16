from libs.python.services.coincap_api import CoincapConnection

class CoincapAPI:
    def __init__(self, conn_param: dict):
        self.conn_param = conn_param
        self.conn_api = CoincapConnection(conn_param=conn_param)

    
    def get_rates(self, currency: str) -> dict:
        response = self.conn_api.get_request(f'/rates/{currency}')
        if response.status_code == 200:
            data = response.json()
            data = data['data']
            return data
        else: 
            print(response.status_code)