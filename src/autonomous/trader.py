import logging
import time
import yaml

from core.engine import TradingEngine
from execution import PaperTrader

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def run_autonomous(config_path: str = "config/strategies.yaml", interval: float = 1.0, paper: bool = True, iterations: int | None = None) -> None:
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    executor = PaperTrader() if paper else None
    engine = TradingEngine(cfg.get("strategies", []), interval=interval, executor=executor)
    i = 0
    while iterations is None or i < iterations:
        engine.run_once()
        i += 1
        time.sleep(interval)
    if executor:
        logging.info("Final balance: %s", executor.balance)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run autonomous trading loop")
    parser.add_argument("--config", default="config/strategies.yaml")
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--paper", action="store_true")
    parser.add_argument("--iterations", type=int)
    args = parser.parse_args()
    run_autonomous(args.config, interval=args.interval, paper=args.paper, iterations=args.iterations)


if __name__ == "__main__":
    main()
