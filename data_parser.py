# Function to extract and convert price to EUR
import re


def extract_price(price_text, eur_to_pln_rate):
    # Use regular expressions to extract the numeric part of the price
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
