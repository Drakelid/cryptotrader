class PaperTrader:
    """Simple paper trading executor for testing strategies."""

    def __init__(self, starting_balance: float = 1000.0, risk_manager=None):
        self.balance = starting_balance
        self.positions: dict[str, float] = {}
        self.entry_prices: dict[str, float] = {}
        self.trades: list[dict] = []
        self.risk_manager = risk_manager

    def execute(self, symbol: str, side: str, price: float, quantity: float = 1.0) -> bool:
        if side == "buy":
            cost = price * quantity
            if self.balance < cost:
                return False
            self.balance -= cost
            old_qty = self.positions.get(symbol, 0.0)
            new_qty = old_qty + quantity
            self.positions[symbol] = new_qty
            prev_price = self.entry_prices.get(symbol, 0.0)
            if old_qty == 0:
                self.entry_prices[symbol] = price
                if hasattr(self.risk_manager, "update_high"):
                    self.risk_manager.update_high(symbol, price)
            else:
                self.entry_prices[symbol] = (prev_price * old_qty + price * quantity) / new_qty
        elif side == "sell":
            qty = self.positions.get(symbol, 0.0)
            if qty < quantity:
                return False
            self.balance += price * quantity
            remaining = qty - quantity
            self.positions[symbol] = remaining
            if remaining == 0:
                self.entry_prices.pop(symbol, None)
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

    def evaluate(self, symbol: str, price: float) -> None:
        if not self.risk_manager:
            return
        qty = self.positions.get(symbol, 0.0)
        if qty <= 0:
            return
        entry = self.entry_prices.get(symbol)
        if entry is None:
            return
        try:
            action = self.risk_manager.check(symbol, entry, price)
        except TypeError:
            action = self.risk_manager.check(entry, price)
        if action:
            self.execute(symbol, "sell", price=price, quantity=qty)
