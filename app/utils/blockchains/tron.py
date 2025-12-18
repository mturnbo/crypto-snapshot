import os
from dotenv import load_dotenv
import requests
from app.models.asset import Asset
from typing import Optional

load_dotenv()

def get_tron_balance(wallet_address: str) -> Optional[float]:
    try:
        url = f"https://api.trongrid.io/v1/accounts/{wallet_address}"
        headers = {"Accept": "application/json"}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            # Balance is in SUN (1 TRX = 1,000,000 SUN)
            balance_sun = data["data"][0].get("balance", 0)
            balance_trx = balance_sun / 1_000_000
            return balance_trx
        else:
            return 0.0

    except requests.exceptions.RequestException as e:
        print(f"Error fetching TRON balance: {e}")
        return None


def get_tron_price() -> Optional[float]:
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "tron",
            "vs_currencies": "usd"
        }
        API_KEY = os.getenv('API_CG')
        headers = { 'x-cg-demo-api-key': API_KEY }

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        price = data.get("tron", {}).get("usd")

        return price

    except requests.exceptions.RequestException as e:
        print(f"Error fetching price: {e}")
        return None


def get_tron_wallet_info(wallet_address: str) -> Asset:
    balance = get_tron_balance(wallet_address)
    price = get_tron_price()
    usd_value = None
    if balance is not None and price is not None:
        usd_value = balance * price

    return Asset(
        name="TRON",
        symbol="TRX",
        blockchain="tron",
        address=wallet_address,
        balance=balance,
        price=price,
        currency="USD",
    )


print(get_tron_price())
