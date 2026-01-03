from app.models.token import Token
import os
from dotenv import load_dotenv
from app.services.cmc_api_service import CoinMarketCapAPI

class Asset(Token):
    def __init__(self, name, symbol, blockchain=None, address="", balance=0, price=0, currency="USD"):
        super().__init__(name, symbol, blockchain)
        self.address: str = address
        self.balance: float = balance
        self.price: float = price
        self.currency: str = currency

    def get_price(self, currency: str = 'USD'):
        load_dotenv()
        cmc_api_key = os.getenv('COINMARKETCAP_API_KEY')
        cmc = CoinMarketCapAPI(api_key=cmc_api_key)
        usd_value = cmc.get_token_prices([self.symbol], currency)
        self.price = usd_value

    def formatted_output(self):
        output = [{
            "title": "Symbol",
            "justification": "left",
            "value": self.symbol,
        }, {
            "title": "Blockchain",
            "justification": "left",
            "value": self.blockchain,
            "max_width": 10,
        }, {
            "title": "Address",
            "justification": "left",
            "value": self.address,
            "max_width": 30,
        }, {
            "title": "Balance",
            "justification": "right",
            "value": f"{self.balance:,.4f}",
        }, {
            "title": "Price",
            "justification": "right",
            "value": f"{self.price:.8f}" if self.price is not None else "N/A",
        }]
        total_value = self.balance * self.price if self.price is not None else None
        output.append({
            "title": "Value",
            "justification": "right",
            "value": f"${total_value:,.2f}" if total_value is not None else "N/A",
        })
        output.append({
            "title": "Currency",
            "justification": "center",
            "value": self.currency,
            "max_width": 8,
        })

        return output