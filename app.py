from flask import Flask, request, jsonify
import requests
import os
import time

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# store latest signal (for cBot polling)
latest_signal = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    global latest_signal

    data = request.json or {}

    # ✅ extract fields safely
    signal = data.get("signal", "N/A")
    symbol = data.get("symbol", "N/A")
    entry = data.get("entry", "N/A")
    sl = data.get("sl", "0")
    tp1 = data.get("tp1", "0")
    tp2 = data.get("tp2", "0")
    reason = data.get("reason", "N/A")
    timeframe = data.get("timeframe", "N/A")

    # ✅ generate unique ID (for cBot duplicate prevention)
    signal_id = str(int(time.time()))

    # ✅ store for cBot
    latest_signal = {
        "id": signal_id,
        "signal": signal,
        "symbol": symbol,
        "entry": entry,
        "sl": float(sl),
        "tp1": float(tp1),
        "tp2": float(tp2),
        "timeframe": timeframe,
        "timestamp": time.time()
    }

    # ✅ nicer formatting (BUY/SELL color)
    direction_icon = "🟢 BUY" if signal == "BUY" else "🔴 SELL"

    message = f"""
📊 TRADE SIGNAL

🚀 Direction: {direction_icon} {symbol}
⏰ Timeframe: {timeframe}

💰 Entry: {entry}
🛑 SL: {sl}
🎯 TP1: {tp1}
🎯 TP2: {tp2}

📌 Reason:
{reason}
"""

    # ✅ send to Telegram
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        response = requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": message
        })

        print("Telegram status:", response.status_code)
        print("Telegram response:", response.text)

    except Exception as e:
        print("Telegram error:", str(e))

    return jsonify({"status": "ok"})


# ✅ endpoint for cBot
@app.route('/signal', methods=['GET'])
def get_signal():
    return jsonify(latest_signal)


# ✅ health check
@app.route('/')
def home():
    return "Bot running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
