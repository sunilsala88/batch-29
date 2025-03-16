from backtesting import Backtest,Strategy
import yfinance as yf
import pandas_ta as ta
from backtesting.lib import resample_apply
# data=yf.download('^NSEI',period='5y')
# data=yf.download('^NSEI',period='7d',interval='1m')
# data.columns=[c[0] for c in data.columns]
# print(data)

import pandas as pd
df=pd.read_csv('/Users/algotrading2024/batch 29/AMZN.csv')
df.drop(['symbol','trade_count','vwap'],axis=1,inplace=True)
df['timestamp']=pd.to_datetime(df['timestamp'])
df=df.rename(columns={'timestamp':'Date','open':'Open','high':'High','low':'Low','close':'Close'})
df=df.set_index('Date')
data=df.copy()
# data=data.iloc[:50_000]

def band_lower(close,l):
    bb=ta.bbands(close,l)
    print(bb)
    return bb[f'BBL_{l}_2.0']

def band_upper(close,l):
    bb=ta.bbands(close,l)
    # print(bb)
    return bb[f'BBU_{l}_2.0']

bl=band_lower(data['Close'],30)
print(bl)
bu=band_upper(data['Close'],30)
print(bu)
import time

class bollinger_strategy(Strategy):
    n1=20
    gran='5min'


    def init(self):
        # self.upper=self.I(band_upper,self.data.df['Close'],self.n1)
        # self.lower=self.I(band_lower,self.data.df['Close'],self.n1)

        self.upper = resample_apply(self.gran, band_upper,self.data.Close.s,self.n1)
        self.lower = resample_apply(self.gran, band_lower,self.data.Close.s,self.n1)

    def next(self):

        if self.lower[-1] > self.data.Close[-1] and  self.lower[-2] < self.data.Close[-2]:
            # print('buy')
            if self.position.is_short:
                self.position.close()
            self.buy()
        
        #sell condition
        if self.upper[-1] < self.data.Close[-1]  and  self.upper[-2] > self.data.Close[-2]:
            # print('sell')
            if self.position.is_long:
                self.position.close()
            self.sell()
        

bt=Backtest(data,bollinger_strategy,cash=1000000,commission=0.002)
output=bt.run()
print(output)
# bt.plot()

# def custom_optimization(stats):
#     return stats['Win Rate [%]'] * stats['Return [%]']

# stats=bt.optimize(n1=range(10,60,3),maximize=custom_optimization)
# print(stats)
# print(stats['_strategy'])
# bt.plot()


l1=['5min','15min','30min','60min','120min','240min']
stats=bt.optimize(gran=l1,maximize='Return [%]')
print(stats)
print(stats['_strategy'])
bt.plot()