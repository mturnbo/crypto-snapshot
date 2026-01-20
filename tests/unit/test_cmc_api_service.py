from unittest.mock import Mock

import requests
from app.services.api.cmc_api_service import CoinMarketCapAPI


def test_make_request_success(monkeypatch):
    # Prepare mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '{"data": {"symbol": "BTC", "price": 30000}, "cached": true}'

    def mock_get(*args, **kwargs):
        return mock_response

    # Patch the session's get method
    api_instance = CoinMarketCapAPI(api_key="dummy_api_key")
    monkeypatch.setattr(api_instance.session, "get", mock_get)

    # Call the method
    result = api_instance.make_request(endpoint="/test-endpoint", params={"symbol": "BTC"})

    # Assertions
    assert result == {
        "data": {"symbol": "BTC", "price": 30000},
        "cached": True,
    }


def test_make_request_json_decode_error(monkeypatch):
    # Prepare mock response with incorrect JSON
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Invalid JSON"

    def mock_get(*args, **kwargs):
        return mock_response

    # Patch the session's get method
    api_instance = CoinMarketCapAPI(api_key="dummy_api_key")
    monkeypatch.setattr(api_instance.session, "get", mock_get)

    # Call the method
    result = api_instance.make_request(endpoint="/test-endpoint", params={"symbol": "BTC"})

    # Assertions
    assert result == "Invalid JSON"


def test_make_request_request_exception(monkeypatch):
    # Simulate a request exception
    def mock_get(*args, **kwargs):
        raise requests.RequestException("Request failed")

    # Patch the session's get method
    api_instance = CoinMarketCapAPI(api_key="dummy_api_key")
    monkeypatch.setattr(api_instance.session, "get", mock_get)

    # Call the method
    result = api_instance.make_request(endpoint="/test-endpoint", params={"symbol": "BTC"})

    # Assertions
    assert isinstance(result, requests.RequestException)
    assert "Request failed" in str(result)
