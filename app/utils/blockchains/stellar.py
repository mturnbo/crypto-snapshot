import requests
from app.models.asset import Asset
from typing import Optional

BASE_URL = "https://horizon.stellar.org/accounts/"


def get_xlm_balance(wallet_address: str) -> Optional[float]:
    response = requests.get(BASE_URL + wallet_address)
    if response.status_code == 200:
        balance = float(response.json()["balances"][0]["balance"])

        return balance
    else:
        return None


def get_xlm_asset(wallet_address: str, get_price: bool = True) -> Asset:
    balance = get_xlm_balance(wallet_address)

    asset = Asset(
        name="Stellar",
        symbol="XLM",
        blockchain="stellar",
        address=wallet_address,
        balance=balance,
        currency="USD",
    )

    if get_price:
        asset.get_current_price('USD')

    return asset
