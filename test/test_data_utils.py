import pytest
from unittest.mock import patch, MagicMock
from src.scraper import Car


@pytest.fixture
def mock_fetch_olx_car_data():
    with patch("src.analysis.fetch_olx_car_data") as mock_fetch:
        yield mock_fetch


@pytest.fixture
def mock_open():
    with patch("builtins.open", MagicMock()) as mock_file:
        yield mock_file


@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        yield mock_get


@pytest.fixture
def mock_beautiful_soup():
    with patch("src.scraper.BeautifulSoup") as mock_bs:
        yield mock_bs


def get_test_car_data():
    car1_pl_data = [
        Car(id=1, title="Car1", link="link1", price=100),
        Car(id=2, title="Car1", link="link2", price=100)
    ]
    car1_pt_data = [
        Car(id=3, title="Car1", link="link3", price=150),
        Car(id=4, title="Car1", link="link4", price=150)
    ]

    car2_pl_data = []  # Empty data for PL
    car2_pt_data = [
        Car(id=5, title="Car2", link="link5", price=300),
        Car(id=6, title="Car2", link="link6", price=300)
    ]

    all_cars_data = [
        {"Car1": {"PL": car1_pl_data, "PT": car1_pt_data}},
        {"Car2": {"PL": car2_pl_data, "PT": car2_pt_data}}
    ]

    return all_cars_data
