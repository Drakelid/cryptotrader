import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data.binance.binance_client import BinanceClient


def test_get_ticker_price():
    client = BinanceClient(api_key="test")
    with patch.object(client.session, "get") as mock_get:
        mock_get.return_value.json.return_value = {"price": "1.23"}
        mock_get.return_value.raise_for_status.return_value = None
        price = client.get_ticker_price("BTCUSDT")
        assert price == 1.23


def test_ping():
    client = BinanceClient(api_key="test")
    with patch.object(client.session, "get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        assert client.ping()
