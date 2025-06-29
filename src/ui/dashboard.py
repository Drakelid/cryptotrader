from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from src.data.binance.binance_client import BinanceClient
from src.data.cmc.cmc_client import CoinMarketCapClient

from src.backtest.simulator import run_backtest as cli_run_backtest
from src.autonomous.trader import run_autonomous as cli_run_autonomous
from src.main import run_engine as cli_run_engine

app = FastAPI(title="CryptoTrader Dashboard")


class RunRequest(BaseModel):
    config: str = "config/strategies.yaml"
    iterations: int = 1
    interval: float = 1.0
    paper: bool = False


class RunResponse(BaseModel):
    results: List[List[dict]]


class BacktestRequest(BaseModel):
    csv_file: str
    symbol: str = "BTCUSDT"


class BacktestResponse(BaseModel):
    signals: List[str | None]


class AutoRequest(BaseModel):
    config: str = "config/strategies.yaml"
    interval: float = 1.0
    paper: bool = True
    iterations: int | None = None
    stop_loss: float = 0.02
    take_profit: float = 0.04
    trailing: float = 0.03


class StatusResponse(BaseModel):
    binance_ok: bool


class TrendingResponse(BaseModel):
    tokens: List[dict]


@app.get("/")
def read_root():
    return {"message": "CryptoTrader dashboard"}


@app.post("/run", response_model=RunResponse)
def run_engine(req: RunRequest):
    results = cli_run_engine(
        config_path=req.config,
        iterations=req.iterations,
        interval=req.interval,
        paper=req.paper,
    )
    return RunResponse(results=results)


@app.post("/backtest", response_model=BacktestResponse)
def backtest_endpoint(req: BacktestRequest):
    signals = cli_run_backtest(req.csv_file, req.symbol)
    return BacktestResponse(signals=signals)


@app.post("/autonomous")
def autonomous_endpoint(req: AutoRequest):
    cli_run_autonomous(
        config_path=req.config,
        interval=req.interval,
        paper=req.paper,
        iterations=req.iterations,
        stop_loss=req.stop_loss,
        take_profit=req.take_profit,
        trailing=req.trailing,
    )
    return {"status": "completed", "iterations": req.iterations or 0}


@app.get("/status", response_model=StatusResponse)
def status_endpoint():
    client = BinanceClient()
    return StatusResponse(binance_ok=client.ping())


@app.get("/trending", response_model=TrendingResponse)
def trending_endpoint(limit: int = 5):
    cmc = CoinMarketCapClient()
    tokens = cmc.get_trending_tokens(limit=limit)
    return TrendingResponse(tokens=tokens)
