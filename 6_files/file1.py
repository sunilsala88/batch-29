

a='trading'

#write mode
# f=open('data.txt','w')
# f.write(a)
# f.close()

#append mode
# f=open('data.txt','a')
# f.write(a)
# f.close()

#read mode
f=open('new.txt','r')
d=f.read()
print(d)
f.close()
# print(d.split('\n'))


#shortcut

with open('new.txt','w') as f1:
    f1.write('hello world')
    