import pandas as pd

df=pd.read_csv("/Users/algotrading2024/batch 29/10_data_analysis/SBIN.csv")
print(df)


df['date']=pd.to_datetime(df['date'])
print(df.info())