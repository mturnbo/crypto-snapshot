from app.models.portfolio import Portfolio
from app.utils.utils_cardano import get_wallet_assets as get_cardano_assets
from app.utils.utils_erc20 import get_wallet_assets as get_erc20_assets
from app.utils.utils_solana import get_wallet_assets as get_solana_assets

class Wallet(Portfolio):
    def __init__(self, name: str="", address: str="", blockchain: str="", type: str="wallet"):
        super().__init__(name, type)
        self.address = address
        self.blockchain = blockchain
        self.get_assets()

    def get_assets(self):
        match self.blockchain.lower():
            case "cardano":
                self.assets = get_cardano_assets(self.address)
            case "erc20":
                self.assets = get_erc20_assets(self.address)
            case "solana":
                self.assets = get_solana_assets(self.address)
            case _:
                self.assets = []
