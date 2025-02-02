import yfinance as yf
import pandas as pd
import pandas_ta as ta
import mplfinance as mpf
import numpy as np



data=yf.download(tickers='TSLA',period='2y')
print(data)

a=ta.cdl_doji(data['Open'],data['High'],data['Low'],data['Close'])
print(a)
data['doji']=a
data['doji']=data['doji'].astype('str')
print(data)
print(data.info())
# data['doji']=data['doji'].str.replace('0',"").astype(int)

b=[]
for i,j in a.items():
    print(i,j)
    if j==0:
        b.append(np.nan)
    else:
        b.append(data.loc[i,'Close'])
data['doji']=b
print(data)

d=mpf.make_addplot(data['doji'],color='black',type='scatter')
mpf.plot(data,addplot=d,type='candle',style='yahoo')



star = data.ta.cdl_pattern(name="inside")
print(star)
print(star.info())
b=[]
for i,j in star['CDL_INSIDE'].items():
    print(i,j)
    if j==0:
        b.append(np.nan)
    else:
        b.append(data.loc[i,'Close'])
data['star']=b

d=mpf.make_addplot(data['star'],color='black',type='scatter')
mpf.plot(data,addplot=d,type='candle',style='yahoo')

# hammer = data.ta.cdl_pattern(name="hammer")
# print(hammer)
# print(hammer.info())


# b=[]
# for i,j in hammer['CDL_HAMMER'].items():
#     print(i,j)
#     if j==0:
#         b.append(np.nan)
#     else:
#         b.append(data.loc[i,'Close'])
# data['hammer']=b


# d=mpf.make_addplot(data['hammer'],color='black',type='scatter')
# mpf.plot(data,addplot=d,type='candle',style='yahoo')

#pivot