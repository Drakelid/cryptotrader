<<<<<<< HEAD
# Cryptotrader

This repository contains a minimal trading framework used for tests. It includes a dynamic risk manager and simple trader implementations for paper trading and Binance.

## Running tests

Run the unit tests with `pytest`:
=======
# CryptoTrader

CryptoTrader is an experimental algorithmic trading bot. It now uses a small
engine that loads strategies from a YAML configuration file and polls the
Binance API for prices. The code layout mirrors a production oriented
architecture but only implements a handful of features.

## Features

- Binance REST API client (`BinanceClient`)
- CoinMarketCap API client (`CoinMarketCapClient`)
- Configurable strategy engine (`core.engine.TradingEngine`)
- Example moving average crossover strategy
- Mean reversion strategy
- Grid trading strategy
- AI predictive strategy
- Simple backtesting simulator
- Binance trading executor for live orders
- Paper trading executor
- Risk management with stop-loss, take-profit and trailing stop
- YAML strategy configuration in `config/strategies.yaml`
- FastAPI dashboard for running tasks
- Autonomous trading helper
- Pytest based unit tests

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and set BINANCE_API_KEY, BINANCE_API_SECRET and CMC_API_KEY


### Run the Dashboard

Start the FastAPI web dashboard and trigger the engine via HTTP:

```bash
uvicorn src.ui.dashboard:app --reload
```

Example requests:

Run strategies for a few iterations in paper mode:

```bash
curl -X POST http://localhost:8000/run -H "Content-Type: application/json" \
  -d '{"iterations": 5, "interval": 2, "paper": true}'
```

Backtest against historical prices:

```bash
curl -X POST http://localhost:8000/backtest -H "Content-Type: application/json" \
  -d '{"csv_file": "prices.csv", "symbol": "BTCUSDT"}'
```

Launch a simple autonomous loop:

```bash
curl -X POST http://localhost:8000/autonomous -H "Content-Type: application/json" \
  -d '{"iterations": 10, "stop_loss": 0.02, "take_profit": 0.05, "trailing": 0.03}'
```

Check Binance connectivity:

```bash
curl http://localhost:8000/status
```

Fetch trending tokens from CoinMarketCap:

```bash
curl http://localhost:8000/trending
```

### Run from CLI

You can still run the sample script directly:

```bash
python -m src.main --config config/strategies.yaml --iterations 5 --interval 2 --paper
```

Backtest a strategy with a CSV file of prices:

```bash
python -m src.backtest.simulator your_prices.csv
```

Run the autonomous trader from CLI:

```bash
python -m src.autonomous.trader --iterations 10 --paper --stop-loss 0.02 --take-profit 0.05 --trailing 0.03
```

For live trading ensure BINANCE_API_KEY and BINANCE_API_SECRET are set and omit `--paper`:
```bash
python -m src.autonomous.trader --iterations 10
```

Run tests with:
>>>>>>> fhkv5t-main/develop-autonomous-crypto-trading-platform

```bash
pytest -q
```
