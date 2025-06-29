from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
import yaml

from core.engine import TradingEngine
from backtest.simulator import BacktestSimulator, _default_strategy
from execution import PaperTrader, BinanceTrader

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


@app.get("/")
def read_root():
    return {"message": "CryptoTrader dashboard"}


@app.post("/run", response_model=RunResponse)
def run_engine(req: RunRequest):
    with open(req.config) as f:
        cfg = yaml.safe_load(f)
    executor = PaperTrader() if req.paper else BinanceTrader()
    engine = TradingEngine(cfg.get("strategies", []), interval=req.interval, executor=executor)
    results = engine.run(req.iterations)
    return RunResponse(results=results)


@app.post("/backtest", response_model=BacktestResponse)
def run_backtest(req: BacktestRequest):
    strategy = _default_strategy(req.symbol)
    sim = BacktestSimulator(strategy)
    signals = list(sim.run(BacktestSimulator.load_prices(req.csv_file)))
    return BacktestResponse(signals=signals)


@app.post("/autonomous")
def run_autonomous(req: AutoRequest):
    with open(req.config) as f:
        cfg = yaml.safe_load(f)
    executor = PaperTrader() if req.paper else BinanceTrader()
    engine = TradingEngine(cfg.get("strategies", []), interval=req.interval, executor=executor)
    i = 0
    while req.iterations is None or i < req.iterations:
        engine.run_once()
        i += 1
    return {"status": "completed", "iterations": i}
