import os
import requests
from app.models.asset import Asset
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "https://api.vechainstats.com/v2/"
API_KEY = os.environ.get('VECHAINSTATS_API')

def get_vechain_balance(wallet_address: str) -> Optional[float]:
    try:
        endpoint = "account/vet-vtho"
        url = f"{API_BASE_URL}{endpoint}"
        headers = {
            "Accept": "application/json",
            "X-API-Key": API_KEY,
        }
        params = {
            "address": wallet_address
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return float(data["data"]["vet"]) if data["status"]["success"] == True else 0

    except requests.exceptions.RequestException as e:
        print(f"Error fetching VECHAIN balance: {e}")
        return None


def get_vechain_asset(wallet_address: str, get_price: bool = True) -> Asset:
    balance = get_vechain_balance(wallet_address)

    asset = Asset(
        name="VECHAIN",
        symbol="VET",
        blockchain="vechain",
        address=wallet_address,
        balance=balance,
        currency="USD",
    )

    if get_price:
        asset.get_price('USD')

    return asset
