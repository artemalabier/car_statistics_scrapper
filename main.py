from analysis import calculate_price_coefficients, collect_cars
from configuration import FILENAME
from data_parser import url_read


if __name__ == '__main__':
    model_urls = url_read(FILENAME)
    collected_cars = collect_cars(model_urls)
    price_coefficients = calculate_price_coefficients(collected_cars)

    for coefficient_data in price_coefficients:
        for car_model, percentage_difference in coefficient_data.items():
            print(f"Car Model: {car_model}")
            print(f"Percentage Price Difference: {percentage_difference}%")