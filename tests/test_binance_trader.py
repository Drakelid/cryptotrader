import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.execution.binance import BinanceTrader
from src.core.engine import TradingEngine
from src.strategies.base import Strategy

class DummyStrategy(Strategy):
    def __init__(self):
        self.symbol = "TEST"
        self.count = 0

    def on_price_update(self, symbol: str, price: float) -> None:
        pass

    def generate_signal(self):
        self.count += 1
        return "buy" if self.count == 1 else None


def test_binance_trader_execute():
    mock_client = MagicMock()
    trader = BinanceTrader(client=mock_client)
    trader.execute("TEST", "buy", quantity=1)
    mock_client.create_order.assert_called_once()


def test_engine_with_binance_trader():
    mock_client = MagicMock()
    trader = BinanceTrader(client=mock_client)
    engine = TradingEngine([], interval=0, executor=trader)
    engine.strategies = [DummyStrategy()]
    with patch.object(engine.client, "get_ticker_price", return_value=1.0):
        engine.run(1)
    mock_client.create_order.assert_called_once()
