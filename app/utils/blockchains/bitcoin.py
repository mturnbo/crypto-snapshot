import requests
from app.models.asset import Asset

def get_btc_wallet_balance(address: str) -> Asset:
    try:
        # blockchain.info API
        url = f"https://blockchain.info/balance?active={address}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if address in data:
            balance_satoshi = data[address]['final_balance']
            balance_btc = balance_satoshi / 100000000  # Convert satoshi to BTC
            usd_value = 0

            asset = Asset(
                name="Bitcoin",
                symbol="BTC",
                blockchain="bitcoin",
                address=address,
                balance=balance_btc,
                price=usd_value,
                currency="USD",
            )

            return asset
        else:
            print(f"Address {address} not found in response")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
