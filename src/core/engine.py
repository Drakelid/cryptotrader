import importlib
import logging
from typing import Any, Dict, List

from data.binance.binance_client import BinanceClient


def load_strategies(config: List[Dict[str, Any]]):
    strategies = []
    for entry in config:
        module = importlib.import_module(entry["module"])
        cls = getattr(module, entry["class"])
        params = entry.get("params", {})
        strategies.append(cls(**params))
    return strategies


class TradingEngine:
    def __init__(self, strategy_configs: List[Dict[str, Any]], interval: float = 1.0):
        self.client = BinanceClient()
        self.strategies = load_strategies(strategy_configs)
        self.interval = interval

    def run_once(self):
        for strat in self.strategies:
            symbol = getattr(strat, "symbol", None)
            if not symbol:
                continue
            price = self.client.get_ticker_price(symbol)
            if price is None:
                logging.warning("No price for %s", symbol)
                continue
            strat.on_price_update(symbol, price)
            signal = strat.generate_signal()
            if signal:
                logging.info("%s generated signal: %s", strat.__class__.__name__, signal)

    def run(self, iterations: int):
        import time
        for _ in range(iterations):
            self.run_once()
            time.sleep(self.interval)
