# https://www.geeksforgeeks.org/python-classes-and-objects/


#procedural prog

#oops
#object oriented programming

#what is class
#class is a blueprint for the object

#what is object
#object is an instance of the class

#what is attribute
#attribute is a variable that is inside the class

#class attribute
#class attribute is a variable that is shared by all instances of the class

#instance attribute
#instance attribute is a variable that is unique to each instance

#what is method
#method is a function that is inside the class

#what is constructor
#constructor is a special method that is called when the object is created (__init__)


#self
#first parameter of the method is self
#self is a reference to the current instance of the class
#self is used to access the attributes and methods of the class

class Dog:
    sound = "bark" 

    def __init__(self,name,age):
        print('this is constructor')
        self.name = name
        self.age = age

# Create an object from the class
dog1 = Dog('Tommy', 2)
dog2 = Dog('Max', 3)


# Access the class attribute
print(dog1.sound)
print(dog2.sound)

print(dog1.name)
print(dog2.name)




#class book

class Book:
    material = "paper"

    #constructor
    def __init__(self,title,author):
        self.title = title
        self.author = author

    def read(self):
        print(f'reading the book {self.title}')
    def write(self):
        print(f'writing in the book {self.title}')

book1 = Book('Harry Potter', 'J.K. Rowling')
book2 = Book('Lord of the Rings', 'J.R.R. Tolkien')

print(book1.material)
print(book2.material)

print(book1.title)
print(book2.title)

book1.read()
book1.write()


#class circle




class Circle:
    PI=3.14

    def __init__(self,r):
        self.radius = r
    
    def area(self):
        return self.PI * self.radius * self.radius

    def circumference(self):
        return 2 * self.PI * self.radius

circle1 = Circle(7)
circle2 = Circle(14)


print(circle1.radius)
print(circle2.radius)

print(circle1.area())
print(circle2.area())


class BankAccount:
    bank_name='jpmorgan'

    def __init__(self,acc_no,ini_bal):
        self.account_no=acc_no
        self.balance=ini_bal

    def deposit(self,amount:int):
        try:
            if amount>0:
                
                    self.balance=self.balance+amount
                    return self.balance
            else:
                print('invalid amount')
        except:
            print('invalid amount')

    def withdraw(self,amount:int):
        if amount<self.balance:
            self.balance=self.balance-amount
            return self.balance
        else:
            print('invalid amount')

    def get_balance(self):
        return self.balance
    

acc1=BankAccount(450,1000)
acc2=BankAccount(451,2000)

print(acc1.get_balance())
acc1.deposit('500')
acc1.deposit(5000)
print(acc1.get_balance())

acc1.withdraw(2000)
print(acc1.get_balance())



class Broker:
    stock_prices={'goog':500,'tsla':200,'nifty':900}

    def __init__(self,name,acc_no,ini_bal):
        self.name=name
        self.account_number=acc_no
        self.wallet=ini_bal
        self.porfolio={}
    
    def __str__(self):
        return self.name
    
    def buy(self,stock_name):
        found=self.stock_prices.get(stock_name)
        if found:
            self.porfolio.update({stock_name:found})
            self.wallet=self.wallet-found
        else:
            print('invalid stock name')
    def sell(self,stock_name):
        found=self.porfolio.get(stock_name)
        if found:
            self.porfolio.pop(stock_name)
            self.wallet=self.wallet+found
        else:
            print('invalid stock name')

    def get_portfolio(self):
        for i,j in self.porfolio.items():
            print(f'{i}:{j}')

acc1=Broker('sunil',234,1000)
acc2=Broker('matt',456,1000)




acc1.buy('goog')
acc1.get_portfolio()

print(acc1)
