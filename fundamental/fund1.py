
import yfinance as yf
import pandas as pd
name='TSLA'
ticker=yf.Ticker(name)
print(ticker.get_info().get('beta'))

print(pd.Series(ticker.get_info()).to_csv('reliance_info.csv'))

print(ticker.get_income_stmt())
print(ticker.quarterly_income_stmt)

print(ticker.balance_sheet)
print(ticker.quarterly_balance_sheet)

print(ticker.get_cashflow())
print(ticker.quarterly_cash_flow)