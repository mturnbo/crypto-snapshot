class Token:
    def __init__(self, name, symbol, blockchain=None):
        self.name = name
        self.symbol:str = symbol
        self.blockchain:str = blockchain
