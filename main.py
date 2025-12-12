import os
import sys
import json
from app.models.wallet import Wallet
from app.models.exchange import Exchange
import argparse

addresses = {}
file_path = os.path.join('config','addresses.json')
with open(file_path) as f:
    addresses = json.load(f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Crypto Portfolio Snapshot")
    parser.add_argument("operation", choices=["scan", "save"], help="Scan and display assets or save to CSV")
    parser.add_argument("--wallet", type=str, required=False, help="Name of wallet to scan")
    parser.add_argument("--exchange", type=str, required=False, help="Name of exchange to scan")
    parser.add_argument("--blockchain", type=str, required=False, help="Name of blockchain to scan")
    args = parser.parse_args()

    # get wallet assets

    # get exchange assets

    print(args)
