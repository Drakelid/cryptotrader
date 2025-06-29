from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
import yaml

from core.engine import TradingEngine

app = FastAPI(title="CryptoTrader Dashboard")

class RunRequest(BaseModel):
    config: str = "config/strategies.yaml"
    iterations: int = 1
    interval: float = 1.0

class RunResponse(BaseModel):
    results: List[List[dict]]

@app.get("/")
def read_root():
    return {"message": "CryptoTrader dashboard"}

@app.post("/run", response_model=RunResponse)
def run_engine(req: RunRequest):
    with open(req.config) as f:
        cfg = yaml.safe_load(f)
    engine = TradingEngine(cfg.get("strategies", []), interval=req.interval)
    results = engine.run(req.iterations)
    return RunResponse(results=results)
