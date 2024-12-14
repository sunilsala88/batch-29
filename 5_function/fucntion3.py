


# Python program to demonstrate
# default arguments
def myFun(x, y=1):
    """
    this is my first doc string
    """
    print("x: ", x)
    print("y: ", y)


# Driver code (We call myFun() with only
# argument)
myFun(10)



# Python program to demonstrate Keyword Arguments
def student(firstname, lastname):
    """
    student function
    """
    print(firstname, lastname)


# Keyword arguments
student('gala','akshay')
student(firstname='Geeks', lastname='Practice')
student(lastname='Practice', firstname='Geeks')






def get_square(num): return num**2