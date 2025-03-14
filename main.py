import os
from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

# Top 5 companies from NIFTY 50 & BANK NIFTY
nifty50_top5 = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]
banknifty_top5 = ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "AXISBANK.NS", "KOTAKBANK.NS"]

@app.route('/')
def home():
    return "Stock Price API is Running!"

@app.route('/nifty-bank-live')
def get_nifty_bank_prices():
    try:
        def get_prices(stock_list):
            stock_prices = {}
            for ticker in stock_list:
                stock = yf.Ticker(ticker)
                history = stock.history(period="1d")  # Get today's price
                
                if history.empty:
                    stock_prices[ticker] = "N/A"
                else:
                    stock_prices[ticker] = round(history["Close"].iloc[-1], 2)  # Get last closing price

            return stock_prices

        nifty_prices = get_prices(nifty50_top5)
        banknifty_prices = get_prices(banknifty_top5)

        return jsonify({"nifty50": nifty_prices, "banknifty": banknifty_prices})

    except Exception as e:
        print("Error fetching stock prices:", e)
        return jsonify({"error": "Unable to fetch stock prices"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
