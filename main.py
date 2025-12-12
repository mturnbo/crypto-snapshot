import os
import json
from app.models.portfolio import Portfolio
import argparse

wallets_addresses = {}
file_path = os.path.join('config','wallets.json')
with open(file_path) as f:
    wallets = json.load(f)


if __name__ == '__main__':
    # get command line arguments
    parser = argparse.ArgumentParser(description="Crypto Portfolio Snapshot")
    parser.add_argument("operation", choices=["scan", "save"], help="Scan and display assets or save to CSV")
    parser.add_argument("--wallet", type=str, required=False, help="Name of wallet to scan")
    parser.add_argument("--exchange", type=str, required=False, help="Name of exchange to scan")
    parser.add_argument("--blockchain", type=str, required=False, help="Name of blockchain to scan")
    args = parser.parse_args()

    portfolio = Portfolio("tangem", "wallet", wallets["tangem"])
    portfolio.show_addresses()
    portfolio.show_assets()


    # get wallet assets
    portfolios = []
    for wallet, tokens in wallets.items():
        portfolio = Portfolio(wallet, "wallet", tokens)
        portfolio.show_assets()


    # get exchange assets


