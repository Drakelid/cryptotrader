from __future__ import annotations

from abc import ABC, abstractmethod

from risk.base import Account, BaseRiskManager


class Trader(ABC):
    def __init__(self, account: Account, risk_manager: BaseRiskManager):
        self.account = account
        self.risk_manager = risk_manager

    @abstractmethod
    def execute_trade(self, symbol: str, price: float, side: str) -> float:
        """Execute trade and return executed size."""
