import pandas as pd
df=pd.read_csv('/Users/algotrading2024/batch 29/18_backtesting_str/AMZN.csv')
df.drop(['symbol','trade_count','vwap'],axis=1,inplace=True)
df['timestamp']=pd.to_datetime(df['timestamp'])
df=df.rename(columns={'timestamp':'Date','open':'Open','high':'High','low':'Low','close':'Close'})
df=df.set_index('Date')
print(df)