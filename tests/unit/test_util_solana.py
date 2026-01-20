import requests
from app.utils.blockchains.solana import get_sol_balance


class DummyResponse:
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data


def test_get_sol_balance_success(monkeypatch):
    wallet_address = "sol_wallet_placeholder"
    payload = {
        "jsonrpc": "2.0",
        "result": {
            "value": 1_234_567_890
        },
        "id": 1
    }

    def fake_post(*args, **kwargs):
        return DummyResponse(payload)

    monkeypatch.setattr(requests, "post", fake_post)
    balance = get_sol_balance(wallet_address)
    assert balance == 1.23456789


def test_get_sol_balance_zero_balance(monkeypatch):
    wallet_address = "sol_wallet_placeholder"
    payload = {
        "jsonrpc": "2.0",
        "result": {
            "value": 0
        },
        "id": 1
    }

    def fake_post(*args, **kwargs):
        return DummyResponse(payload)

    monkeypatch.setattr(requests, "post", fake_post)
    balance = get_sol_balance(wallet_address)
    assert balance == 0.0


def test_get_sol_balance_api_error(monkeypatch):
    wallet_address = "sol_wallet_placeholder"
    payload = {
        "jsonrpc": "2.0",
        "error": {
            "code": -32602,
            "message": "Invalid params"
        },
        "id": 1
    }

    def fake_post(*args, **kwargs):
        return DummyResponse(payload)

    monkeypatch.setattr(requests, "post", fake_post)
    try:
        get_sol_balance(wallet_address)
    except KeyError:
        assert True
    else:
        assert False
