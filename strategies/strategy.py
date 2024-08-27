from dataclasses import dataclass

@dataclass
class strategyInput:
    todayOpenPrice: float
    todayClosePrice: float
    todayHighPrice: float
    todayLowPrice: float

    stockPrice: float


class Strategy:
    def __init__(self, strategyName):
        self.strategyName = strategyName

    def getStrategy(self):
        return self.strategyName
    
    # This method should be implemented by the child class
    def shouldWeBuy(self, strategyinput: strategyInput) -> bool:
        pass

    # This method should be implemented by the child class
    def shouldWeSell(self, strategyinput: strategyInput) -> bool:
        pass

