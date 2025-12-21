from typing import List, Dict, Any

class Token:
    def __init__(self, name: str = "", symbol: str = "", blockchain: str = "", description: str = "", logo: str = "", contracts: List[Dict[str, str]] = []):
        self.name:str = name
        self.symbol:str = symbol
        self.blockchain:str = blockchain
        self.description:str = description
        self.logo:str = logo
        self.contracts:List[Dict[str, str]] = contracts
