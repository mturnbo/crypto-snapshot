import binascii
from datetime import datetime
import dateutil.parser
import base64
from rich.table import Table
from rich.console import Console
from typing import List, Any
import re

def split_list(lst: List, size: int):
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def decode_ec_private_key(encoded_key: str) -> str:
    if not encoded_key or not isinstance(encoded_key, str):
        raise ValueError("Private key must be a non-empty string.")

    text = encoded_key.strip()

    # If it's already PEM, normalize line endings and return as-is
    if text.startswith("-----BEGIN"):
        pem = text.replace("\r\n", "\n").replace("\r", "\n").strip()
        return pem + "\n"

    # Otherwise treat as base64-encoded key body
    try:
        decoded_bytes = base64.b64decode(text, validate=True)
    except (ValueError, binascii.Error) as e:
        raise ValueError(f"Invalid base64 private key: {e}")

    try:
        decoded_text = decoded_bytes.decode("utf-8").strip()
    except UnicodeDecodeError as e:
        raise ValueError(f"Decoded key is not valid UTF-8: {e}")

    # If decoded text is PEM, normalize and return
    if decoded_text.startswith("-----BEGIN"):
        pem = decoded_text.replace("\r\n", "\n").replace("\r", "\n").strip()
        return pem + "\n"

    # Otherwise, assume it's the raw base64 body; wrap at 64 chars
    key_body = re.sub(r"\s+", "", decoded_text)
    if not key_body:
        raise ValueError("Decoded key body is empty.")

    wrapped = "\n".join(key_body[i:i + 64] for i in range(0, len(key_body), 64))
    return (
        "-----BEGIN EC PRIVATE KEY-----\n"
        f"{wrapped}\n"
        "-----END EC PRIVATE KEY-----\n"
    )


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


def show_object_attribute_table(obj: Any):
    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.title = f"{obj.__class__.__name__} Object Attributes"

    # add columns
    table.add_column("Key", justify="right", min_width=12)
    table.add_column("Value", justify="left", min_width=40)

    for key, val in obj.__dict__.items():
        table.add_row(key, str(val))

    console.print(table)
