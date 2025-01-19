import yfinance as yf
import mplfinance as mpf
import pandas as pd
import datetime as dt

#pip install yfinance==0.2.37

data=yf.download(tickers='TSLA',period='5d',interval='1m')
print(data)
#stock split
#dividend
start=dt.datetime(2024,1,1)
end=dt.datetime(2024,12,31)

# data=yf.download(tickers='BTC-USD',start=start,end=end,interval='1h',ignore_tz=True)
# print(data)

# ohlc_dict={"Open":'first','High':'max','Low':'min','Close':'last','Volume':'sum'}
# new_data=data.resample('5min').agg(ohlc_dict).dropna()
# print(new_data.tail(30))

# mpf.plot(new_data,type='candle',style='yahoo')


#bitcoin 2023
#eth 2022

data1=yf.download(tickers='ETH-USD',start='2022-01-01',end='2022-12-31',interval='1d')
print(data1)

data2=yf.download(tickers='BTC-USD',start='2023-01-01',end='2023-12-31',interval='1d')
print(data2)

df=pd.concat([data1,data2])
print(df)

mpf.plot(df,type='candle',style='yahoo')