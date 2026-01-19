import pytest
from unittest.mock import MagicMock, patch
from app.models.asset import Asset
from app.services.api.cmc_api_service import CoinMarketCapAPI


@pytest.fixture
def mock_env_and_cmc():
    cmc_mock = MagicMock(spec=CoinMarketCapAPI)
    with patch("app.models.asset.load_dotenv"), patch("app.models.asset.CoinMarketCapAPI", return_value=cmc_mock):
        yield cmc_mock


def test_get_price_success(mock_env_and_cmc):
    mock_env_and_cmc.get_token_prices.return_value = 123.45

    asset = Asset(name="Ethereum", symbol="ETH", blockchain="Ethereum", balance=1.0)
    asset.get_current_price(currency="USD")

    assert asset.price == 123.45
    mock_env_and_cmc.get_token_prices.assert_called_once_with(["ETH"], "USD")


def test_get_price_no_key(mock_env_and_cmc):
    with patch("os.getenv", side_effect=lambda key: None if key == "COINMARKETCAP_API_KEY" else "some_value"):
        asset = Asset(name="Ethereum", symbol="ETH", blockchain="Ethereum", balance=1.0)
        with pytest.raises(Exception):
            asset.get_current_price(currency="USD")


def test_get_price_api_error(mock_env_and_cmc):
    mock_env_and_cmc.get_token_prices.side_effect = Exception("CMC API error")

    asset = Asset(name="Ethereum", symbol="ETH", blockchain="Ethereum", balance=1.0)
    asset.get_current_price(currency="USD")

    assert asset.price == 0  # Assuming fallback is 0 in case of errors
    mock_env_and_cmc.get_token_prices.assert_called_once_with(["ETH"], "USD")
