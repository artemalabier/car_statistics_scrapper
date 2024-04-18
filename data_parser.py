import json
import re
import requests
import os
from configuration import DEFAULT_EXCHANGE_RATE

api_key = os.environ.get('EXCHANGE_API_KEY')

def url_read(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError as e:
        print(f"File '{filename}' not found: {str(e)}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data from file '{filename}': {str(e)}")
        raise

def extract_price(price_text, eur_to_pln_rate):
    price_match = re.search(r'([\d\s,]+[.,]*[\d]*)', price_text)

    if price_match:
        cleaned_price = price_match.group(1).replace(' ', '').replace(',', '').replace('.', '')
        numeric_price = float(cleaned_price)
        if '€' in price_text:
            return round(numeric_price)
        elif 'zł' in price_text:
            price_in_eur = numeric_price / eur_to_pln_rate
            return round(price_in_eur)

    return 'N/A'

def get_exchange_rate():
    try:
        response = requests.get(api_key)

        if response.status_code == 200:
            exchange_rate_data = response.json()
            print(f'[INFO] Received rate is {exchange_rate_data}')
            pln_to_eur_rate = exchange_rate_data['rates']['PLN']
            print(f'[INFO] Received rate is {pln_to_eur_rate}')
            return pln_to_eur_rate

        else:
            print(f'Failed to fetch exchange rate. Status code: {response.status_code}')

    except Exception as e:
        print(f'An error occurred: {str(e)}')

    print(f'[WARN] No rate fetched, using the default')
    return DEFAULT_EXCHANGE_RATE