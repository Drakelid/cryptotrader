import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.strategies.moving_average import MovingAverageStrategy
from src.strategies.mean_reversion import MeanReversionStrategy
from src.strategies.grid_trading import GridTradingStrategy
from src.strategies.ai_predictive import AIPredictiveStrategy


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


def test_grid_trading_strategy():
    strat = GridTradingStrategy(symbol="TEST", grid_size=0.1)
    prices = [10, 9, 8, 9, 10, 11]
    signals = []
    for p in prices:
        strat.on_price_update(strat.symbol, p)
        signals.append(strat.generate_signal())
    assert signals.count("buy") >= 1 and signals.count("sell") >= 1


def test_ai_predictive_strategy():
    strat = AIPredictiveStrategy(symbol="TEST")
    prices = [1, 2, 3, 2, 1]
    signals = []
    for p in prices:
        strat.on_price_update(strat.symbol, p)
        signals.append(strat.generate_signal())
    assert signals[1] == "buy" and signals[3] == "sell"
