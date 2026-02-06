import app.utils.blockchains.polygon as polygon


class DummyWeb3:
    class HTTPProvider:
        def __init__(self, url):
            self.url = url

    def __init__(self, provider, balance_wei=None):
        self.provider = provider
        self._balance_wei = balance_wei

    @property
    def eth(self):
        class DummyEth:
            def __init__(self, balance_wei):
                self._balance_wei = balance_wei

            def get_balance(self, address):
                return self._balance_wei

        return DummyEth(self._balance_wei)

    @staticmethod
    def from_wei(value, unit):
        return value / 1e18


def test_get_polygon_balance_success(monkeypatch):
    class MockWeb3:
        HTTPProvider = DummyWeb3.HTTPProvider

        def __init__(self, provider):
            self.provider = provider
            self._balance_wei = 1_234_567_890_000_000_000

        @property
        def eth(self):
            class DummyEth:
                def get_balance(self, address):
                    return 1_234_567_890_000_000_000

            return DummyEth()

        @staticmethod
        def from_wei(value, unit):
            return value / 1e18

    monkeypatch.setattr(polygon, "Web3", MockWeb3)
    wallet_address = "0x1234567890abcdef1234567890abcdef12345678"
    expected_balance = 1.23456789
    actual_balance = polygon.get_polygon_balance(wallet_address)
    assert expected_balance == actual_balance


def test_get_polygon_balance_none(monkeypatch):
    class MockWeb3:
        HTTPProvider = DummyWeb3.HTTPProvider

        def __init__(self, provider):
            self.provider = provider

        @property
        def eth(self):
            class DummyEth:
                def get_balance(self, address):
                    return None

            return DummyEth()

        @staticmethod
        def from_wei(value, unit):
            return value / 1e18

    monkeypatch.setattr(polygon, "Web3", MockWeb3)
    wallet_address = "0x1234567890abcdef1234567890abcdef12345678"
    assert polygon.get_polygon_balance(wallet_address) == 0.0
