import urllib
import requests

from dataclasses import dataclass
from bs4 import BeautifulSoup
from data_parser import extract_price, get_exchange_rate


@dataclass(frozen=True)
class Car:
    id: int
    title: str
    link: str
    price: float

    def __eq__(self, other):
        return isinstance(other, Car) and self.id == other.id

    def __hash__(self):
        return hash(self.id)


def fetch_olx_car_data(url):
    eur_to_pln_rate = get_exchange_rate()

    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            car_listings = soup.find_all('div', {'data-cy': 'l-card'})
            cars = set()

            for car_listing in car_listings:
                id = car_listing['id']

                title_elem = car_listing.find('h6', class_='css-16v5mdi er34gjf0')
                title = title_elem.text.strip() if title_elem else None

                link_elem = car_listing.findNext('a', class_='css-z3gu2d')
                link = link_elem.get('href', None) if link_elem else None
                if link.startswith('/'):
                    link = urllib.parse.urljoin('https://www.olx.pt', link)

                price_elem = car_listing.find('p', {'data-testid': 'ad-price'})
                price = extract_price(price_elem.text.strip(), eur_to_pln_rate) if price_elem else None

                car = Car(id, title, link, price)
                cars.add(car)

            return cars

        else:
            print(f'Failed to fetch data. Status code: {response.status_code}')

    except Exception as e:
        print(f'An error occurred: {str(e)}')


