from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG

import pandas_ta as ta
import yfinance as yf

class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()

print(GOOG)

bt = Backtest(GOOG, SmaCross,
              cash=10000, commission=.002,
              exclusive_orders=True)

output = bt.run()
print(output)
print(output['_trades'].to_csv('trades.csv'))
bt.plot()

#https://www.babypips.com/forexpedia/profit-factor
#https://www.babypips.com/forexpedia/expectancy
#https://tradingtact.com/system-quality-number/
#https://zerodha.com/varsity/chapter/kellys-criterion/