

stock_prices={'tsla':100,'amzn':900,'nvda':800}
#accessing value
print(stock_prices['tsla'])


#adding a new elemnt in dict
stock_prices.update({'nifty':1500})
print(stock_prices)

#update value of existing key
stock_prices.update({'nvda':900})
print(stock_prices)

#remove
stock_prices.pop('tsla')
print(stock_prices)


print('-'.join(['a','b','c']))
print(stock_prices.get('nvda1'))

print(stock_prices.keys())
print(stock_prices.values())
print(stock_prices.items())


s1={1,2,3,2,4,88,4}
print(s1)
s1.add(99)
s1.pop()
s1.pop()
print(s1)
