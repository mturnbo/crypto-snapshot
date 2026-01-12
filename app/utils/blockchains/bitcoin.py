import requests
from app.models.asset import Asset

def get_btc_balance(address: str) -> float | None:
    try:
        # blockchain.info API
        url = f"https://blockchain.info/balance?active={address}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if address in data:
            balance_satoshi = data[address]['final_balance']
            return balance_satoshi / 100000000  # Convert satoshi to BTC

        else:
            print(f"Address {address} not found in response")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def get_btc_asset(wallet_address: str, get_price: bool = True) -> Asset:
    btc_balance = get_btc_balance(wallet_address)

    asset = Asset(
        name="Bitcoin",
        symbol="BTC",
        blockchain="bitcoin",
        address=wallet_address,
        balance=btc_balance,
        currency="USD",
    )

    if get_price:
        asset.get_price('USD')

    return asset
