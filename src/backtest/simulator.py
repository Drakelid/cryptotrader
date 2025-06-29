import csv
from typing import Iterable


class BacktestSimulator:
    def __init__(self, strategy):
        self.strategy = strategy

    def run(self, prices: Iterable[float]):
        for price in prices:
            self.strategy.on_price_update(self.strategy.symbol, price)
            yield self.strategy.generate_signal()

    @staticmethod
    def load_prices(csv_file: str, column: str = "close"):
        with open(csv_file, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield float(row[column])


def _default_strategy(symbol: str):
    from strategies.moving_average import MovingAverageStrategy

    return MovingAverageStrategy(symbol)


def run_backtest(csv_file: str, symbol: str = "BTCUSDT"):
    """Run the backtest and return generated signals."""
    strategy = _default_strategy(symbol)
    sim = BacktestSimulator(strategy)
    return list(sim.run(BacktestSimulator.load_prices(csv_file)))


def main(csv_file: str, symbol: str = "BTCUSDT") -> None:
    for signal in run_backtest(csv_file, symbol):
        if signal:
            print(signal)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run a simple backtest")
    parser.add_argument("csv_file", help="CSV file with historical prices")
    parser.add_argument("--symbol", default="BTCUSDT")
    args = parser.parse_args()
    main(args.csv_file, symbol=args.symbol)
