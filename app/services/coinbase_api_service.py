from cryptography.hazmat.primitives import serialization
from app.utils.utils import decode_ec_private_key
from app.models.asset import Asset
import time
import jwt
import secrets
import hmac
import hashlib
from typing import Dict, List
from coinbase.rest import RESTClient


class CoinbaseAPI():
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = decode_ec_private_key(api_secret)
        self.rest_client = RESTClient(api_key=self.api_key, api_secret=self.api_secret)

    def generate_signature(self, timestamp: str, method: str, path: str, body: str = '') -> str:
        # Generate CB-ACCESS-SIGN header for authentication
        message = timestamp + method + path + body
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return signature


    def get_headers(self, method: str, path: str, body: str = '') -> Dict:
        # Generate authentication headers for Coinbase API
        timestamp = str(int(time.time()))
        signature = self.generate_signature(timestamp, method, path, body)

        return {
            'CB-ACCESS-KEY': self.api_secret,
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'Content-Type': 'application/json'
        }
    

    def build_jwt(self, uri: str, private_key: bytes) -> str:
        try:
            private_key = serialization.load_pem_private_key(private_key, password=None)
            jwt_payload = {
                'sub': self.api_key,
                'iss': "cdp",
                'nbf': int(time.time()),
                'exp': int(time.time()) + 120,
                'uri': uri,
            }

            jwt_token = jwt.encode(
                jwt_payload,
                private_key,
                algorithm='ES256',
                headers={'kid': self.api_key, 'nonce': secrets.token_hex()},
            )

            return jwt_token
        except ValueError as e:
            print(f"Error loading private key: {e}")
            return None


    def get_portfolio_data(self):
        portfolios = self.rest_client.get_portfolios()
        portUuid = portfolios['portfolios'][0]['uuid']
        portfolio_data = self.rest_client.get_portfolio_breakdown(portfolio_uuid=portUuid)

        return portfolio_data


    def get_portfolio_assets(self) -> List[Asset]:
        portfolio_data = self.get_portfolio_data()

        assets = []
        for position in portfolio_data['breakdown']['spot_positions']:
            balance = position['total_balance_crypto']
            fiat_val = position['total_balance_fiat']
            crypto_price = fiat_val / balance if balance > 0 else 0

            assets.append(Asset(
                name=position['asset'],
                symbol=position['asset'],
                balance=position['total_balance_crypto'],
                price=crypto_price,
                currency="USD"
            ))

        return assets


    def get_ticker_price(self, trade_pair):
        ticker = self.rest_client.get_product(trade_pair)

        return ticker
