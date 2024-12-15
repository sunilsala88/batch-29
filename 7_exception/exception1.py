
try:
    num1=10
    num2=int('5')
    ans=num1/num2
    print(ans)
    a=[1,2,3]
    print(a[7])
except:
    print('something is wrong')
#ZeroDivisionError
#TypeError
#ValueError
#IndexError


try:
    
    num1=10
    num2=int('a')
    ans=num1/num2
    print(ans)
    a=[1,2,3]
    print(a[2])
except Exception as e:
    print(e)
    print('something is wrong')


try:   
    num1=10
    num2=11
    ans=num1/num2
    print(ans)
    a=[1,2,3]
    print(a[9])
except ZeroDivisionError:
    print('zero is not allowed')
except IndexError:
    print('type correct index')



print('this is important')