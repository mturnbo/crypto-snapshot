import requests
from app.utils.blockchains.tron import get_tron_balance


class DummyResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"HTTP Error: {self.status_code}")


def test_get_tron_balance_success(monkeypatch):
    wallet_address = "valid_wallet_address"
    payload = {"data": [{"balance": 1_234_567_890}]}

    def fake_get(*args, **kwargs):
        return DummyResponse(payload, 200)

    monkeypatch.setattr(requests, "get", fake_get)
    balance = get_tron_balance(wallet_address)
    assert balance == 1_234_567_890 / 1_000_000


def test_get_tron_balance_empty_data(monkeypatch):
    wallet_address = "empty_data_wallet"
    payload = {"data": []}

    def fake_get(*args, **kwargs):
        return DummyResponse(payload, 200)

    monkeypatch.setattr(requests, "get", fake_get)
    balance = get_tron_balance(wallet_address)
    assert balance == 0.0


def test_get_tron_balance_no_data_key(monkeypatch):
    wallet_address = "no_data_key_wallet"
    payload = {}

    def fake_get(*args, **kwargs):
        return DummyResponse(payload, 200)

    monkeypatch.setattr(requests, "get", fake_get)
    balance = get_tron_balance(wallet_address)
    assert balance == 0.0


def test_get_tron_balance_http_error(monkeypatch):
    wallet_address = "http_error_wallet"

    def fake_get(*args, **kwargs):
        return DummyResponse(None, 404)  # Simulate HTTP 404 Not Found

    monkeypatch.setattr(requests, "get", fake_get)
    balance = get_tron_balance(wallet_address)
    assert balance is None


def test_get_tron_balance_request_exception(monkeypatch):
    wallet_address = "exception_wallet"

    def fake_get(*args, **kwargs):
        raise requests.exceptions.RequestException("Some error occurred")

    monkeypatch.setattr(requests, "get", fake_get)
    balance = get_tron_balance(wallet_address)
    assert balance is None
