

#pip install yfinance==0.2.37
#pip install numpy==1.26.4
#pip install pandas_ta
#pip install mplfinance
#pip install setuptools

import pandas_ta as ta
import mplfinance as mpf
import yfinance as yf

#getting the data
data=yf.download('^NSEI',start='2024-01-01',end='2025-12-25')
print(data)


#macd
fast=10
slow=40
signal=11
macd=ta.macd(data['Close'],fast=fast,slow=slow,signal=signal)
print(macd)

a=mpf.make_addplot(macd[f'MACD_{fast}_{slow}_{signal}'],color='blue',panel=1)
b=mpf.make_addplot(macd[f'MACDh_{fast}_{slow}_{signal}'],color='red',panel=1,type='bar')
c=mpf.make_addplot(macd[f'MACDs_{fast}_{slow}_{signal}'],color='green',panel=1)
e=mpf.make_addplot(ta.ema(data['Close'],length=10),color='orange')

# mpf.plot(data,style='yahoo',type='candle',addplot=[a,b,c,e])

#adx
l=20
adx=ta.adx(data['High'],data['Low'],data['Close'],length=l)
print(adx[f'ADX_{l}'])

e=mpf.make_addplot(adx[f'ADX_{l}'],color='orange',panel=1)

# mpf.plot(data,style='yahoo',type='candle',addplot=[e])


#supertrend
length=10
mult=3
super=ta.supertrend(data['High'],data['Low'],data['Close'],length=length,multiplier=mult)
print(super)


l=mpf.make_addplot(super['SUPERTl_10_3.0'],color='g')
s=mpf.make_addplot(super['SUPERTs_10_3.0'],color='r')

# mpf.plot(data,style='yahoo',type='candle',addplot=[l,s])


bands=ta.bbands(data['Close'],length=20)
print(bands)

u=mpf.make_addplot(bands['BBU_20_2.0'],color='g')
l=mpf.make_addplot(bands['BBL_20_2.0'],color='r')
m=mpf.make_addplot(bands['BBM_20_2.0'],color='b')

# mpf.plot(data,style='yahoo',type='candle',addplot=[u,l,m])

#rsi

rsi=ta.rsi(data['Close'],length=14)
print(rsi)

# mpf.plot(data,style='yahoo',type='candle',addplot=[mpf.make_addplot(rsi,color='orange',panel=1)])
