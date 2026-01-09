import os
from dotenv import load_dotenv
from app.models.asset import Asset
from app.utils.blockchains.bitcoin import get_btc_balance
from app.utils.blockchains.litecoin import get_ltc_balance
from app.utils.blockchains.polygon import get_polygon_balance
from app.utils.blockchains.cardano import get_wallet_assets as get_cardano_assets
from app.utils.blockchains.erc20 import get_wallet_assets as get_erc20_assets
from app.utils.blockchains.solana import get_wallet_assets as get_solana_assets
from app.utils.blockchains.tron import get_tron_wallet_info as get_tron_balance
from app.services.api.coinbase_api_service import CoinbaseAPI
from app.services.api.kraken_api_service import KrakenAPI
from typing import List, Dict

class AssetsService():

    @staticmethod
    def get_wallet_assets(token_addresses:  Dict[str, str]) -> List[Asset]:
        assets = []

        for blockchain, address in token_addresses.items():
            new_assets = []
            match blockchain.lower():
                case "btc":
                    new_assets = [get_btc_balance(address)]
                case "ltc":
                    new_assets = [get_ltc_balance(address)]
                case "ada":
                    new_assets = get_cardano_assets(address)
                case "erc20":
                    new_assets = get_erc20_assets(address)
                case "sol":
                    new_assets = get_solana_assets(address)
                case "pol":
                    new_assets = [get_polygon_balance(address)]
                case "trx":
                    new_assets = [get_tron_balance(address)]

            assets.extend(new_assets)

        return assets


    @staticmethod
    def get_exchange_assets(exchange_name: str) -> List[Asset]:
        assets = []
        load_dotenv()
        match exchange_name.lower():
            case "coinbase":
                api_key = os.getenv('COINBASE_API_KEY')
                api_secret = os.getenv('COINBASE_API_SECRET')
                cb_api = CoinbaseAPI(api_key, api_secret)
                assets = cb_api.get_portfolio_assets()
            case "kraken":
                api_key = os.getenv('KRAKEN_API_KEY')
                api_secret = os.getenv('KRAKEN_API_SECRET')
                kraken_api = KrakenAPI(api_key, api_secret)
                assets = kraken_api.get_portfolio_assets()

        return assets