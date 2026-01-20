import json
import time
import websocket

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"

def on_message(ws, message):
    data = json.loads(message)

    event = {
        "symbol": data["s"],
        "price": float(data["p"]),
        "volume": float(data["q"]),
        "timestamp": data["T"]
    }

    # For now, just print (later send to C++ engine / DB)
    print(event)

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
    ws.run_forever()
