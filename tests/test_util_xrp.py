import requests
from app.utils.blockchains.xrp import get_xrp_balance


class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.RequestException(f"HTTP {self.status_code}")


def test_get_xrp_balance_success(monkeypatch):
    wallet_address = "rExampleAddress123"
    payload = {"xrpBalance": "123.456"}

    def fake_get(*args, **kwargs):
        return DummyResponse(payload)

    monkeypatch.setattr(requests, "get", fake_get)
    balance = get_xrp_balance(wallet_address)
    assert balance == 123.456


def test_get_xrp_balance_error(monkeypatch):
    wallet_address = "rExampleAddress123"

    def fake_get(*args, **kwargs):
        raise requests.exceptions.RequestException("Error fetching data")

    monkeypatch.setattr(requests, "get", fake_get)
    balance = get_xrp_balance(wallet_address)
    assert balance is None


def test_get_xrp_balance_invalid_status(monkeypatch):
    wallet_address = "rExampleAddress123"

    def fake_get(*args, **kwargs):
        return DummyResponse({}, status_code=500)

    monkeypatch.setattr(requests, "get", fake_get)
    balance = get_xrp_balance(wallet_address)
    assert balance is None


def test_get_xrp_balance_malformed_json(monkeypatch):
    wallet_address = "rExampleAddress123"

    class MalformedResponse(DummyResponse):
        def json(self):
            raise ValueError("Malformed JSON")

    def fake_get(*args, **kwargs):
        return MalformedResponse({}, status_code=200)

    monkeypatch.setattr(requests, "get", fake_get)
    balance = get_xrp_balance(wallet_address)
    assert balance is None
