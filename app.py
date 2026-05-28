from flask import Flask, request, jsonify
import requests
import os
import time
import json

# ✅ create flask app FIRST
app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# store latest signal
latest_signal = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    global latest_signal

    data = {}

    try:
        # ✅ Try JSON first
        if request.is_json:
            data = request.get_json(silent=True) or {}

        # ✅ Try raw body
        if not data:
            raw_data = request.data.decode('utf-8').strip()

            print("Raw incoming data:", raw_data)

            if raw_data:
                data = json.loads(raw_data)

    except Exception as e:
        print("JSON parse error:", str(e))
        data = {}

    # ✅ safely extract fields
    signal = str(data.get("signal", "N/A"))
    symbol = str(data.get("symbol", "N/A"))
    entry = str(data.get("entry", "N/A"))
    reason = str(data.get("reason", "N/A"))
    timeframe = str(data.get("timeframe", "N/A"))

    # ✅ safe float conversion
    def safe_float(value, default=0):
        try:
            return float(value)
        except:
            return default

    sl = safe_float(data.get("sl", 0))
    tp1 = safe_float(data.get("tp1", 0))
    tp2 = safe_float(data.get("tp2", 0))

    # ✅ signal ID
    signal_id = str(int(time.time()))

    latest_signal = {
        "id": signal_id,
        "signal": signal,
        "symbol": symbol,
        "entry": entry,
        "sl": sl,
        "tp1": tp1,
        "tp2": tp2,
        "timeframe": timeframe,
        "timestamp": time.time()
    }

    # ✅ direction formatting
    signal_raw = str(data.get("signal", "N/A"))
    signal_upper = signal_raw.strip().upper()

    if signal_upper == "BUY":
        direction_text = f"🟢 BUY 📈 {symbol}"
    elif signal_upper == "SELL":
        direction_text = f"🔴 SELL 📉 {symbol}"
    else:
        direction_text = f"⚪ {signal_upper} {symbol}"

    message = f"""
📊 TRADE SIGNAL

🚀 Direction: {direction_text}
⏰ Timeframe: {timeframe}

💰 Entry: {entry}
🛑 SL: {sl}
🎯 TP1: {tp1}
🎯 TP2: {tp2}

📌 Reason:
{reason}
"""

    # ✅ Telegram
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
