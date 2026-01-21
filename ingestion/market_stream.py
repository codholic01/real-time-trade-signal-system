import json
import websocket
import requests

# Binance WebSocket URL for real-time BTC/USDT trades
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"

# C++ Signal Engine HTTP endpoint
ENGINE_URL = "http://127.0.0.1:18080/event"


def send_to_engine(event):
    """
    Sends normalized market event to the C++ signal engine
    and prints the returned signal.
    """
    try:
        response = requests.post(ENGINE_URL, json=event, timeout=1)
        print("Signal:", response.json())
    except Exception as e:
        print("Error sending to engine:", e)


def on_message(ws, message):
    """
    Called every time Binance sends a new trade event
    """
    data = json.loads(message)

    # ---- DATA NORMALIZATION (STEP 2) ----
    event = {
        "symbol": data["s"],
        "price": float(data["p"]),
        "volume": float(data["q"]),
        "timestamp": data["T"]
    }

    # ---- SEND TO C++ SIGNAL ENGINE (STEP 3) ----
    send_to_engine(event)


def on_error(ws, error):
    print("WebSocket error:", error)


def on_close(ws):
    print("WebSocket closed")


def on_open(ws):
    print("WebSocket connection opened")


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        BINANCE_WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    # Keep the WebSocket connection alive
    ws.run_forever()
