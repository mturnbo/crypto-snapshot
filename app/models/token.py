from typing import List, Dict, Any

class Token:
    def __init__(self, name: str = "", symbol: str = "", blockchain: str = "", description: str = "", logo: str = "", contracts: List[Dict[str, str]] = []):
        self.name:str = name
        self.symbol:str = symbol
        self.blockchain:str = blockchain
        self.description:str = description
        self.logo:str = logo
        self.contracts:List[Dict[str, str]] = contracts

    def __str__(self):
        return f"Token(\n\tname=: {self.name}\n\tsymbol: {self.symbol}\n\tblockchain: {self.blockchain}\n\tdescription: {self.description}\n\tlogo: {self.logo}\n)"


t = Token("Bitcoin","BTC","Bitcoin","OG Cryptocurrency")
print(t)
