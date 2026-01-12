import requests
from app.models.asset import Asset
from typing import Optional

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


def get_tron_asset(wallet_address: str, get_price: bool = True) -> Asset:
    balance = get_tron_balance(wallet_address)

    asset = Asset(
        name="TRON",
        symbol="TRX",
        blockchain="tron",
        address=wallet_address,
        balance=balance,
        currency="USD",
    )

    if get_price:
        asset.get_price('USD')

    return asset
