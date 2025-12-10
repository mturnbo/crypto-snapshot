from kraken.spot import User
from dotenv import load_dotenv
from typing import List
from app.models.asset import Asset
import os

load_dotenv()

API_KEY = os.getenv('KRAKEN_API_KEY')
API_SECRET = os.getenv('KRAKEN_PRIVATE_KEY')

def get_kraken_portfolio():
    print(API_SECRET)
    try:
        user_client = User(key=API_KEY, secret=API_SECRET)
        account_balance = user_client.get_account_balance()
        assets = []
        for asset, balance in account_balance.items():
            if float(balance) > 0:
                assets.append(Asset(name=asset, symbol=asset, balance=float(balance)))

        return assets

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your API keys and ensure they have 'Query funds' permission.")

    return None
