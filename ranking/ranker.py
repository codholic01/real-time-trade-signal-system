import redis
import json

# Connect to Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

RANKING_KEY = "signal_ranking"   # Redis Sorted Set


def update_ranking(signal):
    """
    signal = {
        'symbol': 'BTCUSDT',
        'signal_score': 40,
        'reasons': ['volume_spike']
    }
    """
    symbol = signal["symbol"]
    score = signal["signal_score"]

    # Ignore zero signals
    if score <= 0:
        return

    # Store score in sorted set
    r.zadd(RANKING_KEY, {symbol: score})

    # Store reasons separately
    r.set(f"reason:{symbol}", json.dumps(signal["reasons"]))


def get_top_k(k=5):
    """
    Returns top-k ranked instruments
    """
    results = r.zrevrange(RANKING_KEY, 0, k - 1, withscores=True)

    top = []
    for symbol, score in results:
        reasons = r.get(f"reason:{symbol}")
        top.append({
            "symbol": symbol,
            "score": score,
            "reasons": json.loads(reasons) if reasons else []
        })

    return top
