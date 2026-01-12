import requests
from app.models.asset import Asset

def get_ltc_balance(address: str) -> float | None:
    try:
        # BlockCypher API
        url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Convert from litoshi to LTC (1 LTC = 100,000,000 litoshi)
        return data['final_balance'] / 100000000

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def get_ltc_asset(wallet_address: str, get_price: bool = True) -> Asset:
    ltc_balance = get_ltc_balance(wallet_address)

    asset = Asset(
        name="Litecoin",
        symbol="LTC",
        blockchain="litecoin",
        address=wallet_address,
        balance=ltc_balance,
        currency="USD",
    )

    if get_price:
        asset.get_price('USD')

    return asset