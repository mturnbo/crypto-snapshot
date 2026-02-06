import importlib
from pathlib import Path
import sys
import types

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))


def _install_test_stubs(monkeypatch):
    monkeypatch.setitem(sys.modules, "dotenv", types.SimpleNamespace(load_dotenv=lambda: None))

    rich_module = types.ModuleType("rich")
    rich_console_module = types.ModuleType("rich.console")
    rich_table_module = types.ModuleType("rich.table")
    rich_box_module = types.ModuleType("rich.box")

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

    class DummyBox:
        def __init__(self, *args, **kwargs):
            self.style = ""

    rich_console_module.Console = DummyConsole
    rich_table_module.Table = DummyTable
    rich_box_module.SQUARE_DOUBLE_HEAD = DummyBox()

    monkeypatch.setitem(sys.modules, "rich", rich_module)
    monkeypatch.setitem(sys.modules, "rich.console", rich_console_module)
    monkeypatch.setitem(sys.modules, "rich.table", rich_table_module)
    monkeypatch.setitem(sys.modules, "rich.box", rich_box_module)

    blockchain_stub = types.ModuleType("blockchain_stub")
    blockchain_stub.get_wallet_assets = lambda *args, **kwargs: []
    blockchain_stub.get_btc_asset = lambda *args, **kwargs: None
    blockchain_stub.get_ltc_asset = lambda *args, **kwargs: None
    blockchain_stub.get_cardano_assets = lambda *args, **kwargs: []
    blockchain_stub.get_erc20_assets = lambda *args, **kwargs: []
    blockchain_stub.get_sol_assets = lambda *args, **kwargs: []
    blockchain_stub.get_polygon_assets = lambda *args, **kwargs: None
    blockchain_stub.get_tron_asset = lambda *args, **kwargs: None
    blockchain_stub.get_xrp_asset = lambda *args, **kwargs: None
    blockchain_stub.get_substrate_asset = lambda *args, **kwargs: None
    blockchain_stub.get_vechain_asset = lambda *args, **kwargs: None
    blockchain_stub.get_xlm_asset = lambda *args, **kwargs: None
    blockchain_stub.get_doge_asset = lambda *args, **kwargs: None

    stubbed_blockchains = [
        "app.utils.blockchains.bitcoin",
        "app.utils.blockchains.litecoin",
        "app.utils.blockchains.polygon",
        "app.utils.blockchains.cardano",
        "app.utils.blockchains.erc20",
        "app.utils.blockchains.solana",
        "app.utils.blockchains.tron",
        "app.utils.blockchains.xrp",
        "app.utils.blockchains.substrate",
        "app.utils.blockchains.vechain",
        "app.utils.blockchains.stellar",
        "app.utils.blockchains.dogecoin",
    ]

    for module_name in stubbed_blockchains:
        monkeypatch.setitem(sys.modules, module_name, blockchain_stub)

    services_stub = types.ModuleType("services_stub")

    class DummyExchangeAPI:
        def __init__(self, *args, **kwargs):
            pass

        def get_portfolio_assets(self):
            return []

    services_stub.CoinbaseAPI = DummyExchangeAPI
    services_stub.KrakenAPI = DummyExchangeAPI
    monkeypatch.setitem(sys.modules, "app.services.coinbase_api_service", services_stub)
    monkeypatch.setitem(sys.modules, "app.services.kraken_api_service", services_stub)


@pytest.fixture()
def models_with_stubs(monkeypatch):
    _install_test_stubs(monkeypatch)

    modules_to_clear = [
        "app.models.asset",
        "app.models.portfolio",
        "app.models.token",
        "app.services.assets_service",
    ]
    for module_name in modules_to_clear:
        sys.modules.pop(module_name, None)

    asset_module = importlib.import_module("app.models.asset")
    portfolio_module = importlib.import_module("app.models.portfolio")
    token_module = importlib.import_module("app.models.token")

    yield asset_module.Asset, portfolio_module.Portfolio, token_module.Token

    for module_name in modules_to_clear:
        sys.modules.pop(module_name, None)
