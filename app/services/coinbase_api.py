import os
from dotenv import load_dotenv
from app.utils.utils import decode_ec_private_key
from coinbase.rest import RESTClient
from app.models.asset import Asset

class CoinbaseAPI():
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = decode_ec_private_key(api_secret)
        self.client = RESTClient(api_key=self.api_key, api_secret=self.api_secret)

    def get_portfolio_data(self):
        portfolios = self.client.get_portfolios()
        portUuid = portfolios['portfolios'][0]['uuid']
        portfolio_data = self.client.get_portfolio_breakdown(portfolio_uuid=portUuid)

        return portfolio_data

    def get_portfolio_assets(self):
        portfolio_data = self.get_portfolio_data()

        assets = []
        for position in portfolio_data['breakdown']['spot_positions']:
            crypto_price = position['total_balance_fiat'] / position['total_balance_crypto']
            assets.append(Asset(
                name=position['asset'],
                symbol=position['asset'],
                balance=position['total_balance_crypto'],
                price=crypto_price,
                currency="USD"
            ))

        return assets


# load_dotenv()
# API_KEY_NAME = os.getenv('COINBASE_API_KEY')
# API_PRIVATE_KEY = os.getenv('COINBASE_API_SECRET')
# cb_api = CoinbaseAPI(API_KEY_NAME, API_PRIVATE_KEY)
# assets = cb_api.get_portfolio_assets()
# print(assets[0].symbol, assets[0].balance)