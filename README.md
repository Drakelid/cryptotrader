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
- Paper trading executor
- YAML strategy configuration in `config/strategies.yaml`
- Pytest based unit test

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```


### Run the Dashboard

Start the FastAPI web dashboard and trigger the engine via HTTP:

```bash
uvicorn src.ui.dashboard:app --reload
```

You can then POST to `/run` to execute the engine. For example:

```bash
curl -X POST http://localhost:8000/run -H "Content-Type: application/json" \
  -d '{"iterations": 5, "interval": 2}'
```

### Run from CLI

You can still run the sample script directly:

```bash
python -m src.main --config config/strategies.yaml --iterations 5 --interval 2 --paper
```

The `--paper` flag enables paper trading so no real funds are used.

Backtest a strategy with a CSV file of prices:

```bash
python -m src.backtest.simulator your_prices.csv
```

Run tests with:

```bash
pytest
```
