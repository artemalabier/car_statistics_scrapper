import urllib
import re
import requests
from bs4 import BeautifulSoup



class Car:
    def __init__(self, id, title, link, price):
        self.id = id
        self.title = title
        self.link = link
        self.price = price


def fetch_olx_car_data(url):
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
                price = extract_price(price_elem.text.strip()) if price_elem else 'N/A'

                # Create a Car instance and add it to the set
                car = Car(id, title, link, price)
                cars.add(car)

            return cars

        else:
            print(f'Failed to fetch data. Status code: {response.status_code}')

    except Exception as e:
        print(f'An error occurred: {str(e)}')


def url_read(filename):
    car_urls = {}
    with open(filename, 'r') as file:
        for line in file:
            car_name, car_url = line.strip().split(': ')
            car_urls[car_name] = car_url
    return car_urls


def cars_to_set(car_urls):
    all_cars = {}
    for car_name, car_url in car_urls.items():
        car_data = fetch_olx_car_data(car_url)
        if car_data:
            all_cars[car_name] = car_data
    return all_cars


# Function to extract and convert price to EUR
def extract_price(price_text):
    # Define the current EUR/PLN exchange rate (replace with the actual rate)

    # Use regular expressions to extract the numeric part of the price
    #price_match = re.search(r'([\d,\.]+)', price_text)
    price_match = re.search(r'([\d\s,]+[.,]*[\d]*)', price_text)

    if price_match:
        # Remove spaces and commas, and replace comma with period for correct float conversion
        cleaned_price = price_match.group(1).replace(' ', '').replace(',', '').replace('.', '')

        # Convert to float
        numeric_price = float(cleaned_price)

        # Check if the price text contains EUR symbol
        if '€' in price_text:
            # If EUR is present, return the numeric value
            return round(numeric_price)
        elif 'zł' in price_text:
            # If PLN is present, convert to EUR
            price_in_eur = numeric_price / eur_to_pln_rate
            return round(price_in_eur)

    return 'N/A'  # Return 'N/A' for unsupported formats


def get_exchange_rate():
    try:
        # Define the base URL for the exchange rate API
        base_url = 'http://api.exchangeratesapi.io/v1/latest?access_key=563a0d673a2f0b71544fb07b856c7686&format=1&symbols=PLN'
        response = requests.get(base_url)

        if response.status_code == 200:
            # Parse the JSON response to get the exchange rate data
            exchange_rate_data = response.json()
            print(f'[INFO] Received rate is {exchange_rate_data}')

            # Extract the PLN to EUR exchange rate
            pln_to_eur_rate = exchange_rate_data['rates']['PLN']

            print(f'[INFO] Received rate is {pln_to_eur_rate}')
            return pln_to_eur_rate

        else:
            print(f'Failed to fetch exchange rate. Status code: {response.status_code}')

    except Exception as e:
        print(f'An error occurred: {str(e)}')

    print(f'[WARN] No rate fetched, using the default')
    return 4.55


if __name__ == '__main__':
    filename = 'prefiltered.txt'
    eur_to_pln_rate = get_exchange_rate()  # 1 EUR = 4.55 PLN (for example)

    # Read car names and URLs from the file using url_read()
    car_urls = url_read(filename)

    # Create separate sets of Car objects for each URL using cars_to_set()
    all_cars = cars_to_set(car_urls)

    # Print or further process the collected car data
    for car_name, cars in all_cars.items():
        print(f'Car Name: {car_name}')
        for car in cars:
            print(f'ID: {car.id}')
            print(f'Title: {car.title}')
            print(f'Link: {car.link}')
            print(f'Price: {car.price}')
            print('-' * 30)
