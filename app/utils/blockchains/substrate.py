import requests
from app.models.asset import Asset
from typing import Optional
from app.utils.env import get_env
import json

DOT_DECIMALS = 10

def get_substrate_balance(wallet_address: str) -> float:

    api_key = get_env('TATUM_API_KEY')
    url = f'https://polkadot-assethub.gateway.tatum.io/substrateapi/accounts/{wallet_address}/balance-info'
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_key
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return float(data['free']) / (10 ** DOT_DECIMALS)


def get_substrate_asset(wallet_address: str, get_price: bool = True) -> Asset:
    balance = get_substrate_balance(wallet_address)

    asset = Asset(
        name="Polkadot",
        symbol="DOT",
        blockchain="Substrate",
        address=wallet_address,
        balance=balance,
        currency="USD",
    )

    if get_price:
        asset.get_current_price('USD')

    return asset
