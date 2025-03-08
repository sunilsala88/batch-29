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
    n1=50
    n2=30

    def init(self):
        pass

    def next(self):
        pass

bt=Backtest(data,SMA_cross,cash=1000)
output=bt.run()
print(output)
bt.plot()