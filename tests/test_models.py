import csv
from pathlib import Path
import sys
import types

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

sys.modules.setdefault("dotenv", types.SimpleNamespace(load_dotenv=lambda: None))

if "rich" not in sys.modules:
    rich_module = types.ModuleType("rich")
    rich_console_module = types.ModuleType("rich.console")
    rich_table_module = types.ModuleType("rich.table")

    class DummyConsole:
        def print(self, *args, **kwargs):  # pragma: no cover - simple stub
            return None

    class DummyTable:
        def __init__(self, *args, **kwargs):
            self.title = ""

        def add_column(self, *args, **kwargs):  # pragma: no cover - simple stub
            return None

        def add_row(self, *args, **kwargs):  # pragma: no cover - simple stub
            return None

    rich_console_module.Console = DummyConsole
    rich_table_module.Table = DummyTable

    sys.modules["rich"] = rich_module
    sys.modules["rich.console"] = rich_console_module
    sys.modules["rich.table"] = rich_table_module

blockchain_stub = types.ModuleType("blockchain_stub")
blockchain_stub.get_btc_balance = lambda address: None
blockchain_stub.get_ltc_balance = lambda address: None
blockchain_stub.get_polygon_balance = lambda address: None
blockchain_stub.get_wallet_assets = lambda address: []
blockchain_stub.get_tron_wallet_info = lambda address: None

sys.modules.setdefault("app.utils.blockchains.bitcoin", blockchain_stub)
sys.modules.setdefault("app.utils.blockchains.litecoin", blockchain_stub)
sys.modules.setdefault("app.utils.blockchains.polygon", blockchain_stub)
sys.modules.setdefault("app.utils.blockchains.cardano", blockchain_stub)
sys.modules.setdefault("app.utils.blockchains.erc20", blockchain_stub)
sys.modules.setdefault("app.utils.blockchains.solana", blockchain_stub)
sys.modules.setdefault("app.utils.blockchains.tron", blockchain_stub)

services_stub = types.ModuleType("services_stub")

class DummyExchangeAPI:
    def __init__(self, *args, **kwargs):
        pass

    def get_portfolio_assets(self):
        return []

services_stub.CoinbaseAPI = DummyExchangeAPI
services_stub.KrakenAPI = DummyExchangeAPI

sys.modules.setdefault("app.services.coinbase_api_service", services_stub)
sys.modules.setdefault("app.services.kraken_api_service", services_stub)

import pytest

from app.models.asset import Asset
from app.models.portfolio import Portfolio
from app.models.token import Token


def test_token_defaults_and_fields():
    token = Token()

    assert token.name == ""
    assert token.symbol == ""
    assert token.blockchain == ""
    assert token.description == ""
    assert token.logo == ""
    assert token.contracts == []


def test_asset_formatted_output_with_price():
    asset = Asset(name="Bitcoin", symbol="BTC", blockchain="Bitcoin", address="addr", balance=1.5, price=20000)

    output = asset.table_format()

    assert output[0]["value"] == "BTC"
    assert output[1]["value"] == "Bitcoin"
    assert output[2]["value"] == "addr"
    assert output[3]["value"] == "1.5000"
    assert output[4]["value"] == "20000.00000000"
    assert output[5]["value"] == "$30,000.00"
    assert output[6]["value"] == "USD"


def test_asset_formatted_output_without_price():
    asset = Asset(name="Bitcoin", symbol="BTC", address="addr", balance=1.5, price=None)

    output = asset.table_format()

    assert output[4]["value"] == "N/A"


def test_portfolio_add_remove_assets(monkeypatch):
    monkeypatch.setattr(Portfolio, "get_assets", lambda self: None)
    portfolio = Portfolio(name="Test", portfolio_type="wallet")

    asset = Asset(name="Bitcoin", symbol="BTC", balance=1)
    portfolio.add_asset(asset)

    assert portfolio.assets == [asset]

    portfolio.remove_asset("Bitcoin")

    assert portfolio.assets == []


def test_portfolio_export_assets_creates_csv(monkeypatch, tmp_path):
    monkeypatch.setattr(Portfolio, "get_assets", lambda self: None)
    monkeypatch.chdir(tmp_path)

    export_dir = tmp_path / "export"
    export_dir.mkdir()

    portfolio = Portfolio(name="Test", portfolio_type="wallet")
    asset = Asset(name="Bitcoin", symbol="BTC", balance=1.25, price=20000)
    asset.id = ""
    portfolio.assets = [asset]

    portfolio.export_assets()

    exported_files = list(export_dir.glob("wallet.test.*.csv"))
    assert len(exported_files) == 1

    with exported_files[0].open(newline="") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    assert rows[0] == ["Symbol", "ID", "Balance", "Price"]
    assert rows[1] == ["BTC", "", "1.25", "20000"]
