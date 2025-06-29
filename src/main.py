import argparse
import logging
import yaml

from core.engine import TradingEngine
from execution import PaperTrader

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def load_config(path: str):
    with open(path) as f:
        return yaml.safe_load(f)


def main(config_path: str, iterations: int, interval: float, paper: bool):
    config = load_config(config_path)
    strategies = config.get("strategies", [])
    executor = PaperTrader() if paper else None
    engine = TradingEngine(strategies, interval=interval, executor=executor)
    engine.run(iterations)
    if executor:
        print("Balance:", executor.balance)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CryptoTrader engine")
    parser.add_argument("--config", default="config/strategies.yaml")
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--paper", action="store_true", help="Enable paper trading")
    args = parser.parse_args()
    main(args.config, args.iterations, args.interval, args.paper)
