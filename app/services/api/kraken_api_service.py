from kraken.spot import User
from app.models.asset import Asset
from typing import List
import re

class KrakenAPI:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = User(key=api_key, secret=api_secret)


    def filter_symbol(self, s: str) -> str:
        return re.sub(r'\d', '', s.split('.', 1)[0])


    def get_portfolio_data(self):
        try:
            portfolio_data = self.client.get_account_balance()

            # consolidate staked balances
            consolidated_portfolio_data = {}
            for asset, balance in portfolio_data.items():
                if consolidated_portfolio_data.get(self.filter_symbol(asset)):
                    consolidated_portfolio_data[self.filter_symbol(asset)] += float(balance)
                else:
                    consolidated_portfolio_data[self.filter_symbol(asset)] = float(balance)

            return consolidated_portfolio_data
        except Exception as e:
            print(f"An error occurred accessing Kraken API: {e}")
            print("Please check your API keys and ensure they have 'Query funds' permission.")


    def get_portfolio_assets(self) -> List[Asset]:
        portfolio_data = self.get_portfolio_data()
        print(portfolio_data)

        assets = []
        for asset, balance in portfolio_data.items():
            if float(balance) > 0:
                new_asset = Asset(
                    name=asset,
                    symbol=asset,
                    balance=float(balance),
                    currency="USD"
                )

                assets.append(new_asset)

        return assets