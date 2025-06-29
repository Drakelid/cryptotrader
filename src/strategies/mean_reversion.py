from collections import deque
from typing import Deque, Optional

from .base import Strategy


class MeanReversionStrategy(Strategy):
    """Buy when price dips below moving average, sell when above."""

    def __init__(self, symbol: str, period: int = 20, threshold: float = 0.02):
        self.symbol = symbol.upper()
        self.period = period
        self.threshold = threshold
        self.prices: Deque[float] = deque(maxlen=period)
        self.last_signal: Optional[str] = None

    def on_price_update(self, symbol: str, price: float) -> None:
        self.prices.append(price)

    def _moving_average(self) -> Optional[float]:
        if len(self.prices) < self.prices.maxlen:
            return None
        return sum(self.prices) / len(self.prices)

    def generate_signal(self) -> Optional[str]:
        ma = self._moving_average()
        if ma is None:
            return None
        price = self.prices[-1]
        diff = (price - ma) / ma
        if diff <= -self.threshold and self.last_signal != "buy":
            self.last_signal = "buy"
            return "buy"
        if diff >= self.threshold and self.last_signal != "sell":
            self.last_signal = "sell"
            return "sell"
        return None
