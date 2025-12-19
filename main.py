import os
import json
from app.models.portfolio import Portfolio
import argparse

def get_wallets():
    file_path = os.path.join('config', 'wallets.json')
    with open(file_path) as f:
        wallets = json.load(f)

    return wallets


def get_wallet_assets(wallets):
    for wallet, tokens in wallets.items():
        portfolio = Portfolio(wallet, "wallet", tokens)
        portfolio.show_assets()

def get_exchange_assets():
    portfolio = Portfolio('kraken','exchange')
    portfolio.show_assets()
    portfolio = Portfolio('coinbase','exchange')
    portfolio.show_assets()


if __name__ == '__main__':
    # get command line arguments
    parser = argparse.ArgumentParser(description="Crypto Portfolio Snapshot")
    parser.add_argument("operation", choices=["scan", "save"], help="Scan and display assets or save to CSV")
    parser.add_argument("--wallet", type=str, required=False, help="Name of wallet to scan")
    parser.add_argument("--exchange", type=str, required=False, help="Name of exchange to scan")
    parser.add_argument("--blockchain", type=str, required=False, help="Name of blockchain to scan")
    args = parser.parse_args()


    if args.wallet:
        wallets = get_wallets()
        if args.wallet == "all":
            get_wallet_assets(wallets)
        else:
            print(f"Scanning wallet: {args.wallet} ...")
            tokens = wallets[args.wallet]
            portfolio = Portfolio(args.wallet, "wallet", tokens)
            portfolio.show_assets()

    if args.exchange:
        if args.exchange == "all":
            get_exchange_assets()
        else:
            print(f"Scanning exchange: {args.exchange} ...")
            portfolio = Portfolio(args.exchange, "exchange")
            portfolio.show_assets()
