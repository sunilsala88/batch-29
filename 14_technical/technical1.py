import yfinance as yf
import pendulum as dt

data=yf.download(tickers='TSLA',period='5d',interval='1m')
print(data)

data2=yf.download(tickers='RELIANCE.NS',period='5d',interval='1m')
print(data2)

# data2=yf.download(tickers='BTC-USD',start='2023-01-01',end='2023-12-31',interval='1d')
# print(data2)