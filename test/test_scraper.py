import os
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from src.scraper import fetch_olx_car_data, Car
from test_data_utils import mock_requests_get, mock_beautiful_soup


def test_fetch_olx_car_data_success(mock_requests_get, mock_beautiful_soup):
    with open("mock_page_olx.html", "r") as file:
        html_content = file.read()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = html_content
    mock_requests_get.return_value = mock_response

    # Mock BeautifulSoup to parse the HTML response
    mock_soup = MagicMock(spec=BeautifulSoup)
    mock_beautiful_soup.return_value = mock_soup

    # Mock find_all to return multiple mock elements (simulate car listings)
    mock_soup.find_all.return_value = [
        MagicMock(spec=BeautifulSoup.find_all),  # Mock element for first car
        MagicMock(spec=BeautifulSoup.find_all),  # Mock element for second car (optional)
    ]

    # Mock get_exchange_rate to return a fixed rate
    with patch("src.scraper.get_exchange_rate") as mock_exchange_rate:
        mock_exchange_rate.return_value = 4.5

        # Test case: Valid data returned
        cars = fetch_olx_car_data("https://www.example.com/car_data")  # Pass URL as a string
        assert cars == {Car(id=653882995, title='Car1', link='https://www.olx.pt/car1', price=100)}


def test_fetch_olx_car_data_failure(mock_requests_get):
    # Mock requests.get to return a failure response
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_requests_get.return_value = mock_response

    # Test case: Failed to fetch data
    assert fetch_olx_car_data("test_url") is None


def test_fetch_olx_car_data_exception(mock_requests_get):
    # Mock requests.get to raise an exception
    mock_requests_get.side_effect = Exception("Request failed")

    # Test case: Exception occurred during request
    assert fetch_olx_car_data("test_url") is None
