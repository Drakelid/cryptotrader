import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from src.ui.dashboard import app


def test_dashboard_endpoints():
    client = TestClient(app)
    with patch("src.core.engine.time.sleep", return_value=None):
        resp = client.post("/run", json={"iterations": 1, "paper": True})
    assert resp.status_code == 200
    assert "results" in resp.json()

    with patch("src.backtest.simulator.BacktestSimulator.load_prices", return_value=[1, 2, 3]):
        resp = client.post("/backtest", json={"csv_file": "dummy.csv"})
    assert resp.status_code == 200
    assert "signals" in resp.json()

    with patch("src.autonomous.trader.time.sleep", return_value=None):
        resp = client.post("/autonomous", json={"iterations": 1, "stop_loss": 0.02})
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"

    with patch("src.data.binance.binance_client.requests.Session.get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        resp = client.get("/status")
    assert resp.status_code == 200
    assert "binance_ok" in resp.json()

    with patch("src.data.cmc.cmc_client.requests.Session.get") as mock_cmc:
        mock_cmc.return_value.raise_for_status.return_value = None
        mock_cmc.return_value.json.return_value = {"data": [{"id": 1}]}
        resp = client.get("/trending")
    assert resp.status_code == 200
    assert resp.json()["tokens"] == [{"id": 1}]
