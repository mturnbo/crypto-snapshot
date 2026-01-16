import requests
from app.utils.blockchains.litecoin import get_ltc_balance


class DummyResponse:
    def __init__(self, json_data, status_code):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.HTTPError(f"HTTP {self.status_code}")


def test_get_ltc_balance_success(monkeypatch):
    address = "ltc_address_placeholder"
    payload = {"final_balance": 12_345_678}

    def fake_get(*args, **kwargs):
        return DummyResponse(payload, 200)

    monkeypatch.setattr(requests, "get", fake_get)
    balance = get_ltc_balance(address)
    assert balance == 12_345_678 / 100_000_000


def test_get_ltc_balance_invalid_address(monkeypatch):
    address = "invalid_ltc_address"

    def fake_get(*args, **kwargs):
        return DummyResponse({}, 404)

    monkeypatch.setattr(requests, "get", fake_get)
    balance = get_ltc_balance(address)
    assert balance is None


def test_get_ltc_balance_connection_error(monkeypatch):
    address = "ltc_address_placeholder"

    def fake_get(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Failed to establish a connection")

    monkeypatch.setattr(requests, "get", fake_get)
    balance = get_ltc_balance(address)
    assert balance is None


def test_get_ltc_balance_unexpected_error(monkeypatch):
    address = "ltc_address_placeholder"

    def fake_get(*args, **kwargs):
        raise ValueError("Unexpected error occurred")

    monkeypatch.setattr(requests, "get", fake_get)
    balance = get_ltc_balance(address)
    assert balance is None
