import yfinance as yf
import mplfinance as mpf

#pip install yfinance==0.2.37

data=yf.download(tickers='TSLA',period='5d',interval='1m')
print(data)
#stock split
#dividend

# data=yf.download(tickers='BTC-USD',start='2025-01-11',end='2025-01-18',interval='1h')
# print(data)

ohlc_dict={"Open":'first','High':'max','Low':'min','Close':'last','Volume':'sum'}
new_data=data.resample('5min').agg(ohlc_dict).dropna()
print(new_data.tail(30))

mpf.plot(new_data,type='candle',style='yahoo')