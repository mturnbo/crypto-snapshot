from kraken.spot import User, Market
from dotenv import load_dotenv
from app.models.asset import Asset
from app.utils.util_price_data import get_token_prices
import os

load_dotenv()

API_KEY = os.getenv('KRAKEN_API_KEY')
API_SECRET = os.getenv('KRAKEN_PRIVATE_KEY')

def get_kraken_portfolio():
    try:
        user_client = User(key=API_KEY, secret=API_SECRET)
        portfolio = user_client.get_account_balance()
        assets = []

        tokens = list(portfolio.keys())
        filtered_tokens = [token for token in tokens if '.' not in token]
        prices = get_token_prices(filtered_tokens)

        for asset, balance in portfolio.items():
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

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your API keys and ensure they have 'Query funds' permission.")

    return None
