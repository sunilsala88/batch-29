






from backtesting import Strategy, Backtest
import yfinance as yf
import pandas_ta as ta
from backtesting.lib import resample_apply
import time

def supertrend1(high_data,low_data,close_data,l):
    o=ta.supertrend(high_data,low_data,close_data,length=l)
    # print(o)
    return o[f'SUPERTd_{l}_3.0']
def supertrend2(high_data,low_data,close_data,l):
    o=ta.supertrend(high_data,low_data,close_data,length=l)
    return o[f'SUPERT_{l}_3.0']

def ema(close_data,period=9):
    return ta.ema(close_data,length=period)


class supertrend_ema(Strategy):
    super_length=30
    ema_length=10


    def init(self):
        self.super1=self.I(supertrend1,self.data.High.s,self.data.Low.s,self.data.Close.s,self.super_length)
        self.super2=self.I(supertrend2,self.data.High.s,self.data.Low.s,self.data.Close.s,self.super_length)
        
        # self.ema_hour=self.I(ema,self.data.Close.s,self.n1)

        self.daily_ema = resample_apply('D', ema,self.data.Close.s,self.ema_length)

    def next(self):

      
        if self.super1[-1]>0 and self.data.Close[-1]> self.daily_ema[-1]:


            if self.position.is_short:
                self.position.close()
            self.buy()



            # elif not self.position:  
            #     self.buy()


        elif self.super1[-1]<0 and self.data.Close[-1]<self.daily_ema[-1]:
            if self.position.is_long:
                self.position.close()
            self.sell()




import yfinance as yf
data=yf.download('^NSEI',period='700d',interval='1h')
data.index = data.index.tz_convert('Asia/Kolkata')
#change timezone from utc to ist


data.columns=[c[0] for c in data.columns]
print(data)

s1=supertrend1(data.High,data.Low,data.Close,10)
s2=supertrend2(data.High,data.Low,data.Close,10)
e1=ema(data.Close,10)
print(s1)
print(s2)
print(e1)

bt=Backtest(data,supertrend_ema,cash=250000)
output=bt.run()
print(output)
print(output['_trades'].to_csv('trades.csv'))
# bt.plot()

def custom_optimization(stats):
    return stats['Win Rate [%]'] * stats['Return [%]']



stats=bt.optimize(super_length=range(10,60,5),ema_length=range(10,60,5),maximize=custom_optimization)
print(stats)
print(stats['_strategy'])
bt.plot()