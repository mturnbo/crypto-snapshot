import requests
from app.utils.blockchains.bitcoin import get_btc_balance


class DummyResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


def test_get_btc_balance_success(monkeypatch):
    address = "btc_address_placeholder"
    payload = {address: {"final_balance": 12_345_678}}

    def fake_get(*args, **kwargs):
        return DummyResponse(payload)

    monkeypatch.setattr(requests, "get", fake_get)

    balance = get_btc_balance(address)
    assert balance == 12_345_678 / 100_000_000


def test_get_btc_balance_address_not_found(monkeypatch):
    address = "btc_address_placeholder"
    payload = {"other_address": {"final_balance": 1}}

    def fake_get(*args, **kwargs):
        return DummyResponse(payload)

    monkeypatch.setattr(requests, "get", fake_get)

    balance = get_btc_balance(address)
    assert balance is None


def test_get_btc_balance_request_exception(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.exceptions.RequestException("network error")

    monkeypatch.setattr(requests, "get", fake_get)

    balance = get_btc_balance("btc_address_placeholder")
    assert balance is None


def test_get_btc_balance_unexpected_exception(monkeypatch):
    class BadResponse:
        def raise_for_status(self):
            pass

        def json(self):
            raise ValueError("bad json")

    def fake_get(*args, **kwargs):
        return BadResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    balance = get_btc_balance("btc_address_placeholder")
    assert balance is None
