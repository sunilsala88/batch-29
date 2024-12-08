




def average(numbers):
    total=0
    for i in numbers:
        total=total+i
    avg=total/len(numbers)
    return avg

price=[11,22,3,55,66,77]
a1=average(price)
print(a1)
customers=[22,33,477,8]
a2=average(customers)
print(a2)


