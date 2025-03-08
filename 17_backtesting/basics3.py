from backtesting import Strategy,Backtest
import yfinance as yf
import pandas_ta as ta

data=yf.download('^NSEI',period='5y')
data.columns=[c[0] for c in data.columns]
print(data)

def SMA(close,l):
    return ta.sma(close,l)
sma1=SMA(data['Close'],30)
print(sma1)
import time

class sma_cross(Strategy):
    n1=20
    n2=50

    def init(self):
        self.sma1=self.I(SMA,self.data.df['Close'],self.n1)
        self.sma2=self.I(SMA,self.data.df['Close'],self.n2)

    def next(self):
        # print(self.data.df)
        # time.sleep(1)
        if (self.sma1[-1]>self.sma2[-1]) and (self.sma1[-2]<self.sma2[-2]) :
            if self.position.is_short:
                self.position.close()
            self.buy()
        elif (self.sma1[-1]<self.sma2[-1]) and (self.sma1[-2]>self.sma2[-2]) :
            if (self.position.is_long):
                self.position.close()
            self.sell()
        

bt=Backtest(data,sma_cross,cash=50_000,commission=0.002)
output=bt.run()
print(output)
bt.plot()