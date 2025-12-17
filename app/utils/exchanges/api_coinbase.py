from dotenv import load_dotenv
import os
from coinbase.rest import RESTClient
import time
from typing import Optional, Dict, List
import jwt
from cryptography.hazmat.primitives import serialization
import secrets
import base64

load_dotenv()

API_KEY_NAME = os.getenv('COINBASE_API_KEY')
API_PRIVATE_KEY = os.getenv('COINBASE_API_SECRET')


def decode_private_key_from_env() -> str:
    encoded_key: str = os.getenv('COINBASE_API_SECRET')

    try:
        # Decode from base64
        decoded_key = base64.b64decode(encoded_key).decode('utf-8')

        # Clean up the key - remove extra whitespace and ensure proper PEM format
        decoded_key = decoded_key.strip()

        # If the key doesn't have PEM headers, add them
        if not decoded_key.startswith('-----BEGIN'):
            # Remove any existing newlines and reconstruct proper PEM format
            key_body = decoded_key.replace('\n', '').replace('\r', '')
            decoded_key = f"-----BEGIN EC PRIVATE KEY-----\n{key_body}\n-----END EC PRIVATE KEY-----"

        return decoded_key
    except Exception as e:
        raise ValueError(f"Failed to decode private key from environment: {e}")


def generate_signature(timestamp: str, method: str, path: str, body: str = '') -> str:
    # Generate CB-ACCESS-SIGN header for authentication
    message = timestamp + method + path + body
    print(API_SECRET, message)
    signature = hmac.new(
        API_SECRET.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    return signature


def get_headers(method: str, path: str, body: str = '') -> Dict:
    # Generate authentication headers for Coinbase API
    timestamp = str(int(time.time()))
    signature = generate_signature(timestamp, method, path, body)

    return {
        'CB-ACCESS-KEY': API_SECRET,
        'CB-ACCESS-SIGN': signature,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'Content-Type': 'application/json'
    }

def build_jwt(uri: str, private_key: bytes):
    try:
        private_key = serialization.load_pem_private_key(private_key, password=None)
        jwt_payload = {
            'sub': API_KEY_NAME,
            'iss': "cdp",
            'nbf': int(time.time()),
            'exp': int(time.time()) + 120,
            'uri': uri,
        }

        jwt_token = jwt.encode(
            jwt_payload,
            private_key,
            algorithm='ES256',
            headers={'kid': API_KEY_NAME, 'nonce': secrets.token_hex()},
        )

        return jwt_token
    except ValueError as e:
        print(f"Error loading private key: {e}")
        return None


def get_portfolio_data(client):
    portfolios = client.get_portfolios()
    portUuid = portfolios['portfolios'][0]['uuid']

    # Fetch portfolio breakdown data
    portfolio_data = client.get_portfolio_breakdown(portfolio_uuid=portUuid)

    # Display portfolio breakdown
    for position in portfolio_data['breakdown']['spot_positions']:
        print(f"{position['asset']}\t{position['total_balance_crypto']}\t${position['available_to_trade_fiat']}")


def main():
    api_secret = decode_private_key_from_env()
    client = RESTClient(api_key=API_KEY_NAME, api_secret=api_secret)
    get_portfolio_data(client)


if __name__ == "__main__":
    main()
