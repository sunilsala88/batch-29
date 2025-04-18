from backtesting import Strategy,Backtest
import yfinance as yf
import pandas_ta as ta

data=yf.download('BTC-USD',period='5y')
data.columns=[c[0] for c in data.columns]
print(data)

def SMA(closing_data,length):
    return ta.sma(closing_data,length=length)

def EMA(closing_data,length):
    return ta.ema(closing_data,length)

print(SMA(data['Close'],50))
print(EMA(data['Close'],20))
import time

class sma_ema(Strategy):
    sma_l=50
    ema_l=20
    sl_point=5
    tp_point=10

    def init(self):
        self.sma=self.I(SMA,self.data.df.Close,self.sma_l)
        self.ema=self.I(EMA,self.data.df.Close,self.ema_l)

    def next(self):

        # time.sleep(1)
        # print('perious time',self.data.df.index[-2],'current close',self.data.df.Close[-2])
        # print('current time',self.data.df.index[-1],'current close',self.data.df.Close[-1])
        # print('current sma',self.sma[-1],'cuurent ema',self.ema[-1])

        if (self.ema[-1]>self.sma[-1]) and (self.ema[-2]<self.sma[-2]):
            cp=self.data.df.Close.iloc[-1]
            if self.position.is_short:
                self.position.close()
            self.buy(sl=cp*(1-(self.sl_point/100)),tp=cp*(1+(self.tp_point/100)))
        elif (self.ema[-1]<self.sma[-1]) and (self.ema[-2]>self.sma[-2]):
            cp=self.data.df.Close.iloc[-1]
            if self.position.is_long:
                self.position.close()
            self.sell(sl=cp*(1+(self.sl_point/100)),tp=cp*(1-(self.tp_point/100)))

bt=Backtest(data,sma_ema,cash=120_000,commission=0.002)
output=bt.run()
print(output)
print(output['_trades'])
# bt.plot()


output=bt.optimize(sl_point=range(2,30,2),tp_point=range(2,50,2),maximize='Return [%]')
print(output)
print(output['_strategy'])
bt.plot()

#overfitting
