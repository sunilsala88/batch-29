a="hello"
print(a[0:3])
# a[0]='a' #immutable
b=a.replace('h','a')
print(b)
print(a.index('o'))
stocks='amzn-tsla-goog'
stock_l=stocks.split('-')
print(stock_l)
s2=",".join(stock_l)
print(s2)


l1=[300,400,'tsla','goog']
print(l1[:2])
l1[1]=500
print(l1)
l1.append('nifty')

l1.insert(0,0)
l1.remove('goog')
i=l1.pop(1)
print(i)
print(l1)

d1={'amzn':300,'tsla':900,'goog':700}
print(type(a))
d1.update({'tsla':700})
print(d1)

# print(d1['amzna'])
print(d1.get('amzna',0))
print(d1.items())
print(d1.pop('tsla'))