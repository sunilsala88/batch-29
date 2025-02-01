import yfinance as yf


# data=yf.download(tickers='TSLA',period='5d',interval='1m')
# print(data)

data2=yf.download(tickers='RELIANCE.NS',period='5d',interval='1m')
print(data2)

# data3=yf.download(tickers='BTC-USD',start='2025-01-20',end='2025-01-25',interval='1m')
# print(data3)

#resample
ohlc_dict={
    "Open":'first',
    'High':'max',
    'Low':'min',
    'Close':'last',
    'Volume':'sum',
    'Adj Close':'last'
}

data4=data2.resample('120min').agg(ohlc_dict).dropna()
print(data4.head(15))

import pandas_ta as ta
data2['sma']=ta.sma(data2['Close'],length=5)

data2['ema']=ta.ema(data2['Close'],length=5)
print(data2)
#No module named 'pkg_resources' (pip install setuptools)
#pip install numpy==1.26.4 
#pip install pandas_ta

#talib
#pandas_ta

import mplfinance as mpf
i1=mpf.make_addplot(data2['sma'],color='black')
i2=mpf.make_addplot(data2['ema'],color='red')
mpf.plot(data2,type='candle',style='yahoo',volume=True,addplot=[i1,i2])