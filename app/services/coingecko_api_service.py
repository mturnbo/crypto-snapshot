from app.models.asset import Asset
import requests
from typing import Dict, List


class CoinGeckoAPI():
    DEFAULT_BASE_URL = "https://api.coingecko.com/api/v3/simple/"

    def __init__(self, api_key: str):
        self.api_key: str = api_key


    def make_request(self, endpoint: str, params: Dict[str, str] = {}):
        headers = {'x-cg-demo-api-key': self.api_key}
        response = requests.get(self.DEFAULT_BASE_URL + endpoint, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching data from CoinGecko API!")
            return None


    def get_token_price(self, id: str):
        endpoint = "price"
        params = {
            "ids": id,
            "vs_currencies": "USD"
        }

        data = self.make_request(endpoint, params)

        return data[id]["usd"] if data else None
