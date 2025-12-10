from app.models.asset import Asset
from typing import List
from rich.console import Console
from rich.table import Table
import csv
from datetime import datetime, timezone

class Portfolio:
    def __init__(self, name: str="", type: str=""):
        self.name = name
        self.type = type
        self.assets: List[Asset] = []

    def add_asset(self, asset: Asset):
        self.assets.append(asset)

    def remove_asset(self, asset_name: str):
        self.assets = [x for x in self.assets if x.name != asset_name]

    def show_assets(self):
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
            total_value += asset.price * asset.balance
            table.add_row(*values)

        table.title = f"{self.name} Wallet - Total Value: ${total_value:.2f}"
        console.print(table)

    def export_assets(self):
        utc_timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        file_path = f"export/{self.type}.{self.name.lower()}.{utc_timestamp}.csv"
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Symbol', 'ID', 'Balance', 'Price'])
            for asset in self.assets:
                writer.writerow([asset.symbol, asset.id, asset.balance, asset.price])
