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
