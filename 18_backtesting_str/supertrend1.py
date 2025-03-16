

import yfinance as yf
import pandas_ta as ta
from backtesting import Strategy,Backtest

import time



def get_supertrend(closing_price, high, low, period):
    st=ta.supertrend(closing_price, high, low, period)
    print(st)
    return st[f'SUPERTd_{period}_3.0']

def get_supertrend2(closing_price, high, low, period):
    st=ta.supertrend(closing_price, high, low, period)
    # print(st)
    return st[f'SUPERT_{period}_3.0']

class SupertrendStrategy(Strategy):
    n1 = 50


    def init(self):
        print('this is data inside init')
        closing_price=self.data.df['Close']
        self.super=self.I(get_supertrend,self.data.df['Close'],self.data.df['High'],self.data.df['Low'],self.n1)
        self.super2=self.I(get_supertrend2,self.data.df['Close'],self.data.df['High'],self.data.df['Low'],self.n1)
        
    def next(self):
  
        if self.super[-1] > self.super[-2]:
            if self.position.is_short:
                self.position.close()
            self.buy()
        
        # Sell condition
        if self.super[-1] < self.super[-2]:
            if self.position.is_long:
                self.position.close()
            self.sell()



data=yf.download('RELIANCE.NS',period='10y')
data.columns=[c[0] for c in data.columns]
print(data)


print(get_supertrend(data['Close'], data['High'], data['Low'], 10))

bt=Backtest(data,SupertrendStrategy,cash=50000)
output=bt.run()
print(output)
bt.plot()

