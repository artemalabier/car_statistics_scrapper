from src.analysis import (
    fetch_cars_for_country,
    collect_cars,
    calculate_median,
    calculate_percentage_difference,
    calculate_price_coefficients
)
from test_data_utils import get_test_car_data, mock_fetch_olx_car_data


def test_fetch_cars_for_country(mock_fetch_olx_car_data):
    # Mock the fetch_olx_car_data function
    mock_fetch_olx_car_data.return_value = [{"price": 100}, {"price": 200}]

    # Test case: Valid data returned
    assert fetch_cars_for_country("test_url") == [{"price": 100}, {"price": 200}]

    # Test case: Empty list returned
    mock_fetch_olx_car_data.return_value = None
    assert fetch_cars_for_country("test_url") == []


def test_collect_cars(mock_fetch_olx_car_data):
    # Mock the fetch_olx_car_data function
    mock_fetch_olx_car_data.side_effect = [
        [{"price": 100}, {"price": 200}],  # Data for PL
        [{"price": 150}, {"price": 250}]  # Data for PT
    ]

    # Test case: Valid data for both countries
    car_urls = {"Car1": {"PL": "pl_url", "PT": "pt_url"}}
    assert collect_cars(car_urls) == [{"Car1": {"PL": [{"price": 100}, {"price": 200}],
                                                "PT": [{"price": 150}, {"price": 250}]}}]

    # Test case: Empty data for PL
    mock_fetch_olx_car_data.side_effect = [
        None,  # Data for PL
        [{"price": 150}, {"price": 250}]  # Data for PT
    ]
    assert collect_cars(car_urls) == [{"Car1": {"PL": [], "PT": [{"price": 150}, {"price": 250}]}}]


def test_calculate_median():
    # Test case: Valid prices
    assert calculate_median([100, 200, 300]) == 200

    # Test case: Empty list
    assert calculate_median([]) is None


def test_calculate_percentage_difference():
    # Test case: Valid prices
    assert calculate_percentage_difference(100, 150) == 50.0

    # Test case: One or both prices are None
    assert calculate_percentage_difference(None, 150) is None
    assert calculate_percentage_difference(100, None) is None
    assert calculate_percentage_difference(None, None) is None


def test_calculate_price_coefficients():
    all_cars_data = get_test_car_data()

    # Test case: Valid data
    expected_coefficients = [{"Car1": 50.0}]
    assert calculate_price_coefficients(all_cars_data) == expected_coefficients

    # Test case: Empty data
    assert calculate_price_coefficients([]) == []
