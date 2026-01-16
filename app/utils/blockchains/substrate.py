import os
import requests
from app.models.asset import Asset
from typing import Optional
from dotenv import load_dotenv
from substrateinterface import SubstrateInterface
from substrateinterface.exceptions import SubstrateRequestException
import json

load_dotenv()

WSS_API_ENDPOINT = "wss://rpc.polkadot.io"
DOT_DECIMALS = 10

def get_substrate_balance(wallet_address: str) -> Optional[float]:
    api_key = os.getenv('SUBSCAN_API_KEY')
    api_url = f"https://acala.api.subscan.io/api/scan/assets/account/balances"
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "address": wallet_address
    })

    try:
        response = requests.post(api_url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(data)

        if data.get("code") == 0 and data.get("data"):
            balance_raw = data["data"].get("balance")
            if balance_raw is not None:
                balance_dot = balance_raw / (10 ** DOT_DECIMALS)
                return balance_dot
            else:
                print("Balance data not found in the response.")
        else:
            print(f"API Error: {data.get('message', 'Unknown error')}")


    except requests.exceptions.RequestException as e:
        print(f"Error fetching substrate balance: {e}")
    except json.JSONDecodeError:
        print("Failed to parse JSON response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None


def get_substrate_balance_si(wallet_address: str) -> Optional[float]:
    substrate = None
    try:
        substrate = SubstrateInterface(url=WSS_API_ENDPOINT)
        account_info = substrate.query("System", "Account", [wallet_address])
        free_balance = int(account_info.value["data"]["free"])
        reserved_balance = int(account_info.value["data"]["reserved"])
        return (free_balance + reserved_balance) / (10 ** DOT_DECIMALS)
    except (SubstrateRequestException, requests.RequestException) as exc:
        print(f"Error fetching Polkadot balance: {exc}")
        return None
    except Exception as exc:
        print(f"Unexpected error fetching Polkadot balance: {exc}")
        return None
    finally:
        if substrate:
            substrate.close()



def get_substrate_asset(wallet_address: str, get_price: bool = True) -> Asset:
    balance = get_substrate_balance_si(wallet_address)

    asset = Asset(
        name="Polkadot",
        symbol="DOT",
        blockchain="Substrate",
        address=wallet_address,
        balance=balance,
        currency="USD",
    )

    if get_price:
        asset.get_price('USD')

    return asset
