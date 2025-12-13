from dotenv import load_dotenv
from app.models.asset import Asset
from app.utils.price_data import get_token_prices
import os
import requests
# from coinbase.rest import RESTClient

load_dotenv()

API_KEY = os.getenv('COINBASE_API_KEY')
API_SECRET = os.getenv('COINBASE_PRIVATE_KEY')
BASE_URL = 'https://api.coinbase.com/api/v3/brokerage/'

def get_coinbase_portfolio():
    api_url = BASE_URL + "portfolios"
    headers = {
        'X-CMC_PRO_API_KEY': API_KEY,
        'Accept': 'application/json'
    }
    response = requests.get(api_url)
    portfolio_data = response.json()
    print(portfolio_data)


def get_coinbase_portfolio_restclient():
    client = RESTClient(api_key=API_KEY, api_secret=API_SECRET)
    try:
        portfolios_data = client.get_portfolios()
        portfolios = portfolios_data.get('portfolios', [])

        if not portfolios:
            print("No portfolios found or API key has no access.")
            return

        # Use the first portfolio found
        first_portfolio = portfolios[0]
        portfolio_uuid = first_portfolio['uuid']
        portfolio_name = first_portfolio.get('name', 'N/A')

        print(f"--- Portfolio Details: {portfolio_name} (UUID: {portfolio_uuid}) ---")

        # Fetch the detailed breakdown for the specific portfolio UUID
        portfolio_breakdown = client.get_portfolio_breakdown(portfolio_uuid=portfolio_uuid)

        # Extract and print spot positions (assets held)
        spot_positions = portfolio_breakdown.get('breakdown', {}).get('spot_positions', [])

        if not spot_positions:
            print("This portfolio is empty or has no spot positions.")
        else:
            print("Assets (Spot Positions):")
            for position in spot_positions:
                asset_code = position['asset']
                balance = position['balance']
                print(f"* {asset_code}: {balance}")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your API keys and permissions.")


get_coinbase_portfolio()