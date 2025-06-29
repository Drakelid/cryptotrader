# CryptoTrader

CryptoTrader is an experimental algorithmic trading bot.  It now uses a small
engine that loads strategies from a YAML configuration file and polls the
Binance API for prices.  The code layout mirrors a production oriented
architecture but only implements a handful of features.

## Features

- Binance REST API client (`BinanceClient`)
- CoinMarketCap API client (`CoinMarketCapClient`)
- Configurable strategy engine (`core.engine.TradingEngine`)
- Example moving average crossover strategy
- Mean reversion strategy
- Simple backtesting simulator
- YAML strategy configuration in `config/strategies.yaml`
- Pytest based unit test

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the sample script to fetch prices and generate signals:

```bash
python -m src.main --config config/strategies.yaml --iterations 5 --interval 2
```

Backtest a strategy with a CSV file of prices:

```bash
python -m src.backtest.simulator your_prices.csv
```

Run tests with:

```bash
pytest
```
