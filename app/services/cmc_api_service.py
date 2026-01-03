import os
import requests
from typing import List, Dict, Any
from app.utils.utils import split_list
import tempfile
import requests_cache
import json

class CoinMarketCapAPI():
    DEFAULT_TIMEOUT = 60
    DEFAULT_BASE_URL = 'https://pro-api.coinmarketcap.com/v2'
    TEMPDIR_CACHE = True
    _session = None

    def __init__(self, api_key=None, request_timeout=DEFAULT_TIMEOUT, base_url=DEFAULT_BASE_URL, tempdir_cache = TEMPDIR_CACHE):
        self.api_key = api_key
        self.base_url = base_url
        self.request_timeout = request_timeout
        self.cache_filename = 'coinmarketcap_cache'
        self.cache_name = os.path.join(tempfile.gettempdir(), self.cache_filename) if tempdir_cache else self.cache_filename
        self.token_prices: Dict[str, float] = {}


    @property
    def session(self):
        if not self._session:
            self._session = requests_cache.CachedSession(cache_name=self.cache_name, backend='memory', expire_after=120)
            self._session.headers.update({'Content-Type': 'application/json'})
            self._session.headers.update({'X-CMC_PRO_API_KEY': self.api_key})
            self._session.headers.update({'Accept': 'application/json'})
            self._session.headers.update({'User-agent': 'crypto-snapshot - python wrapper around CoinMarketCap.com API (github.com/mturnbo/crypto-snapshot)'})
        return self._session


    def make_request(self, endpoint: str, params):
        url = self.base_url + endpoint
        response_object = self.session.get(url, params=params, timeout=self.request_timeout)

        try:
            response = json.loads(response_object.text)

            if isinstance(response, list) and response_object.status_code == 200:
                response = [dict(item, **{u'cached': response_object.from_cache}) for item in response]
            if isinstance(response, dict) and response_object.status_code == 200:
                response[u'cached'] = response_object.from_cache

            return response

        except json.decoder.JSONDecodeError as e:
            print(f"Error fetching from CoinMarketCap: {e}")
            return response_object.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from CoinMarketCap: {e}")
        except Exception as e:
            print(f"Error fetching from CoinMarketCap: {e}")
            return e

        return {}


    def get_token_info(self, symbol: str = "") -> Dict[str, Any]:
        params = {
            'symbol': symbol,
        }

        response = self.make_request('/cryptocurrency/info', params)
        data = response['data'][symbol][0]

        contracts: List[Dict] = []
        for address in data['contract_address']:
            contracts.append({
                'address': address['contract_address'],
                'platform_name': address['platform']['name'],
                'platform_symbol': address['platform']['coin']['symbol'],
            })

        return {
            'name': data['name'],
            'symbol': symbol,
            'description': data['description'],
            'logo': data['logo'],
            'date_launched': data['date_launched'],
            'contracts': contracts,
            'circulating_supply': float(data['self_reported_circulating_supply']),
        }


    def get_token_prices(self, symbols: List[str], currency: str = "USD") -> float | Dict[str, float]:
        endpoint = '/cryptocurrency/quotes/latest'
        try:
            if len(symbols) == 1:
                symbol = symbols[0]
                params = {
                    'symbol': symbols,
                    'convert': currency,
                }

                response = self.make_request(endpoint, params)
                return float(response['data'][symbol][0]['quote'][currency]['price'])
            else:
                token_prices: Dict[str, float] = {}
                symbol_groups = split_list(symbols, 40)
                for group in symbol_groups:
                    params = {
                        'symbol': ','.join(group),
                        'convert': currency,
                    }

                    response = self.make_request('/cryptocurrency/quotes/latest', params)

                    for symbol in symbols:
                        if symbol in response['data']:
                            token_prices[symbol] = float(response['data'][symbol][0]['quote'][currency]['price'])

                return token_prices[symbols[0]] if len(token_prices) == 1 else token_prices
        except Exception as e:
            print(f"Error fetching from CoinMarketCap: {e}")
            return 0
