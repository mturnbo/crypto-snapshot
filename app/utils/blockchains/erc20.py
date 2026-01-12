from typing import List
import requests
from app.models.asset import Asset

BASE_API_URL = "https://api.ethplorer.io/getAddressInfo/__ADDRESS__?apiKey=freekey"

def get_erc20_assets(wallet_address: str) -> List[Asset]:
    api_url = BASE_API_URL.replace("__ADDRESS__", wallet_address)
    response = requests.get(api_url)
    wallet_data = response.json()

    wallet_assets = []
    # get ETH
    if wallet_data.get("ETH", {}):
        asset_info = wallet_data.get("ETH", {})
        asset = Asset(
            name="",
            symbol="ETH",
            blockchain="erc20",
            address=wallet_address,
            balance=asset_info.get("balance", "0"),
            price=asset_info["price"]["rate"],
            currency="USD",
        )
        wallet_assets.append(asset)

    # get ERC20 tokens
    for token in wallet_data.get("tokens", []):
        asset_info = token.get("tokenInfo", {})
        if asset_info.get("symbol", "") and asset_info.get("price", ""):
            decimals = int(asset_info.get("decimals", 0))
            balance = float(token.get("rawBalance", 0)) / (10 ** decimals)
            asset = Asset(
                name=asset_info.get("name", ""),
                symbol=asset_info.get("symbol", ""),
                blockchain="erc20",
                address=wallet_address,
                balance=balance,
                price=asset_info["price"]["rate"],
                currency="USD",
            )
            wallet_assets.append(asset)

    return wallet_assets
