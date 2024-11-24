l1=[11,2,33,44,5]
print(l1)
print(l1[2:4])

l1.append(98)
l1.append(98)

l1.remove(33)
a=l1.pop(0)
print(a)
print(l1)
l1.insert(0,65)


i=l1.index(65)
print(i)
print(l1)
a1=[1,2,3]
s2=[5,6,7]
a1.extend(s2)
print(a1)

stocks=['amzn','tsla']
stocks.insert(10,88)
print(stocks)

s1='amzn--tsla--goog--nifty'
w=s1.split(',')
print(w)

k='@'.join(w)
print(k)

a='  ab c  '
print(a.strip())

s1='amzn--tsla--goog--nifty'