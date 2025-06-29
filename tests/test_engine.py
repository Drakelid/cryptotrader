import asyncio
import json
import pytest

from src.trading.engine import TradingEngine
from src.trading.strategies.base import BaseStrategy

class DummyWebSocket:
    def __init__(self, messages):
        self._messages = asyncio.Queue()
        for m in messages:
            self._messages.put_nowait(json.dumps(m))

    async def recv(self):
        return json.loads(await self._messages.get())

    async def listen(self):
        while not self._messages.empty():
            yield json.loads(await self._messages.get())

class DummyStrategy(BaseStrategy):
    def __init__(self):
        self.received = []

    async def on_price_update(self, data: dict) -> None:
        self.received.append(data)

@pytest.mark.asyncio
async def test_engine_run_once():
    ws = DummyWebSocket([{"price": "1"}])
    strategy = DummyStrategy()
    engine = TradingEngine(ws, strategy)
    await engine.run_once()
    assert strategy.received == [{"price": "1"}]

@pytest.mark.asyncio
async def test_engine_run_forever():
    ws = DummyWebSocket([{"price": "1"}, {"price": "2"}])
    strategy = DummyStrategy()
    engine = TradingEngine(ws, strategy)
    await engine.run_forever()
    assert strategy.received == [{"price": "1"}, {"price": "2"}]
