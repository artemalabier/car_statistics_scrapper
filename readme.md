# Car Statistics Scrapper

## Description
The Car Price Analysis project is a Python script designed to analyze car prices from online listings on OLX websites for different countries. It retrieves car listings from OLX.pl (Poland) and OLX.pt (Portugal), calculates the median prices for each car, and then determines the percentage difference in prices between the two countries.

## Features
- **Data Collection:** The script collects car data from OLX.pl and OLX.pt based on the URLs provided in a specified file. It utilizes web scraping techniques to extract relevant information such as car title, link, and price.
- **Price Analysis:** After fetching the car data, the script calculates the median prices for all the cars in EUR currency.
- **Percentage Difference:** It calculates the percentage difference in prices between Poland (PL) and Portugal (PT) for each car based on the median prices.

## Usage
1. Set up the `EXCHANGE_API_KEY` environment variable to provide access to the exchange rate API. The API key can be obtained from exchangeratesapi.io.
2. Run the script and provide the necessary input, such as the file containing the URLs of car listings (URLs.json by default, but can be configured in configuration.py).

## Known Issues
- The `test_fetch_olx_car_data_success()` test case fails due to the Mock Object returning None instead of the expected car data from the mock page.

## Future Improvements
- Fix the failing test script.
- Improve error handling and error messages to provide better feedback to users in case of failures.
- Enhance testing coverage to include edge cases and handle different scenarios more effectively.
- Implement logging functionality to track script execution and capture relevant information for debugging purposes.
- Consider adding support for additional OLX websites or other car listing platforms to expand the scope of the analysis.
- Enhance the functionality to monitor the prices automatically and on regular basis to see the prices in dynamics.
- Equip this scrapper with nice UI with fancy graphs based on the scrapped data.

## Contributing
Contributions to the project are welcome! Please feel free to submit bug reports, feature requests, or pull requests via the project's GitHub repository.

## License
This project is licensed under the MIT License.
