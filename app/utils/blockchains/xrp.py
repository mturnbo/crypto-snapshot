import requests
from app.models.asset import Asset
from typing import Optional

def get_xrp_balance(wallet_address: str) -> Optional[float]:
    api_url = f"https://api.xrpscan.com/api/v1/account/{wallet_address}"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        return float(data["xrpBalance"])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching XRP balance: {e}")
        return None


def get_xrp_asset(wallet_address: str, get_price: bool = True) -> Asset:
    balance = get_xrp_balance(wallet_address)

    asset = Asset(
        name="XRP",
        symbol="XRP",
        blockchain="XRP",
        address=wallet_address,
        balance=balance,
        currency="USD",
    )

    if get_price:
        asset.get_price('USD')

    return asset
