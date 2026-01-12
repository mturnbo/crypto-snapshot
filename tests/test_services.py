import base64
import hashlib
import hmac
import json
import os
import sys
import types
import urllib.parse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

sys.modules.setdefault("dotenv", types.SimpleNamespace(load_dotenv=lambda: None))
os.environ.setdefault("BINANCEUS_API_KEY", "test-key")
os.environ.setdefault("BINANCEUS_API_SECRET", "test-secret")

dateutil_parser_stub = types.ModuleType("dateutil.parser")
dateutil_parser_stub.parse = lambda value: value
dateutil_stub = types.ModuleType("dateutil")
dateutil_stub.parser = dateutil_parser_stub
sys.modules.setdefault("dateutil", dateutil_stub)
sys.modules.setdefault("dateutil.parser", dateutil_parser_stub)

sys.modules.pop("app.services.coinbase_api_service", None)
sys.modules.pop("app.services.kraken_api_service", None)

class DummyResponse:
    def __init__(self, text, status_code=200, from_cache=False):
        self.text = text
        self.status_code = status_code
        self.from_cache = from_cache

class DummyCachedSession:
    def __init__(self, *args, **kwargs):
        self.headers = {}

    def get(self, url, params=None, timeout=None):
        payload = {"symbol": params.get("symbol", ""), "price": "1"}
        return DummyResponse(json.dumps(payload), status_code=200, from_cache=False)

requests_cache_stub = types.ModuleType("requests_cache")
requests_cache_stub.CachedSession = DummyCachedSession
sys.modules.setdefault("requests_cache", requests_cache_stub)

requests_stub = types.ModuleType("requests")
requests_stub.exceptions = types.SimpleNamespace(RequestException=Exception)
sys.modules.setdefault("requests", requests_stub)

rich_pretty_stub = types.ModuleType("rich.pretty")
rich_pretty_stub.pprint = lambda *args, **kwargs: None
sys.modules.setdefault("rich.pretty", rich_pretty_stub)

serialization_stub = types.ModuleType("cryptography.hazmat.primitives.serialization")
serialization_stub.load_pem_private_key = lambda key, password=None: "loaded-key"

hazmat_stub = types.ModuleType("cryptography.hazmat.primitives")
hazmat_stub.serialization = serialization_stub

cryptography_stub = types.ModuleType("cryptography")
cryptography_hazmat_stub = types.ModuleType("cryptography.hazmat")
cryptography_hazmat_stub.primitives = hazmat_stub

sys.modules.setdefault("cryptography", cryptography_stub)
sys.modules.setdefault("cryptography.hazmat", cryptography_hazmat_stub)
sys.modules.setdefault("cryptography.hazmat.primitives", hazmat_stub)
sys.modules.setdefault("cryptography.hazmat.primitives.serialization", serialization_stub)

jwt_stub = types.ModuleType("jwt")
jwt_stub.encode = lambda payload, key, algorithm=None, headers=None: "jwt-token"
sys.modules.setdefault("jwt", jwt_stub)

coinbase_rest_stub = types.ModuleType("coinbase.rest")

class DummyRESTClient:
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key
        self.api_secret = api_secret

    def get_portfolios(self):
        return {"portfolios": [{"uuid": "portfolio-1"}]}

    def get_portfolio_breakdown(self, portfolio_uuid=None):
        return {"breakdown": {"spot_positions": []}}

    def get_product(self, trade_pair):
        return {"trade_pair": trade_pair}

coinbase_rest_stub.RESTClient = DummyRESTClient
sys.modules.setdefault("coinbase.rest", coinbase_rest_stub)

kraken_spot_stub = types.ModuleType("kraken.spot")

class DummyKrakenUser:
    def __init__(self, key=None, secret=None):
        self.key = key
        self.secret = secret

    def get_account_balance(self):
        return {}

kraken_spot_stub.User = DummyKrakenUser
sys.modules.setdefault("kraken.spot", kraken_spot_stub)

from app.services.api.binance_api_service import BinanceUSAPI
from app.services.api.cmc_api_service import CoinMarketCapAPI
from app.services.api.coinbase_api_service import CoinbaseAPI
from app.services.api.kraken_api_service import KrakenAPI


def test_binance_signature_matches_expected():
    api = BinanceUSAPI("key", "secret")
    params = {"timestamp": 123, "recvWindow": 5000}
    expected = hmac.new(
        b"secret",
        urllib.parse.urlencode(params).encode(),
        hashlib.sha256,
    ).hexdigest()

    assert api.get_binanceus_signature(params) == expected


def test_binance_make_request_adds_cached_and_signature(monkeypatch):
    api = BinanceUSAPI("key", "secret")

    class Session:
        def __init__(self):
            self.headers = {}
            self.last_params = None

        def get(self, url, params=None, timeout=None):
            self.last_params = params
            return DummyResponse("{}", status_code=200, from_cache=True)

    api._session = Session()

    response = api.make_request("/account", {"timestamp": 123})

    assert response["cached"] is True
    assert "signature" in api._session.last_params


def test_cmc_get_token_info_parses_contracts():
    api = CoinMarketCapAPI(api_key="token")

    def fake_request(endpoint, params):
        return {
            "data": {
                "BTC": [
                    {
                        "name": "Bitcoin",
                        "description": "desc",
                        "logo": "logo",
                        "date_launched": "2020-01-01",
                        "self_reported_circulating_supply": "100",
                        "contract_address": [
                            {
                                "contract_address": "0x1",
                                "platform": {"name": "Ethereum", "coin": {"symbol": "ETH"}},
                            }
                        ],
                    }
                ]
            }
        }

    api.make_request = fake_request

    info = api.get_token_info("BTC")

    assert info["name"] == "Bitcoin"
    assert info["contracts"] == [
        {
            "address": "0x1",
            "platform_name": "Ethereum",
            "platform_symbol": "ETH",
        }
    ]


def test_cmc_get_token_prices_returns_mapping():
    api = CoinMarketCapAPI(api_key="token")
    captured_params = []

    def fake_request(endpoint, params):
        try:
            if len(symbols) == 1:
                symbol = symbols[0]
                params = {
                    'symbol': symbol,
                    'convert': currency,
                }

                response = self.make_request(endpoint, params)
        except:
            captured_params.append(params["symbol"])
            return {
                "data": {
                    "BTC": [{"quote": {"USD": {"price": 1}}}],
                    "ETH": [{"quote": {"USD": {"price": 2}}}],
                }
            }

    api.make_request = fake_request

    prices = api.get_token_prices(["BTC", "ETH"], currency="USD")

    assert prices == {"BTC": 1.0, "ETH": 2.0}
    assert captured_params == ["BTC,ETH"]


def test_coinbase_get_portfolio_assets_builds_assets(monkeypatch):
    secret = base64.b64encode(b"secret").decode("utf-8")
    api = CoinbaseAPI("key", secret)

    monkeypatch.setattr(
        api,
        "get_portfolio_data",
        lambda: {
            "breakdown": {
                "spot_positions": [
                    {"asset": "BTC", "total_balance_fiat": 20000, "total_balance_crypto": 1}
                ]
            }
        },
    )

    assets = api.get_portfolio_assets()

    assert len(assets) == 1
    assert assets[0].symbol == "BTC"
    assert assets[0].price == 20000


def test_coinbase_build_jwt_returns_token():
    secret = base64.b64encode(b"secret").decode("utf-8")
    api = CoinbaseAPI("key", secret)

    token = api.build_jwt("/products", b"dummy-key")

    assert token == "jwt-token"


def test_kraken_get_portfolio_assets_uses_prices(monkeypatch):
    api = KrakenAPI("key", "secret")

    monkeypatch.setattr(api, "get_portfolio_data", lambda: {"BTC": "1.5", "ETH": "2"})
    monkeypatch.setattr(api, "get_prices", lambda tokens: {"BTC": 100})

    assets = api.get_portfolio_assets()

    assert [asset.symbol for asset in assets] == ["BTC", "ETH"]
    assert assets[0].price == 100
