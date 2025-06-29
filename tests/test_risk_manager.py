
from risk.base import Account
from risk.dynamic import DynamicRiskManager
from trader.paper import PaperTrader


def test_dynamic_position_size():
    account = Account(equity=10000)
    rm = DynamicRiskManager(risk_pct=1, daily_loss_limit_pct=2, max_exposure_pct=5)
    trader = PaperTrader(account, rm)

    size = trader.execute_trade("BTC", price=100, side="buy")
    assert size == 1
    assert account.open_exposure == 100


def test_exposure_limit():
    account = Account(equity=10000, open_exposure=490)
    rm = DynamicRiskManager(risk_pct=1, daily_loss_limit_pct=2, max_exposure_pct=5)
    trader = PaperTrader(account, rm)

    size = trader.execute_trade("BTC", price=100, side="buy")
    assert size == 0.1
    assert account.open_exposure == 500


def test_daily_loss_limit():
    account = Account(equity=10000, daily_loss=200)
    rm = DynamicRiskManager(risk_pct=1, daily_loss_limit_pct=2, max_exposure_pct=5)
    trader = PaperTrader(account, rm)

    size = trader.execute_trade("BTC", price=100, side="buy")
    assert size == 0
    assert account.open_exposure == 0


def test_sell_reduces_exposure():
    account = Account(equity=10000, open_exposure=200)
    rm = DynamicRiskManager(risk_pct=1, daily_loss_limit_pct=2, max_exposure_pct=5)
    trader = PaperTrader(account, rm)

    size = trader.execute_trade("BTC", price=100, side="sell")
    assert size == 1
    assert account.open_exposure == 100


def test_register_loss_updates_equity():
    account = Account(equity=10000)
    rm = DynamicRiskManager(risk_pct=1, daily_loss_limit_pct=2, max_exposure_pct=5)
    rm.register_loss(account, 50)
    assert account.daily_loss == 50
    assert account.equity == 9950
