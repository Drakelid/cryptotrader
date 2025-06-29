from collections import deque
from typing import Deque, Optional

from .base import Strategy


class GridTradingStrategy(Strategy):
    """Very naive grid trading strategy for demonstration."""

    def __init__(self, symbol: str, grid_size: float = 0.01, window: int = 2):
        self.symbol = symbol.upper()
        self.grid_size = grid_size
        self.prices: Deque[float] = deque(maxlen=window)
        self.base_price: Optional[float] = None
        self.last_signal: Optional[str] = None

    def on_price_update(self, symbol: str, price: float) -> None:
        self.prices.append(price)
        if self.base_price is None:
            self.base_price = price

    def generate_signal(self) -> Optional[str]:
        if len(self.prices) < self.prices.maxlen:
            return None
        if self.base_price is None:
            return None
        price = self.prices[-1]
        diff = (price - self.base_price) / self.base_price
        if diff <= -self.grid_size and self.last_signal != "buy":
            self.last_signal = "buy"
            self.base_price = price
            return "buy"
        if diff >= self.grid_size and self.last_signal != "sell":
            self.last_signal = "sell"
            self.base_price = price
            return "sell"
        return None
