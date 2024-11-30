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

s1='amzn,tsla,goog,nifty'
w=s1.split(',')
print(w)

k='@'.join(w)
print(k)

a='  ab c  '
print(a.strip())

s1='amzn--tsla--goog--nifty'
l4=s1.split('--')

# last=l4.pop(-1)
# first=l4.pop(0)

# l4.insert(0,last)
# l4.append(first)
# print(l4)

last=l4[-1]
first=l4[0]
l4[-1]=first
l4[0]=last
print(l4)


t1=(44,5,6,7,'tsla')
print(t1[0:3])
i=t1.index(7)
print(i)
#diff between list and tuple
#list is mutable and tuple is not
#list uses [] and tuple uses ()