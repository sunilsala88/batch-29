from backtesting import Backtest,Strategy
import yfinance as yf
import pandas_ta as ta


data=yf.download('TSLA',start='2021-01-01',end='2024-12-30')
print(data.columns)
# l=[]
# for c in data.columns:
#     l.append(c[0])
# data.columns=l
data.columns=[c[0] for c in data.columns]
print(data)

def get_sma(closing_data,length):
    sma1=ta.sma(closing_data,length)
    return sma1

print(get_sma(data['Close'],50))

class SMA_cross(Strategy):
    n1=20
    n2=50

    def init(self):
        self.sma1=self.I(get_sma,self.data.df['Close'],self.n1)
        self.sma2=self.I(get_sma,self.data.df.Close,self.n2)

    def next(self):
        if (self.sma1[-1]>self.sma2[-1]) and (self.sma1[-2]<self.sma2[-1]):
            self.buy()
        elif (self.sma1[-1]<self.sma2[-1]) and (self.sma1[-2]>self.sma2[-1]) and self.position.is_long:
            self.position.close()


bt=Backtest(data,SMA_cross,cash=1000)
output=bt.run()
print(output)
bt.plot()