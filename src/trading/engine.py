import asyncio
from typing import Optional

from .strategies.base import BaseStrategy

class TradingEngine:
    """Engine that processes streaming price updates."""

    def __init__(self, client, strategy: BaseStrategy):
        self.client = client
        self.strategy = strategy
        self._task: Optional[asyncio.Task] = None

    async def run_once(self) -> None:
        data = await self.client.recv()
        await self.strategy.on_price_update(data)

    async def run_forever(self) -> None:
        async for data in self.client.listen():
            await self.strategy.on_price_update(data)

    def start_background(self) -> None:
        self._task = asyncio.create_task(self.run_forever())

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
