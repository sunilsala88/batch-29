import yfinance as yf
import datetime as dt
print(dt.datetime.now())

# s=dt.datetime(2021,1,1)
# e=dt.datetime(2021,12,30)

# daily_data=yf.download('^NSEI',start=s,end=e)
# print(daily_data)

# data=yf.download(tickers='TSLA',start=dt.datetime(2025,1,21,0,0,0),end=dt.datetime(2025,1,25,0,0,0),interval='1m')
# print(data)



import pendulum as dt
# print(dt.timezones())
zone='America/New_York'
t=dt.now(tz=zone)
print(t)
s=dt.datetime(2021,1,1)
e=dt.datetime(2021,12,30)

daily_data=yf.download('^NSEI',start=s,end=e)
print(daily_data)

data=yf.download(tickers='TSLA',start=dt.datetime(2025,1,21,0,0,0),end=dt.datetime(2025,1,25,0,0,0),interval='1m')
print(data)
data=data.reset_index()
print(data)
new_zone='Asia/Kolkata'
data['Datetime']=data['Datetime'].dt.tz_convert('UTC')
print(data)

data['Datetime']=data['Datetime'].dt.tz_convert(new_zone)
print(data)
data['Datetime']=data['Datetime'].dt.tz_localize(None)
print(data)
# data2=yf.download(tickers='RELIANCE.NS',period='5d',interval='1m')
# print(data2)

#-5 et
#00 utc
#+5:30 ist