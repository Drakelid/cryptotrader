import asyncio
import json
from typing import AsyncGenerator, Optional
import websockets

class BinanceWebSocket:
    """Simple Binance WebSocket client for ticker or kline streams."""
    BASE_URL = "wss://stream.binance.com:9443/ws"

    def __init__(self, symbol: str, stream: str = "ticker"):
        self.symbol = symbol.lower()
        self.stream = stream
        self.url = f"{self.BASE_URL}/{self.symbol}@{self.stream}"
        self._conn: Optional[websockets.WebSocketClientProtocol] = None

    async def connect(self) -> websockets.WebSocketClientProtocol:
        self._conn = await websockets.connect(self.url)
        return self._conn

    async def disconnect(self) -> None:
        if self._conn:
            await self._conn.close()
            self._conn = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

    async def recv(self) -> dict:
        if not self._conn:
            await self.connect()
        msg = await self._conn.recv()
        return json.loads(msg)

    async def listen(self) -> AsyncGenerator[dict, None]:
        if not self._conn:
            await self.connect()
        try:
            async for msg in self._conn:
                yield json.loads(msg)
        finally:
            await self.disconnect()
