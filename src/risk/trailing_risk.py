from .simple_risk import SimpleRiskManager


class TrailingRiskManager(SimpleRiskManager):
    """Risk manager with trailing stop support."""

    def __init__(self, stop_loss: float, take_profit: float, trailing: float):
        super().__init__(stop_loss, take_profit)
        self.trailing = trailing
        self.highs: dict[str, float] = {}

    def update_high(self, symbol: str, price: float) -> None:
        prev = self.highs.get(symbol)
        if prev is None or price > prev:
            self.highs[symbol] = price

    def check(self, symbol: str, entry_price: float, current_price: float) -> str | None:
        self.update_high(symbol, current_price)
        high = self.highs.get(symbol, current_price)
        if current_price <= high * (1 - self.trailing):
            return "trailing_stop"
        return super().check(entry_price, current_price)
