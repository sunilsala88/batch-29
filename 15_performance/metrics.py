
#cagr
import pandas_ta as ta
import yfinance as yf
import numpy as np
import pandas as pd

def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["return"] = DF["Close"].pct_change()
    print(df)
    df["cum_return"] = (1 + df["return"]).cumprod()
    print(df)
    n = len(df)/252
    CAGR = (df["cum_return"][-1])**(1/n) - 1
    return CAGR

def CAGR2(df):
    return ta.cagr(df.Close)

data=yf.download('TSLA',start='2023-01-01',end='2023-12-31')
print(data)
c1=CAGR(data)
print(c1)
c2=CAGR2(data)
print(c2)



#max drawdown
def max_dd(DF):
    "function to calculate max drawdown"
    df = DF.copy()
    df["return"] = df["Close"].pct_change()
    df["cum_return"] = (1+df["return"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    return (df["drawdown"]/df["cum_roll_max"]).max()

d1=max_dd(data)
print(d1)    

dd=ta.max_drawdown(data['Close'],method='percent')
print(dd)

#calmar ratio
def calmar(DF):
    "function to calculate calmar ratio"
    df = DF.copy()
    return CAGR(df)/max_dd(df)

calmar=calmar(data)
print(calmar)

calmar2=ta.calmar_ratio(data['Close'],method='percent',years=1)
print(calmar2)


#volatility
def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    df["daily_ret"] = DF["Close"].pct_change()
    vol = df["daily_ret"].std() * np.sqrt(252)
    return vol

def vol2(df):
    return ta.volatility(df.Close,tf='days')

v1=volatility(data)
print(v1)


#shape ratio
def sharpe(DF, rf):
    "function to calculate Sharpe Ratio of a trading strategy"
    df = DF.copy()
    return (CAGR(df) - rf)/volatility(df)


s1=sharpe(data,10)
s2=ta.sharpe_ratio(data['Close'])
print(s1)
print(s2)



def sortino(DF, rf):
    "function to calculate Sortino Ratio of a trading strategy"
    df = DF.copy()
    df["return"] = df["Close"].pct_change()
    neg_return = np.where(df["return"]>0,0,df["return"])
    neg_vol = pd.Series(neg_return[neg_return!=0]).std() * np.sqrt(252)
    return (CAGR(df) - rf)/neg_vol

sor1=sortino(data,5)
print(sor1)

sor2=ta.sortino_ratio(data['Close'],5)
print(sor2)