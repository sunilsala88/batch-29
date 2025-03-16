
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
        print(self.data.index[-1].time())
        print(pd.Timestamp('10:00').time())

        if self.data.index[-1].time() == pd.Timestamp('10:00').time():
            print('inside')
            df=self.data.df
            print(df)
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



import yfinance as yf
data=yf.download('TSLA',period='7d',interval='5m')
print(data)
data.columns=[c[0] for c in data.columns]
data.index = data.index.tz_convert('US/Eastern')
print(data)



data.reset_index(inplace=True)
data['Datetime']=data['Datetime'].dt.tz_localize(None)
data.set_index('Datetime',inplace=True)

print(data)
bt = Backtest(data, ORBStrategy, cash=3000, commission=.002)
stats = bt.run()
print(stats)
bt.plot()



# data = fetch_data('AMZN')
# print(data)


  # Focus on regular trading hours
# data.to_csv('data.csv')
# data['Date']=data['Date'].dt.tz_localize(None)
# data.set_index('Date',inplace=True)
# data = data.between_time('09:00:00', '16:00:00')

# bt = Backtest(data, ORBStrategy, cash=100_000, commission=.002)
# stats = bt.run()
# print(stats)
# bt.plot()

# def fetch_data(symbol):
#     data = yf.download(symbol, period='7d', interval='5m')
#     data.reset_index(inplace=True)
#     data['Datetime']=data['Datetime'].dt.tz_localize(None)
#     data.set_index('Datetime',inplace=True)
#     return data

# stocks=['AAPL','GOOG','AMZN','MSFT']
# results = {}
# for stock in stocks:
#     data = fetch_data(stock)
#     print(data)
#     data['Date']=data['Date'].dt.tz_localize(None)
#     data.set_index('Date',inplace=True)
#     bt = Backtest(data, ORBStrategy, cash=100_000, commission=.002)
#     stats = bt.run()
#     results[stock] = stats
#     # bt.plot()

# for stock, stats in results.items():
#     print(f"{stock}:")
#     print(stats)