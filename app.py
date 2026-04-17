from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    symbol = data.get("symbol", "N/A")
    price = data.get("price", "N/A")
    signal = data.get("signal", "N/A")
    timeframe = data.get("timeframe", "")

    message = f"""
🚀 {signal} {symbol}
💰 Price: {price}
⏰ TF: {timeframe}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
