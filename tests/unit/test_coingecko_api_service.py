from unittest.mock import Mock, patch

import pytest


import_response = Mock()
import_response.status_code = 200
import_response.json.return_value = [{"id": "bitcoin"}]

with patch("requests.get", return_value=import_response):
    from app.services.api.coingecko_api_service import CoinGeckoAPI


@pytest.fixture
def api_client():
    return CoinGeckoAPI(api_key="test_api_key")


def test_make_request_success(api_client):
    endpoint = "simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "USD"}
    payload = {"bitcoin": {"usd": 50000}}
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = payload

    with patch(
        "app.services.api.coingecko_api_service.requests.get",
        return_value=mock_response,
    ) as mock_get:
        result = api_client.make_request(endpoint, params=params)

    assert result == payload
    mock_get.assert_called_once_with(
        "https://api.coingecko.com/api/v3/simple/price",
        headers={"x-cg-demo-api-key": "test_api_key"},
        params=params,
    )


def test_make_request_failure_returns_none(api_client, capsys):
    mock_response = Mock()
    mock_response.status_code = 500

    with patch(
        "app.services.api.coingecko_api_service.requests.get",
        return_value=mock_response,
    ):
        result = api_client.make_request("simple/price")

    assert result is None
    assert "Error fetching data from CoinGecko API!" in capsys.readouterr().out


def test_get_token_price_returns_usd_price(api_client):
    with patch.object(
        api_client,
        "make_request",
        return_value={"bitcoin": {"usd": 51234.56}},
    ) as mock_make_request:
        result = api_client.get_token_price("bitcoin")

    assert result == 51234.56
    mock_make_request.assert_called_once_with(
        "simple/price",
        {"ids": "bitcoin", "vs_currencies": "USD"},
    )


def test_get_token_price_uses_requested_currency_parameter(api_client):
    with patch.object(
        api_client,
        "make_request",
        return_value={"bitcoin": {"usd": 51234.56}},
    ) as mock_make_request:
        result = api_client.get_token_price("bitcoin", currency="eur")

    assert result == 51234.56
    mock_make_request.assert_called_once_with(
        "simple/price",
        {"ids": "bitcoin", "vs_currencies": "eur"},
    )


def test_get_token_price_returns_none_when_request_fails(api_client):
    with patch.object(api_client, "make_request", return_value=None):
        result = api_client.get_token_price("bitcoin")

    assert result is None


def test_get_top_tokens_returns_none_when_request_fails(api_client):
    with patch.object(api_client, "make_request", return_value=None) as mock_make_request:
        result = api_client.get_top_tokens(currency="eur")

    assert result is None
    mock_make_request.assert_called_once_with(
        "coins/markets",
        {
            "vs_currency": "eur",
            "order": "market_cap_desc",
            "per_page": 250,
            "page": 1,
            "sparkline": False,
        },
    )


def test_get_top_tokens_returns_response_data(api_client):
    payload = [
        {"id": "bitcoin", "symbol": "btc", "current_price": 51234.56},
        {"id": "ethereum", "symbol": "eth", "current_price": 2500.12},
    ]

    with patch.object(
        api_client,
        "make_request",
        return_value=payload,
    ) as mock_make_request:
        result = api_client.get_top_tokens()

    assert result == payload
    mock_make_request.assert_called_once_with(
        "coins/markets",
        {
            "vs_currency": "USD",
            "order": "market_cap_desc",
            "per_page": 250,
            "page": 1,
            "sparkline": False,
        },
    )
