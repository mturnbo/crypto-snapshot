import os
import requests
from app.models.asset import Asset
from typing import Optional
from dotenv import load_dotenv
from substrateinterface import SubstrateInterface

load_dotenv()

def get_substrate_balance(wallet_address: str) -> Optional[float]:
    api_key = os.getenv('SUBSCAN_API_KEY')
    api_url = f"https://acala.api.subscan.io/{wallet_address}"
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        return float(data["xrpBalance"])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching XRP balance: {e}")
        return None


def get_substrate_balance_si(wallet_address: str) -> Optional[float]:
    substrate = SubstrateInterface(url="wss://rpc.polkadot.io/ws")
    account_info = substrate.query(
        module="System",
        storage_function="Account",
        params=[wallet_address]
    )

    free_balance = account_info.value["data"]["free"]
    token_decimals = substrate.token_decimals
    free_balance_dot = free_balance / (10 ** token_decimals)

    return free_balance_dot


def get_substrate_asset(wallet_address: str, get_price: bool = True) -> Asset:
    balance = get_substrate_balance(wallet_address)

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
