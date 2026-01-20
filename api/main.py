from fastapi import FastAPI

app = FastAPI()

# Temporary in-memory signals (later Redis)
signals = [
    {"symbol": "BTCUSDT", "score": 82},
    {"symbol": "ETHUSDT", "score": 65},
    {"symbol": "SOLUSDT", "score": 40}
]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/signals/top")
def get_top_signals(limit: int = 5):
    return signals[:limit]

@app.get("/signals/{symbol}")
def get_signal(symbol: str):
    for s in signals:
        if s["symbol"] == symbol:
            return s
    return {"error": "Symbol not found"}
