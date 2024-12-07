
str1='fessorpro'
l=len(str1)
print(l)
print(list(range(-1,-(l+1),-1)))

new_str=""
for i in range(-1,-(len(str1)+1),-1):
    new_str=new_str+str1[i]
print(new_str)