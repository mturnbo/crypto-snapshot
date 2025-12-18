from typing import List
import requests
import os
import json
from app.models.asset import Asset
from app.utils.price_data import get_token_price
from config.settings import ROOT_DIR

BASE_API_URL = "https://api.mainnet-beta.solana.com"
BDS_API_KEY = os.environ.get('BDS_API_KEY')

def refresh_solana_token_metadata():
    url = "https://raw.githubusercontent.com/solana-labs/token-list/main/src/tokens/solana.tokenlist.json"
    res = requests.get(url).json()
    token_map = {}
    for token in res["tokens"]:
        token_map[token["address"]] = {
            "name": token["name"],
            "symbol": token["symbol"],
            "decimals": token["decimals"]
        }

    file_path = os.path.join(ROOT_DIR, 'config', 'tokenmap.solana.json')
    with open(file_path, 'w') as f:
        json.dump(token_map, f, indent=4)

    print(f"{len(token_map)} tokens written to file {file_path}")


def get_sol_balance(wallet_address: str) -> float:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [wallet_address]
    }
    res = requests.post(BASE_API_URL, json=payload).json()
    balance = res['result']['value']

    return balance / 1_000_000_000


def get_wallet_assets(wallet_address) -> List[Asset]:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccountsByOwner",
        "params": [
            wallet_address,
            {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
            {"encoding": "jsonParsed"}
        ]
    }
    res = requests.post(BASE_API_URL, json=payload).json()
    result = res.get("result", {}).get("value", [])

    file_path = os.path.join(ROOT_DIR, 'config', 'tokenmap.solana.json')
    with open(file_path) as f:
        token_map = json.load(f)

    wallet_assets = [] = []
    for account in result:
        info = account['account']['data']['parsed']['info']
        mint = info['mint']
        token_amount = info['tokenAmount']
        balance = int(token_amount['amount']) / (10 ** int(token_amount['decimals']))

        if balance > 0:
            asset = Asset(
                name=token_map.get(mint, {}).get("name", ""),
                symbol=token_map.get(mint, {}).get("symbol", ""),
                id=mint,
                blockchain="solana",
                address=wallet_address,
                balance=balance,
                currency="USD",
            )
            asset.price = get_token_price(asset.symbol)

            wallet_assets.append(asset)

    return wallet_assets
