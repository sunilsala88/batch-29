from finvizfinance.quote import finvizfinance



stock = finvizfinance('tsla')
print(stock)

stock_fundament = stock.ticker_fundament()
print(stock_fundament)

import pandas as pd
df=pd.Series(stock_fundament).to_csv('data.csv')


from finvizfinance.screener.overview import Overview

foverview = Overview()
filters_dict = {'Index':'NASDAQ 100','Market Cap.':'Mega ($200bln and more)'}
foverview.set_filter(filters_dict=filters_dict)
df = foverview.screener_view()
df.head()
print(df)