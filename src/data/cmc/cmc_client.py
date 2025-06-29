import os
import logging
from typing import Optional, List, Dict

import requests

CMC_API_URL = "https://pro-api.coinmarketcap.com"

class CoinMarketCapClient:
    """Client for CoinMarketCap public REST API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("CMC_API_KEY")
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"X-CMC_PRO_API_KEY": self.api_key})

    def get_trending_tokens(self, limit: int = 10) -> List[Dict[str, str]]:
        try:
            resp = self.session.get(
                f"{CMC_API_URL}/v1/cryptocurrency/trending/latest",
                params={"limit": limit},
                timeout=5,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("data", [])
        except requests.RequestException as exc:
            logging.error("Failed to fetch trending tokens: %s", exc)
            return []
