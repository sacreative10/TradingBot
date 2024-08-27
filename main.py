from dotenv import dotenv_values
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from getRelevantStockData import getRelevantStockData
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from datetime import datetime
import pytz

def isMarketOpen() -> bool:
    now = datetime.now(pytz.timezone('US/Eastern'))
    return now.hour >= 9 and now.hour < 16 and now.weekday() < 5


secrets = dotenv_values(".env")

stocksToTrade = ["AAPL", "ASTS", "RKLB", "PANW", "NVDA", "AMD"]
startingValue = 100000

def login() -> TradingClient:
    client = TradingClient(secrets["APCA_API_KEY_ID"], secrets["APCA_API_SECRET_KEY"], paper=True)

    account = client.get_account()

    if account.trading_blocked:
        print("Account is currently restricted from trading.")
        exit (1)
    # Greet the user

    print("Logged in")


    return client

def doWeHaveThisStock(account, stockToTrade) -> bool:
    portfolio = account.get_all_positions()
    for position in portfolio:
        if position.symbol == stockToTrade:
            return True
    return False

from strategies.buythedip import BuyTheDip
from strategies.strategy import Strategy, strategyInput

def createStrategyInput(stockToTrade) -> strategyInput:
    stockData = getRelevantStockData(stockToTrade)


    todayOpenPrice = stockData["Open"][0]
    todayClosePrice = stockData["Close"][0]
    todayHighPrice = stockData["High"][0]
    todayLowPrice = stockData["Low"][0]

    stockPrice = stockData["Close"][0]

    return strategyInput(todayOpenPrice, todayClosePrice, todayHighPrice, todayLowPrice, stockPrice)


def getStrategy() -> Strategy:
    return BuyTheDip(20)


def buyStock(account, stockToTrade):
    marketOrderRequest = MarketOrderRequest(
        symbol=stockToTrade,
        qty=1,
        side="buy",
        type="market",
        time_in_force="gtc"
    )
    order = account.submit_order(marketOrderRequest)

def sellStock(account, stockToTrade):
    marketOrderRequest = MarketOrderRequest(
        symbol=stockToTrade,
        qty=1,
        side="sell",
        type="market",
        time_in_force="gtc"
    )
    order = account.submit_order(marketOrderRequest)


def seePerformance(account):
    portfolio = account.get_all_positions()
    print("Portfolio: ")
    print("Symbol | Quantity | Market Value")
    for position in portfolio:
        print(position.symbol + "       " + position.qty + "        " + position.market_value)


    print("Performance: ")
    tradeAccount = account.get_account()
    balanceChange = float(tradeAccount.equity) - float(tradeAccount.last_equity)
    print("Today's Balance change: " + str(balanceChange))
    print("Total balance change: " + str(float(tradeAccount.equity) - startingValue))

    print("Equity: " + str(tradeAccount.equity))


def runStrategyAtClose(account):
    # This function is to be run from
    # a daemon
    if isMarketOpen():
        print("Market is open. Exiting.")
        exit(1)

    strategy = getStrategy()

    for stockToTrade in stocksToTrade:
        strategyInput = createStrategyInput(stockToTrade)
        if not doWeHaveThisStock(account, stockToTrade):
            if strategy.shouldWeBuy(strategyInput):
                print("Buying stock " + stockToTrade)
                buyStock(account, stockToTrade)
            else:
                print("Not buying stock " + stockToTrade)
            
        else:
            if strategy.shouldWeSell(strategyInput):
                print ("Selling stock " + stockToTrade)
                sellStock(account, stockToTrade)
            else:
                print ("Holding" + stockToTrade)
            






    

