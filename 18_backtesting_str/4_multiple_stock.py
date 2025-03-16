
from backtesting import Backtest, Strategy

import pandas as pd
import yfinance as yf
import time



class ORBStrategy(Strategy):
    
    def init(self):
        self.orb_high = None
        self.orb_low = None
        self.trade=0


    def next(self):
 

        if self.data.index[-1].time() == pd.Timestamp('10:00').time():
            print('inside')
            df=self.data.df
            # print(df)
            d=self.data.index[-1]
            d=pd.to_datetime(d.date())
            df=df[df.index>=d]
            self.orb_high = df.High.max()
            self.orb_low = df.Low.min()
            self.trade=0
            # print(self.orb_high, self.orb_low)

    
        if not self.position and self.orb_high and self.orb_low:
            # print('inside condition')
            if (self.data.Close[-1] > self.orb_high) and self.trade==0:
                # print('buy condition satisfied')
                p=self.data.Close[-1]
                self.buy(sl=self.orb_low)
                self.trade=1
            elif (self.data.Close[-1] < self.orb_low) and self.trade==0:
                # print('sell condition satisfied')
                self.sell(sl=self.orb_high)
                self.trade=1

        elif self.position:
            # Close position by the end of the day
            # print('i have some position')
            if self.data.index[-1].time() == pd.Timestamp('15:20').time():
                self.position.close()
                # self.orb_high = None
                # self.orb_low = None
                # self.trade=0

            # print(self.position)


def fetch_data(symbol):
    data=yf.download(symbol,period='7d',interval='5m')
    data.columns=[c[0] for c in data.columns]
    data.index = data.index.tz_convert('US/Eastern')
    data.reset_index(inplace=True)
    data['Datetime']=data['Datetime'].dt.tz_localize(None)
    data.set_index('Datetime',inplace=True)
    return data

stocks=['AAPL','GOOG','AMZN','MSFT']
results = {}
returns={}
for stock in stocks:
    data = fetch_data(stock)
    bt = Backtest(data, ORBStrategy, cash=100_000, commission=.002)
    stats = bt.run()
    results[stock] = stats
    print(stats)
    # bt.plot()
    returns[stock]=stats['Return [%]']

for stock, stats in results.items():
    print(f"{stock}:")
    print(stats)
print(returns)