from collections import deque
from typing import Deque, Optional

from .base import Strategy

class MovingAverageStrategy(Strategy):
    """Simple moving average crossover strategy."""

    def __init__(self, symbol: str, fast_period: int = 5, slow_period: int = 20):
        self.symbol = symbol.upper()
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.fast_prices: Deque[float] = deque(maxlen=fast_period)
        self.slow_prices: Deque[float] = deque(maxlen=slow_period)
        self.last_signal: Optional[str] = None  # "buy" or "sell"

    def on_price_update(self, symbol: str, price: float) -> None:
        self.fast_prices.append(price)
        self.slow_prices.append(price)

    def _moving_average(self, prices: Deque[float]) -> Optional[float]:
        if len(prices) < prices.maxlen:
            return None
        return sum(prices) / len(prices)

    def generate_signal(self) -> Optional[str]:
        fast_ma = self._moving_average(self.fast_prices)
        slow_ma = self._moving_average(self.slow_prices)
        if fast_ma is None or slow_ma is None:
            return None

        if fast_ma > slow_ma and self.last_signal != "buy":
            self.last_signal = "buy"
            return "buy"
        if fast_ma < slow_ma and self.last_signal != "sell":
            self.last_signal = "sell"
            return "sell"
        return None
