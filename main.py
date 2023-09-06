import json

from analysis import calculate_price_coefficients
from scraper import fetch_olx_car_data

if __name__ == '__main__':
    filename = 'URLs.json'

    def url_read(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            return {}
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return {}


    def collecting_cars(car_urls):
        all_cars_data = []

        for car_name, urls in car_urls.items():
            pl_url = urls.get("PL", "")
            pt_url = urls.get("PT", "")

            pl_data = fetch_olx_car_data(pl_url)
            pt_data = fetch_olx_car_data(pt_url)

            car_data = {
                car_name: [{"PL": list(pl_data)}, {"PT": list(pt_data)}]
            }

            all_cars_data.append(car_data)

        return all_cars_data

    # Read car names and URLs from the file using url_read()
    model_urls = url_read(filename)

    # Create separate collections of Car objects for each URL using cars_to_set()
    collected_cars = collecting_cars(model_urls)

    # Print or further process the collected car data
    '''for car_data in collected_cars:
        for car_name, data in car_data.items():
            print(car_name)
            for source_data in data:
                country, cars = list(source_data.items())[0]
                print('-' * 30)
                print(f"Country: {country}:")
                print('-' * 30)
                for car in cars:
                    print(f'ID: {car.id}')
                    print(f'Title: {car.title}')
                    print(f'Link: {car.link}')
                    print(f'Price: {car.price}')
                    print('-' * 30)'''

    price_coefficients = calculate_price_coefficients(collected_cars)

    # Print the price coefficients
    for coefficient_data in price_coefficients:
        for car_model, percentage_difference in coefficient_data.items():
            print(f"Car Model: {car_model}")
            print(f"Percentage Price Difference: {percentage_difference}%")