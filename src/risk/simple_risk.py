class SimpleRiskManager:
    """Very basic risk management with fixed stop loss and take profit."""

    def __init__(self, stop_loss: float, take_profit: float):
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def check(self, entry_price: float, current_price: float) -> str | None:
        if current_price <= entry_price * (1 - self.stop_loss):
            return "stop_loss"
        if current_price >= entry_price * (1 + self.take_profit):
            return "take_profit"
        return None
