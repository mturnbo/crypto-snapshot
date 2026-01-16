import pytest
from app.utils.blockchains.polygon import get_polygon_balance
from web3 import Web3


class DummyWeb3:
    def __init__(self, balance_wei):
        self.balance_wei = balance_wei

    class Eth:
        def __init__(self, balance_wei):
            self.balance_wei = balance_wei

        def get_balance(self, address):
            return self.balance_wei

    def __getattr__(self, item):
        if item == 'eth':
            return self.Eth(self.balance_wei)


@pytest.fixture
def mock_web3(monkeypatch):
    def mock_provider(*args, **kwargs):
        return DummyWeb3(1234567890000000000)  # Example balance in wei

    monkeypatch.setattr(Web3, 'HTTPProvider', mock_provider)


def test_get_polygon_balance_success(mock_web3):
    wallet_address = "0x1234567890abcdef1234567890abcdef12345678"
    expected_balance = 1.23456789  # Convert 1234567890000000000 wei to ether
    actual_balance = get_polygon_balance(wallet_address)
    assert expected_balance == actual_balance


def test_get_polygon_balance_none(mock_web3, monkeypatch):
    class MockEth:
        @staticmethod
        def get_balance(address):
            return None

    class MockWeb3:
        eth = MockEth()

    monkeypatch.setattr(Web3, "HTTPProvider", lambda *args, **kwargs: MockWeb3())
    wallet_address = "0x1234567890abcdef1234567890abcdef12345678"
    assert get_polygon_balance(wallet_address) is None
