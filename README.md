# Crypto Snapshot

Crypto Snapshot is a Python CLI utility for aggregating cryptocurrency balances across wallets and exchanges and presenting them in a unified view. It collects asset balances from supported blockchains, fetches pricing data, and outputs portfolio summaries in a readable table or exportable CSV format.

## Features

- Collect balances from wallets across supported chains (BTC, LTC, ADA, ERC-20, SOL, POL, TRX).
- Pull exchange portfolio data from Coinbase and Kraken APIs.
- Enrich holdings with token metadata and pricing from CoinMarketCap.
- Export portfolio snapshots to CSV for reporting and analysis.

## Project Layout

- `app/models/`: Core domain models (`Token`, `Asset`, `Portfolio`).
- `app/services/`: Exchange and market data service clients (BinanceUS, Coinbase, CoinMarketCap, Kraken).
- `app/utils/`: Blockchain utilities, price lookups, and helper functions.
- `config/`: Configuration files such as wallet mappings and token metadata.
- `main.py`: CLI entry point.

## Getting Started

1. Install dependencies (example with pip):

   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables for exchange APIs:

   ```bash
   export COINBASE_API_KEY=...
   export COINBASE_API_SECRET=...
   export KRAKEN_API_KEY=...
   export KRAKEN_API_SECRET=...
   export COINMARKETCAP_API_KEY=...
   ```

3. Add wallets to `config/wallets.json`.

4. Run the CLI:

   ```bash
   python main.py
   ```

## Exports

Portfolio snapshots can be exported to CSV files in the `export/` directory. Filenames include the portfolio type, name, and UTC timestamp.