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


#class car