import requests
from app.models.asset import Asset
from app.utils.env import get_env

def get_doge_balance(wallet_address: str) -> float:
    try:
        API_KEY = get_env("TATUM_API_KEY")
        url = f"https://api.tatum.io/v3/dogecoin/address/balance/{wallet_address}"
        headers = {"x-api-key": API_KEY}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            return float(data["incoming"]) - float(data["outgoing"])
        else:
            print(f"Error fetching balance for {wallet_address}: {response.status_code} - {response.text}")
            return 0.0
    except requests.RequestException as e:
        print(f"Request error for {wallet_address}: {e}")
        return 0.0


def get_doge_asset(wallet_address: str, get_price: bool = True) -> Asset:
    balance = get_doge_balance(wallet_address)

    asset = Asset(
        name="Dogecoin",
        symbol="DOGE",
        blockchain="dogecoin",
        address=wallet_address,
        balance=balance,
        currency="USD",
    )

    if get_price:
        asset.get_current_price('USD')

    return asset
