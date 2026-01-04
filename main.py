import os
import json
from app.models.portfolio import Portfolio
import argparse
from typing import List, Dict

def get_wallets():
    file_path = os.path.join('config', 'wallets.json')
    with open(file_path) as f:
        wallets = json.load(f)

    return wallets


def get_wallet_portfolios(wallets):
    portfolio_list: List[Portfolio] = []
    for wallet, tokens in wallets.items():
        portfolio = Portfolio(wallet, "wallet", tokens)
        portfolio_list.append(portfolio)
        # portfolio.show_assets()

    return portfolio_list


def get_exchange_portfolios():
    portfolio_list: List[Portfolio] = [
        Portfolio('kraken', 'exchange'),
        Portfolio('coinbase', 'exchange')
    ]

    return portfolio_list


if __name__ == '__main__':
    # get command line arguments
    parser = argparse.ArgumentParser(description="Crypto Portfolio Snapshot")
    parser.add_argument("operation", choices=["scan", "save"], help="Scan and display assets or save to CSV")
    parser.add_argument("--wallet", type=str, required=False, help="Name of wallet to scan")
    parser.add_argument("--exchange", type=str, required=False, help="Name of exchange to scan")
    parser.add_argument("--blockchain", type=str, required=False, help="Name of blockchain to scan")
    args = parser.parse_args()

    portfolios: List[Portfolio] = []

    if args.wallet:
        wallets = get_wallets()
        if args.wallet == "all":
            portfolios.extend(get_wallet_portfolios(wallets))
        else:
            tokens = wallets[args.wallet]
            portfolio = Portfolio(args.wallet, "wallet", tokens)
            portfolios.append(portfolio)

    if args.exchange:
        if args.exchange == "all":
            portfolios.extend(get_exchange_portfolios())
        else:
            portfolio = Portfolio(args.exchange, "exchange")
            portfolios.append(portfolio)

    if len(portfolios):
        for portfolio in portfolios:
            portfolio.show_assets()
