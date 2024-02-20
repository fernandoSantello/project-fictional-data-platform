from libs.python.services.coincap_api import CoincapConnection

class CoincapAPI:
    def __init__(self, conn_api: CoincapConnection):
        self.conn_api = conn_api
        

    
    def get_rates(self, currency: str) -> dict:
        response = self.conn_api.get_request(f'/rates/{currency}')
        if response.status_code == 200:
            data = response.json()
            data = data['data']
            return data
        else: 
            print(response.status_code)
            