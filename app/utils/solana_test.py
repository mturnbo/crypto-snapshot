import requests

# -----------------------------
# CONFIGURATION
# -----------------------------
RPC_ENDPOINT = "https://api.mainnet-beta.solana.com"
WALLET_ADDRESS = "F1Fqw6Naaw1rW2VaX77pUVVJr6mCTXC6VsP9gEhUsbqK"  # 👈 Replace this
BIRDEYE_PRICE_API = "https://public-api.birdeye.so/public/price"
BIRDEYE_API_KEY = "public"  # Optional: Use public or your key if rate-limited

# -----------------------------
# GET SOL BALANCE
# -----------------------------
def get_sol_balance(wallet_address):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [wallet_address]
    }
    res = requests.post(RPC_ENDPOINT, json=payload).json()
    lamports = res['result']['value']
    return lamports / 1_000_000_000

# -----------------------------
# GET SPL TOKENS
# -----------------------------
def get_spl_tokens(wallet_address):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccountsByOwner",
        "params": [
            wallet_address,
            {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
            {"encoding": "jsonParsed"}
        ]
    }
    res = requests.post(RPC_ENDPOINT, json=payload).json()
    result = res.get("result", {}).get("value", [])

    tokens = []
    for account in result:
        info = account['account']['data']['parsed']['info']
        mint = info['mint']
        token_amount = info['tokenAmount']
        amount = int(token_amount['amount']) / (10 ** int(token_amount['decimals']))
        if amount > 0:
            tokens.append({
                "mint": mint,
                "amount": amount,
                "decimals": token_amount['decimals']
            })
    return tokens

# -----------------------------
# GET TOKEN METADATA FROM Solana Token List
# -----------------------------
def load_token_metadata():
    url = "https://raw.githubusercontent.com/solana-labs/token-list/main/src/tokens/solana.tokenlist.json"
    res = requests.get(url).json()
    token_map = {}
    for token in res["tokens"]:
        token_map[token["address"]] = {
            "name": token["name"],
            "symbol": token["symbol"],
            "decimals": token["decimals"]
        }
    return token_map

# -----------------------------
# GET USD PRICE USING BIRDEYE
# -----------------------------
def get_token_price_usd(mint_address):
    try:
        res = requests.get(BIRDEYE_PRICE_API, params={"address": mint_address}, headers={"x-api-key": BIRDEYE_API_KEY})
        return res.json().get("data", {}).get("value", 0)
    except:
        return 0

# -----------------------------
# MAIN
# -----------------------------
def main():
    print(f"📥 Wallet: {WALLET_ADDRESS}\n")

    sol_balance = get_sol_balance(WALLET_ADDRESS)
    sol_price = get_token_price_usd("So11111111111111111111111111111111111111112")
    print(f"💰 SOL: {sol_balance:.4f} ($ {sol_balance * sol_price:.2f})\n")

    print("📦 SPL Tokens:")
    tokens = get_spl_tokens(WALLET_ADDRESS)
    token_metadata = load_token_metadata()

    for token in tokens:
        mint = token['mint']
        amount = token['amount']
        metadata = token_metadata.get(mint, {})
        symbol = metadata.get("symbol", "UNKNOWN")
        name = metadata.get("name", "Unknown Token")
        price = get_token_price_usd(mint)
        usd_value = amount * price

        print(f"  - {symbol} ({name})")
        print(f"    Mint: {mint}")
        print(f"    Amount: {amount:.4f}")
        print(f"    USD Value: ${usd_value:.2f}\n")

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    main()
