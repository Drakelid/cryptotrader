from abc import ABC, abstractmethod
from typing import Any

class Strategy(ABC):
    """Abstract base class for trading strategies."""

    @abstractmethod
    def on_price_update(self, symbol: str, price: float) -> None:
        """Handle new price data for the given symbol."""
        pass

    @abstractmethod
    def generate_signal(self) -> Any:
        """Return signal object or None if no trade is desired."""
        pass
