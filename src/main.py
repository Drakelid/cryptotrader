import argparse
import logging
import yaml

from core.engine import TradingEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def load_config(path: str):
    with open(path) as f:
        return yaml.safe_load(f)


def main(config_path: str, iterations: int, interval: float):
    config = load_config(config_path)
    strategies = config.get("strategies", [])
    engine = TradingEngine(strategies, interval=interval)
    engine.run(iterations)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CryptoTrader engine")
    parser.add_argument("--config", default="config/strategies.yaml")
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args()
    main(args.config, args.iterations, args.interval)
