from finvizfinance.quote import finvizfinance



stock = finvizfinance('tsla')
print(stock)

stock_fundament = stock.ticker_fundament()
print(stock_fundament)

# import pandas as pd
# df=pd.Series(stock_fundament).to_csv('data.csv')


from finvizfinance.screener.overview import Overview

foverview = Overview()
filters_dict = {'Index':'NASDAQ 100','Market Cap.':'Mega ($200bln and more)','Current Volume':'Over 20M'}
foverview.set_filter(filters_dict=filters_dict)
df = foverview.screener_view()
df.head()
print(df)

list_of_stocks=df['Ticker'].to_list()
dict_of_pe={}

for stock in list_of_stocks:
    stock = finvizfinance(stock)
    stock_fundament = stock.ticker_fundament()

    dict_of_pe[stock_fundament['Company']]=stock_fundament['P/E']
    
print(dict_of_pe.values())
print(len(dict_of_pe.values()))
print(max(dict_of_pe.values()))  