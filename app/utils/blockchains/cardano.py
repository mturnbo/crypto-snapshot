from typing import List
import requests
from app.models.asset import Asset

BASE_API_URL = "https://agg-api.minswap.org/aggregator/"

def get_ada_price(currency: str = "usd") -> float:
    api_url = BASE_API_URL + "ada-price"
    params = {
        "currency": currency,
    }
    response = requests.get(api_url, params=params)
    ada_price = response.json()["value"]["price"]
    return ada_price

def get_wallet_assets(wallet_address: str) -> List[Asset]:
    api_url = BASE_API_URL + "wallet"
    params = {
        "address": wallet_address,
        "amount_in_decimal": "true"
    }
    response = requests.get(api_url, params=params)
    wallet_data = response.json()

    ada_price = get_ada_price()
    wallet_assets = []
    if wallet_data.get("balance"):
        for token in wallet_data["balance"]:
            asset_info = token.get("asset", {})
            if asset_info.get("token_id", ""):
                ada_value = float(asset_info.get("price_by_ada", 0))
                usd_value = ada_value * ada_price
                asset = Asset(
                    name=asset_info.get("name", ""),
                    symbol=asset_info.get("ticker", ""),
                    blockchain="cardano",
                    address=wallet_address,
                    balance=float(token.get("amount", 0)),
                    price=usd_value,
                    currency="USD",
                )
                wallet_assets.append(asset)

    return wallet_assets
