
from risk.base import Account
from risk.dynamic import DynamicRiskManager
from trader.binance import BinanceTrader


def test_binance_trader_uses_risk_manager():
    account = Account(equity=10000)
    rm = DynamicRiskManager(risk_pct=1, daily_loss_limit_pct=2, max_exposure_pct=5)
    trader = BinanceTrader(account, rm)

    size = trader.execute_trade("BTC", price=100, side="buy")
    assert size == 1
    assert account.open_exposure == 100


def test_binance_trader_sell():
    account = Account(equity=10000, open_exposure=200)
    rm = DynamicRiskManager(risk_pct=1, daily_loss_limit_pct=2, max_exposure_pct=5)
    trader = BinanceTrader(account, rm)

    size = trader.execute_trade("BTC", price=100, side="sell")
    assert size == 1
    assert account.open_exposure == 100
