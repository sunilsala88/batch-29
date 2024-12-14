
def add_2_number(num1 : int,num2 :int) ->  list:
    ans=num1+num2
    a=[]
    return a

a=add_2_number(4,4)
print(a)


def get_highest(numbers:list)->int:
    high=numbers[0]
    for elem in numbers:
        if high<elem:
            high=elem
    return high


h=get_highest([66,55,44,77,32])
print(h)



def get_area(radius:int)->int:
    a=3.14*(radius**2)
    return a

def do_reverse(string1:str)->str:
    f=''
    # for i in range(-1,-len(string1)-1,-1):
    #     f=f+string1[i]
    for i in string1:
        f=i+f
    return f

ans=do_reverse('fessorpro')
print(ans)


def get_second_highest(numbers:list)->int:
    high=numbers[0]
    second_high=numbers[0]
    for elem in numbers:
        if high<elem:
            second_high=high
            high=elem
    return second_high

a=get_second_highest([5,6,7,8,4,3,9])
print(a)

