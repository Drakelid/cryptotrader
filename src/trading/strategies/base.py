from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    """Base trading strategy."""

    @abstractmethod
    async def on_price_update(self, data: dict) -> None:
        """Handle a new price update from the exchange."""
        raise NotImplementedError
