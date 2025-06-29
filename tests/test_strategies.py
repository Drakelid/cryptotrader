import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from strategies.moving_average import MovingAverageStrategy
from strategies.mean_reversion import MeanReversionStrategy


def test_moving_average_strategy():
    strat = MovingAverageStrategy(symbol="TEST", fast_period=2, slow_period=3)
    prices = [1, 2, 3, 2, 1, 5]
    signals = []
    for p in prices:
        strat.on_price_update(strat.symbol, p)
        signals.append(strat.generate_signal())
    assert signals == [None, None, "buy", None, "sell", "buy"]


def test_mean_reversion_strategy():
    strat = MeanReversionStrategy(symbol="TEST", period=3, threshold=0.1)
    prices = [100, 102, 98, 80, 110]
    signals = []
    for p in prices:
        strat.on_price_update(strat.symbol, p)
        signals.append(strat.generate_signal())
    assert signals == [None, None, None, "buy", "sell"]
