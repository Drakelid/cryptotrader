import os
from typing import Any
from binance.client import Client


class BinanceTrader:
    """Executor that places real orders via Binance."""

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        client: Client | None = None,
    ) -> None:
        api_key = api_key or os.getenv("BINANCE_API_KEY")
        api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        if client is not None:
            self.client = client
        else:
            if not api_key or not api_secret:
                raise ValueError(
                    "API key and secret must be provided for live trading"
                )
            self.client = Client(api_key, api_secret)

    def execute(
        self,
        symbol: str,
        side: str,
        price: float | None = None,
        quantity: float = 1.0,
        order_type: str = "MARKET",
    ) -> Any:
        side_str = "BUY" if side == "buy" else "SELL"
        params = {
            "symbol": symbol.upper(),
            "side": side_str,
            "type": order_type,
            "quantity": quantity,
        }
        if order_type == "LIMIT" and price is not None:
            params["price"] = str(price)
            params["timeInForce"] = "GTC"
        return self.client.create_order(**params)
