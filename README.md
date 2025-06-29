# CryptoTrader

This repository contains a minimal skeleton for an automated cryptocurrency
trading system. The project integrates with the Binance and CoinMarketCap APIs
and demonstrates a simple moving average strategy. It is **not** production
ready but provides a starting point for further development.

## Features

- Basic Binance REST API client (`BinanceClient`)
- CoinMarketCap API client (`CoinMarketCapClient`)
- Example moving average crossover strategy
- Command line entry point in `src/main.py`
- Simple unit test using `pytest`

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the sample script to fetch prices and generate signals:

```bash
python -m src.main BTCUSDT --iterations 5 --interval 2
```

Run tests with:

```bash
pytest
```
