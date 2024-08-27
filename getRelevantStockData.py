

import yfinance as yf

def getRelevantStockData(stock):
    # we only want today's data
    data = yf.Ticker(stock).history(period="1d")
    return data



