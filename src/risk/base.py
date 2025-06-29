from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Account:
    equity: float
    open_exposure: float = 0.0
    daily_loss: float = 0.0


class BaseRiskManager(ABC):
    """Abstract base class for risk managers."""

    @abstractmethod
    def calculate_position_size(self, account: Account, price: float) -> float:
        """Return the number of units to trade given account and price."""

    def register_loss(self, account: Account, loss: float) -> None:
        """Record a realized loss and update account equity."""
        account.daily_loss += loss
        account.equity = max(account.equity - loss, 0)

    def update_exposure(self, account: Account, delta: float) -> None:
        account.open_exposure = max(account.open_exposure + delta, 0.0)
