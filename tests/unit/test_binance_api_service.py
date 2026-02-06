from unittest.mock import Mock, patch
import pytest
from app.services.api.binance_api_service import BinanceUSAPI


@pytest.fixture
def api_client():
    return BinanceUSAPI(api_key="test_api_key", api_secret="test_api_secret")


def test_make_request_success(api_client):
    # Arrange
    endpoint = "/test-endpoint"
    params = {"symbol": "BTCUSD"}
    mock_response = Mock()
    mock_response.json.return_value = {"price": "50000"}
    mock_response.text = '{"price": "50000"}'
    mock_response.status_code = 200
    mock_response.from_cache = False

    with patch.object(api_client.session, "get", return_value=mock_response):
        # Act
        response = api_client.make_request(endpoint, params=params, use_signature=False)

        # Assert
        assert response == {"price": "50000", "cached": False}


def test_make_request_failure(api_client):
    # Arrange
    endpoint = "/test-endpoint"
    mock_response = Mock()
    mock_response.text = "Internal Server Error"
    mock_response.status_code = 500

    with patch.object(api_client.session, "get", return_value=mock_response):
        # Act
        response = api_client.make_request(endpoint, use_signature=False)

    # Assert
    assert isinstance(response, Exception)


def test_make_request_with_signature(api_client):
    # Arrange
    endpoint = "/test-endpoint"
    params = {"symbol": "BTCUSD"}
    mock_response = Mock()
    mock_response.json.return_value = {"price": "50000"}
    mock_response.text = '{"price": "50000"}'
    mock_response.status_code = 200
    mock_response.from_cache = True

    with patch.object(api_client, "get_binanceus_signature", return_value="test_signature") as mock_signature:
        with patch.object(api_client.session, "get", return_value=mock_response):
            # Act
            response = api_client.make_request(endpoint, params=params, use_signature=True)

            # Assert
            mock_signature.assert_called_once_with(params)
            assert response == {"price": "50000", "cached": True}
            assert params["signature"] == "test_signature"


def test_make_request_handles_invalid_json(api_client):
    # Arrange
    endpoint = "/test-endpoint"
    mock_response = Mock()
    mock_response.text = "Invalid JSON"
    mock_response.status_code = 200

    with patch.object(api_client.session, "get", return_value=mock_response):
        # Act
        response = api_client.make_request(endpoint, use_signature=False)

        # Assert
        assert isinstance(response, Exception)
