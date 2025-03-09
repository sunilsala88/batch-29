from backtesting import Strategy,Backtest
import yfinance as yf
import pandas_ta as ta

data=yf.download('TSLA',period='5y')
data.columns=[c[0] for c in data.columns]
print('downloading data for first time')
print(data)

def SMA(closing_data,length):
    return ta.sma(closing_data,length=length)

def EMA(closing_data,length):
    return ta.ema(closing_data,length)

# print(SMA(data['Close'],50))
# print(EMA(data['Close'],20))
# import time

class sma_ema(Strategy):
    sma_l=50
    ema_l=20

    def init(self):
        self.sma=self.I(SMA,self.data.df.Close,self.sma_l)
        self.ema=self.I(EMA,self.data.df.Close,self.ema_l)

    def next(self):

        # time.sleep(1)
        # print('perious time',self.data.df.index[-2],'current close',self.data.df.Close[-2])
        # print('current time',self.data.df.index[-1],'current close',self.data.df.Close[-1])
        # print('current sma',self.sma[-1],'cuurent ema',self.ema[-1])

        if (self.ema[-1]>self.sma[-1]) and (self.ema[-2]<self.sma[-2]):
            if self.position.is_short:
                self.position.close()
            self.buy()
        elif (self.ema[-1]<self.sma[-1]) and (self.ema[-2]>self.sma[-2]):
            if self.position.is_long:
                self.position.close()
            self.sell()

bt=Backtest(data,sma_ema,cash=120_000,commission=0.002)
output=bt.run()
print(output)
# print(output['_trades'])
# bt.plot()


# output=bt.optimize(sma_l=range(60,120,2),ema_l=range(20,60,2),maximize='Win Rate [%]')
# print(output)
# print(output['_strategy'])
# bt.plot()
#pip install backtesting==0.6.1



def custom_optimization(stats):
    return stats['Win Rate [%]'] * stats['Return [%]']


#optimize multiple parameters at once
# l1=range(50,100,3)
# l2=range(10,40,3)
stats=bt.optimize(sma_l=range(60,120,2),ema_l=range(20,60,2),maximize=custom_optimization)
print(stats)
print(stats['_strategy'])
# bt.plot()