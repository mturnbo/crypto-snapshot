from unittest.mock import patch, Mock

import pytest
from app.utils.blockchains.vechain import get_vechain_balance


@pytest.fixture
def mock_response_success():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {
        "status": {"success": True},
        "data": {"vet": "123.45"}
    }
    return mock


@pytest.fixture
def mock_response_failure():
    mock = Mock()
    mock.status_code = 400
    mock.json.return_value = {
        "status": {"success": False},
        "data": {}
    }
    return mock


@pytest.fixture
def mock_response_error():
    mock = Mock()
    mock.raise_for_status.side_effect = Exception("Request failed")
    return mock


def test_get_vechain_balance_success(mock_response_success):
    with patch("app.utils.blockchains.vechain.requests.get", return_value=mock_response_success):
        wallet_address = "0x1234567890abcdef"
        balance = get_vechain_balance(wallet_address)
        assert balance == 123.45


def test_get_vechain_balance_failure(mock_response_failure):
    with patch("app.utils.blockchains.vechain.requests.get", return_value=mock_response_failure):
        wallet_address = "0x1234567890abcdef"
        balance = get_vechain_balance(wallet_address)
        assert balance == 0


def test_get_vechain_balance_request_exception(mock_response_error):
    with patch("app.utils.blockchains.vechain.requests.get", return_value=mock_response_error):
        wallet_address = "0x1234567890abcdef"
        balance = get_vechain_balance(wallet_address)
        assert balance is None
