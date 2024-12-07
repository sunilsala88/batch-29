stock_prices={'goog':400,'tsla':900,'amzn':690,'nifty':1000}

# for i in stock_prices:
#     print(i,stock_prices.get(i))


# print(stock_prices.keys())
# print(stock_prices.values())
# print(stock_prices.items())

# #type 4 loop
# total=0
# for i,j in stock_prices.items():
#     print(i,j)
#     total=total+j
# print(total)


#revers a list
list1=[33,66,22,7,55]
# list1.reverse()
# print(list1)
l1=[4,3,2,1,0]
new_list=[]
# for i in l1:
#     new_list.append(list1[i])
# print(new_list)

print(list(range(10)))
print(list(range(20,30)))
print(list(range(10,90,5)))

print(list(range(6,-1,-1)))

for i in range(len(list1)-1,-1,-1):
    new_list.append(list1[i])
print(new_list)



# for i in str1:
#     print(i)

list1=[33,66,22,7,55,89]
#[-1,-2,-3,-4,-5]
print(list(range(-1,-(len(list1)+1),-1)))

