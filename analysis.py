from statistics import median

import requests


"""def calculate_price_coefficient(car_data_pl, car_data_pt):
    try:
        # Calculate the median price for cars in Poland
        prices_pl = [car['price_pln'] for car in car_data_pl]
        median_price_pl = median(prices_pl)

        # Calculate the median price for cars in Portugal
        prices_pt = [car['price_eur'] for car in car_data_pt]
        median_price_pt = median(prices_pt)

        # Calculate the coefficient (price ratio) using median prices
        coefficient = median_price_pt / median_price_pl

        return coefficient

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return None"""


def calculate_price_coefficients(all_cars_data):
    coefficients = []

    for car_data in all_cars_data:
        car_name, data = list(car_data.items())[0]
        pl_data = data[0]["PL"]
        pt_data = data[1]["PT"]

        prices_pl = [car.price for car in pl_data if car.price != 'N/A']
        prices_pt = [car.price for car in pt_data if car.price != 'N/A']

        if prices_pl and prices_pt:
            median_price_pl = median(prices_pl)
            median_price_pt = median(prices_pt)

            price_difference = median_price_pt - median_price_pl
            percentage_difference = round((price_difference / median_price_pl) * 100, 1)

            coefficients.append({car_name: percentage_difference})

    return coefficients


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