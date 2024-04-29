import json
import pytest
from unittest.mock import patch, MagicMock
from src.data_parser import url_read, extract_price, get_exchange_rate
from test_data_utils import mock_open, mock_requests_get
from conf.configuration import DEFAULT_EXCHANGE_RATE


def test_url_read_file_not_found(mock_open):
    mock_open.side_effect = FileNotFoundError
    with pytest.raises(FileNotFoundError):
        url_read("nonexistent_file.json")


def test_url_read_json_decode_error(mock_open):
    mock_open.return_value.__enter__.return_value = MagicMock()
    mock_open.return_value.__enter__.return_value.read.side_effect = json.JSONDecodeError("", "", 0)
    with pytest.raises(json.JSONDecodeError):
        url_read("malformed_json_file.json")


@pytest.mark.parametrize("response_status_code,expected_rate", [
    (200, 4.5),
    (404, DEFAULT_EXCHANGE_RATE)
])
def test_get_exchange_rate(response_status_code, expected_rate):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = response_status_code
        mock_response.json.return_value = {"rates": {"PLN": 4.5}}
        mock_get.return_value = mock_response

        assert get_exchange_rate() == expected_rate


def test_url_read_valid_json(mock_open):
    # Prepare mock open function
    mock_open.return_value.__enter__.return_value = MagicMock()
    mock_open.return_value.__enter__.return_value.read.return_value = '{"key": "value"}'
    data = url_read("test.json")
    assert data == {"key": "value"}


def test_extract_price():
    eur_to_pln_rate = 4.5  # Assume an exchange rate for testing

    # Test price in EUR
    price_text_eur = "100€"
    assert extract_price(price_text_eur, eur_to_pln_rate) == 100

    # Test price in PLN
    price_text_pln = "9000zł"
    assert extract_price(price_text_pln, eur_to_pln_rate) == 2000


def test_get_exchange_rate_success(mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"PLN": 4.5}}
    mock_requests_get.return_value = mock_response

    assert get_exchange_rate() == 4.5


def test_get_exchange_rate_failure(mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_requests_get.return_value = mock_response

    assert get_exchange_rate() == DEFAULT_EXCHANGE_RATE


def test_get_exchange_rate_exception(mock_requests_get):
    mock_requests_get.side_effect = Exception("API request failed")
    assert get_exchange_rate() == DEFAULT_EXCHANGE_RATE
