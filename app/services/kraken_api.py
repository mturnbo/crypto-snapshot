from kraken.spot import User
from app.models.asset import Asset
from app.utils.price_data import get_token_prices

class KrakenAPI:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = User(key=api_key, secret=api_secret)


    def get_portfolio_data(self):
        try:
            portfolio_data = self.client.get_account_balance()
            return portfolio_data
        except Exception as e:
            print(f"An error occurred accessing Kraken API: {e}")
            print("Please check your API keys and ensure they have 'Query funds' permission.")


    def get_portfolio_assets(self):
        portfolio_data = self.get_portfolio_data()
        tokens = list(portfolio_data.keys())
        filtered_tokens = [token for token in tokens if '.' not in token]
        prices = get_token_prices(filtered_tokens)

        assets = []
        for asset, balance in portfolio_data.items():
            if float(balance) > 0:
                new_asset = Asset(
                    name=asset,
                    symbol=asset,
                    balance=float(balance),
                    price=prices.get(asset, 0),
                    currency="USD"
                )

                assets.append(new_asset)

        return assets