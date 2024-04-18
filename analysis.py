from statistics import median
from scraper import fetch_olx_car_data

def fetch_cars_for_country(country_url):
    return fetch_olx_car_data(country_url) or []

def collect_cars(car_urls):
    return [
        {
            car_name: {
                "PL": fetch_cars_for_country(urls.get("PL", "")),
                "PT": fetch_cars_for_country(urls.get("PT", ""))
            }
        }
        for car_name, urls in car_urls.items()
    ]

def calculate_median(prices):
    valid_prices = [price for price in prices if price != 'N/A']
    if valid_prices:
        return median(valid_prices)
    else:
        return None

def calculate_percentage_difference(median_price_pl, median_price_pt):
    if median_price_pl is not None and median_price_pt is not None:
        price_difference = median_price_pt - median_price_pl
        return round((price_difference / median_price_pl) * 100, 1)
    else:
        return None

def calculate_price_coefficients(all_cars_data):
    coefficients = []

    for car_data in all_cars_data:
        car_name, data = list(car_data.items())[0]
        pl_data = data["PL"]
        pt_data = data["PT"]

        median_price_pl = calculate_median([car.price for car in pl_data])
        median_price_pt = calculate_median([car.price for car in pt_data])

        percentage_difference = calculate_percentage_difference(median_price_pl, median_price_pt)

        if percentage_difference is not None:
            coefficients.append({car_name: percentage_difference})

    return coefficients

