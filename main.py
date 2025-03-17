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
            stock_data = {}
            for ticker in stock_list:
                stock = yf.Ticker(ticker)
                try:
                    live_price = stock.fast_info["last_price"]
                    history = stock.history(period="1d")  # Get today's price data
                    
                    if not history.empty:
                        opening_price = history["Open"].iloc[0]  # Get today's opening price
                        change = ((live_price - opening_price) / opening_price) * 100  # % Change from Open
                        stock_data[ticker] = {
                            "price": round(live_price, 2),
                            "change": round(change, 2)
                        }
                    else:
                        stock_data[ticker] = {"price": "N/A", "change": "N/A"}
                
                except:
                    stock_data[ticker] = {"price": "N/A", "change": "N/A"}

            return stock_data

        nifty_data = get_prices(nifty50_top5)
        banknifty_data = get_prices(banknifty_top5)

        return jsonify({"nifty50": nifty_data, "banknifty": banknifty_data})

    except Exception as e:
        print("Error fetching stock prices:", e)
        return jsonify({"error": "Unable to fetch stock prices"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
