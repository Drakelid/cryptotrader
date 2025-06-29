from __future__ import annotations

from .base import BaseRiskManager, Account


class DynamicRiskManager(BaseRiskManager):
    """Risk manager that sizes positions based on account equity."""

    def __init__(self, risk_pct: float, daily_loss_limit_pct: float, max_exposure_pct: float):
        self.risk_pct = risk_pct
        self.daily_loss_limit_pct = daily_loss_limit_pct
        self.max_exposure_pct = max_exposure_pct

    def _loss_limit_reached(self, account: Account) -> bool:
        return account.daily_loss >= (self.daily_loss_limit_pct / 100) * account.equity

    def calculate_position_size(self, account: Account, price: float) -> float:
        if self._loss_limit_reached(account):
            return 0.0

        max_risk_value = account.equity * (self.risk_pct / 100)
        desired_size = max_risk_value / price

        max_exposure_value = account.equity * (self.max_exposure_pct / 100)
        remaining_exposure = max_exposure_value - account.open_exposure
        if remaining_exposure <= 0:
            return 0.0

        max_size_by_exposure = remaining_exposure / price
        return max(0.0, min(desired_size, max_size_by_exposure))
