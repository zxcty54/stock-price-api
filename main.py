from flask import Flask, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def home():
    return "Stock Price API is Running!"

@app.route('/get-price/<symbol>')
def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        price = stock.history(period="1d")["Close"].iloc[-1]
        return jsonify({"symbol": symbol, "price": price})
    except:
        return jsonify({"error": "Invalid symbol or data unavailable"})

if __name__ == '__main__':
    app.run(debug=True)
