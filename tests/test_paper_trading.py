import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.execution.paper import PaperTrader
from src.core.engine import TradingEngine
from src.strategies.base import Strategy
from src.risk.simple_risk import SimpleRiskManager
from src.risk.trailing_risk import TrailingRiskManager

class DummyStrategy(Strategy):
    def __init__(self):
        self.symbol = "TEST"
        self.count = 0
    def on_price_update(self, symbol: str, price: float) -> None:
        pass
    def generate_signal(self):
        self.count += 1
        return "buy" if self.count == 1 else "sell" if self.count == 2 else None

def test_paper_trader_execute():
    trader = PaperTrader(starting_balance=100)
    assert trader.execute("BTC", "buy", price=10, quantity=5)
    assert trader.balance == 50
    assert trader.positions["BTC"] == 5
    assert trader.execute("BTC", "sell", price=20, quantity=2)
    assert trader.balance == 90
    assert trader.positions["BTC"] == 3


def test_engine_integration_with_paper_trader():
    trader = PaperTrader(starting_balance=100)
    engine = TradingEngine([], interval=0, executor=trader)
    engine.strategies = [DummyStrategy()]
    with patch.object(engine.client, "get_ticker_price", return_value=1.0):
        engine.run(2)
    assert trader.balance == 100
    assert trader.positions.get("TEST", 0) == 0


def test_paper_trader_risk_manager():
    risk = SimpleRiskManager(stop_loss=0.05, take_profit=0.05)
    trader = PaperTrader(starting_balance=100, risk_manager=risk)
    trader.execute("BTC", "buy", price=10, quantity=5)
    trader.evaluate("BTC", price=9)  # triggers stop loss
    assert trader.positions.get("BTC", 0) == 0
    assert trader.balance == 95


def test_trailing_risk_manager():
    risk = TrailingRiskManager(stop_loss=0.1, take_profit=0.5, trailing=0.05)
    trader = PaperTrader(starting_balance=100, risk_manager=risk)
    trader.execute("BTC", "buy", price=10, quantity=5)
    trader.evaluate("BTC", price=12)
    trader.evaluate("BTC", price=11)  # drop more than trailing from 12
    assert trader.positions.get("BTC", 0) == 0
    assert trader.balance == 105

