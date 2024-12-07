
#loop iteration
l1=[5,6,7,8,9]

#type 1 me
total=0
for i in l1:
    total=total+i
    print(total)

print(total//len(l1))


# type 2
print(list(range(5)))
for i in range(100):
    print('hello')


# even=[]
# for i in range(10):
#     if i%2==0:
#         even.append(i)
# print(even)

#type 3 loop
l1=['amzn','tsla','goog','nifty','ongc']

for i in range(len(l1)):
    print(l1[i])


# pnl=[+10, -20, +15, +30, -5]
# days=0
# for i in pnl:
#     if i>0:
#         days=days+1

# print(days)




# prices=[120, 110, 130, 140, 150]
# high=prices[0]
# for p in prices:
#     if high<p:
#         high=p

# print(high)

# low=prices[0]
# for p in prices:
#     if low>p:
#         low=p

# print(low)


l1=[51000,51100,51200,51300,51400]
stock_price=51150
lowest_diff=l1[0]
atm_strike=l1[0]

# for s in l1:

#     d=abs(s-stock_price)
#     if lowest_diff>=d:
#         lowest_diff=d
#         atm_strike=s

# for s in range(len(l1)):

#     d=abs(l1[s]-stock_price)
#     if lowest_diff>=d:
#         lowest_diff=d
#         atm_strike=l1[s]

# print(atm_strike)

# prices=[100, 105, 110]
# volumes=[200, 150, 300,888]

# cum_vol=sum(volumes)
# print(cum_vol)
# num=0
# for i in range(len(prices)):
#     num=num + (prices[i]*volumes[i])
# vwap=num/cum_vol
# vwap=round(vwap,2)
# print('last')
# print(vwap)
