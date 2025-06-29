from typing import Optional

from .base import Strategy


class AIPredictiveStrategy(Strategy):
    """Extremely naive predictive strategy using previous price momentum."""

    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self.prev_price: Optional[float] = None
        self.last_signal: Optional[str] = None

    def on_price_update(self, symbol: str, price: float) -> None:
        self.prev_price, self.current_price = getattr(self, "current_price", price), price

    def generate_signal(self) -> Optional[str]:
        if self.prev_price is None:
            return None
        if self.current_price > self.prev_price and self.last_signal != "buy":
            self.last_signal = "buy"
            return "buy"
        if self.current_price < self.prev_price and self.last_signal != "sell":
            self.last_signal = "sell"
            return "sell"
        return None
