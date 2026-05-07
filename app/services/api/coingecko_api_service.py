import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict

import requests

from app.utils.utils import convert_timestamp

if TYPE_CHECKING:
    import pandas as pd


class CoinGeckoAPI():
    DEFAULT_BASE_URL = "https://api.coingecko.com/api/v3/"

    def __init__(self, api_key: str):
        self.api_key: str = api_key

    def make_request(self, endpoint: str, params: Dict[str, str] = {}):
        headers = {'x-cg-demo-api-key': self.api_key}
        response = requests.get(
            self.DEFAULT_BASE_URL + endpoint,
            headers=headers,
            params=params,
        )

        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching data from CoinGecko API!")
            return None

    def get_token_price(self, id: str, currency: str = "USD"):
        endpoint = "simple/price"
        params = {
            "ids": id,
            "vs_currencies": currency,
        }

        data = self.make_request(endpoint, params)

        return data[id]["usd"] if data else None

    def get_top_tokens(self, currency: str = "USD", save=True):
        endpoint = "coins/markets"
        params = {
            "vs_currency": currency,
            "order": "market_cap_desc",
            "per_page": 250,
            "page": 1,
            "sparkline": False,
        }

        data = self.make_request(endpoint, params)

        if data and save:
            Path("data/prices").mkdir(parents=True, exist_ok=True)
            utc_now = datetime.now(timezone.utc)
            file_timestamp = utc_now.strftime("%Y%m%d_%H%M%S")
            file_name = f"gc_top_tokens_{file_timestamp}.csv"
            csv_file_path = Path(f"data/prices/{file_name}")

            with open(
                csv_file_path,
                mode='w',
                newline='',
                encoding='utf-8',
            ) as csv_file:
                if len(data) > 0:
                    fieldnames = data[0].keys()
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)

        return data


    def create_symbol_id_lookup(
        self,
        currency: str = "USD",
        limit: int = 1000,
        output_path: str = "data/coingecko_symbol_lookup.json",
    ) -> Dict[str, Any]:
        endpoint = "coins/markets"
        per_page = 250
        tokens = []

        for page in range(1, (limit + per_page - 1) // per_page + 1):
            params = {
                "vs_currency": currency,
                "order": "market_cap_desc",
                "per_page": min(per_page, limit - len(tokens)),
                "page": page,
                "sparkline": False,
            }

            data = self.make_request(endpoint, params)
            if not data:
                break

            tokens.extend(data)

            if len(tokens) >= limit:
                break

        lookup = {}

        for token in tokens[:limit]:
            symbol = token.get("symbol")
            token_id = token.get("id")

            if not symbol or not token_id:
                continue

            lookup_symbol = symbol.upper()
            lookup.setdefault(lookup_symbol, []).append(token_id)

        output = {
            "lookup": lookup,
            "metadata": {
                "currency": currency,
                "limit": limit,
                "token_count": len(tokens[:limit]),
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
        }

        file_path = Path(output_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, mode="w", encoding="utf-8") as json_file:
            json.dump(output, json_file, indent=2, sort_keys=True)

        return output

    def get_token_price_history(self, token_id: str, currency: str = "USD", days: int = 30) -> "pd.DataFrame":
        import pandas as pd

        endpoint = f"coins/{token_id}/market_chart"
        params = {
            "vs_currency": currency,
            "days": str(days),
        }

        data = self.make_request(endpoint, params)

        for sublist in data['prices']:
            sublist[0] = convert_timestamp(int(sublist[0]) / 1000),

        return pd.DataFrame(data)
