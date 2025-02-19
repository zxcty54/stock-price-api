import os
from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Stock Price API is Running!"

@app.route('/get-price/<symbol>')
def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period="1d")

        if history.empty:
            return jsonify({"error": "No data available for this symbol"}), 400

        price = history["Close"].iloc[-1]  # Get latest closing price
        return jsonify({"symbol": symbol, "price": round(price, 2)})

    except Exception as e:
        print("Error fetching stock price:", e)
        return jsonify({"error": "Invalid symbol or data unavailable"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render assigns a port dynamically
    app.run(host="0.0.0.0", port=port)
