from app.models.token import Token
import os
from dotenv import load_dotenv
from app.services.cmc_api_service import CoinMarketCapAPI
from typing import List

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

    def formatted_output(self, included_fields: List[str]=['symbol', 'balance', 'price', 'value']):
        total_value = self.balance * self.price if self.price is not None else 0
        formatted_fields = [{
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
        }, {
            "title": "Value",
            "justification": "right",
            "value": f"${total_value:,.2f}" if total_value is not None else "N/A",
        }, {
            "title": "Currency",
            "justification": "center",
            "value": self.currency,
            "max_width": 8,
        }]

        # return filtered list containing only fields matching included_fields
        titles_lower = [title.lower() for title in included_fields]
        return [item for item in formatted_fields if item.get("title").lower() in titles_lower]
