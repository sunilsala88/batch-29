
#get 100 prime numbers

def is_prime(number:int)->bool:
    for i in range(2,number):
        r=number%i
        if r==0:
            return False
    
    return True


primes=[1,2]
count=0
num=2
while True:
    if count==98:
        break
    num=num+1
    p=is_prime()
    if p:
        count=count+1
        primes.append(num)

print(primes)
#truthy value 
#falsy value 0,False,None,"",[],{}


if [1]:
    print('inside if')
else:
    print('inside else')