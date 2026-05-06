import requests
from datetime import datetime, timezone
import csv
from pathlib import Path
from typing import Dict
from app.utils.utils import convert_timestamp
import pandas as pd


class CoinGeckoAPI():
    DEFAULT_BASE_URL = "https://api.coingecko.com/api/v3/"

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


    def get_token_price(self, id: str, currency: str = "USD"):
        endpoint = "simple/price"
        params = {
            "ids": id,
            "vs_currencies": currency,
        }

        data = self.make_request(endpoint, params)

        return data[id]["usd"] if data else None

    def get_top_tokens(self, currency: str = "USD", save=True):
        endpoint = "coins/markets"
        params = {
            "vs_currency": currency,
            "order": "market_cap_desc",
            "per_page": 250,
            "page": 1,
            "sparkline": False,
        }

        data = self.make_request(endpoint, params)

        if data and save:
            Path("data/prices").mkdir(parents=True, exist_ok=True)
            utc_now = datetime.now(timezone.utc)
            file_timestamp = utc_now.strftime("%Y%m%d_%H%M%S")
            file_name = f"gc_top_tokens_{file_timestamp}.csv"
            csv_file_path = Path(f"data/prices/{file_name}")

            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                if len(data) > 0:
                    fieldnames = data[0].keys()
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)

        return data


    def get_token_price_history(self, id: str, currency: str = "USD", days: int = 30) -> pd.DataFrame:
        endpoint = f"coins/{id}/market_chart"
        params = {
            "vs_currency": currency,
            "days": days,
        }

        data = self.make_request(endpoint, params)

        for sublist in data['prices']:
            sublist[0] = convert_timestamp(int(sublist[0]) / 1000),

        return pd.DataFrame(data)

