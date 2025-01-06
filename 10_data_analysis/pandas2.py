import pandas as pd
df=pd.read_csv('/Users/algotrading2024/batch 29/10_data_analysis/sp500.csv')
print(df)
# df=df.set_index('Price')
df.set_index('Name',inplace=True)
print(df)

print(df.loc[ "Wal-Mart Stores","Price" ])
print(df.iloc[-2,-2])

print(df.loc[["Walgreens Boots Alliance","Wells Fargo & Company"],["Sector"   ,"Price"]])
print(df.loc["Verizon Communications Inc":"Exxon Mobil Corp","Sector":"EPS"])

print(df.iloc[-5:,-3:])

df1=pd.read_csv("/Users/algotrading2024/batch 29/10_data_analysis/Unicorn_companies.csv")
df1.set_index('Company',inplace=True)
print(df1.loc["Stripe":'Canva',"Valuation":'Industry'])
print(df1.iloc[3:6,0:3])