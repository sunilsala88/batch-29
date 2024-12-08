#fibonacci number
#0,1,1,2,3,5,8,13,21,34

fib_num=10
fib=[0,1]
num1=fib[0]
num2=fib[1]
# count=0
# while True:
#     if count==(fib_num-2):
#         break
#     count=count+1
#     num3=num1+num2
#     num1=num2
#     num2=num3
#     fib.append(num3)
# print(fib)

for i in range(fib_num-2):
    num3=num1+num2
    num1=num2
    num2=num3
    fib.append(num3)
print(fib)



quantity=100
div=2
price=50
years=5

current_port=price*quantity
while True:
    if years==0:
        break
    years=years-1
    current_port=current_port+(div*quantity)
    quantity=current_port/price

print(quantity)

saving=10_000
years=5
inflation=0.03
while True:
    if years==0:
        break
    years=years-1
    saving=saving-(inflation*saving)
print(saving)

initial_investment=300_000
investment=300_000
rental=1200
appr=0.03
months=12*5
current_month=0
rental_income=0
while True:
    if current_month%12==0:
        investment=investment+(appr*investment)
        print('done')

    if current_month==60:
        break
    current_month=current_month+1


    rental_income=rental_income+rental
print(investment)
print(rental_income)
print(rental_income+investment-initial_investment)


intrest=[0.01, -0.01, 0.02]
money=0
for i in intrest:
    money=money+500
    money=money+money*i
    print(money)
print(money)


balance=50_000
monthly_cont=200
interest=0.06
months=20*12
monthly_int=interest/12

while True:
    if months==0:
        break
    months=months-1
    balance=balance+monthly_cont
    balance=balance+(balance*monthly_int)

print(balance)

