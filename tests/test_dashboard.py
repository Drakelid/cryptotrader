import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fastapi.testclient import TestClient
from ui.dashboard import app


def test_dashboard_endpoints():
    client = TestClient(app)
    with patch("core.engine.time.sleep", return_value=None):
        resp = client.post("/run", json={"iterations": 1, "paper": True})
    assert resp.status_code == 200
    assert "results" in resp.json()

    with patch("backtest.simulator.BacktestSimulator.load_prices", return_value=[1, 2, 3]):
        resp = client.post("/backtest", json={"csv_file": "dummy.csv"})
    assert resp.status_code == 200
    assert "signals" in resp.json()

    with patch("autonomous.trader.time.sleep", return_value=None):
        resp = client.post("/autonomous", json={"iterations": 1})
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"
