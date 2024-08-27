
from strategies.strategy import Strategy, strategyInput



class BuyTheDip(Strategy):
    def __init__(self, PCT_THRESHOLD):
        super().__init__("BuyTheDip")
        self.PCT_THRESHOLD = 20
    
    def shouldWeBuy(self, strategyinput: strategyInput) -> bool:
        range = strategyinput.todayHighPrice - strategyinput.todayLowPrice
        distance = abs(strategyinput.todayClosePrice - strategyinput.todayLowPrice)
        pct = (distance / range) * 100 

        if pct < self.PCT_THRESHOLD:
            return True
        return False
    
    def shouldWeSell(self, strategyinput: strategyInput) -> bool:
        # If we are here, we have the stock. If the dip
        # continues, we should hold
        return self.shouldWeBuy(strategyinput)==False