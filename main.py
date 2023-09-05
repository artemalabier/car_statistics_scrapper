from scraper import fetch_olx_car_data

if __name__ == '__main__':
    filename = 'prefiltered.txt'

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
