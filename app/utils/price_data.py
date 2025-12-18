import os
from dotenv import load_dotenv
import requests
from typing import List
from app.utils.utils import split_list

load_dotenv()

API_KEY = os.getenv('API_CMC')
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
headers = {
    'X-CMC_PRO_API_KEY': API_KEY,
    'Accept': 'application/json'
}

def get_token_price(symbol: str):
    return get_token_prices([symbol])[symbol]


def get_token_prices(symbols: List):
    prices = {}
    try:
        symbol_groups = split_list(symbols, 40)
        for group in symbol_groups:
            params = {
                'symbol': ','.join(group),
                'convert': 'USD'
            }

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if 'data' in data:
                for symbol in symbols:
                    if symbol in data['data']:
                        # Handle case where symbol might have multiple entries
                        symbol_data = data['data'][symbol]
                        if isinstance(symbol_data, list):
                            symbol_data = symbol_data[0]
                        prices[symbol] = symbol_data['quote']['USD']['price']

        return prices

    except requests.exceptions.RequestException as e:
        print(f"Error fetching from CoinMarketCap: {e}")
        return {}
