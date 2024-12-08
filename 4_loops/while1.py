# stock_prices={'goog':400,'tsla':900,'amzn':690,'nifty':1000}

# portfolio=[]
# for i in stock_prices:
#     s=input('enter the stock name')
#     portfolio.append(s)


# number=0
# even_list=[]
# odd_list=[]
# while True:
#     if number==100:
#         break
#     number=number+1     
#     print(number)
#     if number%2==0:
#         even_list.append(number)
#     else:
#         odd_list.append(number)
# print(even_list)
# print(odd_list)



# print('end of the loop')



stock_prices={'goog':400,'tsla':900,'amzn':690,'nifty':1000}

# portfolio=[]
# while True:
#     s=input('enter the stock name')
#     if s.upper()=='Q':
#         break
#     found=stock_prices.get(s)
#     if found:
#         portfolio.append(s)
#     else:
#         print('we dont have this stock')
# print(portfolio)




investment=1000
current_money=1000
year=0
while True:
    if current_money>2*investment:
        break
    current_money=current_money+(current_money*0.08)
    year=year+1
print(year)
