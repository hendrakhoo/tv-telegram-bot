from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    signal = data.get("signal", "N/A")
    symbol = data.get("symbol", "N/A")
    entry = data.get("entry", "N/A")
    sl = data.get("sl", "N/A")
    tp1 = data.get("tp1", "N/A")
    tp2 = data.get("tp2", "N/A")
    reason = data.get("reason", "N/A")
    timeframe = data.get("timeframe", "N/A")

    message = f"""
📊 TRADE SIGNAL

🚀 Direction: {signal} {symbol}
⏰ Timeframe: {timeframe.period}

💰 Entry: {entry}
🛑 SL: {sl}
🎯 TP1: {tp1}
🎯 TP2: {tp2}

📌 Reason:
{reason}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
