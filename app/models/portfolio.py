import os
from app.models.asset import Asset
from typing import List, Dict
from rich import box
from rich.console import Console
from rich.table import Table
from app.services.assets_service import AssetsService
import csv
from datetime import datetime, timezone

class Portfolio:
    def __init__(self, name: str="", portfolio_type: str="", address_list: Dict[str, str]={}):
        self.name = name
        self.type: str = portfolio_type
        self.addresses: Dict[str, str] = address_list
        self.assets: List[Asset] = []
        self.console = Console()
        self.get_assets()


    def get_assets(self):
        # self.console.clear()
        # self.console.print("[yellow] f"Retrieving assets for {self.type}: {self.name} ...")
        # print(f"Retrieving assets for {self.type}: {self.name} ...")
        with self.console.status(f"Retrieving assets for {self.type}: {self.name} ...", spinner="dots"):
            match self.type.lower():
                case "exchange":
                    self.assets = AssetsService.get_exchange_assets(self.name)
                case "wallet":
                    self.assets = AssetsService.get_wallet_assets(self.addresses)


    def add_asset(self, asset: Asset):
        self.assets.append(asset)


    def remove_asset(self, asset_name: str):
        self.assets = [x for x in self.assets if x.name != asset_name]


    def total_value(self):
        total = sum(asset.price * asset.balance for asset in self.assets if asset.price is not None)
        return total


    def show_addresses(self):
        # console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.title = f"{self.name} Portfolio Addresses"
        table.add_column("Blockchain", justify="left", min_width=12)
        table.add_column("Address", justify="left", min_width=40)
        for blockchain, address in self.addresses.items():
            table.add_row(blockchain, address)
        self.console.print(table)


    def show_assets(self):
        self.assets = [asset for asset in self.assets if asset is not None]
        if not self.assets:
            return

        total_value = self.total_value()

        table = Table(show_header=True, show_footer=True, header_style="bold magenta", box=box.SQUARE_DOUBLE_HEAD, title_justify="left")
        table.title = f"{self.name.capitalize()} Portfolio - Total Value: ${total_value:.2f}"

        included_fields = ['symbol', 'balance', 'price', 'value']
        if self.type == "wallet":
            included_fields.extend(['blockchain', 'address'])

        for item in self.assets[0].formatted_output(included_fields):
            table.add_column(
                item["title"],
                justify=item["justification"],
                min_width=12,
                max_width=item.get("max_width", 20)
            )

        for asset in self.assets:
            values = [d["value"] for d in asset.formatted_output(included_fields)]
            table.add_row(*values)

        self.console.print(table)


    def export_assets(self):
        utc_now = datetime.now(timezone.utc)
        file_timestamp = utc_now.strftime("%Y%m%d%H%M%S")
        data_timestamp = utc_now.strftime("%Y-%m-%d %H:%M:%S")
        directory = "data/export/" + utc_now.strftime("%Y-%m")
        style = "bold yellow"

        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            file_path = f"{directory}/{self.type}_{self.name.lower()}_{file_timestamp}.csv"
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Symbol', 'Balance', 'Price', 'Currency', 'Snapshot Date'])
                for asset in self.assets:
                    if asset.symbol and asset.balance:
                        writer.writerow([asset.symbol, asset.balance, asset.price, asset.currency, data_timestamp])
            self.console.print(f"{self.name} assets exported to {file_path}\n\n", style=style)
        except Exception as e:
            print(f"Error exporting assets: {e}")
