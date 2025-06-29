import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fastapi.testclient import TestClient
from ui.dashboard import app


def test_dashboard_run():
    client = TestClient(app)
    # Patch sleep to avoid delays during tests
    with patch("core.engine.time.sleep", return_value=None):
        resp = client.post("/run", json={"iterations": 1})
    assert resp.status_code == 200
    data = resp.json()
    assert "results" in data
