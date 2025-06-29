import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data.cmc.cmc_client import CoinMarketCapClient


def test_get_trending_tokens():
    client = CoinMarketCapClient(api_key="test")
    with patch.object(client.session, "get") as mock_get:
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = {"data": [{"id": 1}]}
        tokens = client.get_trending_tokens(limit=1)
        assert tokens == [{"id": 1}]
