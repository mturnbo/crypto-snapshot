from app.models.token import Token

class Asset(Token):
    def __init__(self, name, symbol, id=None, blockchain=None, address="", balance=0, price=0, currency="USD"):
        super().__init__(name, symbol, id, blockchain)
        self.address: str = address
        self.balance: float = balance
        self.price: float = price
        self.currency: str = currency

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
            "title": "Address",
            "justification": "left",
            "value": self.address,
            "max_width": 30,
        })
        output.append({
            "title": "Balance",
            "justification": "right",
            "value": f"{self.balance:,.8f}",
        })
        output.append({
            "title": "Price",
            "justification": "right",
            "value": f"{self.price:.8f}" if self.price is not None else "N/A",
        })
        total_value = self.balance * self.price if self.price is not None else None
        output.append({
            "title": "Value",
            "justification": "right",
            "value": f"${total_value:,.2f}" if total_value is not None else "N/A",
        })
        output.append({
            "title": "Currency",
            "justification": "left",
            "value": self.currency
        })

        return output