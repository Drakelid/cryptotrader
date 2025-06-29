from __future__ import annotations

from .base import Trader


class BinanceTrader(Trader):
    """Stub for Binance execution."""

    def execute_trade(self, symbol: str, price: float, side: str) -> float:
        size = self.risk_manager.calculate_position_size(self.account, price)
        if size <= 0:
            return 0.0

        exposure_change = price * size
        if side.lower() == "sell":
            exposure_change *= -1

        self.risk_manager.update_exposure(self.account, exposure_change)
        # Placeholder for real API call
        return size
