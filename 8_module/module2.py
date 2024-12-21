import file1 as f1

print(f1.b)
print(f1.add(10,20))

import os
print(os.getcwd())

import sys

while True:
    n=input('enter a number:')
    if n=='q':
        sys.exit()
        # break
    print(n)

print('last line')