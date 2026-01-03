import requests
from app.models.asset import Asset
from app.services.cmc_api_service import CoinMarketCapAPI
import os
from dotenv import load_dotenv

def get_btc_balance(address: str, get_price: bool = True) -> Asset | None:
    try:
        # blockchain.info API
        url = f"https://blockchain.info/balance?active={address}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if address in data:
            balance_satoshi = data[address]['final_balance']
            balance_btc = balance_satoshi / 100000000  # Convert satoshi to BTC

            asset = Asset(
                name="Bitcoin",
                symbol="BTC",
                blockchain="bitcoin",
                address=address,
                balance=balance_btc,
                currency="USD",
            )

            if get_price:
                asset.get_price('USD')

            return asset
        else:
            print(f"Address {address} not found in response")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
