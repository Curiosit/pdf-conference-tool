import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def stock_portfolio(user_id, db):
    list_stocks =  (db.execute("SELECT symbol, SUM(amount) AS total_quantity FROM shares WHERE user_id = ? AND sold=false GROUP BY symbol", user_id))
    list_sold =  (db.execute("SELECT symbol, SUM(amount) AS total_quantity FROM shares WHERE user_id = ? AND sold=true GROUP BY symbol", user_id))
    stocks = []
    stocks_value = 0
    print("all sold")
    print(list_sold)
    for stock in list_stocks:
        amount = stock["total_quantity"]
        print("all stocks:")
        print(stock)
        for sold_stock in list_sold:
            #print(sold_stock["symbol"])
            if sold_stock["symbol"] == stock["symbol"]:
                print("sold:")
                print(sold_stock)
                amount -= sold_stock["total_quantity"]
        print("amount: ")
        print(amount)
        if amount < 0:
            amount = 0
        if amount > 0:

            symbol_dict = lookup(stock["symbol"])
            price = symbol_dict.get("price")
            worth = amount * price
            stocks_value =+ worth
            stocks.append({"symbol":stock["symbol"], "amount":amount,"price":usd(price), "worth":usd(worth)})
    return stocks, stocks_value


def stock_history(user_id, db):
    list_history =  (db.execute("SELECT symbol, sold, datetime,  amount FROM shares WHERE user_id = ?", user_id))

    stocks = []
    stocks_value = 0

    for stock in list_history:
        amount = stock["amount"]
        symbol_dict = lookup(stock["symbol"])
        price = symbol_dict.get("price")
        worth = amount * price
        stocks_value =+ worth
        sold =''
        if stock["sold"] == 1:
            sold = "Sell"
        else:
            sold = "Buy"
        stocks.append({"symbol":stock["symbol"], "amount":amount,"price":usd(price), "worth":usd(worth), "sold":sold, "time":stock["datetime"]})
    return stocks, stocks_value
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")

        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history&includeAdjustedClose=true"
    )

    # Query API
    try:
        response = requests.get(url, cookies={"session": str(uuid.uuid4())}, headers={"User-Agent": "python-requests", "Accept": "*/*"})
        response.raise_for_status()

        # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
        quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
        quotes.reverse()
        price = round(float(quotes[0]["Adj Close"]), 2)
        return {
            "name": symbol,
            "price": price,
            "symbol": symbol
        }
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
