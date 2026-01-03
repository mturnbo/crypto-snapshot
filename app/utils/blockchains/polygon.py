from web3 import Web3
from app.models.asset import Asset
from app.utils.price_data import get_token_price

BASE_API_URL = "https://polygon-rpc.com"

def get_polygon_balance(wallet_address: str, get_price: bool = True):
    w3 = Web3(Web3.HTTPProvider(BASE_API_URL))
    balance_wei = w3.eth.get_balance(wallet_address)
    balance_polygon = float(w3.from_wei(balance_wei, 'ether'))
    usd_value = get_token_price('POL')

    asset = Asset(
        name="Polygon",
        symbol="POL",
        blockchain="polygon",
        address=wallet_address,
        balance=balance_polygon,
        price=usd_value,
        currency="USD",
    )

    if get_price:
        asset.get_price('USD')

    return asset
