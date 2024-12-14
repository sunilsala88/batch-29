


#parameter
#argument

# def average(numbers):
#     global age
#     age=30
#     print(age)
#     total=0
#     for i in numbers:
#         total=total+i
#     avg=total/len(numbers)
#     return avg

# def main():
#     price=[11,22,3,55,66,77]
#     a1=average(price)
#     print(a1)

# age=35


# main()
# print(age)

stock_prices={'goog':300,'tsla':699,'amzn':798,'nifty':765}

for i,j in stock_prices.items():
    # print(i,":",j)
    print(f"{i} : {j}")

def get_stocks():
    portfolio=[]
    while True:
        name=input('enter stock name')
        if name.upper()=='Q':
            break
        found=stock_prices.get(name)
        if found:
            portfolio.append(name)
        else:
            print('invalid stock name')
    return portfolio

p=get_stocks()
print(p)