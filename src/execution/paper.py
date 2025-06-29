class PaperTrader:
    """Simple paper trading executor for testing strategies."""

    def __init__(self, starting_balance: float = 1000.0):
        self.balance = starting_balance
        self.positions: dict[str, float] = {}
        self.trades: list[dict] = []

    def execute(self, symbol: str, side: str, price: float, quantity: float = 1.0) -> bool:
        if side == "buy":
            cost = price * quantity
            if self.balance < cost:
                return False
            self.balance -= cost
            self.positions[symbol] = self.positions.get(symbol, 0.0) + quantity
        elif side == "sell":
            qty = self.positions.get(symbol, 0.0)
            if qty < quantity:
                return False
            self.balance += price * quantity
            self.positions[symbol] = qty - quantity
        else:
            return False
        self.trades.append({
            "symbol": symbol,
            "side": side,
            "price": price,
            "quantity": quantity,
        })
        return True

    def portfolio_value(self, prices: dict[str, float]) -> float:
        value = self.balance
        for symbol, qty in self.positions.items():
            price = prices.get(symbol)
            if price is not None:
                value += qty * price
        return value
