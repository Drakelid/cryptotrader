import logging
import time
import yaml

from src.core.engine import TradingEngine
from src.execution import PaperTrader, BinanceTrader
from src.risk import TrailingRiskManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def run_autonomous(
    config_path: str = "config/strategies.yaml",
    interval: float = 1.0,
    paper: bool = True,
    iterations: int | None = None,
    stop_loss: float = 0.02,
    take_profit: float = 0.04,
    trailing: float = 0.03,
) -> None:
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    risk = TrailingRiskManager(stop_loss, take_profit, trailing)
    executor = PaperTrader(risk_manager=risk) if paper else BinanceTrader()
    engine = TradingEngine(cfg.get("strategies", []), interval=interval, executor=executor)
    i = 0
    while iterations is None or i < iterations:
        engine.run_once()
        i += 1
        time.sleep(interval)
    if isinstance(executor, PaperTrader):
        logging.info("Final balance: %s", executor.balance)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run autonomous trading loop")
    parser.add_argument("--config", default="config/strategies.yaml")
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--paper", action="store_true")
    parser.add_argument("--iterations", type=int)
    parser.add_argument("--stop-loss", type=float, default=0.02)
    parser.add_argument("--take-profit", type=float, default=0.04)
    parser.add_argument("--trailing", type=float, default=0.03)
    args = parser.parse_args()
    run_autonomous(
        args.config,
        interval=args.interval,
        paper=args.paper,
        iterations=args.iterations,
        stop_loss=args.stop_loss,
        take_profit=args.take_profit,
        trailing=args.trailing,
    )


if __name__ == "__main__":
    main()

