
import numpy as np
l3d=[ [11,22,33],[44,55,66],[77,88,99]]
print(l3d)
np3=np.array(l3d)
print(np3)

print(np3[1,[1,2]])

x=np.arange(25,50).reshape(5,5)
print(x)

# y=np.random.randint(1,100,size=16).reshape(4,4)
# print(y)

# print(x[[1,2],[2,3]])
print(x[ 1:3 , 2:4 ])
print(x[ -2: , -2: ])