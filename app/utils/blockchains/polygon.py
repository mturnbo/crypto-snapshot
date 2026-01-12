from web3 import Web3
from app.models.asset import Asset

BASE_API_URL = "https://polygon-rpc.com"

def get_polygon_balance(wallet_address: str) -> float | None:
    w3 = Web3(Web3.HTTPProvider(BASE_API_URL))
    balance_wei = w3.eth.get_balance(wallet_address)

    return float(w3.from_wei(balance_wei, 'ether'))


def get_polygon_assets(wallet_address: str, get_price: bool = True) -> Asset:
    polygon_balance = get_polygon_balance(wallet_address)

    asset = Asset(
        name="Polygon",
        symbol="POL",
        blockchain="polygon",
        address=wallet_address,
        balance=polygon_balance,
        currency="USD",
    )

    if get_price:
        asset.get_price('USD')

    return asset