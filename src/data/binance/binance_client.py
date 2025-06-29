import os
import logging
from typing import Optional, Dict

import requests

BINANCE_API_URL = "https://api.binance.com"

class BinanceClient:
    """Minimal client for Binance public REST API."""

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def ping(self) -> bool:
        try:
            resp = self.session.get(f"{BINANCE_API_URL}/api/v3/ping", timeout=5)
            resp.raise_for_status()
            return True
        except requests.RequestException as exc:
            logging.error("Binance ping failed: %s", exc)
            return False

    def get_ticker_price(self, symbol: str) -> Optional[float]:
        try:
            resp = self.session.get(
                f"{BINANCE_API_URL}/api/v3/ticker/price",
                params={"symbol": symbol.upper()},
                timeout=5,
            )
            resp.raise_for_status()
            data: Dict[str, str] = resp.json()
            return float(data["price"])
        except (requests.RequestException, KeyError, ValueError) as exc:
            logging.error("Failed to fetch ticker price: %s", exc)
            return None
