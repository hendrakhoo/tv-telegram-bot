from flask import Flask, request, jsonify
import requests
import os
import time
import json

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# store latest signal (for cBot polling)
latest_signal = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    global latest_signal

    data = {}

    try:
        # ✅ Try normal JSON first
        if request.is_json:
            data = request.get_json()

        else:
            # ✅ Fallback to raw body text
            raw_data = request.data.decode('utf-8')
            print("Raw incoming data:", raw_data)

            # Try converting raw string into JSON
            data = json.loads(raw_data)

    except Exception as e:
        print("JSON parse error:", str(e))

        # fallback empty object
        data = {}

    # ✅ extract fields safely
    signal = data.get("signal", "N/A")
    symbol = data.get("symbol", "N/A")
    entry = data.get("entry", "N/A")
    sl = data.get("sl", "0")
    tp1 = data.get("tp1", "0")
    tp2 = data.get("tp2", "0")
    reason = data.get("reason", "N/A")
    timeframe = data.get("timeframe", "N/A")

    # ✅ generate unique ID
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

    # ✅ normalize signal
    signal_upper = str(signal).upper()

    # ✅ BUY / SELL display
    if signal_upper == "BUY":
        direction_text = f"🟢 BUY 📈 {symbol}"
    elif signal_upper == "SELL":
        direction_text = f"🔴 SELL 📉 {symbol}"
    else:
        direction_text = f"⚪ {signal_upper} {symbol}"

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

    return jsonify({
        "status": "ok",
        "received": data
    })


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
