import secrets
import base64
from typing import List

def split_list(lst: List, size: int):
    return [lst[i:i + size] for i in range(0, len(lst), size)]

def decode_ec_private_key(encoded_key: str) -> str:
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
