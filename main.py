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

        price = history["Close"].iloc[-1]
        return jsonify({"symbol": symbol, "price": round(price, 2)})

    except Exception as e:
        print("Error fetching stock price:", e)
        return jsonify({"error": "Invalid symbol or data unavailable"}), 500

@app.route('/gainers-losers')
def get_gainers_losers():
    try:
        tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]  # Example stocks
        stock_data = {ticker: yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1] for ticker in tickers}

        sorted_stocks = sorted(stock_data.items(), key=lambda x: x[1], reverse=True)
        top_gainers = sorted_stocks[:3]  # Top 3 gainers
        top_losers = sorted_stocks[-3:]  # Bottom 3 losers

        return jsonify({"top_gainers": top_gainers, "top_losers": top_losers})

    except Exception as e:
        print("Error fetching gainers/losers:", e)
        return jsonify({"error": "Unable to fetch gainers/losers"}), 500

# New API for Market Indices (Dow Jones, S&P 500, NASDAQ)
@app.route('/market-indices')
def get_market_indices():
    try:
        indices = {
            "Dow Jones": "^DJI",
            "S&P 500": "^GSPC",
            "NASDAQ": "^IXIC"
        }
        
        index_prices = {}
        for name, symbol in indices.items():
            stock = yf.Ticker(symbol)
            history = stock.history(period="1d")

            if not history.empty:
                index_prices[name] = round(history["Close"].iloc[-1], 2)

        return jsonify(index_prices)

    except Exception as e:
        print("Error fetching market indices:", e)
        return jsonify({"error": "Unable to fetch market indices"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
