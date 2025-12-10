from app.models.token import Token

class Asset(Token):
    def __init__(self, name, symbol, id=None, blockchain=None, balance=0, price=0, currency="USD"):
        super().__init__(name, symbol, id, blockchain)
        self.balance: float = balance
        self.price: float = price

    def formatted_output(self):
        output = []
        output.append({
            "title": "Symbol",
            "justification": "left",
            "value": self.symbol,
        })
        output.append({
            "title": "ID",
            "justification": "left",
            "value": self.id,
            "max_width": 20,
        })
        output.append({
            "title": "Balance",
            "justification": "right",
            "value": f"{self.balance:,.8f}",
        })
        output.append({
            "title": "Price",
            "justification": "right",
            "value": f"{self.price:.8f}",
        })
        total_value = self.balance * self.price
        output.append({
            "title": "Value",
            "justification": "right",
            "value": f"${total_value:,.2f}",
        })

        return output