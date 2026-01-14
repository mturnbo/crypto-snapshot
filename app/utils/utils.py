from datetime import datetime
import dateutil.parser
import base64
from rich import inspect
from rich.table import Table
from rich.console import Console
from typing import List, Any


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


def parse_date(date_input):
    if isinstance(date_input, datetime):
        return date_input
    elif isinstance(date_input, str):
        try:
            # Attempt to parse as ISO 8601 format
            return datetime.fromisoformat(date_input)
        except ValueError:
            # Fallback to a more flexible parser like dateutil.parser.parse
            try:
                return dateutil.parser.parse(date_input)
            except ValueError:
                raise ValueError(f"Could not parse date from string: {date_input}. Ensure it's a valid format.")
    else:
        raise TypeError("Date input must be a datetime object or a string.")


def show_object_values(obj: Any):
    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.title = f"{obj.__class__.__name__} Object Attributes"

    # add columns
    table.add_column("Key", justify="right", min_width=12)
    table.add_column("Value", justify="left", min_width=40)

    for key, val in obj.__dict__.items():
        table.add_row(key, val)

    console.print(table)



class TestObject():
    def __init__(self, name, type, description):
        self.name: str = name
        self.type: str = type
        self.description: str = description

a = TestObject("TEST", "Type A", "yada yada yada")

show_object(a)



