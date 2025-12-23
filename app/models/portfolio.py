import os
from dotenv import load_dotenv
from app.models.asset import Asset
from typing import List, Dict
from rich.console import Console
from rich.table import Table
from app.utils.blockchains.bitcoin import get_btc_balance
from app.utils.blockchains.litecoin import get_ltc_balance
from app.utils.blockchains.polygon import get_polygon_balance
from app.utils.blockchains.cardano import get_wallet_assets as get_cardano_assets
from app.utils.blockchains.erc20 import get_wallet_assets as get_erc20_assets
from app.utils.blockchains.solana import get_wallet_assets as get_solana_assets
from app.utils.blockchains.tron import get_tron_wallet_info as get_tron_balance
from app.services.coinbase_api import CoinbaseAPI
from app.services.kraken_api import KrakenAPI
import csv
from datetime import datetime, timezone

class Portfolio:
    def __init__(self, name: str="", portfolio_type: str="", address_list: Dict[str, str]={}):
        self.name = name
        self.type: str = portfolio_type
        self.addresses: Dict[str, str] = address_list
        self.assets: List[Asset] = []
        self.get_assets()

    def get_assets(self):
        self.assets = []

        match self.type.lower():
            case "exchange":
                load_dotenv()
                match self.name.lower():
                    case "coinbase":
                        api_key = os.getenv('COINBASE_API_KEY')
                        api_secret = os.getenv('COINBASE_API_SECRET')
                        cb_api = CoinbaseAPI(api_key, api_secret)
                        self.assets = cb_api.get_portfolio_assets()
                    case "kraken":
                        api_key = os.getenv('KRAKEN_API_KEY')
                        api_secret = os.getenv('KRAKEN_API_SECRET')
                        kraken_api = KrakenAPI(api_key, api_secret)
                        self.assets = kraken_api.get_portfolio_assets()

            case "wallet":
                for blockchain, address in self.addresses.items():
                    new_assets = []
                    match blockchain.lower():
                        case "btc":
                            new_assets = [get_btc_balance(address)]
                        case "ltc":
                            new_assets = [get_ltc_balance(address)]
                        case "ada":
                            new_assets = get_cardano_assets(address)
                        case "erc20":
                            new_assets = get_erc20_assets(address)
                        case "sol":
                            new_assets = get_solana_assets(address)
                        case "pol":
                            new_assets = [get_polygon_balance(address)]
                        case "trx":
                            new_assets = [get_tron_balance(address)]

                    self.assets.extend(new_assets)

    def add_asset(self, asset: Asset):
        self.assets.append(asset)

    def remove_asset(self, asset_name: str):
        self.assets = [x for x in self.assets if x.name != asset_name]

    def show_addresses(self):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.title = f"{self.name} Portfolio Addresses"
        table.add_column("Blockchain", justify="left", min_width=12)
        table.add_column("Address", justify="left", min_width=40)
        for blockchain, address in self.addresses.items():
            table.add_row(blockchain, address)
        console.print(table)

    def show_assets(self):
        if not self.assets:
            return

        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        column_titles = list(self.assets[0].__dict__.keys())
        column_titles.insert(-1, "USD Value")

        for item in self.assets[0].formatted_output():
            table.add_column(
                item["title"],
                justify=item["justification"],
                min_width=12,
                max_width=item.get("max_width", 20)
            )

        total_value = 0
        for asset in self.assets:
            values = [d["value"] for d in asset.formatted_output()]
            if asset.price is not None:
                total_value += asset.price * asset.balance
            table.add_row(*values)

        table.title = f"{self.name.capitalize()} Portfolio - Total Value: ${total_value:.2f}"
        console.print(table)

    def export_assets(self):
        utc_timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        file_path = f"export/{self.type}.{self.name.lower()}.{utc_timestamp}.csv"
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Symbol', 'ID', 'Balance', 'Price'])
            for asset in self.assets:
                writer.writerow([asset.symbol, asset.id, asset.balance, asset.price])
