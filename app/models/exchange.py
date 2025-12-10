from app.models.portfolio import Portfolio
from app.utils.exchanges.kraken_util import get_kraken_portfolio

class Exchange(Portfolio):
    def __init__(self, name: str="", type: str="exchange"):
        super().__init__(name, type)
        self.get_assets()

    def get_assets(self):
        match self.name.lower():
            case "kraken":
                self.assets = get_kraken_portfolio()
            case _:
                self.assets = []
