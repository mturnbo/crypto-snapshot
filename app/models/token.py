class Token:
    def __init__(self, name, symbol, id=None, blockchain=None):
        self.symbol:str = symbol
        self.id:str = id
        self.blockchain:str = blockchain
