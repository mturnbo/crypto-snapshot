from unittest.mock import Mock
import requests
import pytest

from app.services.api.cmc_api_service import CoinMarketCapAPI


def test_make_request_success(monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '{"data": {"symbol": "BTC", "price": 30000}, "cached": true}'
    mock_response.from_cache = True

    api_instance = CoinMarketCapAPI(api_key="dummy_api_key")
    monkeypatch.setattr(api_instance.session, "get", lambda *args, **kwargs: mock_response)

    result = api_instance.make_request(endpoint="/test-endpoint", params={"symbol": "BTC"})

    assert result == {
        "data": {"symbol": "BTC", "price": 30000},
        "cached": True,
    }


def test_make_request_json_decode_error(monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Invalid JSON"

    api_instance = CoinMarketCapAPI(api_key="dummy_api_key")
    monkeypatch.setattr(api_instance.session, "get", lambda *args, **kwargs: mock_response)

    result = api_instance.make_request(endpoint="/test-endpoint", params={"symbol": "BTC"})

    assert result == "Invalid JSON"


def test_make_request_request_exception(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.RequestException("Request failed")

    api_instance = CoinMarketCapAPI(api_key="dummy_api_key")
    monkeypatch.setattr(api_instance.session, "get", mock_get)

    with pytest.raises(requests.RequestException):
        api_instance.make_request(endpoint="/test-endpoint", params={"symbol": "BTC"})
