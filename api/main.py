from fastapi import FastAPI, Query
from ranking.ranker import get_top_k
import redis
import json

app = FastAPI(title="Real-Time Signal API")

# Redis connection
r = redis.Redis(host="localhost", port=6379, decode_responses=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/signals/top")
def top_signals(k: int = Query(5, ge=1, le=20)):
    """
    Returns top-k ranked instruments
    """
    return get_top_k(k)


@app.get("/signals/{symbol}")
def signal_by_symbol(symbol: str):
    """
    Returns signal info for a specific instrument
    """
    score = r.zscore("signal_ranking", symbol)
    if score is None:
        return {"error": "Symbol not found"}

    reasons = r.get(f"reason:{symbol}")
    return {
        "symbol": symbol,
        "score": score,
        "reasons": json.loads(reasons) if reasons else []
    }
