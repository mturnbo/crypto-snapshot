from dotenv import load_dotenv
from websockets import uri

from app.models.asset import Asset
import os
import requests
import json
import hmac
import hashlib
import time
from typing import Optional, Dict, List

import jwt
from cryptography.hazmat.primitives import serialization
import secrets
import base64

load_dotenv()

API_KEY_NAME = os.getenv('COINBASE_API_KEY_NAME')
API_PRIVATE_KEY = os.getenv('COINBASE_API_PRIVATE_KEY')
BASE_URL = 'https://api.coinbase.com/api/v3/brokerage'


def load_private_key_from_env() -> str:
    encoded_key: str = os.getenv('COINBASE_API_PRIVATE_KEY')

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

def get_accounts() -> Dict:
    """
    Fetch all accounts (wallets) from Coinbase.

    Returns:
        Dictionary containing all account information
    """
    path = '/accounts'
    endpoint = f"{BASE_URL}{path}"
    headers = get_headers('GET', path)
    session = requests.Session()

    try:
        response = session.get(endpoint, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching accounts: {e}")
        return {"error": str(e)}

def get_coinbase_portfolio():
    accounts = get_accounts()
    return accounts


pk0 = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIFQfdOUg83O7q/n809GLlQmctshftjJeQeHiSKsuK1bSoAoGCCqGSM49AwEHoUQDQgAEv7AbqTlwLghWKY6MpfzLEIJZ+A9Ie/hjUcYu1+Cj4UY6ui5jI2pCqAdnfVbJh4MkiPuawL6Lj7EGxSK7Zixmvg==\n-----END EC PRIVATE KEY-----\n"

pk1 = load_private_key_from_env()
print(pk0)
print(pk1)

uri = f"GET {BASE_URL}/accounts"
jwt_token = build_jwt(uri, pk1.encode('utf-8'))
print(jwt_token)
