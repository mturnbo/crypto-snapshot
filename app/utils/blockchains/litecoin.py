import requests
from app.models.asset import Asset

def get_ltc_balance(address: str) -> Asset:
    try:
        # BlockCypher API
        url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Convert from litoshi to LTC (1 LTC = 100,000,000 litoshi)
        balance_ltc = data['final_balance'] / 100000000
        usd_value = 0

        if address == data['address']:
            asset = Asset(
                name="Litecoin",
                symbol="LTC",
                blockchain="litecoin",
                address=address,
                balance=balance_ltc,
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
