import time
import logging
from typing import Optional

from exchange.binance_client import BinanceClient
from strategies.moving_average import MovingAverageStrategy

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def main(symbol: str, iterations: int = 10, interval: float = 1.0) -> None:
    client = BinanceClient()
    strategy = MovingAverageStrategy()

    for _ in range(iterations):
        price = client.get_ticker_price(symbol)
        if price is None:
            logging.warning("No price for %s", symbol)
            time.sleep(interval)
            continue
        logging.info("%s price=%s", symbol, price)
        strategy.on_price_update(symbol, price)
        signal = strategy.generate_signal()
        if signal:
            logging.info("Generated signal: %s", signal)
        time.sleep(interval)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simple crypto trading skeleton")
    parser.add_argument("symbol", help="Trading pair symbol, e.g. BTCUSDT")
    parser.add_argument("--iterations", type=int, default=10, help="Number of price updates")
    parser.add_argument("--interval", type=float, default=1.0, help="Delay between updates in seconds")
    args = parser.parse_args()

    main(args.symbol, args.iterations, args.interval)
