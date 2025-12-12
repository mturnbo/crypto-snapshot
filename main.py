import os
import sys
import json
from app.models.wallet import Wallet
from app.models.exchange import Exchange

addresses = {}
file_path = os.path.join('config','addresses.json')
with open(file_path) as f:
    addresses = json.load(f)


if __name__ == '__main__':
    try:
        # get wallet assets

        # get exchange assets

        wallet_address = addresses[sys.argv[1]][sys.argv[2]]
    except KeyError:
        print("Invalid wallet name or address.")
        sys.exit(1)

    # wallet = Wallet(sys.argv[2].title(), wallet_address, sys.argv[1])
    # wallet.export_assets()
    # wallet.show_assets()

    exchange = Exchange("Kraken")
    exchange.show_assets()
    exchange.export_assets()
