import urllib
import requests
from bs4 import BeautifulSoup

from analysis import get_exchange_rate
from data_parser import extract_price


class Car:
    def __init__(self, id, title, link, price):
        self.id = id
        self.title = title
        self.link = link
        self.price = price


def fetch_olx_car_data(url):
    eur_to_pln_rate = 4.576452
    eur_to_pln_rate = get_exchange_rate()

    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all car listings
            car_listings = soup.find_all('div', {'data-cy': 'l-card'})

            # Create a set to store Car objects
            cars = set()

            for car_listing in car_listings:
                # Extract data for each car listing
                id = car_listing['id']

                title_elem = car_listing.find('h6', class_='css-16v5mdi er34gjf0')
                title = title_elem.text.strip() if title_elem else 'N/A'

                link_elem = car_listing.findNext('a', class_='css-rc5s2u')
                link = link_elem['href'] if link_elem and 'href' in link_elem.attrs else 'N/A'
                if link.startswith('/'):
                    # Add the base OLX URL to the PT link
                    link = urllib.parse.urljoin('https://www.olx.pt', link)

                price_elem = car_listing.find('p', {'data-testid': 'ad-price'})
                price = extract_price(price_elem.text.strip(), eur_to_pln_rate) if price_elem else 'N/A'

                # Create a Car instance and add it to the set
                car = Car(id, title, link, price)
                cars.add(car)

            return cars

        else:
            print(f'Failed to fetch data. Status code: {response.status_code}')

    except Exception as e:
        print(f'An error occurred: {str(e)}')


